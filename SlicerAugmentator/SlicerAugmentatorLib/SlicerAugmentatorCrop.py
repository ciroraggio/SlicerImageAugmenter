import slicer
from typing import Dict, List

try:
    from monai.transforms import SpatialPad, BorderPad, SpatialCrop, CenterSpatialCrop
    from munch import Munch, munchify
except ModuleNotFoundError:
    slicer.util.pip_install("monai[itk]")
    slicer.util.pip_install("munch")
    from monai.transforms import SpatialPad, BorderPad, SpatialCrop, CenterSpatialCrop
    from munch import Munch, munchify

from SlicerAugmentatorLib.SlicerAugmentatorTransformControllerInterface import SlicerAugmentatorTransformControllerInterface

class SlicerAugmentatorCropController(SlicerAugmentatorTransformControllerInterface):
    def __init__(self, ui, mappedTransformations: List[object], dictKeys: Dict[str, str]) -> None:
        self.ui = ui
        self.transformations: Munch = munchify(self.getTransformations())
        self.mappedTransformations: List[object] = mappedTransformations
        self.dictKeys: Dict[str, str] = dictKeys

    def getTransformations(self) -> Dict[str, Dict]:
        return {
            "spatialPad": {
                "enabled": self.ui.spatialPadEnabled.isChecked(),
                "spatialSize": (self.ui.spatialPadW.text, self.ui.spatialPadH.text),
                "method": self.ui.spatialPadMethod.currentText,
                "mode": self.ui.spatialPadMode.currentText
            },
            "borderPad": {
                "enabled": self.ui.borderPadEnabled.isChecked(),
                "spatialBorder": self.ui.borderPadSpatialBorder.text,
                "mode": self.ui.borderPadMode.currentText,
            },
            "spatialCrop": {
                "enabled": self.ui.spatialCropEnabled.isChecked(),
                "roiCenter": (self.ui.spatialCropCenterH.text, self.ui.spatialCropCenterW.text, self.ui.spatialCropCenterC.text),
                "roiSize": (self.ui.spatialCropSizeH.text, self.ui.spatialCropSizeW.text, self.ui.spatialCropSizeC.text),
            },
            "centerSpatialCrop": {
                "enabled": self.ui.centerSpatialCropEnabled.isChecked(),
                "roiSize": (self.ui.centerSpatialCropSizeW.text, self.ui.centerSpatialCropSizeH.text),
            },
        }

    def mapTransformations(self) -> List[object]:
        if (self.transformations.spatialPad.enabled):
            params = self.transformations.spatialPad
            
            if (not all(params.spatialSize)): raise ValueError("The 'Spatial Pad' transformation is enabled but spatial size is not valid")

            self.mappedTransformations.append(SpatialPad(spatial_size=(int(params.spatialSize[0]), int(params.spatialSize[1])),
                                                        mode=params.mode,
                                                        method=params.method))
            
        if (self.transformations.borderPad.enabled):
            params = self.transformations.borderPad
            if (params.spatialBorder == "" or params.spatialBorder == None):
                     raise ValueError("The 'Border Pad' transformation is enabled but spatial border is not valid")

            self.mappedTransformations.append(BorderPad(spatial_border=int(params.spatialBorder), mode=params.mode))

        if (self.transformations.spatialCrop.enabled):
            params = self.transformations.spatialCrop

            if (not all(params.roiSize) or not all(params.roiCenter)):
                    raise ValueError("The 'Spatial Crop' transformation is enabled but ROI size or ROI center is not valid")
            
            self.mappedTransformations.append(SpatialCrop(
                roi_center=(int(params.roiCenter[0]),int(params.roiCenter[1]), int(params.roiCenter[2])),
                roi_size=(int(params.roiSize[0]),int(params.roiSize[1]), int(params.roiSize[2]))))
            
        if (self.transformations.centerSpatialCrop.enabled):
            params = self.transformations.centerSpatialCrop
            if (not all(params.roiSize)):
                    raise ValueError("The 'Center Spatial Crop' transformation is enabled but ROI size is not valid")
            
            self.mappedTransformations.append(CenterSpatialCrop(roi_size=
                                                                (int(params.roiSize[0]),int(params.roiSize[1]))
                                                                ))

        return self.mappedTransformations
