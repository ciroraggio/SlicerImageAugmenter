from typing import Any, Dict, List, Optional, Tuple, Union
import SimpleITK as sitk
import torch
from monai.transforms import RandomizableTransform
from torch.utils.data import Dataset

from ImageAugmenterLib.ImageAugmenterUtils import (
    extractDeviceNumber,
    getTransformName,
    CHANNEL_FIRST_REQUIRED
)


class ImageAugmenterDataset(Dataset):
    def __init__(
        self,
        imgPaths: List[str],
        maskPaths: Optional[List[str]] = None,
        transformations: List[object] = [],
        device: Union[str, int] = "CPU",
    ):
        self.imgPaths: List[str] = imgPaths
        self.maskPaths: Optional[List[str]] = maskPaths
        self.transformations: List[object] = transformations
        self.device: Union[str, int] = extractDeviceNumber(device) if device.lower() != "cpu" else device.lower()

    def __len__(self) -> int:
        return len(self.imgPaths)

    def load(self, path: str) -> Optional[torch.Tensor]:
        try:
            if (path):
                img = sitk.ReadImage(path)
                img_array = sitk.GetArrayFromImage(img)
                data = torch.tensor(img_array)
                return data
            return None
        except:
            return None

    def apply_transform(self, transform: object, img: torch.Tensor, transformedList: List[List[Any]]) -> List[List[Any]]:
        transform_name = getTransformName(transform)
        channel_first_required = transform_name in CHANNEL_FIRST_REQUIRED
    
        if(channel_first_required):
            img = img.unsqueeze(dim=0)

        transformedImg = transform(img.float())
        
        if(channel_first_required):
            transformedImg = transformedImg.squeeze(dim=0)
            
        # adding ["rotate", torch.Tensor[[...]] ]
        transformedList.append([transform_name, transformedImg])

        return transformedList

    def apply_dict_transform(
        self,
        transform: object,
        data_dict: Dict[str, torch.Tensor],
        transformedImages: List[List[Any]],
        transformedMasks: Optional[List[List[Any]]] = None,
    ) -> List[List[Any]]:  # Generic return for flexibility
        
        transform_name = getTransformName(transform)
        channel_first_required = transform_name in CHANNEL_FIRST_REQUIRED

        if(transformedMasks != None):
            if(channel_first_required):
                data_dict["img"] = data_dict["img"].unsqueeze(dim=0)
                data_dict["mask"] = data_dict["mask"].unsqueeze(dim=0)
                
            transformedImg, transformedMask = transform(data_dict).values()
            
            if(channel_first_required):
                transformedImg =transformedImg.squeeze(dim=0)
                transformedMask = transformedMask.squeeze(dim=0)
                
            # adding ["rotate", torch.Tensor[[...]] ]
            transformedImages.append([transform_name, transformedImg])
            transformedMasks.append([transform_name, transformedMask])
            return transformedImages, transformedMasks

        transformedImg = transform(data_dict)
        transformedImages.append([transform_name, transformedImg["img"]])
        return transformedImages, []

    def __getitem__(self, idx: int) -> Tuple[List[List[Any]], Optional[List[List[Any]]]]:
        """Returns
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
            if (img != None and mask != None and isinstance(transform, RandomizableTransform)):
                transformedImages, transformedMasks = self.apply_dict_transform(transform, {"img": img.to(self.device), "mask": mask.to(self.device)}, transformedImages, transformedMasks)

            if (img != None and mask == None and isinstance(transform, RandomizableTransform)):
                transformedImages, transformedMasks = self.apply_dict_transform(transform, {"img": img.to(self.device)}, transformedImages, None)

            if (img != None and not isinstance(transform, RandomizableTransform)):
                transformedImages = self.apply_transform(transform, img.to(self.device), transformedImages)

            if (mask != None and not isinstance(transform, RandomizableTransform)):
                transformedMasks = self.apply_transform(transform, mask.to(self.device), transformedMasks)

        return transformedImages, transformedMasks
