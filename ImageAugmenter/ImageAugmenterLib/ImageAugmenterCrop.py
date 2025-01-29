from typing import Dict, List
from ImageAugmenterLib.ImageAugmenterTransformControllerInterface import ImageAugmenterTransformControllerInterface

class ImageAugmenterCropController(ImageAugmenterTransformControllerInterface):
    def __init__(self, ui, mappedTransformations: List[object], dictKeys: Dict[str, str]) -> None:
        from munch import Munch, munchify
        self.ui = ui
        self.transformations: Munch = munchify(self.getTransformations())
        self.mappedTransformations: List[object] = mappedTransformations
        self.dictKeys: Dict[str, str] = dictKeys

    def getTransformations(self) -> Dict[str, Dict]:
        return {
            "spatialPad": {
                "enabled": self.ui.spatialPadEnabled.isChecked(),
                "spatialSize": (self.ui.spatialPadC.text, self.ui.spatialPadW.text, self.ui.spatialPadH.text),
                "method": self.ui.spatialPadMethod.currentText,
                "mode": self.ui.spatialPadMode.currentText,
                "fillValue": self.ui.spatialPadFillValue.text
            },
            "borderPad": {
                "enabled": self.ui.borderPadEnabled.isChecked(),
                "spatialBorder": self.ui.borderPadSpatialBorder.text,
                "mode": self.ui.borderPadMode.currentText,
                "fillValue": self.ui.borderPadFillValue.text
            },
            "spatialCrop": {
                "enabled": self.ui.spatialCropEnabled.isChecked(),
                "roiCenter": (self.ui.spatialCropCenterH.text, self.ui.spatialCropCenterW.text, self.ui.spatialCropCenterC.text),
                "roiSize": ( self.ui.spatialCropSizeC.text, self.ui.spatialCropSizeW.text, self.ui.spatialCropSizeH.text),
            },
            "centerSpatialCrop": {
                "enabled": self.ui.centerSpatialCropEnabled.isChecked(),
                "roiSize": (self.ui.centerSpatialCropSizeC.text, self.ui.centerSpatialCropSizeW.text, self.ui.centerSpatialCropSizeH.text),
            },
        }

    def mapTransformations(self) -> List[object]:
        
        from monai.transforms import SpatialPad, BorderPad, SpatialCrop, CenterSpatialCrop
        
        if (self.transformations.spatialPad.enabled):
            params = self.transformations.spatialPad
            
            if (not all(params.spatialSize) or params.fillValue == None or params.fillValue == ""): 
                raise ValueError("The 'Spatial Pad' transformation is enabled but parameters are not valid. Please check all the parameters.")

            self.mappedTransformations.append(
                SpatialPad(spatial_size=(int(params.spatialSize[0]), int(params.spatialSize[1]), int(params.spatialSize[2])),    
                            mode=params.mode,
                            method=params.method,
                            value=params.fillValue)
                )
            
        if (self.transformations.borderPad.enabled):
            params = self.transformations.borderPad
            if (params.spatialBorder == "" or params.spatialBorder == None or params.fillValue == None or params.fillValue == ""):
                     raise ValueError("The 'Border Pad' transformation is enabled but parameters are not valid. Please check all the parameters.")

            self.mappedTransformations.append(BorderPad(spatial_border=int(params.spatialBorder), mode=params.mode, value=params.fillValue))

        if (self.transformations.spatialCrop.enabled):
            params = self.transformations.spatialCrop

            if (not all(params.roiSize) or not all(params.roiCenter) ):
                    raise ValueError("The 'Spatial Crop' transformation is enabled but ROI size or ROI center is not valid")
            
            self.mappedTransformations.append(SpatialCrop(
                roi_center=(int(params.roiCenter[0]),int(params.roiCenter[1]), int(params.roiCenter[2])),
                roi_size=(int(params.roiSize[0]),int(params.roiSize[1]), int(params.roiSize[2]))))
            
        if (self.transformations.centerSpatialCrop.enabled):
            params = self.transformations.centerSpatialCrop
            if (not all(params.roiSize)):
                    raise ValueError("The 'Center Spatial Crop' transformation is enabled but ROI size is not valid")
            
            self.mappedTransformations.append(CenterSpatialCrop(roi_size=(int(params.roiSize[0]), int(params.roiSize[1]), int(params.roiSize[2]))))

        return self.mappedTransformations
