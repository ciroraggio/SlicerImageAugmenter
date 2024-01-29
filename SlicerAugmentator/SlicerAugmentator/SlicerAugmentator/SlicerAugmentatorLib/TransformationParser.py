def mapTransformations(ui) -> list:
    transformations = getTransformations(ui)
    
    return NotImplementedError


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