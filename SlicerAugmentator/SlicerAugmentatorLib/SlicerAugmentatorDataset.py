import slicer

from PIL import Image
try:
    import monai
    import torch
    from monai.transforms import LoadImage
    from torch.utils.data import Dataset
except ModuleNotFoundError:
    slicer.util.pip_install("monai[all]")
    import monai
    import torch
    from monai.transforms import LoadImage
    from torch.utils.data import Dataset

class SlicerAugmentatorDataset(Dataset):
    def __init__(self, imgPaths, maskPaths = None, transformations = [], shuffle = False):
        self.imgPaths = imgPaths
        self.maskPaths = maskPaths
        self.transformations = transformations
        self.shuffleEnabled = shuffle
    
        self.loader = LoadImage(dtype=torch.float32)

    def __len__(self):
        return len(self.imgPaths)
    
    def getDataAndFilename(self, path: str):
        if(path):
            filename = path.split("/")[-1]
            data = self.loader(path)
            return filename, data
        return None, None

    def __getitem__(self, idx) -> tuple[str, list, str, list]:
        transformedImages = []
        transformedSegmentations = []

        _, img = self.getDataAndFilename(self.imgPaths[idx])
        
        if self.maskPaths is not None:
            maskFilename, mask = self.getDataAndFilename(self.maskPaths[idx])

        for transform in self.transformations:
            transformedImages.append(transform(img))
            if(mask):
                transformedSegmentations.append(transform(mask))
            
        return transformedImages, transformedSegmentations