import slicer
from SlicerAugmentatorLib.SlicerAugmentatorIntensity import SlicerAugmentatorIntensityController
from SlicerAugmentatorLib.SlicerAugmentatorSpatial import SlicerAugmentatorSpatialController
from typing import List

try:
  from munch import Munch
except ModuleNotFoundError:
  slicer.util.pip_install("munch")
  from munch import Munch

DICT_KEYS = ["img", "mask"]
IMPOSSIBLE_COPY_INFO_TRANSFORM = ["Resize"]
class SlicerAugmentatorTransformationParser():
    def __init__(self, ui):
       self.ui = ui
       self.spatialTransformationController : SlicerAugmentatorSpatialController = None 
       self.intensityTransformationController : SlicerAugmentatorIntensityController = None
       
    def mapTransformations(self) -> List[object]:
        mappedTransformations = []
        
        self.spatialTransformationController = SlicerAugmentatorSpatialController(ui=self.ui, mappedTransformations=mappedTransformations, dictKeys=DICT_KEYS)
        self.intensityTransformationController = SlicerAugmentatorIntensityController(ui=self.ui, mappedTransformations=mappedTransformations, dictKeys=DICT_KEYS)

        mappedTransformations = self.spatialTransformationController.mapTransformations()
        mappedTransformations = self.intensityTransformationController.mapTransformations()

        if(not mappedTransformations): raise ValueError("Choose at least one transformation to apply")

        return mappedTransformations