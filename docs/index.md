<style>
ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: #333;
}

li {
  float: left;
}

li a {
  display: block;
  color: white;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
}

/* Change the link color to #111 (black) on hover */
li a:hover {
  background-color: #111;
}
</style>

<ul>
  <li><a href="https://ciroraggio.github.io/SlicerImageAugmenter/index">Home</a></li>
  <li><a href="https://ciroraggio.github.io/SlicerImageAugmenter/tutorial">Tutorial</a></li>
  <li><a href="https://ciroraggio.github.io/SlicerImageAugmenter/developers">Developers</a></li>
</ul>

## Description
MONAI and PyTorch based medical image augmentation tool integrated in [3D Slicer](https://www.slicer.org/).
The project aims to be a low-code version of the tool: <https://github.com/ciroraggio/AugmentedDataLoader>.

It's designed to operate on a dataset of medical images and apply a series of specific transformations to each image. This process augments the original dataset, providing a greater variety of samples for training deep learning models.

## Features
***MONAI Transformations***

ImageAugmenter provides more than 20 MONAI transformations, leaving the user the freedom to choose all the parameters available for the transformation. If you want to delve deeper into MONAI transformations and understand more about the meaning of the parameters of each transformation, visit the [MONAI](https://docs.monai.io/en/latest/transforms.html) documentation.

***Preview mode***

ImageAugmenter allows users to view images or augmented images and masks directly in the scene thanks to the "Preview" function. In this way it will be possible to explore the transformations and test the parameters taking the first image as an example, saving the images to disk only when you are completely satisfied with the result.

***Use the device you prefer***

In the "Advanced" section it will be possible to choose which device to apply the transformations with. In addition to the CPU, all PyTorch compatible GPUs will be shown.


## How to cite
Please cite the following [publication](https://www.sciencedirect.com/science/article/pii/S2352711024002930) when publishing work that uses or incorporates ImageAugmenter:


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
