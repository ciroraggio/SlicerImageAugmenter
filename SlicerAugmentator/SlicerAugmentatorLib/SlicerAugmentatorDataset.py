import slicer

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
    def __init__(self, imgPaths, maskPaths = None, transformations = []):
        self.imgPaths = imgPaths
        self.maskPaths = maskPaths
        self.transformations = transformations
        
    def __len__(self):
        return len(self.imgPaths)
    
    def load(self, path: str):
        if(path):
            try:
                img = sitk.ReadImage(path)
                img_array = sitk.GetArrayFromImage(img)
                data = torch.tensor(img_array)
                return data
            except Exception as e:
                raise RuntimeError(e)
        return None, None

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
        transformedSegmentations = []

        img = self.load(self.imgPaths[idx])   
        if self.maskPaths is not None:
            mask = self.load(self.maskPaths[idx])

        for transform in self.transformations:
            if(img.any()):
                transformedImg = transform(img)
                transformedImages.append([transform.get_transform_info()["class"], transformedImg]) # adding ["rotate", torch.Tensor[[...]] ]
            if(mask.any()):
                transformedMask = transform(mask)
                transformedSegmentations.append([transform.get_transform_info()["class"], transformedMask])
            
        return transformedImages, transformedSegmentations