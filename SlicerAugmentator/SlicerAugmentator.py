import logging
import os
import time

import slicer
from slicer.i18n import tr as _
from slicer.i18n import translate
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin

from SlicerAugmentatorLib.SlicerAugmentatorDataset import SlicerAugmentatorDataset
from SlicerAugmentatorLib.TransformationParser import mapTransformations
from SlicerAugmentatorLib.SlicerAugmentatorUtils import collectImagesAndMasksList

import SimpleITK as sitk

#
# SlicerAugmentator
#

# If needed install dependencies
try:
    import monai
    import torch
except ModuleNotFoundError:
    slicer.util.pip_install("monai[itk]")  
    import monai
    import torch



class SlicerAugmentator(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = _("SlicerAugmentator")  # TODO: make this more human readable by adding spaces
        self.parent.categories = [translate("qSlicerAbstractCoreModule", "Utilities")]
        self.parent.dependencies = []  # TODO: add here list of module names that this module requires
        self.parent.contributors = ["Ciro Benito Raggio (Karlsruhe Institute of Technology), Paolo Zaffino (), Maria Francesca Spadea (Karlsruhe Institute of Technology)"]
        # TODO: update with short description of the module and a link to online module documentation
        # _() function marks text as translatable to other languages
        self.parent.helpText = _("""
This is an example of scripted loadable module bundled in an extension.
See more information in <a href="https://github.com/organization/projectname#SlicerAugmentator">module documentation</a>.
""")
        # TODO: replace with organization, grant and thanks
        self.parent.acknowledgementText = _("""
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""")

        # Additional initialization step after application startup is complete
        slicer.app.connect("startupCompleted()", registerSampleData)


#
# Register sample data sets in Sample Data module
#


def registerSampleData():
    """Add data sets to Sample Data module."""
    # It is always recommended to provide sample data for users to make it easy to try the module,
    # but if no sample data is available then this method (and associated startupCompeted signal connection) can be removed.

    import SampleData

    iconsPath = os.path.join(os.path.dirname(__file__), "Resources/Icons")

    # To ensure that the source code repository remains small (can be downloaded and installed quickly)
    # it is recommended to store data sets that are larger than a few MB in a Github release.

    # SlicerAugmentator1
    SampleData.SampleDataLogic.registerCustomSampleDataSource(
        # Category and sample name displayed in Sample Data module
        category="SlicerAugmentator",
        sampleName="SlicerAugmentator1",
        # Thumbnail should have size of approximately 260x280 pixels and stored in Resources/Icons folder.
        # It can be created by Screen Capture module, "Capture all views" option enabled, "Number of images" set to "Single".
        thumbnailFileName=os.path.join(iconsPath, "SlicerAugmentator1.png"),
        # Download URL and target file name
        uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95",
        fileNames="SlicerAugmentator1.nrrd",
        # Checksum to ensure file integrity. Can be computed by this command:
        #  import hashlib; print(hashlib.sha256(open(filename, "rb").read()).hexdigest())
        checksums="SHA256:998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95",
        # This node name will be used when the data set is loaded
        nodeNames="SlicerAugmentator1",
    )

    # SlicerAugmentator2
    SampleData.SampleDataLogic.registerCustomSampleDataSource(
        # Category and sample name displayed in Sample Data module
        category="SlicerAugmentator",
        sampleName="SlicerAugmentator2",
        thumbnailFileName=os.path.join(iconsPath, "SlicerAugmentator2.png"),
        # Download URL and target file name
        uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
        fileNames="SlicerAugmentator2.nrrd",
        checksums="SHA256:1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
        # This node name will be used when the data set is loaded
        nodeNames="SlicerAugmentator2",
    )


#
# SlicerAugmentatorWidget
#


class SlicerAugmentatorWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    """Uses ScriptedLoadableModuleWidget base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent=None) -> None:
        """Called when the user opens the module the first time and the widget is initialized."""
        ScriptedLoadableModuleWidget.__init__(self, parent)
        self.logic = None
        self._parameterNode = None
        self._parameterNodeGuiTag = None
    
    def setup(self) -> None:
        """Called when the user opens the module the first time and the widget is initialized."""
        ScriptedLoadableModuleWidget.setup(self)

        # Load widget from .ui file (created by Qt Designer).
        # Additional widgets can be instantiated manually and added to self.layout.
        uiWidget = slicer.util.loadUI(self.resourcePath("UI/SlicerAugmentator.ui"))
        self.layout.addWidget(uiWidget)
        self.ui = slicer.util.childWidgetVariables(uiWidget)
        # self.init_transformations()

        # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
        # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
        # "setMRMLScene(vtkMRMLScene*)" slot.
        uiWidget.setMRMLScene(slicer.mrmlScene)

        # Create logic class. Logic implements all computations that should be possible to run
        # in batch mode, without a graphical user interface.
        self.logic = SlicerAugmentatorLogic()

        # Connections

        # These connections ensure that we update parameter node when scene is closed
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

        # Buttons
        self.ui.applyButton.connect("clicked(bool)", self.onApplyButton)

    # def cleanup(self) -> None:
    #     """Called when the application closes and the module widget is destroyed."""
    #     self.removeObservers()


    def onSceneStartClose(self, caller, event) -> None:
        """Called just before the scene is closed."""
        # Parameter node will be reset, do not use it anymore
        # self.setParameterNode(None)

    def onSceneEndClose(self, caller, event) -> None:
        """Called just after the scene is closed."""
        # If this module is shown while the scene is closed then recreate a new parameter node immediately
        # if self.parent.isEntered:
        #     self.initializeParameterNode()

    # def initializeParameterNode(self) -> None:
    #     """Ensure parameter node exists and observed."""
    #     # Parameter node stores all user choices in parameter values, node selections, etc.
    #     # so that when the scene is saved and reloaded, these settings are restored.

    #     self.setParameterNode(self.logic.getParameterNode())

    #     # Select default input nodes if nothing is selected yet to save a few clicks for the user
    #     if not self._parameterNode.inputVolume:
    #         firstVolumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
    #         if firstVolumeNode:
    #             self._parameterNode.inputVolume = firstVolumeNode

    # def setParameterNode(self, inputParameterNode: Optional[SlicerAugmentatorParameterNode]) -> None:
    #     """
    #     Set and observe parameter node.
    #     Observation is needed because when the parameter node is changed then the GUI must be updated immediately.
    #     """

    #     if self._parameterNode:
    #         self._parameterNode.disconnectGui(self._parameterNodeGuiTag)
    #         self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self._checkCanApply)
    #     self._parameterNode = inputParameterNode
    #     if self._parameterNode:
    #         # Note: in the .ui file, a Qt dynamic property called "SlicerParameterName" is set on each
    #         # ui element that needs connection.
    #         self._parameterNodeGuiTag = self._parameterNode.connectGui(self.ui)
    #         self.addObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self._checkCanApply)
    #         self._checkCanApply()

    def _checkCanApply(self, caller=None, event=None) -> None:
        print(self.ui._parameterNode)
        if self._parameterNode and self._parameterNode.imagesInputPath and self._parameterNode.ouputPath:
            # self.ui.applyButton.toolTip = _("Compute output volume")
            self.ui.applyButton.enabled = True
        else:
            # self.ui.applyButton.toolTip = _("Select input and output volume nodes")
            self.ui.applyButton.enabled = False

    def onApplyButton(self) -> None:
        """Run processing when user clicks "Apply" button."""
        with slicer.util.tryWithErrorDisplay(_("Failed to compute results."), waitCursor=True):
            if(not any([self.ui.rotateEnabled, self.ui.resizeEnabled])):
                raise ValueError("Choose at least one transformation to apply")
            
            transformationList = mapTransformations(self.ui)
            self.logic.process(imagesInputPath=self.ui.imagesInputPath.directory,
                               imgPrefix=self.ui.imgPrefix.text,
                               maskPrefix=self.ui.maskPrefix.text,
                               outputPath=self.ui.outputPath.directory,
                               transformations=transformationList,
                               shuffle=self.ui.shuffleFlag)

# 
# SlicerAugmentatorLogic
#


class SlicerAugmentatorLogic(ScriptedLoadableModuleLogic):
    def __init__(self) -> None:
        """Called when the logic class is instantiated. Can be used for initializing member variables."""
        ScriptedLoadableModuleLogic.__init__(self)

    def getParameterNode(self):
        return SlicerAugmentatorParameterNode(super().getParameterNode())
    
    def save(self, img, path, filename, extension, idx):
        # extract name and extension
        img = sitk.GetImageFromArray(img)
        sitk.WriteImage(img, f"{path}/{filename}_{idx}.{extension}")

    def process(self,
                imagesInputPath: str,
                imgPrefix: str,
                maskPrefix: str,
                outputPath: float,
                transformations: list = [],
                shuffle: bool = False
                ) -> None:
        """
        Run the processing algorithm.
        Can be used without GUI widget
        """
        
        OUTPUT_IMG_DIR = "SlicerAugmentator/AugmentedDataset"

        if not imagesInputPath:
            raise ValueError("Input path is invalid")
        
        if not outputPath:
            raise ValueError("Output path is invalid")
        
        if not imgPrefix:
            raise ValueError("Indicate the image prefix")
        
        if len(transformations) == 0:
            raise ValueError("Choose at least one transformation")

        if(not os.path.isdir(imagesInputPath)):
            raise ValueError("Images path is not a directory")

        startTime = time.time()
        logging.info("Processing started")
        
        imgs, masks = collectImagesAndMasksList(imagesInputPath=imagesInputPath, 
                                                imgPrefix=imgPrefix,
                                                maskPrefix=maskPrefix)
        
        if len(masks) > 0 and (len(masks) != len(imgs)):
            raise ValueError(f"Images and masks must have same length. Found:\n{len(imgs)} images\n{len(masks)} masks.")

        dataset = SlicerAugmentatorDataset(imgPaths=imgs, 
                                           maskPaths=masks,
                                           transformations=transformations,
                                           shuffle=shuffle)
        
        os.makedirs(f"{outputPath}/{OUTPUT_IMG_DIR}", exist_ok=True)
        
        
        for dirIdx,(transformedImages, transformedMasks) in enumerate(dataset):
            currentDir = f"{outputPath}/{OUTPUT_IMG_DIR}/{dirIdx}"
            os.makedirs(currentDir, exist_ok=True)
            if(len(transformedMasks) > 0):
                for idx, (img, msk) in enumerate(zip(transformedImages, transformedMasks)):
                    self.save(img, currentDir, imgPrefix.split(".")[0], imgPrefix.split(".")[1], idx)
                    self.save(msk, currentDir, maskPrefix.split(".")[0], imgPrefix.split(".")[1], idx)
            else:
                for img in transformedImages:
                    self.save(img, currentDir, imgPrefix, idx)

        stopTime = time.time()
        logging.info(f"Processing completed in {stopTime-startTime:.2f} seconds")


#
# SlicerAugmentatorTest
#


class SlicerAugmentatorTest(ScriptedLoadableModuleTest):
    """
    This is the test case for your scripted module.
    Uses ScriptedLoadableModuleTest base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def setUp(self):
        """Do whatever is needed to reset the state - typically a scene clear will be enough."""
        slicer.mrmlScene.Clear()

    def runTest(self):
        """Run as few or as many tests as needed here."""
        self.setUp()
        self.test_SlicerAugmentator1()

    def test_SlicerAugmentator1(self):
        """Ideally you should have several levels of tests.  At the lowest level
        tests should exercise the functionality of the logic with different inputs
        (both valid and invalid).  At higher levels your tests should emulate the
        way the user would interact with your code and confirm that it still works
        the way you intended.
        One of the most important features of the tests is that it should alert other
        developers when their changes will have an impact on the behavior of your
        module.  For example, if a developer removes a feature that you depend on,
        your test should break so they know that the feature is needed.
        """

        self.delayDisplay("Starting the test")

        # Get/create input data

        import SampleData

        registerSampleData()
        inputVolume = SampleData.downloadSample("SlicerAugmentator1")
        self.delayDisplay("Loaded test data set")

        inputScalarRange = inputVolume.GetImageData().GetScalarRange()
        self.assertEqual(inputScalarRange[0], 0)
        self.assertEqual(inputScalarRange[1], 695)

        outputVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
        threshold = 100

        # Test the module logic

        logic = SlicerAugmentatorLogic()

        # Test algorithm with non-inverted threshold
        logic.process(inputVolume, outputVolume, threshold, True)
        outputScalarRange = outputVolume.GetImageData().GetScalarRange()
        self.assertEqual(outputScalarRange[0], inputScalarRange[0])
        self.assertEqual(outputScalarRange[1], threshold)

        # Test algorithm with inverted threshold
        logic.process(inputVolume, outputVolume, threshold, False)
        outputScalarRange = outputVolume.GetImageData().GetScalarRange()
        self.assertEqual(outputScalarRange[0], inputScalarRange[0])
        self.assertEqual(outputScalarRange[1], inputScalarRange[1])

        self.delayDisplay("Test passed")
