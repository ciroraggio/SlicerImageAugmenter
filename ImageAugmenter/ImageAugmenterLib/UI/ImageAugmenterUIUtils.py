CONTRIBUTORS = ["Ciro Benito Raggio (Karlsruhe Institute of Technology, Germany), Paolo Zaffino (Magna Graecia University of Catanzaro, Italy), Maria Francesca Spadea (Karlsruhe Institute of Technology, Germany)"]

HELP_TEXT = """
    <b>Description</b>
    <br/>
    MONAI and PyTorch based medical image augmentation tool. It's designed to operate on a dataset of medical images and apply a series of specific transformations to each image. 
    This process augments the original dataset, providing a greater variety of samples for training deep learning models.
    <br/>
    <br/>
    
    <b>More info</b>
    <ul>
        <li>Please refer to the official <a href=https://docs.monai.io/en/stable/transforms.html>MONAI documentation</a> to learn more about the available transforms and parameters.</li>
        <li><a href=https://github.com/ciroraggio/SlicerImageAugmenter/releases/download/v1.0.1/PDDCA_sample_data.zip>Click here</a> to download sample data!</li>
        <li>How to use ImageAugmenter: <a href=\"https://ciroraggio.github.io/SlicerImageAugmenter/tutorial\">https://ciroraggio.github.io/SlicerImageAugmenter/tutorial</a></li>
        <li>View on GitHub: <a href=\"https://github.com/ciroraggio/SlicerImageAugmenter">https://github.com/ciroraggio/SlicerImageAugmenter</a></li>
        <li>Read the <a href=\"https://www.sciencedirect.com/science/article/pii/S2352711024002930">article</a>!</li>
    </ul>
    <br/>
    
    <p><b>How to cite</b></p>
    <br/> 
    Please cite the following publication when publishing work that uses or incorporates ImageAugmenter:<br/>
    <cite>Ciro Benito Raggio, Paolo Zaffino, Maria Francesca Spadea. ImageAugmenter: A user-friendly 3D Slicer tool for medical image augmentation, SoftwareX, Volume 28, 2024, 101923, ISSN 2352-7110, https://doi.org/10.1016/j.softx.2024.101923, https://www.sciencedirect.com/science/article/pii/S2352711024002930.</cite>
"""


def updateButtonStyle(button, style):
    button.setStyleSheet(style)
