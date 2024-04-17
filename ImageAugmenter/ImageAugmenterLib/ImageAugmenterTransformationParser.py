from ImageAugmenterLib.ImageAugmenterIntensity import ImageAugmenterIntensityController
from ImageAugmenterLib.ImageAugmenterSpatial import ImageAugmenterSpatialController
from ImageAugmenterLib.ImageAugmenterCrop import ImageAugmenterCropController
from typing import List


DICT_KEYS = ["img", "mask"]
IMPOSSIBLE_COPY_INFO_TRANSFORM = ["Resize", "BorderPad", "SpatialCrop", "CenterSpatialCrop"]
class ImageAugmenterTransformationParser():
    def __init__(self, ui):
       self.ui = ui
       self.spatialTransformationController : ImageAugmenterSpatialController = None 
       self.intensityTransformationController : ImageAugmenterIntensityController = None
       self.cropTransformationController : ImageAugmenterCropController = None
       
    def mapTransformations(self) -> List[object]:
        mappedTransformations = []
        
        self.spatialTransformationController = ImageAugmenterSpatialController(ui=self.ui, mappedTransformations=mappedTransformations, dictKeys=DICT_KEYS)
        self.intensityTransformationController = ImageAugmenterIntensityController(ui=self.ui, mappedTransformations=mappedTransformations, dictKeys=DICT_KEYS)
        self.cropTransformationController = ImageAugmenterCropController(ui=self.ui, mappedTransformations=mappedTransformations, dictKeys=DICT_KEYS)

        mappedTransformations = self.spatialTransformationController.mapTransformations()
        mappedTransformations = self.intensityTransformationController.mapTransformations()
        mappedTransformations = self.cropTransformationController.mapTransformations()

        if(not mappedTransformations): raise ValueError("Choose at least one transformation to apply")

        return mappedTransformations