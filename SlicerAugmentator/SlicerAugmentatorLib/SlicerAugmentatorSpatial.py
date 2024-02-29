import slicer
try:
  from monai.transforms import Rotate, Flip, Resize, RandRotate
except ModuleNotFoundError:
  slicer.util.pip_install("monai[itk]")
  from monai.transforms import Rotate, Flip, Resize, RandRotate


def mapSpatialTransformations(transformations, mappedTransformations: list) -> list:    
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
                                keep_size=True, 
                                align_corners=transformations.randRotate.alignCorners))
      except Exception as e:
        raise ValueError(e)      
      
                                     
    if(transformations.resize.enabled):
        mappedTransformations.append(Resize(spatial_size=(transformations.resize.spatialSize),
                                            mode=transformations.resize.interpolationMode 
                                            ))
    if(transformations.flip.enabled):
        mappedTransformations.append(Flip(spatial_axis=int(transformations.flip.axes)))
     
        
    return mappedTransformations
