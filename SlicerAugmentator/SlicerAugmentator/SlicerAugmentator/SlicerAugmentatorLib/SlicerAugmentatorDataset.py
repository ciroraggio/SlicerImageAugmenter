from torch.utils.data import Dataset
from monai.transforms import LoadImage
import torch

class SlicerAugmentatorDataset(Dataset):
    def __init__(self, img_paths, mask_paths, transforms = [], shuffle = False):
        self.img_paths = img_paths
        self.mask_paths = mask_paths
        self.transforms = transforms
        self.loader = LoadImage(image_only=True, dtype=torch.float32)
        self.shuffle_enabled = shuffle

    def __len__(self):
        return len(self.img_paths)
    
    def get_data_and_filename(self, path: str):
        if(path):
            filename = path.split("/")[-1]
            data = self.loader(path)
            return filename, data
        return None, None

    def __getitem__(self, idx) -> tuple[str, list, str, list]:
        # load data
        transformed_images = []
        transformed_segmentations = []

        img_filename, img = self.get_data_and_filename(self.img_paths[idx])
        
        if self.mask_paths is not None:
            mask_filename, mask = self.get_data_and_filename(self.mask_paths[idx])

        for transform in self.transforms:
            transformed_images.extend(transform(img))
            if(mask):
                transformed_segmentations.extend(transform(mask))
            
        return img_filename, transformed_images, mask_filename, transformed_segmentations