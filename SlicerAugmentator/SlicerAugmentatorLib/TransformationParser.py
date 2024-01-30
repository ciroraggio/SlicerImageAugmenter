import slicer
try:
  from monai.transforms import Rotate, Flip, Resize
except ModuleNotFoundError:
  slicer.util.pip_install("monai[all]")
  from monai.transforms import Rotate, Flip, Resize



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
        mappedTransformations.append(Rotate(angle=transformations.rotate.angle, 
                                            mode=transformations.rotate.interpolationMode
                                            ))
    elif(transformations.resize.enabled):
        mappedTransformations.append(Resize(spatial_size=(transformations.resize.spatial_size),
                                            mode=transformations.resize.interpolationMode 
                                            ))
        
    return mappedTransformations


def getTransformations(ui) -> dict:
      transformations = {
                "rotate": {
                    "enabled": ui.rotateEnabled,
                    "angle": ui.rotateAngle,
                    "interpolationMode": ui.rotateInterpolationMode  
                },
                "resize": {
                    "enabled": ui.resizeEnabled,
                    "spatialSize": (ui.resizeC, ui.resizeW, ui.resizeH),
                    "interpolationMode": ui.resizeInterpolationMode
                }
            }
      return transformations