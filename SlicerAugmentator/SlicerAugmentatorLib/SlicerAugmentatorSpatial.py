import slicer
try:
  from monai.transforms import Rotate, Flip, RandAxisFlipd, Resize, RandRotated, Zoom, RandZoomd
except ModuleNotFoundError:
  slicer.util.pip_install("monai[itk]")
  from monai.transforms import Rotate, Flip, RandAxisFlipd, Resize, RandRotated, Zoom, RandZoomd


def mapSpatialTransformations(transformations, mappedTransformations: list, dict_keys: dict) -> list:    
    if(transformations.rotate.enabled):
        if(transformations.rotate.angle == ""):
          raise ValueError("The 'Rotate' transformation is enabled but angle is not specified")
        
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
                                                
        mappedTransformations.append(RandRotated(prob=1,
                                keys=dict_keys,               
                                range_x=rangeX, 
                                range_y=rangeY, 
                                range_z=rangeZ, 
                                padding_mode=transformations.randRotate.paddingMode, 
                                mode=transformations.randRotate.interpolationMode, 
                                keep_size=True, 
                                align_corners=transformations.randRotate.alignCorners,
                                allow_missing_keys=True))
      except Exception as e:
        raise ValueError(e)      
      
                                     
    if(transformations.resize.enabled):
      for size in transformations.resize.spatialSize:
        if (size == None or size==""): 
          raise ValueError("The 'Resize' transformation is enabled but spatial size is not specified")

        mappedTransformations.append(Resize(spatial_size=(transformations.resize.spatialSize),
                                            mode=transformations.resize.interpolationMode 
                                            ))
    if(transformations.flip.enabled):
      if(transformations.flip.axis == "" or transformations.flip.axis == None):
        raise ValueError("The 'Flip' transformation is enabled but axis is not specified")

      mappedTransformations.append(Flip(spatial_axis=int(transformations.flip.axis)))
     
    if(transformations.randomFlip.enabled):
        mappedTransformations.append(RandAxisFlipd(prob=1, keys=dict_keys, allow_missing_keys=True))
        
    if(transformations.zoom.enabled):
        if(transformations.zoom.factor == ""):
          raise ValueError("The 'Zoom' transformation is enabled but factor is not specified")      
        
        alignCorners = transformations.zoom.alignCorners if(transformations.zoom.interpolationMode in ["linear", "bilinear", "bicubic", "trilinear"]) else None
        mappedTransformations.append(Zoom(zoom=float(transformations.zoom.factor),
                                          mode=transformations.zoom.interpolationMode,
                                          padding_mode=transformations.zoom.paddingMode,
                                          align_corners=alignCorners))
        
    if(transformations.randomZoom.enabled):
        if(transformations.randomZoom.factorMin == "" or transformations.randomZoom.factorMax == ""):
          raise ValueError("The 'Random Zoom' transformation is enabled but factors are not specified")      
        
        alignCorners = transformations.randomZoom.alignCorners if(transformations.randomZoom.interpolationMode in ["linear", "bilinear", "bicubic", "trilinear"]) else None
        mappedTransformations.append(RandZoomd(prob=1,
                                          min_zoom=float(transformations.randomZoom.factorMin),
                                          max_zoom=float(transformations.randomZoom.factorMax),
                                          mode=transformations.randomZoom.interpolationMode,
                                          padding_mode=transformations.randomZoom.paddingMode,
                                          align_corners=alignCorners,
                                          keep_size=True,
                                          keys=dict_keys,
                                          allow_missing_keys=True))
     
        
    return mappedTransformations 