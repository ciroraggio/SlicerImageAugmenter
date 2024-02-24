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


def validateRotation(transformations):
    if (transformations.rotate.enabled and
       (transformations.rotate.angle == "" or
            transformations.rotate.angle == None)):
        raise ValueError(
            "The 'Rotation' transformation is enabled but the angle is not specified")
    else:
        try:
            float(transformations.rotate.angle)
        except:
            print(
                "The transformation angle specified in the 'Rotation' transformation is invalid.")


def validateFlip(transformations):
    if (transformations.flip.enabled and
       (transformations.flip.axes == "" or
            transformations.flip.axes == None)):
        raise ValueError(
            "The 'Flip' transformation is enabled but the axes are not specified")
    else:
        try:
            int(transformations.flip.axes)
        except:
            print(
                "The transformation axes specified in the 'Flip' transformation is invalid.")


def validateTransforms(transformations):
    if len(transformations) == 0:
        raise ValueError("Choose at least one transformation")
    validateRotation(transformations)
    validateFlip(transformations)


def validateForms(ui):
    validatePaths(ui)
    validatePrefixes(ui)


def validateCollectedImagesAndMasks(imgs, masks):
    if (len(imgs) == 0):
        raise ValueError(
            f"No images found with the criteria set, please double check the input data.")

    if len(masks) > 0 and (len(masks) != len(imgs)):
        raise ValueError(
            f"Images and masks must have same length. Found:\n{len(imgs)} images\n{len(masks)} masks.")
