## Examples
Apply augmentation to your medical image dataset in a few simple steps:

**1.** Choose the path of your images

**2.** Specifies by what name or substring of the name SlicerAugmentator can recognize images (CT, CT.nrrd, .nrrd)

**3.** If you also want to include masks/segmentations associated with the images, simply indicate the name or a substring of the name with which SlicerAugmentator can recognize them (mask, mask.nrrd, _label)
**4.** Indicates what type of hierarchy the images respect. This will allow SlicerAugmentator to maintain the original dataset hierarchy when saving. There are two options:
<ul>
    <li>
    <p><u><b>Hierarchical</b></u> - use this setting if your images are grouped by case and each case is a folder</p>
    </li>
    <li>
    <p><u><b>Flat</b></u> - use this setting if your images/masks are in a single folder and the case name matches the file name</p>
    </li>
</ul>
<center>            
<img src="https://raw.githubusercontent.com/ciroraggio/SlicerAugmentator/main/assets/SlicerAugmentatorInputExample.png">
</center>

**5.** Choose where you want to save the augmented samples
**6.** Enable as many transformations as you want by specifying parameters for each transformation
<table>
    <tr>
        <td>
            <img src="https://raw.githubusercontent.com/ciroraggio/SlicerAugmentator/main/assets/SlicerAugmentatorEnableTransformsExample1.png">
        </td>
        <td>
            <img src="https://raw.githubusercontent.com/ciroraggio/SlicerAugmentator/main/assets/SlicerAugmentatorEnableTransformsExample2.png">
        </td>
    </tr>
</table>

**7.1** Use the **Preview** button if you want to preview the final result on the first sample of the dataset directly into the Slicer scene, if you are not satisfied, change the parameters and request a new preview

![filled](https://raw.githubusercontent.com/ciroraggio/SlicerAugmentator/main/assets/SlicerAugmentatorScreen.png)

**7.2** If you are satisfied with the result, use the **Run** button to save the augmented samples in the folder chosen in step 5. The files will be saved respecting the input hierarchy, as in this case:

![output_folder](https://raw.githubusercontent.com/ciroraggio/SlicerAugmentator/main/assets/SlicerAugmentatorOutputExample.png)