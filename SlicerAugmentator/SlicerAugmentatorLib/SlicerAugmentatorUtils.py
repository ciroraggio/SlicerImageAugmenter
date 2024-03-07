import os
import re
import SimpleITK as sitk
import sitkUtils
import threading
import slicer

FLAT = "flat"  # .../path/ImgID.extension, .../path/ImgID_label.extension
HIERARCHICAL = "hierarchical"  # .../path/CaseID/img.extension, # .../path/CaseID/mask.extension

def collectImagesAndMasksList(imagesInputPath, imgPrefix, maskPrefix):
    imgs, masks = [], []
    for dir in os.listdir(imagesInputPath):
        if (os.path.isdir(f"{imagesInputPath}/{dir}")):
            for content in os.listdir(f"{imagesInputPath}/{dir}"):
                # if the path is a new directory ignore it
                if (not os.path.isdir(f"{imagesInputPath}/{dir}/{content}")):
                    if (imgPrefix in content and not content.startswith(".")):
                        imgs.append(f"{imagesInputPath}/{dir}/{content}")
                    elif (maskPrefix != None
                          and maskPrefix != ""
                          and maskPrefix in f"{imagesInputPath}/{dir}/{content}"
                          and not content.startswith(".")):
                        masks.append(f"{imagesInputPath}/{dir}/{content}")
        else:
            content = dir
            if (imgPrefix in content and not content.startswith(".")):
                imgs.append(f"{imagesInputPath}/{content}")
            elif (maskPrefix != None
                  and maskPrefix != ""
                  and maskPrefix in f"{imagesInputPath}/{content}"
                  and not content.startswith(".")):
                masks.append(f"{imagesInputPath}/{content}")
    return imgs, masks


def getFilesStructure(ui):
    if ui.fileStructureHierarchical.isChecked():
        return HIERARCHICAL
    elif ui.fileStructureFlat.isChecked():
        return FLAT
    
    raise ValueError("File structure not recognized!")

def makeDir(outputPath, OUTPUT_IMG_DIR, caseName, transformName):
    # currentDir = f"{outputPath}/{OUTPUT_IMG_DIR}/{caseName}_{transformName}"
    currentDir = f"{outputPath}/{caseName}_{transformName}"
    os.makedirs(currentDir, exist_ok=True)
    return currentDir

def sanitizeTransformName(transform) -> str:
    """
    This function extracts the name of a transformation by cleaning up the result of transform.__class__

    Returns:
        transform name (str)
    """
    pattern = '[' + \
        re.escape(''.join(['>', '<', '_', '.', '\'', '-', ','])) + ']'
    return re.sub(pattern, "", str(transform.__class__).split(".")[-1])


def getOriginalCase(fullImgPath, filesStructure, loadOriginalImg=True):
    """
    This function returns the original image and extracts the specific patient/case name/ID.
    The extracted name/ID will be used as the title of the folder that will contain the augmented images.
    """
    caseName = fullImgPath.split(
        '/')[-2] if (filesStructure == HIERARCHICAL) else fullImgPath.split('/')[-1]

    originalCaseImg = sitk.ReadImage(fullImgPath)

    return caseName, originalCaseImg


def save(img, path, filename, originalCase, extension):
    img = sitk.GetImageFromArray(img)

    if (originalCase.GetDepth() > 0):
        img.CopyInformation(originalCase)

    saveThread = threading.Thread(target=sitk.WriteImage, args=(
        img, f"{path}/{filename}.{extension}"))
    saveThread.start()


def showPreview(img, originalCaseImg, originalCaseMask=None, mask=None, imgNodeName="imgNode", maskNodeName="maskNode"):
    sitkAugmentedImg = sitk.GetImageFromArray(img)
    if (originalCaseImg.GetDepth() > 0):
        sitkAugmentedImg.CopyInformation(originalCaseImg)
    
    outputImgNode = sitkUtils.PushVolumeToSlicer(sitkAugmentedImg, name=imgNodeName, className="vtkMRMLScalarVolumeNode")

    if (mask != None):
        sitkAugmentedMask = sitk.GetImageFromArray(mask)
        if (originalCaseMask.GetDepth() > 0):
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


