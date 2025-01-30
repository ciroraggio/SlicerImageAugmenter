# SlicerImageAugmenter

## Description
MONAI and PyTorch based medical image augmentation tool integrated in 3D Slicer.
The project aims to be a low-code version of the tool: <https://github.com/ciroraggio/AugmentedDataLoader>.

It's designed to operate on a dataset of medical images and apply a series of specific transformations to each image. This process augments the original dataset, providing a greater variety of samples for training deep learning models.

## [Tutorial](https://ciroraggio.github.io/SlicerImageAugmenter/tutorial)

## Developers and contributors
* [Ciro B. Raggio](https://www.ibt.kit.edu/english/Raggio_C.php) (Karlsruhe Institute of Technology, Germany) - [GitHub](<https://github.com/ciroraggio>)
* [Paolo Zaffino](http://dmsc.unicz.it/personale/docente/paolozaffino) (Universita’ degli Studi “Magna Græcia” di Catanzaro, Italy) - [GitHub](<https://github.com/pzaffino>)
* [Maria Francesca Spadea](https://www.ibt.kit.edu/english/Spadea_Francesca.php) (Karlsruhe Institute of Technology, Germany)

## How to cite
Please cite the following [publication](https://www.sciencedirect.com/science/article/pii/S2352711024002930) when publishing work that uses or incorporates ImageAugmenter:

```
Ciro Benito Raggio, Paolo Zaffino, Maria Francesca Spadea. ImageAugmenter: A user-friendly 3D Slicer tool for medical image augmentation, SoftwareX, Volume 28, 2024, 101923, ISSN 2352-7110, https://doi.org/10.1016/j.softx.2024.101923, https://www.sciencedirect.com/science/article/pii/S2352711024002930.
```

```bibtex
@article{RAGGIO2024101923,
title = {ImageAugmenter: A user-friendly 3D Slicer tool for medical image augmentation},
journal = {SoftwareX},
volume = {28},
pages = {101923},
year = {2024},
issn = {2352-7110},
doi = {https://doi.org/10.1016/j.softx.2024.101923},
url = {https://www.sciencedirect.com/science/article/pii/S2352711024002930},
author = {Ciro Benito Raggio and Paolo Zaffino and Maria Francesca Spadea},
keywords = {Medical imaging, Augmentation, 3D Slicer, Deep learning},
abstract = {Limited medical image data hinders the training of deep learning (DL) models in the biomedical field. Image augmentation can reduce the data-scarcity problem by generating variations of existing images. However, currently implemented methods require coding, excluding non-programmer users from this opportunity. We therefore present ImageAugmenter, an easy-to-use and open-source module for 3D Slicer imaging computing platform. It offers a simple and intuitive interface for applying over 20 simultaneous MONAI Transforms (spatial, intensity, etc.) to medical image datasets, all without programming. ImageAugmenter makes accessible medical image augmentation, enabling a wider range of users to improve the performance of DL models in medical image analysis by increasing the number of samples available for training.}
}
```