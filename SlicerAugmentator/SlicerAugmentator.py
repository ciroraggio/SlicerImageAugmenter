import logging
import os
import time

import slicer
from slicer.i18n import tr as _
from slicer.i18n import translate
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
from slicer.util import setSliceViewerLayers

from SlicerAugmentatorLib.SlicerAugmentatorDataset import SlicerAugmentatorDataset
from SlicerAugmentatorLib.SlicerAugmentatorTransformationParser import mapTransformations
from SlicerAugmentatorLib.SlicerAugmentatorUtils import collectImagesAndMasksList, getOriginalCase, getFilesStructure, save, showPreview, clearScene, makeDir
from SlicerAugmentatorLib.SlicerAugmentatorValidator import validateCollectedImagesAndMasks, validateForms
import SimpleITK as sitk

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
        self.parent.title = _("SlicerAugmentator")
        self.parent.categories = [translate("qSlicerAbstractCoreModule", "Utilities")]
        self.parent.dependencies = []
        self.parent.contributors = ["Ciro Benito Raggio (Karlsruhe Institute of Technology, Germany), Paolo Zaffino (Magna Graecia University of Catanzaro, Italy), Maria Francesca Spadea (Karlsruhe Institute of Technology, Germany)"]
        self.parent.helpText = _("""MONAI and PyTorch based medical image augmentation tool. It's designed to operate on a dataset of medical images and apply a series of specific transformations to each image. This process augments the original dataset, providing a greater variety of samples for training deep learning models.""")


class SlicerAugmentatorWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    def __init__(self, parent=None) -> None:
        """Called when the user opens the module the first time and the widget is initialized."""
        ScriptedLoadableModuleWidget.__init__(self, parent)
        self.logic = None
        self._parameterNode = None
        self._parameterNodeGuiTag = None

    def setup(self) -> None:
        """Called when the user opens the module the first time and the widget is initialized."""
        ScriptedLoadableModuleWidget.setup(self)

        uiWidget = slicer.util.loadUI(self.resourcePath("UI/SlicerAugmentator.ui"))
        self.layout.addWidget(uiWidget)
        self.ui = slicer.util.childWidgetVariables(uiWidget)
        uiWidget.setMRMLScene(slicer.mrmlScene)
        
        self.logic = SlicerAugmentatorLogic()

        # Connections
        # These connections ensure that we update parameter node when scene is closed
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
        self.addObserver(slicer.mrmlScene,slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

        # Buttons
        self.ui.applyButton.connect("clicked(bool)", self.onApplyButton)
        self.ui.previewButton.connect("clicked(bool)", self.onPreviewButton)

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
        
    def setButtonsEnabled(self, state: bool = True):
        self.ui.applyButton.setEnabled(state)
        self.ui.previewButton.setEnabled(state)
        
    def resetAndDisable(self):
        self.ui.progressBar.reset()
        self.ui.infoLabel.setText("")
        self.setButtonsEnabled(False)
            
    def onApplyButton(self) -> None:
        """Run processing when user clicks "Apply" button."""
        with slicer.util.tryWithErrorDisplay(_("Failed to compute results."), waitCursor=True):
            validateForms(self.ui)

            transformationList = mapTransformations(self.ui)
            filesStructure = getFilesStructure(self.ui.filesStructureList)
           
            self.resetAndDisable()
            
            self.logic.process(imagesInputPath=self.ui.imagesInputPath.directory,
                               imgPrefix=self.ui.imgPrefix.text,
                               maskPrefix=self.ui.maskPrefix.text,
                               outputPath=self.ui.outputPath.directory,
                               transformations=transformationList,
                               filesStructure=filesStructure,
                               progressBar=self.ui.progressBar,
                               infoLabel=self.ui.infoLabel)
            
            self.setButtonsEnabled(True)
            self.ui.progressBar.reset()


    def onPreviewButton(self) -> None:
        """Run processing when user clicks "Preview" button."""
        with slicer.util.tryWithErrorDisplay(_("Failed to compute results."), waitCursor=True):
            validateForms(self.ui)

            transformationList = mapTransformations(self.ui)
            filesStructure = getFilesStructure(self.ui.filesStructureList)
            
            self.resetAndDisable()

            self.logic.preview(imagesInputPath=self.ui.imagesInputPath.directory,
                               imgPrefix=self.ui.imgPrefix.text,
                               maskPrefix=self.ui.maskPrefix.text,
                               transformations=transformationList,
                               filesStructure=filesStructure,
                               progressBar=self.ui.progressBar,
                               infoLabel=self.ui.infoLabel)
            
            self.setButtonsEnabled(True)
            self.ui.progressBar.reset()
            
                        

class SlicerAugmentatorLogic(ScriptedLoadableModuleLogic):
    def __init__(self) -> None:
        """Called when the logic class is instantiated. Can be used for initializing member variables."""
        ScriptedLoadableModuleLogic.__init__(self)

    def getParameterNode(self):
        return SlicerAugmentatorParameterNode(super().getParameterNode())

    def process(self,
                imagesInputPath: str,
                imgPrefix: str,
                maskPrefix: str,
                outputPath: float,
                filesStructure: str,
                progressBar,
                infoLabel,
                transformations: list = [],
                ) -> None:
        
        OUTPUT_IMG_DIR = "SlicerAugmentator/AugmentedDataset"

        startTime = time.time()
        logging.info("Processing started")

        imgs, masks = collectImagesAndMasksList(imagesInputPath=imagesInputPath,
                                                imgPrefix=imgPrefix,
                                                maskPrefix=maskPrefix)
        
        validateCollectedImagesAndMasks(imgs, masks)
        dataset = SlicerAugmentatorDataset(imgPaths=imgs, maskPaths=masks, transformations=transformations)
        
        progressBar.setMaximum(len(dataset))

        for dirIdx in range(len(dataset)):
            transformedImages, transformedMasks = dataset[dirIdx] # To find out how these objects are formed, look at dataset __getitem__
            try:
                caseName, originalCaseImg = getOriginalCase(imgs[dirIdx], filesStructure)
                if (len(transformedMasks) > 0):
                    originalCaseMask = sitk.ReadImage(masks[dirIdx])
                    for (img_pack, msk_pack) in zip(transformedImages, transformedMasks):
                        transformName, img = img_pack
                        _, msk = msk_pack
                        
                        currentDir = makeDir(outputPath, OUTPUT_IMG_DIR, caseName, transformName)
                        
                        if (len(imgPrefix.split(".")) >= 2):
                            save(img, currentDir, imgPrefix.split(".")[0], originalCaseImg, imgPrefix.split(".")[1])
                            save(msk, currentDir, maskPrefix.split(".")[0], originalCaseMask, imgPrefix.split(".")[1])
                        else:
                            save(img, currentDir, imgPrefix,originalCaseImg, "tif")
                            save(msk, currentDir, maskPrefix, originalCaseMask, "tif")

                else:
                    for img_pack in transformedImages:
                        transformName, img = img_pack
                        
                        currentDir = makeDir(outputPath, OUTPUT_IMG_DIR, caseName, transformName)

                        if (len(imgPrefix.split(".")) > 2):
                            save(img, currentDir, imgPrefix.split(".")[0], originalCaseImg, imgPrefix.split(".")[1])
                        else:
                            save(img, currentDir, caseName.split(".")[0], originalCaseImg, caseName.split(".")[1])
                
                progressBar.setValue(dirIdx+1)
                
            except Exception as e:
                print(e)

        stopTime = time.time()
        infoLabel.setText(f"Processing completed in {stopTime-startTime:.2f} seconds")
        logging.info(f"Processing completed in {stopTime-startTime:.2f} seconds")

    def preview(self,
                imagesInputPath: str,
                imgPrefix: str,
                maskPrefix: str,
                progressBar,
                infoLabel,
                transformations: list = [],
                filesStructure: str = ""
                ) -> None:

        startTime = time.time()
        logging.info("Processing started")
        imgs, masks = collectImagesAndMasksList(imagesInputPath=imagesInputPath,
                                                imgPrefix=imgPrefix,
                                                maskPrefix=maskPrefix)
        validateCollectedImagesAndMasks(imgs, masks)
        clearScene()
        dataset = SlicerAugmentatorDataset(imgPaths=imgs[:1], maskPaths=masks[:1], transformations=transformations) # [:1] to apply the transformations only on the first image
        progressBar.setMaximum(len(dataset))

        for dirIdx in range(len(dataset)):
            transformedImages, transformedMasks = dataset[dirIdx] # To find out how these objects are formed, look at dataset __getitem__
            try:
                caseName, originalCaseImg = getOriginalCase(imgs[dirIdx], filesStructure)
                
                if (len(transformedMasks) > 0):
                    originalCaseMask = sitk.ReadImage(masks[dirIdx])
                    for (img_pack, msk_pack) in zip(transformedImages, transformedMasks):
                        transformName, img = img_pack
                        _, msk = msk_pack
                        showPreview(img=img, originalCaseImg=originalCaseImg, originalCaseMask=originalCaseMask, mask=msk,
                                    imgNodeName=f"{caseName}_{transformName}_img", maskNodeName=f"{caseName}_{transformName}_mask")
                else:
                    for img_pack in transformedImages:
                        transformName, img = img_pack
                        showPreview(img, originalCaseImg, imgNodeName=f"{caseName}_{transformName}_img")
                
                progressBar.setValue(dirIdx+1)

            except Exception as e:
                print(e)

        stopTime = time.time()
        infoLabel.setText(f"Processing completed in {stopTime-startTime:.2f} seconds")
        logging.info(f"Processing completed in {stopTime-startTime:.2f} seconds")
