import logging
import os
from typing import Annotated, Optional
import time

import vtk

import slicer
from slicer.i18n import tr as _
from slicer.i18n import translate
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin

from SlicerAugmentatorLib.SlicerAugmentatorDataset import SlicerAugmentatorDataset
from SlicerAugmentatorLib.TransformationParser import mapTransformations
import SimpleITK as sitk



#
# SlicerAugmentator
#

# If needed install dependencies
try:
  import monai
  import torch
  from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QGroupBox, QPushButton
except ModuleNotFoundError:
  slicer.util.pip_install("monai")
  slicer.util.pip_install("PyQt5")
  import monai
  import torch
  from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QGroupBox, QPushButton



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
    #     self.transformations_dict = {
    #         'spatial': {
    #             'Resize': {'param1': 'value1', 'param2': 'value2'},
    #             'Rotate': {'param1': 'value1', 'param2': 'value2'}
    #         },
    #         'crop': {
    #             'CropType1': {'param1': 'value1', 'param2': 'value2'},
    #             'CropType2': {'param1': 'value1', 'param2': 'value2'}
    #         }
    #     }
    # def init_transformations(self):
    #     layout = QVBoxLayout(self)
    #     tab_widget = self.ui.transformsTabWidget

    #     # Itera attraverso le categorie (spatial, crop, ecc.)
    #     for category, transformations in self.transformations_dict.items():
    #         # Crea un QGroupBox per ogni categoria
    #         category_group_box = QGroupBox(category)
    #         category_layout = QFormLayout()

    #         # Itera attraverso le trasformazioni all'interno di ogni categoria
    #         for transform_name, params in transformations.items():
    #             # Crea un QPushButton per ogni trasformazione
    #             transform_button = QPushButton(transform_name)

    #             # Collega la funzione di gestione degli eventi per aprire/cambiare i parametri
    #             transform_button.clicked.connect(lambda _, name=transform_name, p=params: self.show_parameters(name, p))

    #             # Aggiungi il pulsante al layout
    #             category_layout.addRow(transform_button)

    #         # Imposta il layout per il QGroupBox e aggiungi al tab
    #         category_group_box.setLayout(category_layout)
    #         tab_widget.addTab(category_group_box, category)

    #     # Aggiungi il layout principale alla finestra
    #     layout.addWidget(tab_widget)
    #     self.setLayout(layout)

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
            
            self.logic.process(imagesInputPath=self.ui.imagesInputPath,
                               imgsPrefix=self.ui.imgsPrefix,
                               masksPrefix=self.ui.masksPrefix,
                               outputPath=self.ui.outputPath,
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
    
    def save(self, img, path, filename, idx):
        # extract name and extension
        name, extension = filename.split(".")[0], filename.split(".")[0] # TODO too weak
        sitk.WriteImage(img, f"{path}/{name}_{idx}.{extension}")

    def process(self,
                imagesInputPath: str,
                imgsPrefix: str,
                masksPrefix: str,
                outputPath: float,
                transformations: list = [],
                shuffle: bool = False
                ) -> None:
        """
        Run the processing algorithm.
        Can be used without GUI widget
        """
        
        OUTPUT_IMG_DIR = "SlicerAugmentator/augmented_images"
        OUTPUT_MSK_DIR = "SlicerAugmentator/augmented_masks"

        if not imagesInputPath or not imgsPrefix or not masksPrefix or not outputPath:
            raise ValueError("Input or output volume is invalid")
        
        if len(transformations) == 0:
            raise ValueError("Choose at least one transformation")


        startTime = time.time()
        logging.info("Processing started")
        
        imgs, masks = [], []
        for path in sorted(os.listdir(imagesInputPath)):
            if(imgsPrefix in path):
                imgs.extend(path)
            elif(masksPrefix in path):
                masks.extend(path)
        
        if len(masks)>0 and (len(masks) != len(imgs)):
            raise ValueError("Images and masks must have same length")

        
        dataset = SlicerAugmentatorDataset(img_paths=imgs, 
                                           mask_paths=masks,
                                           transforms=transformations,
                                           shuffle=shuffle)
        
        os.makedirs(f"{outputPath}/{OUTPUT_IMG_DIR}", exist_ok=True)
        if(len(mask_paths) > 0):
            os.makedirs(f"{outputPath}/{OUTPUT_MSK_DIR}", exist_ok=True)
        
        for img_filename, transformed_images, mask_filename, transformed_masks in dataset:
            if(len(transformed_masks) > 0):
                for idx, (img, msk) in enumerate(zip(transformed_images, transformed_masks)):
                    self.save(img, f"{outputPath}/{OUTPUT_IMG_DIR}", img_filename, idx)
                    self.save(msk, f"{outputPath}/{OUTPUT_MSK_DIR}", mask_filename, idx)
            else:
                for img in transformed_images:
                    self.save(img, f"{outputPath}/{OUTPUT_IMG_DIR}", img_filename, idx)

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
