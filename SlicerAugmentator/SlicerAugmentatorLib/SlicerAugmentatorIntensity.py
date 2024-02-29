import slicer
try:
  from monai.transforms import RandScaleIntensity, RandAdjustContrast, RandGaussianNoise, ShiftIntensity, RandShiftIntensity
except ModuleNotFoundError:
  slicer.util.pip_install("monai[itk]")
  from monai.transforms import RandScaleIntensity, RandAdjustContrast, RandGaussianNoise, ShiftIntensity, RandShiftIntensity


def mapIntensityTransformations(transformations, mappedTransformations: list) -> list:    
    if(transformations.randomScaleIntensity.enabled):
        if(transformations.randomScaleIntensity.factor == ""):
          raise ValueError("The 'Random Scale Intensity' transformation is enabled but a factor is not specified")      
        
        mappedTransformations.append(RandScaleIntensity(prob=1, factors=float(transformations.randomScaleIntensity.factor)))    
        
    if(transformations.randomAdjustContrast.enabled):
        if(transformations.randomAdjustContrast.gammaFrom == "" or transformations.randomAdjustContrast.gammaTo == ""):
          raise ValueError("The 'Random Adjust Contrast' transformation is enabled but gamma values are not specified")      
        
        mappedTransformations.append(RandAdjustContrast(prob=1, 
                                                        gamma=(float(transformations.randomAdjustContrast.gammaFrom), float(transformations.randomAdjustContrast.gammaTo)),
                                                        invert_image=transformations.randomAdjustContrast.invertImage,
                                                        retain_stats=True
                                                        )
                                     )    
    if(transformations.randomGaussianNoise.enabled):  
        mean = float(transformations.randomGaussianNoise.mean) if(transformations.randomGaussianNoise.mean != "") else 0.0
        std = float(transformations.randomGaussianNoise.std) if(transformations.randomGaussianNoise.std != "") else 0.1   
        mappedTransformations.append(RandGaussianNoise(prob=1, mean=mean, std=std))  
          
    if(transformations.shiftIntensity.enabled):  
        if(transformations.shiftIntensity.offset == ""):
          raise ValueError("The 'Shift Intensity' transformation is enabled but offset value is not specified")    
      
        mappedTransformations.append(ShiftIntensity(prob=1, offset=float(transformations.shiftIntensity.offset)))    
        
    if(transformations.shiftIntensity.enabled):  
        if(transformations.shiftIntensity.offsetFrom == "" or transformations.shiftIntensity.offsetTo == ""):
          raise ValueError("The 'Random Shift Intensity' transformation is enabled but offsets values are not specified")    
      
        mappedTransformations.append(RandShiftIntensity(prob=1, offsets=(float(transformations.shiftIntensity.offsetFrom, transformations.shiftIntensity.offsetTo))))    
        
    return mappedTransformations
