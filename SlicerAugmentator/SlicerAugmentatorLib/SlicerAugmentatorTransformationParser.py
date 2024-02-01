import slicer
try:
  from monai.transforms import Rotate, Flip, Resize, RandRotate, RandScaleIntensity, RandAdjustContrast
except ModuleNotFoundError:
  slicer.util.pip_install("monai[itk]")
  from monai.transforms import Rotate, Flip, Resize, RandRotate, RandScaleIntensity, RandAdjustContrast


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
    
    if(transformations.rotate.enabled):
        mappedTransformations.append(Rotate(angle=float(transformations.rotate.angle), 
                                            mode=transformations.rotate.interpolationMode
                                            ))
    if(transformations.randRotate.enabled):
      rangeX, rangeY, rangeZ = [0,0], [0,0], [0,0]
      try:
        if(transformations.randRotate.rangeFromX != "" and transformations.randRotate.rangeToX != "" ):
            rangeX = [float(transformations.randRotate.rangeFromX), float(transformations.randRotate.rangeToX)]
        if(transformations.randRotate.rangeFromY != "" and transformations.randRotate.rangeToY != "" ):
            rangeY = [float(transformations.randRotate.rangeFromY), float(transformations.randRotate.rangeToY)]
        if(transformations.randRotate.rangeFromZ != "" and transformations.randRotate.rangeToZ != "" ):
            rangeZ = [float(transformations.randRotate.rangeFromZ), float(transformations.randRotate.rangeToZ)]
                                                
        mappedTransformations.append(RandRotate(prob=1,
                                range_x=rangeX, 
                                range_y=rangeY, 
                                range_z=rangeZ, 
                                padding_mode=transformations.randRotate.paddingMode, 
                                mode=transformations.randRotate.interpolationMode, 
                                keep_size=transformations.randRotate.keepSize, 
                                align_corners=transformations.randRotate.alignCorners))
      except Exception as e:
        raise ValueError(e)      
      
                                     
    if(transformations.resize.enabled):
        mappedTransformations.append(Resize(spatial_size=(transformations.resize.spatialSize),
                                            mode=transformations.resize.interpolationMode 
                                            ))
    if(transformations.flip.enabled):
        mappedTransformations.append(Flip(spatial_axis=int(transformations.flip.axes)))
        
    if(transformations.randomScaleIntensity.enabled):
        if(transformations.randomScaleIntensity.factor == ""):
          raise ValueError("The 'Random Scale Intensity' transformation is enabled but a factor is not specified")      
        
        mappedTransformations.append(RandScaleIntensity(prob=1, factors=float(transformations.randomScaleIntensity.factor)))    
        
    if(transformations.randomAdjustContrast.enabled):
        if(transformations.randomAdjustContrast.gammaFrom == "" or transformations.randomAdjustContrast.gammaTo == ""):
          raise ValueError("The 'Random Adjust Contrast' transformation is enabled but gamma values is not specified")      
        
        mappedTransformations.append(RandAdjustContrast(prob=1, 
                                                        gamma=[float(transformations.randomAdjustContrast.gammaFrom), float(transformations.randomAdjustContrast.gammaTo)],
                                                        invert_image=transformations.randomAdjustContrast.invertImage))    
        
    return mappedTransformations


def getTransformations(ui) -> dict:
      transformations = {
                # Spatial
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
                    "keepSize": ui.randomRotateKeepSize.isChecked(),
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
                # Intensity
                "randomScaleIntensity": {
                    "enabled": ui.randomScaleIntensityEnabled.isChecked(),
                    "factor": ui.randomScaleIntensityFactor.text,
                },
                "randomAdjustContrast": {
                    "enabled": ui.randomAdjustContrastEnabled.isChecked(),
                    "gammaFrom": ui.randomAdjustContrastGammaFrom.text,
                    "gammaTo": ui.randomAdjustContrastGammaTo.text,
                    "invertImage":ui.randomAdjustContrastInvertImage.isChecked()
                }
            }
      
      return transformations