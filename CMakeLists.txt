cmake_minimum_required(VERSION 3.16.3...3.19.7 FATAL_ERROR)

project(ImageAugmentator)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://www.slicer.org/wiki/Documentation/Nightly/Extensions/ImageAugmentator")
set(EXTENSION_CATEGORY "Utils")
set(EXTENSION_CONTRIBUTORS "Ciro Benito Raggio (KIT)")
set(EXTENSION_DESCRIPTION ".")
set(EXTENSION_ICONURL "https://www.example.com/Slicer/Extensions/ImageAugmentator.png")
set(EXTENSION_SCREENSHOTURLS "https://www.example.com/Slicer/Extensions/ImageAugmentator/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a list or "NA" if no dependencies

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(ImageAugmentator)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
