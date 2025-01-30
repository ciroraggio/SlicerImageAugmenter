import os

def validatePrefixes(ui):
    if not ui.imgPrefix.text:
        raise ValueError("Indicate the image prefix")


def validatePaths(ui):
    if not ui.imagesInputPath.directory:
        raise ValueError("Input path is invalid")
    if not ui.outputPath.directory:
        raise ValueError("Output path is invalid")
    if (not os.path.isdir(ui.imagesInputPath.directory)):
        raise ValueError("Images path is not a directory")


def validateForms(ui):
    validatePaths(ui)
    validatePrefixes(ui)


def validateCollectedImagesAndMasks(imgs, masks):
    if (len(imgs) == 0):
        return ValueError(f"No images found with the criteria set, please double check the input data.")

    if len(masks) > 0 and (len(masks) != len(imgs)):
        return ValueError(f"Images and masks must have same length. Found:\n{len(imgs)} images\n{len(masks)} masks.\nMake sure you have specified the correct prefixes to avoid inconsistencies.")
