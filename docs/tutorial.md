<style>
.navbar {
  list-style-type: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: #333;
}

.navbar li {  /* Target nested elements within the navbar */
  float: left;
}

.navbar li a {  /* Target links within the navbar */
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

<ul class="navbar">
  <li><a href="https://ciroraggio.github.io/SlicerImageAugmenter/index">Home</a></li>
  <li><a href="https://ciroraggio.github.io/SlicerImageAugmenter/tutorial">Tutorial</a></li>
  <li><a href="https://ciroraggio.github.io/SlicerImageAugmenter/developers">Developers</a></li>
</ul>

## Tutorial
You can **download sample data** <a href="https://github.com/ciroraggio/SlicerImageAugmenter/releases/download/v1.0.1/PDDCA_sample_data.zip">here</a>!

Apply augmentation to your medical image dataset in a few simple steps:

**1.** Choose the path of your images

**2.** Specifies by what name, substring or with a regular expression how ImageAugmenter can recognize images (CT, CT.nrrd, .nrrd, ^ct\.(nii\.gz)$)

**3.** If you also want to include masks/segmentations associated with the images, simply indicate the name, a substring or a regular expression with which ImageAugmenter can recognize them (mask, mask.nrrd, _label, ^mask\.(nii\.gz)$)

Releases after v1.0.4 support regex mode for both text fields to match more precise patterns.

<center>            
<img src="https://raw.githubusercontent.com/ciroraggio/SlicerImageAugmenter/main/assets/SlicerImageAugmenterInputRegexExample.png">
</center>

**4.** Indicates what type of hierarchy the images respect. This will allow ImageAugmenter to maintain the original dataset hierarchy when saving. There are two options: **hierarchical** (use this setting if your images are grouped by sample and each sample is a folder) or **flat** (use this setting if your images/masks are in a single folder and the sample name matches the file name)

<center>            
<img src="https://raw.githubusercontent.com/ciroraggio/SlicerImageAugmenter/main/assets/SlicerImageAugmenterInputExample.png">
</center>

**5.** Choose where you want to save the augmented samples

**6.** Enable as many transformations as you want by specifying parameters for each transformation

<table>
    <tr>
        <td>
            <img src="https://raw.githubusercontent.com/ciroraggio/SlicerImageAugmenter/main/assets/SlicerImageAugmenterEnableTransformsExample1.png">
        </td>
        <td>
            <img src="https://raw.githubusercontent.com/ciroraggio/SlicerImageAugmenter/main/assets/SlicerImageAugmenterEnableTransformsExample2.png">
        </td>
    </tr>
</table>

**7.1** Use the **Preview** button if you want to preview the final result on the first sample of the dataset directly into the Slicer scene, if you are not satisfied, change the parameters and request a new preview.

![filled](https://raw.githubusercontent.com/ciroraggio/SlicerImageAugmenter/main/assets/SlicerImageAugmenterScreen.png)

Pressing the **Preview Settings** button, will display all cases found by ImageAugmenter with the specified settings in a new window. You can then select all cases on which the preview should be generated. If no cases are selected, the transformation preview will only be generated on the first case.

![filled](https://raw.githubusercontent.com/ciroraggio/SlicerImageAugmenter/main/assets/SlicerImageAugmenterSelectPreviewSamples.png)

**7.2** If you are satisfied with the result, use the **Run** button to save the augmented samples in the folder chosen in step 5. The files will be saved respecting the input hierarchy, as in this sample:

![output_folder](https://raw.githubusercontent.com/ciroraggio/SlicerImageAugmenter/main/assets/SlicerImageAugmenterOutputExample.png)
