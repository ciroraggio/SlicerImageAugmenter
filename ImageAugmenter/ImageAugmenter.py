import logging
import time

import slicer
from slicer.i18n import tr as _
from slicer.i18n import translate
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
from slicer.util import setDataProbeVisible

import SimpleITK as sitk

class ImageAugmenter(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = _("ImageAugmenter")
        self.parent.categories = [translate("qSlicerAbstractCoreModule", "Utilities")]
        self.parent.dependencies = []
        self.parent.contributors = ["Ciro Benito Raggio (Karlsruhe Institute of Technology, Germany), Paolo Zaffino (Magna Graecia University of Catanzaro, Italy), Maria Francesca Spadea (Karlsruhe Institute of Technology, Germany)"]
        self.parent.helpText = _("""MONAI and PyTorch based medical image augmentation tool. It's designed to operate on a dataset of medical images and apply a series of specific transformations to each image. This process augments the original dataset, providing a greater variety of samples for training deep learning models.""")


class ImageAugmenterWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    def __init__(self, parent=None) -> None:
        """Called when the user opens the module the first time and the widget is initialized."""
        ScriptedLoadableModuleWidget.__init__(self, parent)
        self.logic = None
        self._parameterNode = None
        self._parameterNodeGuiTag = None
        
    def checkDependencies(self):
        try:
            from munch import Munch
            import monai
            import torch
            import SimpleITK
            self.ui.installRequirementsButton.setVisible(False)
            self.ui.applyButton.setVisible(True)
            self.ui.previewButton.setVisible(True)
        except ModuleNotFoundError:
            self.ui.installRequirementsButton.setVisible(True)
            self.ui.applyButton.setVisible(False)
            self.ui.previewButton.setVisible(False)
            
    def setup(self) -> None:
        """Called when the user opens the module the first time and the widget is initialized."""
        ScriptedLoadableModuleWidget.setup(self)

        uiWidget = slicer.util.loadUI(self.resourcePath("UI/ImageAugmenter.ui"))
        # Check if all necessary dependencies are installed to run the extension logic
        self.layout.addWidget(uiWidget)
        self.ui = slicer.util.childWidgetVariables(uiWidget)
        
        self.checkDependencies()
        uiWidget.setMRMLScene(slicer.mrmlScene)
        setDataProbeVisible(False)
        
        self.ui.deviceList.addItem("CPU")
        
        self.ui.hierarchicalTreeWidget.expandItem(self.ui.hierarchicalTreeWidget.topLevelItem(0))

        self.logic = ImageAugmenterLogic()

        # Connections
        # These connections ensure that we update parameter node when scene is closed
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
        self.addObserver(slicer.mrmlScene,slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

        # Buttons
        self.ui.applyButton.connect("clicked(bool)", self.onApplyButton)
        self.ui.previewButton.connect("clicked(bool)", self.onPreviewButton)
        self.ui.installRequirementsButton.connect("clicked(bool)", self.onInstallRequirements)

        import torch

        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                device_name = torch.cuda.get_device_name(i)
                self.ui.deviceList.addItem(f"GPU {i} - {device_name}")

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
    
    def onInstallRequirements(self):
        if not slicer.util.confirmOkCancelDisplay(f"The dependencies needed for the extension will be installed, the operation may take a few minutes. A Slicer restart will be necessary.","Press OK to install and restart."):
            raise ValueError("Missing dependencies.")
        else:
            try:
                self.ui.installRequirementsButton.setEnabled(False)
                self.ui.infoLabel.setText("Installing dependencies, please wait...")
                slicer.util.pip_install("munch")
                slicer.util.pip_install("monai[itk]")
                slicer.util.restart()
            except Exception as e:
                raise ValueError(f"Error installing dependencies: {repr(e)}")
                
    def onApplyButton(self) -> None:
        """Run processing when user clicks "Apply" button."""
        with slicer.util.tryWithErrorDisplay(_("Failed to compute results."), waitCursor=True):
            from ImageAugmenterLib.ImageAugmenterTransformationParser import ImageAugmenterTransformationParser
            from ImageAugmenterLib.ImageAugmenterUtils import getFilesStructure
            from ImageAugmenterLib.ImageAugmenterValidator import validateForms

            validateForms(self.ui)
            
            self.transformationParser = ImageAugmenterTransformationParser(self.ui)    
            transformationList = self.transformationParser.mapTransformations()     
            filesStructure = getFilesStructure(self.ui)
           
            self.resetAndDisable()
            
            self.logic.process(imagesInputPath=self.ui.imagesInputPath.directory,
                               imgPrefix=self.ui.imgPrefix.text.strip(),
                               maskPrefix=self.ui.maskPrefix.text.strip(),
                               outputPath=self.ui.outputPath.directory,
                               transformations=transformationList,
                               filesStructure=filesStructure,
                               progressBar=self.ui.progressBar,
                               infoLabel=self.ui.infoLabel,
                               device=self.ui.deviceList.currentText)
            
            self.setButtonsEnabled(True)
            self.ui.progressBar.reset()


    def onPreviewButton(self) -> None:
        """Run processing when user clicks "Preview" button."""
        with slicer.util.tryWithErrorDisplay(_("Failed to compute results."), waitCursor=True):
            from ImageAugmenterLib.ImageAugmenterTransformationParser import ImageAugmenterTransformationParser
            from ImageAugmenterLib.ImageAugmenterUtils import getFilesStructure
            from ImageAugmenterLib.ImageAugmenterValidator import validateForms

            validateForms(self.ui)
            
            self.transformationParser = ImageAugmenterTransformationParser(self.ui)    
            transformationList = self.transformationParser.mapTransformations()
            filesStructure = getFilesStructure(self.ui)
            
            self.resetAndDisable()

            self.logic.preview(imagesInputPath=self.ui.imagesInputPath.directory,
                               imgPrefix=self.ui.imgPrefix.text.strip(),
                               maskPrefix=self.ui.maskPrefix.text.strip(),
                               transformations=transformationList,
                               filesStructure=filesStructure,
                               progressBar=self.ui.progressBar,
                               infoLabel=self.ui.infoLabel)
            
            self.setButtonsEnabled(True)
            self.ui.progressBar.reset()
            
                        

class ImageAugmenterLogic(ScriptedLoadableModuleLogic):
    def __init__(self) -> None:
        """Called when the logic class is instantiated. Can be used for initializing member variables."""
        ScriptedLoadableModuleLogic.__init__(self)

    def getParameterNode(self):
        return ImageAugmenterParameterNode(super().getParameterNode())

    def process(self,
                imagesInputPath: str,
                imgPrefix: str,
                maskPrefix: str,
                outputPath: float,
                filesStructure: str,
                progressBar,
                infoLabel,
                transformations: list = [],
                device: str = "CPU"
                ) -> None:
        from ImageAugmenterLib.ImageAugmenterDataset import ImageAugmenterDataset
        from ImageAugmenterLib.ImageAugmenterTransformationParser import IMPOSSIBLE_COPY_INFO_TRANSFORM
        from ImageAugmenterLib.ImageAugmenterUtils import collectImagesAndMasksList, getOriginalCase, save, makeDir
        from ImageAugmenterLib.ImageAugmenterValidator import validateCollectedImagesAndMasks


        OUTPUT_IMG_DIR = "ImageAugmenter"

        startTime = time.time()
        logging.info("Processing started")
        infoLabel.setText("Processing started, please wait...")
        imgs, masks = collectImagesAndMasksList(imagesInputPath=imagesInputPath,
                                                imgPrefix=imgPrefix,
                                                maskPrefix=maskPrefix)
        
        validateCollectedImagesAndMasks(imgs, masks)
        dataset = ImageAugmenterDataset(imgPaths=imgs, maskPaths=masks, transformations=transformations, device=device)
        
        progressBar.setMaximum(len(dataset))

        for dirIdx in range(len(dataset)):
            transformedImages, transformedMasks = dataset[dirIdx]
            try:
                caseName, originalCaseImg = getOriginalCase(imgs[dirIdx], filesStructure)
                originalCaseMask = sitk.ReadImage(masks[dirIdx]) if transformedMasks else None

                for i in range(len(transformedImages)):
                    imgPack = transformedImages[i]
                    mskPack = transformedMasks[i] if i < len(transformedMasks) else None

                    transformName, img = imgPack
                    _, msk = mskPack if mskPack else (None, None)

                    currentDir = makeDir(outputPath, OUTPUT_IMG_DIR, caseName, transformName)

                    imgPrefixParts = imgPrefix.split(".")
                    maskPrefixParts = maskPrefix.split(".")
                    copyInfo = False if transformName in IMPOSSIBLE_COPY_INFO_TRANSFORM else True

                    save(img=img.detach().cpu(), path=currentDir, 
                         filename=imgPrefixParts[0], 
                         originalCase=originalCaseImg, 
                         extension=imgPrefixParts[1] if len(imgPrefixParts) > 1 else "nrrd", 
                         copyInfo=copyInfo)

                    if originalCaseMask and msk != None and msk.any():
                        save(img=msk.detach().cpu(), path=currentDir, 
                             filename=maskPrefixParts[0], 
                             originalCase=originalCaseMask, 
                             extension=maskPrefixParts[1] if len(maskPrefixParts) > 1 else "nrrd", 
                             copyInfo=copyInfo)
                    
                    
                progressBar.setValue(dirIdx + 1)
        
            except Exception as e:
                raise e

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
                filesStructure: str = "",
                device: str = "CPU" 
                ) -> None:
        
        from ImageAugmenterLib.ImageAugmenterDataset import ImageAugmenterDataset
        from ImageAugmenterLib.ImageAugmenterTransformationParser import IMPOSSIBLE_COPY_INFO_TRANSFORM
        from ImageAugmenterLib.ImageAugmenterUtils import collectImagesAndMasksList, getOriginalCase, showPreview, clearScene, resetViews
        from ImageAugmenterLib.ImageAugmenterValidator import validateCollectedImagesAndMasks
        import SimpleITK as sitk
        
        startTime = time.time()
        logging.info("Processing started")
        infoLabel.setText("Processing started, please wait...")
        
        imgs, masks = collectImagesAndMasksList(imagesInputPath=imagesInputPath,
                                                imgPrefix=imgPrefix,
                                                maskPrefix=maskPrefix)
        
        validateCollectedImagesAndMasks(imgs, masks)
        clearScene()
        dataset = ImageAugmenterDataset(imgPaths=imgs[:1], maskPaths=masks[:1], transformations=transformations, device=device) # [:1] to apply the transformations only on the first image
        progressBar.setMaximum(len(dataset))

        for dirIdx in range(len(dataset)):
            try:
                transformedImages, transformedMasks = dataset[dirIdx]
                caseName, originalCaseImg = getOriginalCase(imgs[dirIdx], filesStructure)

                if transformedMasks:
                    originalCaseMask = sitk.ReadImage(masks[dirIdx])
                    
                    for i in range(len(transformedImages)):
                        imgPack = transformedImages[i]
                        mskPack = transformedMasks[i] if i < len(transformedMasks) else None
                        
                        transformName, img = imgPack
                        _, msk = mskPack
                        
                        imgNodeName = f"{caseName}_{transformName}_img"
                        maskNodeName = f"{caseName}_{transformName}_mask"
                        copyInfo = False if transformName in IMPOSSIBLE_COPY_INFO_TRANSFORM else True
                        showPreview(img=img, originalCaseImg=originalCaseImg, originalCaseMask=originalCaseMask, mask=msk,
                                    imgNodeName=imgNodeName, maskNodeName=maskNodeName, copyInfo=copyInfo)
                else:
                    for imgPack in transformedImages:
                        transformName, img = imgPack
                        imgNodeName = f"{caseName}_{transformName}_img"
                        copyInfo = False if transformName in IMPOSSIBLE_COPY_INFO_TRANSFORM else True
                        showPreview(img, originalCaseImg, imgNodeName=imgNodeName, copyInfo=copyInfo)
                        
                resetViews()
                progressBar.setValue(dirIdx + 1)

            except Exception as e:
                raise e

        stopTime = time.time()
        infoLabel.setText(f"Processing completed in {stopTime-startTime:.2f} seconds")
        logging.info(f"Processing completed in {stopTime-startTime:.2f} seconds")
