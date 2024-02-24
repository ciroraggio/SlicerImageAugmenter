import slicer
from SlicerAugmentatorLib.SlicerAugmentatorUtils import sanitizeTransformName
import SimpleITK as sitk
try:
    import numpy as np
    import torch
    from torch.utils.data import Dataset
except ModuleNotFoundError:
    slicer.util.pip_install("monai[itk]")
    import torch
    from torch.utils.data import Dataset
    import numpy as np


class SlicerAugmentatorDataset(Dataset):
    def __init__(self, imgPaths, maskPaths=None, transformations=[]):
        self.imgPaths = imgPaths
        self.maskPaths = maskPaths
        self.transformations = transformations

    def __len__(self):
        return len(self.imgPaths)

    def load(self, path: str):
        if (path):
            img = sitk.ReadImage(path)
            img_array = sitk.GetArrayFromImage(img)
            data = torch.tensor(img_array)
            return data
        return None, None

    def apply_transform(self, transform, img, transformedList: list) -> list:
        if (img.any()):
            transformedImg = transform(img)
            try:
                transform_name = transform.get_transform_info()["class"]
            except AttributeError:
                # in this case get_transform_info is missing, so recover the name starting from __class__:
                transform_name = sanitizeTransformName(transform)

            # adding ["rotate", torch.Tensor[[...]] ]
            transformedList.append([transform_name, transformedImg])

        return transformedList

    def __getitem__(self, idx) -> tuple[list[list[str, torch.Tensor]], list[list[str, torch.Tensor]]]:
        """
        Returns:
            transformedImgs | transformedMasks  =  [
                ["rotate", torch.Tensor[[...]] ],
                ["rotate", torch.Tensor[[...]] ],
                ["flip", torch.Tensor[[...]] ],
                ["flip", torch.Tensor[[...]] ],
                ...
            ]
        """
        transformedImages = []
        transformedMasks = []
        mask = None
        
        img = self.load(self.imgPaths[idx])
        if self.maskPaths is not None and len(self.maskPaths) > 0:
            mask = self.load(self.maskPaths[idx])

        for transform in self.transformations:
            transformedImages = self.apply_transform(transform, img, transformedImages)
            if (mask != None):
                transformedMasks = self.apply_transform(transform, mask, transformedMasks)

        return transformedImages, transformedMasks
