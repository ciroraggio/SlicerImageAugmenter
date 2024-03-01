import slicer
try:
  from monai.transforms import ScaleIntensity, RandScaleIntensityd, AdjustContrast, RandAdjustContrastd, RandGaussianNoised, ShiftIntensity, RandShiftIntensityd, NormalizeIntensity, ThresholdIntensity, MedianSmooth, GaussianSmooth, RandGaussianSmoothd
except ModuleNotFoundError:
  slicer.util.pip_install("monai[itk]")
  from monai.transforms import ScaleIntensity, RandScaleIntensityd, AdjustContrast, RandAdjustContrastd, RandGaussianNoised, ShiftIntensity, RandShiftIntensityd, NormalizeIntensity, ThresholdIntensity, MedianSmooth, GaussianSmooth, RandGaussianSmoothd


def mapIntensityTransformations(transformations, mappedTransformations: list, dict_keys: dict) -> list:    
    if(transformations.scaleIntensity.enabled):
        if(transformations.scaleIntensity.factor == ""):
          raise ValueError("The 'Scale Intensity' transformation is enabled but factor is not specified")      
        
        mappedTransformations.append(ScaleIntensity(factor=(float(transformations.scaleIntensity.factor))))    
         
    if(transformations.randomScaleIntensity.enabled):
        if(transformations.randomScaleIntensity.factorFrom == "" or transformations.randomScaleIntensity.factorTo == ""):
          raise ValueError("The 'Randomd Scale Intensity' transformation is enabled but factors are not specified")      
        
        mappedTransformations.append(RandScaleIntensityd(prob=1, 
                                                        factors=(float(transformations.randomScaleIntensity.factorFrom), 
                                                                 float(transformations.randomScaleIntensity.factorTo)),
                                                        keys=dict_keys,
                                                        allow_missing_keys=True
                                                        ))    
        
    if(transformations.adjustContrast.enabled):
        if(transformations.adjustContrast.gamma == ""):
          raise ValueError("The 'Adjust Contrast' transformation is enabled but gamma value is not specified")      
        
        mappedTransformations.append(AdjustContrast(gamma=(float(transformations.adjustContrast.gamma)),
                                                    invert_image=transformations.adjustContrast.invertImage,
                                                    retain_stats=True
                                                  )
                                     )  
          
    if(transformations.randomAdjustContrast.enabled):
        if(transformations.randomAdjustContrast.gammaFrom == "" or transformations.randomAdjustContrast.gammaTo == ""):
          raise ValueError("The 'Random Adjust Contrast' transformation is enabled but gamma values are not specified")      
        
        mappedTransformations.append(RandAdjustContrastd(prob=1, 
                                                        gamma=(float(transformations.randomAdjustContrast.gammaFrom), float(transformations.randomAdjustContrast.gammaTo)),
                                                        invert_image=transformations.randomAdjustContrast.invertImage,
                                                        retain_stats=True,
                                                        keys=dict_keys,
                                                        allow_missing_keys=True
                                                        )
                                     )    
    if(transformations.randomGaussianNoise.enabled):  
        mean = float(transformations.randomGaussianNoise.mean) if(transformations.randomGaussianNoise.mean != "") else 0.0
        std = float(transformations.randomGaussianNoise.std) if(transformations.randomGaussianNoise.std != "") else 0.1   
        mappedTransformations.append(RandGaussianNoised(prob=1, 
                                                        mean=mean, 
                                                        std=std,
                                                        keys=dict_keys,
                                                        allow_missing_keys=True))  
          
    if(transformations.shiftIntensity.enabled):  
        if(transformations.shiftIntensity.offset == ""):
          raise ValueError("The 'Shift Intensity' transformation is enabled but offset value is not specified")    
      
        mappedTransformations.append(ShiftIntensity(offset=float(transformations.shiftIntensity.offset)))    
        
    if(transformations.randomShiftIntensity.enabled):  
        if(transformations.randomShiftIntensity.offsetFrom == "" or transformations.randomShiftIntensity.offsetTo == ""):
          raise ValueError("The 'Random Shift Intensity' transformation is enabled but offsets values are not specified")    
      
        mappedTransformations.append(RandShiftIntensityd(prob=1, 
                                                        offsets=(float(transformations.randomShiftIntensity.offsetFrom, transformations.randomShiftIntensity.offsetTo)),
                                                        keys=dict_keys,
                                                        allow_missing_keys=True))    
        
    if(transformations.normalizeIntensity.enabled):  
        if(transformations.normalizeIntensity.subtrahend == "" or transformations.normalizeIntensity.divisor == ""):
          raise ValueError("The 'Normalize Intensity' transformation is enabled but values are not specified")    
      
        mappedTransformations.append(NormalizeIntensity(subtrahend=float(transformations.normalizeIntensity.subtrahend), 
                                                        divisor=float(transformations.normalizeIntensity.divisor),
                                                        nonzero=transformations.normalizeIntensity.nonZero))    
        
    if(transformations.thresholdIntensity.enabled):  
        if(transformations.thresholdIntensity.thresholdValue == ""):
          raise ValueError("The 'Threshold Intensity' transformation is enabled but threshold value are not specified")    

        cVal = float(transformations.thresholdIntensity.cVal) if transformations.thresholdIntensity.cVal else 0.0
        mappedTransformations.append(ThresholdIntensity(threshold=float(transformations.thresholdIntensity.thresholdValue), cval=cVal, above=transformations.thresholdIntensity.above))    
        
    if(transformations.medianSmooth.enabled):  
        radius = float(transformations.medianSmooth.radius) if transformations.medianSmooth.radius else 1
        mappedTransformations.append(MedianSmooth(radius=radius))
            
    if(transformations.gaussianSmooth.enabled):  
        sigma = float(transformations.gaussianSmooth.sigma) if transformations.gaussianSmooth.sigma else 1
        mappedTransformations.append(GaussianSmooth(sigma=sigma, approx=transformations.gaussianSmooth.kernel))    
    
    if(transformations.randGaussianSmooth.enabled):
      sigmaX, sigmaY, sigmaZ = [0,0], [0,0], [0,0]
      
      try:
        if(transformations.randGaussianSmooth.sigmaFromX != "" and transformations.randGaussianSmooth.sigmaToX != "" ):
            sigmaX = [float(transformations.randGaussianSmooth.sigmaFromX), float(transformations.randGaussianSmooth.sigmaToX)]
        if(transformations.randGaussianSmooth.sigmaFromY != "" and transformations.randGaussianSmooth.sigmaToY != "" ):
            sigmaY = [float(transformations.randGaussianSmooth.sigmaFromY), float(transformations.randGaussianSmooth.sigmaToY)]
        if(transformations.randGaussianSmooth.sigmaFromZ != "" and transformations.randGaussianSmooth.sigmaToZ != "" ):
            sigmaZ = [float(transformations.randGaussianSmooth.sigmaFromZ), float(transformations.randGaussianSmooth.sigmaToZ)]
                                                
        mappedTransformations.append(RandGaussianSmoothd(prob=1,
                                sigma_x=sigmaX, 
                                sigma_y=sigmaY, 
                                sigma_z=sigmaZ, 
                                approx=transformations.randGaussianSmooth.kernel,
                                keys=dict_keys,
                                allow_missing_keys=True))
      except Exception as e:
        raise ValueError(e) 
      
               
    return mappedTransformations
