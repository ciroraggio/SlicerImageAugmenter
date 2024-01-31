import slicer
try:
  from monai.transforms import Rotate, Flip, Resize
except ModuleNotFoundError:
  slicer.util.pip_install("monai[itk]")
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
    # print(f"Rotate activated: {transformations.rotate.enabled}")
    if(transformations.rotate.enabled):
        # print(f"Found transformation rotate with params:\nangle:{transformations.rotate.angle}\nmode{transformations.rotate.interpolationMode}")
        mappedTransformations.append(Rotate(angle=float(transformations.rotate.angle), 
                                            mode=transformations.rotate.interpolationMode
                                            ))
    elif(transformations.resize.enabled):
        mappedTransformations.append(Resize(spatial_size=(transformations.resize.spatialSize),
                                            mode=transformations.resize.interpolationMode 
                                            ))
        
    return mappedTransformations


def getTransformations(ui) -> dict:
      transformations = {
                "rotate": {
                    "enabled": ui.rotateEnabled.isChecked(),
                    "angle": ui.rotateAngle.text,
                    "interpolationMode": ui.rotateInterpolationMode.currentText
                },
                "resize": {
                    "enabled": ui.resizeEnabled.isChecked(),
                    "spatialSize": (ui.resizeC.text, ui.resizeW.text, ui.resizeH.text),
                    "interpolationMode": ui.resizeInterpolationMode.currentText
                }
            }
      return transformations