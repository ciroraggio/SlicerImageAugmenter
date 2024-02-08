# SlicerAugmentator

## Project Description
MONAI and PyTorch based medical image augmentation tool that can be integrated in Slicer.
The project aims to be a low-code version of the tool: <https://github.com/ciroraggio/AugmentedDataLoader>.

It's designed to operate on a dataset of medical images and apply a series of specific transformations to each image. This process augments the original dataset, providing a greater variety of samples for training deep learning models.

## Chengelog
 - v0.1:
    1.  Implemented interface for loading images and masks, choosing transformations and saving images.
    2.  Implemented and tested MONAI spatial transformations such as Rotation, RandRotation, Flip, Resize.
    3.  Partially implemented input validation and MONAI intensity transformations, it will be completed in the future.
    4.  Partially implemented "Preview" feature, which allows the output of transformations to be viewed directly in the scene before saving them in the OS, will be completed in the future.

# Illustrations [<ins>beta</ins>]
![main](https://github.com/NA-MIC/ProjectWeek/assets/96300975/4f8e8daf-88e2-483b-9849-e19899fb9260)
![filled](https://github.com/NA-MIC/ProjectWeek/assets/96300975/cc595232-fb44-4ff3-84eb-4a5ef52ec10c)

Files are saved as follows:
![output_folder](https://github.com/NA-MIC/ProjectWeek/assets/96300975/f69f0408-d680-4e60-8675-dfac3e0ac5ed)

Example of image after transformation in the scene:
![output_scene](https://github.com/NA-MIC/ProjectWeek/assets/96300975/4a06470e-8a1a-4b6b-87ed-82913aecc528)

## Contributors
- C. B. Raggio (<https://github.com/ciroraggio>)
- P. Zaffino (<https://github.com/pzaffino>)

