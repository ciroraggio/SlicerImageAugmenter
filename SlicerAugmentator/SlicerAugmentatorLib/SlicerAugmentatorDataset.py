import slicer

import SimpleITK as sitk
try:
    import numpy as np
    import monai
    import torch
    from monai.transforms import LoadImage
    from torch.utils.data import Dataset
    from torchvision.transforms import ToTensor
except ModuleNotFoundError:
    slicer.util.pip_install("monai[itk]")
    import monai
    import torch
    from monai.transforms import LoadImage
    from torch.utils.data import Dataset
    import numpy as np
    


class SlicerAugmentatorDataset(Dataset):
    def __init__(self, imgPaths, maskPaths = None, transformations = [], shuffle = False):
        self.imgPaths = imgPaths
        self.maskPaths = maskPaths
        self.transformations = transformations
        self.shuffleEnabled = shuffle
    
        # self.loader = LoadImage(reader=ITKReader, dtype=torch.float32)

    def __len__(self):
        return len(self.imgPaths)
    
    def getDataAndFilename(self, path: str):
        if(path):
            filename = path.split("/")[-1]
            try:
                img = sitk.ReadImage(path)
                img_array = sitk.GetArrayFromImage(img)
                data = torch.tensor(img_array)
                #data = self.loader(path)
                return filename, data
            except Exception as e:
                raise RuntimeError(e)
        return None, None

    def __getitem__(self, idx) -> tuple[str, list, str, list]:
        transformedImages = []
        transformedSegmentations = []

        imgFilename, img = self.getDataAndFilename(self.imgPaths[idx])
        
        if self.maskPaths is not None:
            maskFilename, mask = self.getDataAndFilename(self.maskPaths[idx])

        for transform in self.transformations:
            print(f"Apply transformation {transform} to {imgFilename}")
            if(img.any()):
                print(f"Img type {img.dtype}, Img shape {img.size()}")
                transformedImages.append(transform(img))
            if(mask.any()):
                transformedSegmentations.append(transform(mask))
            
        return transformedImages, transformedSegmentations