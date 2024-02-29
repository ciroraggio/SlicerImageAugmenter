import slicer
from SlicerAugmentatorLib.SlicerAugmentatorIntensity import mapIntensityTransformations
from SlicerAugmentatorLib.SlicerAugmentatorSpatial import mapSpatialTransformations


try:
  from munch import Munch, munchify
except ModuleNotFoundError:
  slicer.util.pip_install("munch")
  from munch import Munch, munchify

def getSerializedObject(dictionary: dict) -> Munch :     
    return munchify(dictionary)

def mapTransformations(ui) -> list:
    mappedTransformations = []
    transformations = getSerializedObject(getTransformations(ui))

    mappedTransformations.extend(mapSpatialTransformations(mappedTransformations=mappedTransformations,transformations=transformations))  
    mappedTransformations.extend(mapIntensityTransformations(mappedTransformations=mappedTransformations,transformations=transformations))  
        
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
                    "axes": ui.flipAxes.text,
                },
                
                # ----------------- Intensity -----------------                 
                "randomScaleIntensity": {
                    "enabled": ui.randomScaleIntensityEnabled.isChecked(),
                    "factor": ui.randomScaleIntensityFactor.text,
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
                }
            }
      
      return transformations