cmake_minimum_required(VERSION 3.16.3...3.19.7 FATAL_ERROR)

project(ImageAugmenter)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://ciroraggio.github.io/SlicerImageAugmenter/index")
set(EXTENSION_CATEGORY "Utilities")
set(EXTENSION_CONTRIBUTORS "Ciro Benito Raggio (Karlsruhe Institute of Technology, Germany), Paolo Zaffino (Magna Graecia University of Catanzaro, Italy), Maria Francesca Spadea (Karlsruhe Institute of Technology, Germany)")
set(EXTENSION_DESCRIPTION "MONAI and PyTorch based medical image augmentation tool that can be integrated in Slicer. The project aims to be a low-code version of the tool: https://github.com/ciroraggio/AugmentedDataLoader. It's designed to operate on a dataset of medical images and apply a series of specific transformations to each image. This process augments the original dataset, providing a greater variety of samples for training deep learning models.")
set(EXTENSION_ICONURL "https://raw.githubusercontent.com/ciroraggio/SlicerImageAugmenter/main/ImageAugmenter.png")
set(EXTENSION_SCREENSHOTURLS "https://raw.githubusercontent.com/ciroraggio/SlicerImageAugmenter/main/assets/SlicerImageAugmenterScreen.png")
set(EXTENSION_DEPENDS "NA") # Specified as a list or "NA" if no dependencies

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(ImageAugmenter)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
