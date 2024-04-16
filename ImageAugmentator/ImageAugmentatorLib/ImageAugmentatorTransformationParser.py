from ImageAugmentatorLib.ImageAugmentatorIntensity import ImageAugmentatorIntensityController
from ImageAugmentatorLib.ImageAugmentatorSpatial import ImageAugmentatorSpatialController
from ImageAugmentatorLib.ImageAugmentatorCrop import ImageAugmentatorCropController
from typing import List


DICT_KEYS = ["img", "mask"]
IMPOSSIBLE_COPY_INFO_TRANSFORM = ["Resize", "BorderPad", "SpatialCrop", "CenterSpatialCrop"]
class ImageAugmentatorTransformationParser():
    def __init__(self, ui):
       self.ui = ui
       self.spatialTransformationController : ImageAugmentatorSpatialController = None 
       self.intensityTransformationController : ImageAugmentatorIntensityController = None
       self.cropTransformationController : ImageAugmentatorCropController = None
       
    def mapTransformations(self) -> List[object]:
        mappedTransformations = []
        
        self.spatialTransformationController = ImageAugmentatorSpatialController(ui=self.ui, mappedTransformations=mappedTransformations, dictKeys=DICT_KEYS)
        self.intensityTransformationController = ImageAugmentatorIntensityController(ui=self.ui, mappedTransformations=mappedTransformations, dictKeys=DICT_KEYS)
        self.cropTransformationController = ImageAugmentatorCropController(ui=self.ui, mappedTransformations=mappedTransformations, dictKeys=DICT_KEYS)

        mappedTransformations = self.spatialTransformationController.mapTransformations()
        mappedTransformations = self.intensityTransformationController.mapTransformations()
        mappedTransformations = self.cropTransformationController.mapTransformations()

        if(not mappedTransformations): raise ValueError("Choose at least one transformation to apply")

        return mappedTransformations