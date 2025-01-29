import os
import re
import threading

import SimpleITK as sitk
import sitkUtils
import slicer

FLAT = "flat"  # .../path/ImgID.extension, .../path/ImgID_label.extension
HIERARCHICAL = "hierarchical" # .../path/CaseID/img.extension, # .../path/CaseID/mask.extension
CHANNEL_FIRST_REQUIRED = ["Resize", "SpatialPad", "CenterSpatialCrop"]

def collectImagesAndMasksList(imagesInputPath, imgPrefix, maskPrefix):
    imgs, masks = [], []

    for root, _, files in os.walk(imagesInputPath):
        for file in files:
            if file.startswith("."):
                continue
            filePath = os.path.join(root, file)
            if imgPrefix in file:
                imgs.append(filePath)
            elif maskPrefix and maskPrefix in file:
                masks.append(filePath)

    return imgs, masks


def getFilesStructure(ui):
    if ui.fileStructureHierarchical.isChecked():
        return HIERARCHICAL
    elif ui.fileStructureFlat.isChecked():
        return FLAT

    raise ValueError("File structure not recognized!")


def makeDir(outputPath, caseName, transformName):
    currentDir = f"{outputPath}/{caseName}_{transformName}"
    os.makedirs(currentDir, exist_ok=True)
    return currentDir


def sanitizeTransformName(transform) -> str:
    """This function extracts the name of a transformation by cleaning up the result of transform.__class__

    Returns
    -------
        transform name (str)

    """
    pattern = "[" + \
        re.escape("".join([">", "<", "_", ".", "'", "-", ","])) + "]"
    return re.sub(pattern, "", str(transform.__class__).split(".")[-1])


def getTransformName(transform) -> str:
    try:
        return transform.get_transform_info()["class"]
    except AttributeError:
        # in this case get_transform_info is missing, so recover the name starting from __class__:
        return sanitizeTransformName(transform)


def getCaseName(fullImgPath, filesStructure):
    return fullImgPath.split("/")[-2] if (filesStructure == HIERARCHICAL) else fullImgPath.split("/")[-1]


def getOriginalCase(fullImgPath, filesStructure):
    """This function returns the original image and extracts the specific patient/case name/ID.
    The extracted name/ID will be used as the title of the folder that will contain the augmented images.
    """
    caseName = getCaseName(fullImgPath, filesStructure)

    originalCaseImg = sitk.ReadImage(fullImgPath)

    return caseName, originalCaseImg


def copyInfo(origin, target):
    """Same behaviour as sitk.CopyInformation but sizes don't need to match

    Returns
    -------
        Target volume with new information (sitk.Image)

    """
    target.SetOrigin(origin.GetOrigin())
    target.SetSpacing(origin.GetSpacing())
    target.SetDirection(origin.GetDirection())
    return target

def save(img, path, filename, originalCase, extension):
    img = sitk.GetImageFromArray(img)

    if (originalCase.GetDepth() > 0):
        copyInfo(originalCase, img)

    saveThread = threading.Thread(target=sitk.WriteImage, args=(img, f"{path}/{filename}.{extension}"))
    saveThread.start()

def showPreview(img, originalCaseImg, originalCaseMask=None, mask=None, imgNodeName="imgNode", maskNodeName="maskNode"):
    sitkAugmentedImg = sitk.GetImageFromArray(img.cpu())

    if (originalCaseImg.GetDepth() > 0):
        copyInfo(originalCaseImg, sitkAugmentedImg)

    outputImgNode = sitkUtils.PushVolumeToSlicer(sitkAugmentedImg, name=imgNodeName, className="vtkMRMLScalarVolumeNode")

    if (mask != None):
        sitkAugmentedMask = sitk.GetImageFromArray(mask.cpu())
        if (originalCaseMask.GetDepth() > 0):
            copyInfo(originalCaseMask, sitkAugmentedMask)

        outputMaskNode = sitkUtils.PushVolumeToSlicer(sitkAugmentedMask, name=maskNodeName, className="vtkMRMLScalarVolumeNode")

        slicer.util.setSliceViewerLayers(background=outputImgNode, label=outputMaskNode, labelOpacity=0.4)
        return outputImgNode, outputMaskNode
    else:
        slicer.util.setSliceViewerLayers(background=outputImgNode)
        return outputImgNode


def clearScene(previewNodesToClear: list):
    scene = slicer.mrmlScene

    for oldPreviewNode in previewNodesToClear:
        scene.RemoveNode(oldPreviewNode)
    

def resetViews():
    slicer.app.layoutManager().resetThreeDViews()
    slicer.util.resetSliceViews()


def extractDeviceNumber(gpu_info) -> str:
    match = re.search(r"GPU (\d+) -", gpu_info)

    if not match:
        raise ValueError("GPU text format is invalid. Please report this to the developer!")

    return f"cuda:{str(match.group(1))}"
