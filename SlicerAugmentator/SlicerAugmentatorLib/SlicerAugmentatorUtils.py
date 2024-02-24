import os
import re
import SimpleITK as sitk
import threading
import slicer

IS_FILE_ID = "isFileID"  # .../path/CaseID.extension
IS_FOLDER_ID = "isFolderID"  # .../path/CaseID/img.extension


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


def getFilesStructure(filesStructureList):
    structureType = {
        0: IS_FOLDER_ID,
        1: IS_FILE_ID
    }

    return structureType.get(filesStructureList.currentIndex)


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
        '/')[-2] if (filesStructure == IS_FOLDER_ID) else fullImgPath.split('/')[-1]

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
    img = sitk.GetImageFromArray(img)

    if (originalCaseImg.GetDepth() > 0):
        img.CopyInformation(originalCaseImg)

    outputImgVolume = slicer.mrmlScene.AddNewNodeByClass(
        "vtkMRMLScalarVolumeNode", imgNodeName)
    outputImgVolume.SetAndObserveImageData(img)

    if (mask != None):
        mask = sitk.GetImageFromArray(mask)
        if (originalCaseMask.GetDepth() > 0):
            img.CopyInformation(originalCaseImg)
        outputMaskVolume = slicer.mrmlScene.AddNewNodeByClass(
            "vtkMRMLScalarVolumeNode", maskNodeName)
        outputMaskVolume.SetAndObserveImageData(mask)

        slicer.util.setSliceViewerLayers(
            background=outputImgVolume, foreground=outputMaskVolume, foregroundOpacity=0.4)

    else:
        slicer.util.setSliceViewerLayers(background=outputImgVolume)
