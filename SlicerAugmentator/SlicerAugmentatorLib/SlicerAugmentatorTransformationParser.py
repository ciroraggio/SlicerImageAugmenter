import slicer
from SlicerAugmentatorLib.SlicerAugmentatorIntensity import mapIntensityTransformations
from SlicerAugmentatorLib.SlicerAugmentatorSpatial import mapSpatialTransformations


try:
  from munch import Munch, munchify
except ModuleNotFoundError:
  slicer.util.pip_install("munch")
  from munch import Munch, munchify

DICT_KEYS = ["img", "mask"]

def getSerializedObject(dictionary: dict) -> Munch :     
    return munchify(dictionary)

def mapTransformations(ui) -> list:
    mappedTransformations = []
    transformations = getSerializedObject(getTransformations(ui))

    mappedTransformations = mapSpatialTransformations(mappedTransformations=mappedTransformations,transformations=transformations, dict_keys = DICT_KEYS)
    mappedTransformations = mapIntensityTransformations(mappedTransformations=mappedTransformations,transformations=transformations, dict_keys = DICT_KEYS)

    return mappedTransformations


def getTransformations(ui) -> dict:
      transformations = {
                # ----------------- Spatial -----------------           
                "rotate": {
                    "enabled": ui.rotateEnabled.isChecked(),
                    "angle": ui.rotateAngle.text,
                    "interpolationMode": ui.rotateInterpolationMode.currentText
                },
                "randRotate": {
                    "enabled": ui.randomRotateEnabled.isChecked(),
                    "rangeFromX": ui.randomRotateFromX.text,
                    "rangeToX":ui.randomRotateToX.text,
                    "rangeFromY": ui.randomRotateFromY.text,
                    "rangeToY":ui.randomRotateToY.text,
                    "rangeFromZ": ui.randomRotateFromZ.text,
                    "rangeToZ":ui.randomRotateToZ.text,
                    "paddingMode": ui.randomRotatePaddingMode.currentText,
                    "interpolationMode": ui.randomRotateInterpolationMode.currentText,
                    "alignCorners": ui.randomRotateAlignCorners.isChecked(),
                },
                "resize": {
                    "enabled": ui.resizeEnabled.isChecked(),
                    "spatialSize": (ui.resizeC.text, ui.resizeW.text, ui.resizeH.text),
                    "interpolationMode": ui.resizeInterpolationMode.currentText
                },
                "flip": {
                    "enabled": ui.flipEnabled.isChecked(),
                    "axis": ui.flipAxis.text,
                },
                "randomFlip": {
                    "enabled": ui.randomFlipEnabled.isChecked(),
                },
                "zoom": {
                    "enabled": ui.zoomEnabled.isChecked(),
                    "factor": ui.zoomFactor.text,
                    "interpolationMode": ui.zoomInterpolationMode.currentText,
                    "paddingMode": ui.zoomPaddingMode.currentText,
                    "alignCorners": ui.zoomAlignCorners.isChecked(),
                },
                "randomZoom": {
                    "enabled": ui.randomZoomEnabled.isChecked(),
                    "factorMin": ui.randomZoomFactorMin.text,
                    "factorMax": ui.randomZoomFactorMax.text,
                    "interpolationMode": ui.randomZoomInterpolationMode.currentText,
                    "paddingMode": ui.randomZoomPaddingMode.currentText,
                    "alignCorners": ui.randomZoomAlignCorners.isChecked(),
                },
                # ----------------- Intensity -----------------                 
                "scaleIntensity": {
                    "enabled": ui.scaleIntensityEnabled.isChecked(),
                    "factor": ui.scaleIntensityFactor.text,
                },
                "randomScaleIntensity": {
                    "enabled": ui.randomScaleIntensityEnabled.isChecked(),
                    "factorFrom": ui.randomScaleIntensityFactorFrom.text,
                    "factorTo": ui.randomScaleIntensityFactorTo.text,
                },
                "adjustContrast": {
                    "enabled": ui.adjustContrastEnabled.isChecked(),
                    "gamma": ui.adjustContrastGamma.text,
                    "invertImage":ui.adjustContrastInvertImage.isChecked(),
                },
                "randomAdjustContrast": {
                    "enabled": ui.randomAdjustContrastEnabled.isChecked(),
                    "gammaFrom": ui.randomAdjustContrastGammaFrom.text,
                    "gammaTo": ui.randomAdjustContrastGammaTo.text,
                    "invertImage":ui.randomAdjustContrastInvertImage.isChecked(),
                },
                "randomGaussianNoise": {
                    "enabled": ui.randomGaussianNoiseEnabled.isChecked(),
                    "mean": ui.randomGaussianNoiseMean.text,
                    "std": ui.randomGaussianNoiseStd.text,
                },
                "shiftIntensity": {
                    "enabled": ui.shiftIntensityEnabled.isChecked(),
                    "offset": ui.shiftIntensityOffset.text,
                },
                "randomShiftIntensity": {
                    "enabled": ui.randomShiftIntensityEnabled.isChecked(),
                    "offsetFrom": ui.randomShiftIntensityFrom.text,
                    "offsetTo": ui.randomShiftIntensityTo.text,
                },
                "normalizeIntensity": {
                    "enabled": ui.normalizeIntensityEnabled.isChecked(),
                    "subtrahend": ui.normalizeIntensitySubtrahend.text,
                    "divisor": ui.normalizeIntensityDivisor.text,
                    "nonZero": ui.normalizeIntensityNonZero.isChecked(),
                },
                "thresholdIntensity": {
                    "enabled": ui.thresholdIntensityEnabled.isChecked(),
                    "thresholdValue": ui.thresholdIntensityValue.text,
                    "cVal": ui.thresholdIntensityCVal.text,
                    "above": ui.thresholdIntensityAbove.isChecked(),
                },
                "medianSmooth": {
                    "enabled": ui.medianSmoothEnabled.isChecked(),
                    "radius": ui.medianSmoothRadius.text,
                },
                "gaussianSmooth": {
                    "enabled": ui.gaussianSmoothEnabled.isChecked(),
                    "sigma": ui.gaussianSmoothSigma.text,
                    "kernel": ui.gaussianSmoothKernelType.currentText,
                },
                "randGaussianSmooth": {
                    "enabled": ui.randGaussianSmoothEnabled.isChecked(),
                    "sigmaFromX": ui.randGaussianSmoothSigmaXFrom.text,
                    "sigmaToX":ui.randGaussianSmoothSigmaXTo.text,
                    "sigmaFromY": ui.randGaussianSmoothSigmaYFrom.text,
                    "sigmaToY":ui.randGaussianSmoothSigmaYTo.text,
                    "sigmaFromZ": ui.randGaussianSmoothSigmaZFrom.text,
                    "sigmaToZ":ui.randGaussianSmoothSigmaZTo.text,
                    "kernel": ui.randGaussianSmoothKernelType.currentText,
                },
            }
      
      return transformations