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
MONAI and PyTorch based medical image augmentation tool that can be integrated in Slicer.
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

Please cite the following publications when publishing work that uses or incorporates ImageAugmenter:
Ciro Benito Raggio, Paolo Zaffino, Maria Francesca Spadea. ImageAugmenter: A user-friendly 3D Slicer tool for medical image augmentation, SoftwareX, Volume 28, 2024, 101923, ISSN 2352-7110, https://doi.org/10.1016/j.softx.2024.101923, https://www.sciencedirect.com/science/article/pii/S2352711024002930.
