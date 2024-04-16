from typing import Dict, List
from ImageAugmentatorLib.ImageAugmentatorTransformControllerInterface import ImageAugmentatorTransformControllerInterface


class ImageAugmentatorSpatialController(ImageAugmentatorTransformControllerInterface):
    def __init__(self, ui, mappedTransformations: List[object], dictKeys: Dict[str, str]) -> None:
        
        from munch import Munch, munchify
        
        self.ui = ui
        self.transformations: Munch = munchify(self.getTransformations())
        self.mappedTransformations: List[object] = mappedTransformations
        self.dictKeys: Dict[str, str] = dictKeys

    def getTransformations(self) -> Dict[str, Dict]:
        return {
            "rotate": {
                "enabled": self.ui.rotateEnabled.isChecked(),
                "angle": self.ui.rotateAngle.text,
                "interpolationMode": self.ui.rotateInterpolationMode.currentText
            },
            "randRotate": {
                "enabled": self.ui.randomRotateEnabled.isChecked(),
                "rangeFromX": self.ui.randomRotateFromX.text,
                "rangeToX": self.ui.randomRotateToX.text,
                "rangeFromY": self.ui.randomRotateFromY.text,
                "rangeToY": self.ui.randomRotateToY.text,
                "rangeFromZ": self.ui.randomRotateFromZ.text,
                "rangeToZ": self.ui.randomRotateToZ.text,
                "paddingMode": self.ui.randomRotatePaddingMode.currentText,
                "interpolationMode": self.ui.randomRotateInterpolationMode.currentText,
                "alignCorners": self.ui.randomRotateAlignCorners.isChecked(),
            },
            "resize": {
                "enabled": self.ui.resizeEnabled.isChecked(),
                "spatialSize": (self.ui.resizeW.text, self.ui.resizeH.text),
                "interpolationMode": self.ui.resizeInterpolationMode.currentText
            },
            "flip": {
                "enabled": self.ui.flipEnabled.isChecked(),
                "axis": self.ui.flipAxis.text,
            },
            "randomFlip": {
                "enabled": self.ui.randomFlipEnabled.isChecked(),
            },
            "zoom": {
                "enabled": self.ui.zoomEnabled.isChecked(),
                "factor": self.ui.zoomFactor.text,
                "interpolationMode": self.ui.zoomInterpolationMode.currentText,
                "paddingMode": self.ui.zoomPaddingMode.currentText,
                "alignCorners": self.ui.zoomAlignCorners.isChecked(),
            },
            "randomZoom": {
                "enabled": self.ui.randomZoomEnabled.isChecked(),
                "factorMin": self.ui.randomZoomFactorMin.text,
                "factorMax": self.ui.randomZoomFactorMax.text,
                "interpolationMode": self.ui.randomZoomInterpolationMode.currentText,
                "paddingMode": self.ui.randomZoomPaddingMode.currentText,
                "alignCorners": self.ui.randomZoomAlignCorners.isChecked(),
            },
        }

    def mapTransformations(self) -> List[object]:
        from monai.transforms import Rotate, Flip, RandAxisFlipd, Resize, RandRotated, Zoom, RandZoomd
        if (self.transformations.rotate.enabled):
            if (self.transformations.rotate.angle == ""):
                raise ValueError("The 'Rotate' transformation is enabled but angle is not specified")

            self.mappedTransformations.append(Rotate(angle=float(self.transformations.rotate.angle),
                                                     mode=self.transformations.rotate.interpolationMode
                                                     ))
        if (self.transformations.randRotate.enabled):
            rangeX, rangeY, rangeZ = [0, 0], [0, 0], [0, 0]
            try:
                if (self.transformations.randRotate.rangeFromX != "" and self.transformations.randRotate.rangeToX != ""):
                    rangeX = [float(self.transformations.randRotate.rangeFromX), float(
                        self.transformations.randRotate.rangeToX)]
                if (self.transformations.randRotate.rangeFromY != "" and self.transformations.randRotate.rangeToY != ""):
                    rangeY = [float(self.transformations.randRotate.rangeFromY), float(
                        self.transformations.randRotate.rangeToY)]
                if (self.transformations.randRotate.rangeFromZ != "" and self.transformations.randRotate.rangeToZ != ""):
                    rangeZ = [float(self.transformations.randRotate.rangeFromZ), float(
                        self.transformations.randRotate.rangeToZ)]

                self.mappedTransformations.append(RandRotated(prob=1,
                                                              keys=self.dictKeys,
                                                              range_x=rangeX,
                                                              range_y=rangeY,
                                                              range_z=rangeZ,
                                                              padding_mode=self.transformations.randRotate.paddingMode,
                                                              mode=self.transformations.randRotate.interpolationMode,
                                                              keep_size=True,
                                                              align_corners=self.transformations.randRotate.alignCorners,
                                                              allow_missing_keys=True))
            except Exception as e:
                raise ValueError(e)

        if (self.transformations.resize.enabled):
            params = self.transformations.resize
            if(not all(params.spatialSize)): raise ValueError("The 'Resize' transformation is enabled but spatial size is not specified")

            self.mappedTransformations.append(Resize(spatial_size=(int(self.transformations.resize.spatialSize[0]),
                                                                   int(self.transformations.resize.spatialSize[1])),
                                                     mode=self.transformations.resize.interpolationMode
                                                     ))
        if (self.transformations.flip.enabled):
            params = self.transformations.flip
            if (params.axis == "" or params.axis == None):
                raise ValueError("The 'Flip' transformation is enabled but axis is not specified")

            self.mappedTransformations.append(Flip(spatial_axis=int(params.axis)))

        if (self.transformations.randomFlip.enabled):
            self.mappedTransformations.append(RandAxisFlipd(prob=1, keys=self.dictKeys, allow_missing_keys=True))

        if (self.transformations.zoom.enabled):
            params = self.transformations.zoom
            if (params.factor == ""):
                raise ValueError("The 'Zoom' transformation is enabled but factor is not specified")

            alignCorners = params.alignCorners if (params.interpolationMode in ["linear", "bilinear", "bicubic", "trilinear"]) else None
            self.mappedTransformations.append(Zoom(zoom=float(params.factor),
                                              mode=params.interpolationMode,
                                              padding_mode=params.paddingMode,
                                              align_corners=alignCorners))

        if (self.transformations.randomZoom.enabled):
            params = self.transformations.randomZoom
            if (params.factorMin == "" or params.factorMax == ""):
                raise ValueError("The 'Random Zoom' transformation is enabled but factors are not specified")

            alignCorners = params.alignCorners if (
                params.interpolationMode in ["linear", "bilinear", "bicubic", "trilinear"]) else None
            self.mappedTransformations.append(RandZoomd(prob=1,
                                              min_zoom=float(params.factorMin),
                                              max_zoom=float(params.factorMax),
                                              mode=params.interpolationMode,
                                              padding_mode=params.paddingMode,
                                              align_corners=alignCorners,
                                              keep_size=True,
                                              keys=self.dictKeys,
                                              allow_missing_keys=True))

        return self.mappedTransformations
