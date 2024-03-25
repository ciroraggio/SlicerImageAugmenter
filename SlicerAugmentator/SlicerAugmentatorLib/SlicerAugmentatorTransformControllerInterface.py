from abc import ABC, abstractmethod
from typing import Dict, List

class SlicerAugmentatorTransformControllerInterface(ABC):
    @abstractmethod
    def getTransformations(self) -> Dict[str, Dict]:
        """
        Returns a dictionary representing the configured transformations.
        """
        pass

    @abstractmethod
    def mapTransformations(self) -> List[object]:
        """
        Converts the configured transformations to a list of MONAI transformation objects.
        """
        pass