<center> <h2>SlicerAugmentator</h2></center>

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
  <li><a href="https://ciroraggio.github.io/SlicerAugmentator/index">Home</a></li>
  <li><a href="https://ciroraggio.github.io/SlicerAugmentator/examples">Examples</a></li>
  <li><a href="https://ciroraggio.github.io/SlicerAugmentator/changelog">Changelog</a></li>
  <li><a href="https://ciroraggio.github.io/SlicerAugmentator/developers">Developers</a></li>
</ul>

## Changelog
 - v0.4:
   1. Improved code readability with objects
   2. Fixed bug on saving without masks
 - v0.3:
    1. Updated UI
    2. Added device choice
    3. Bugs fixed
    
 - v0.2:
    1. Completed preview mode 
    2. Added spatial and intensity transformations
    3. New interface
    4. Bugs fixed
    
 - v0.1:
    1.  Implemented interface for loading images and masks, choosing transformations and saving images.
    2.  Implemented and tested MONAI spatial transformations such as Rotation, RandRotation, Flip, Resize.
    3.  Partially implemented input validation and MONAI intensity transformations, it will be completed in the future.
    4.  Partially implemented "Preview" feature, which allows the output of transformations to be viewed directly in the scene before saving them in the OS, will be completed in the future.