import os
import re
import threading

import SimpleITK as sitk
import sitkUtils
import slicer

FLAT = "flat"  # .../path/ImgID.extension, .../path/ImgID_label.extension
HIERARCHICAL = "hierarchical" # .../path/CaseID/img.extension, # .../path/CaseID/mask.extension

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

def getOriginalCase(fullImgPath, filesStructure):
    """This function returns the original image and extracts the specific patient/case name/ID.
    The extracted name/ID will be used as the title of the folder that will contain the augmented images.
    """
    caseName = fullImgPath.split("/")[-2] if (filesStructure == HIERARCHICAL) else fullImgPath.split("/")[-1]

    originalCaseImg = sitk.ReadImage(fullImgPath)

    return caseName, originalCaseImg

def save(img, path, filename, originalCase, extension, copyInfo=True):
    img = sitk.GetImageFromArray(img)

    if (copyInfo and originalCase.GetDepth() > 0):
        img.CopyInformation(originalCase)

    saveThread = threading.Thread(target=sitk.WriteImage, args=(img, f"{path}/{filename}.{extension}"))
    saveThread.start()


def showPreview(img, originalCaseImg, originalCaseMask=None, mask=None, imgNodeName="imgNode", maskNodeName="maskNode", copyInfo=True):
    sitkAugmentedImg = sitk.GetImageFromArray(img.cpu())

    if (copyInfo and originalCaseImg.GetDepth() > 0):
        sitkAugmentedImg.CopyInformation(originalCaseImg)

    outputImgNode = sitkUtils.PushVolumeToSlicer(sitkAugmentedImg, name=imgNodeName, className="vtkMRMLScalarVolumeNode")

    if (mask != None):
        sitkAugmentedMask = sitk.GetImageFromArray(mask.cpu())
        if (copyInfo and originalCaseMask.GetDepth() > 0):
            sitkAugmentedMask.CopyInformation(originalCaseMask)

        outputMaskNode = sitkUtils.PushVolumeToSlicer(sitkAugmentedMask, name=maskNodeName, className="vtkMRMLScalarVolumeNode")

        slicer.util.setSliceViewerLayers(background=outputImgNode, label=outputMaskNode, labelOpacity=0.4)

    else:
        slicer.util.setSliceViewerLayers(background=outputImgNode)


def clearScene():
    scene = slicer.mrmlScene
    scene.Clear()


def resetViews():
    slicer.app.layoutManager().resetThreeDViews()
    slicer.util.resetSliceViews()


def extractDeviceNumber(gpu_info) -> str:
    match = re.search(r"GPU (\d+) -", gpu_info)

    if not match:
        raise ValueError("GPU text format is invalid. Please report this to the developer!")

    return f"cuda:{str(match.group(1))}"

        