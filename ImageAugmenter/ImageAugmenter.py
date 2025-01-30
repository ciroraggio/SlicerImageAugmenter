import logging
import time
import slicer
from slicer.i18n import tr as _
from slicer.i18n import translate
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin, setDataProbeVisible
import qt
from typing import Callable
import SimpleITK as sitk

class ImageAugmenter(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """
    def __init__(self, parent):
        from ImageAugmenterLib.UI.ImageAugmenterUIUtils import HELP_TEXT, CONTRIBUTORS
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = _("ImageAugmenter")
        self.parent.categories = [translate("qSlicerAbstractCoreModule", "Utilities")]
        self.parent.dependencies = []
        self.parent.contributors = CONTRIBUTORS
        self.parent.helpText = _(HELP_TEXT)
        self.parent.acknowledgementText = _("")

class ImageAugmenterWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    def __init__(self, parent=None) -> None:
        """Called when the user opens the module the first time and the widget is initialized."""
        ScriptedLoadableModuleWidget.__init__(self, parent)
        self.logic = None
        self._parameterNode = None
        self._parameterNodeGuiTag = None

    def checkDependencies(self):
        from importlib.util import find_spec
        required_modules = ["monai", "SimpleITK", "torch", "munch"]
        all_present = all(find_spec(mod) is not None for mod in required_modules)

        self.ui.installRequirementsButton.setVisible(not all_present)
        self.ui.applyButton.setVisible(all_present)
        self.ui.previewButton.setVisible(all_present)
        self.ui.previewSettingsButton.setVisible(all_present)
            
    def setup(self) -> None:
        from ImageAugmenterLib.UI.ImageAugmenterPreviewDialog import PreviewCheckboxDialog
        import os
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
        
        previewSettingsIconPath = os.path.join(os.path.dirname(slicer.util.modulePath(self.__module__)), 'Resources/Icons', 'cog.png')
        self.ui.previewSettingsButton.setIcon(qt.QIcon(previewSettingsIconPath))
        self.ui.previewSettingsButton.connect("clicked(bool)", self.onPreviewSettingsButton)
        
        regexIconPath = os.path.join(os.path.dirname(slicer.util.modulePath(self.__module__)), 'Resources/Icons', 'regex.png')
        self.ui.imageRegexButton.setIcon(qt.QIcon(regexIconPath))
        self.ui.maskRegexButton.setIcon(qt.QIcon(regexIconPath))

        self.ui.imageRegexButton.connect("clicked(bool)", self.onImageRexegButton)
        self.ui.maskRegexButton.connect("clicked(bool)", self.onMaskRexegButton)
        
        
        self.ui.installRequirementsButton.connect("clicked(bool)", self.onInstallRequirements)
        self.previewSettingsDialog = PreviewCheckboxDialog()
        self.selectedPreviewOptions = []


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
        self.ui.previewSettingsButton.setEnabled(state)
        self.ui.imageRegexButton.setEnabled(state)
        self.ui.maskRegexButton.setEnabled(state)

    def resetAndDisable(self):
        self.ui.progressBar.reset()
        self.ui.infoLabel.setText("")
        self.setButtonsEnabled(False)

    def onInstallRequirements(self):
        if not slicer.util.confirmOkCancelDisplay("The dependencies needed for the extension will be installed, the operation may take a few minutes. A Slicer restart will be necessary.","Press OK to install and restart."):
            raise ValueError("Missing dependencies.")
        try:
            self.ui.installRequirementsButton.setEnabled(False)
            slicer.util.setPythonConsoleVisible(True)
            print("ImageAugmenter - Installing missing dependencies, please wait...")
            self.ui.infoLabel.setText("Installing missing dependencies, please wait...")
            slicer.util.pip_install("munch")
            slicer.util.pip_install("monai[itk]")
            slicer.util.restart()
        except Exception as e:
            raise ValueError(f"Error installing missing dependencies: {e!r}")

    def onApplyButton(self) -> None:
        """Run processing when user clicks "Apply" button."""
        with slicer.util.tryWithErrorDisplay(_("Failed to compute results."), waitCursor=True):
            from ImageAugmenterLib.ImageAugmenterTransformationParser import (
                ImageAugmenterTransformationParser,
            )
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
                               isImgPrefixRegex=self.ui.imageRegexButton.isChecked(),
                               isMaskPrefixRegex=self.ui.maskRegexButton.isChecked(),
                               outputPath=self.ui.outputPath.directory,
                               transformations=transformationList,
                               filesStructure=filesStructure,
                               progressBar=self.ui.progressBar,
                               infoLabel=self.ui.infoLabel,
                               setButtonsEnabled=self.setButtonsEnabled,
                               device=self.ui.deviceList.currentText)

            self.setButtonsEnabled(True)
            self.ui.progressBar.reset()


    def onPreviewButton(self) -> None:
        """Run processing when user clicks "Preview" button."""
        with slicer.util.tryWithErrorDisplay(_("Failed to compute results."), waitCursor=True):
            from ImageAugmenterLib.ImageAugmenterTransformationParser import (
                ImageAugmenterTransformationParser,
            )
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
                               isImgPrefixRegex=self.ui.imageRegexButton.isChecked(),
                               isMaskPrefixRegex=self.ui.maskRegexButton.isChecked(),
                               transformations=transformationList,
                               filesStructure=filesStructure,
                               progressBar=self.ui.progressBar,
                               infoLabel=self.ui.infoLabel,
                               setButtonsEnabled=self.setButtonsEnabled,
                               selectedPreviewOptions=self.selectedPreviewOptions,
                               device=self.ui.deviceList.currentText)

            self.setButtonsEnabled(True)
            self.ui.progressBar.reset()
    
            
    def onPreviewSettingsButton(self):
        """Run processing when user clicks "Preview" button."""
        with slicer.util.tryWithErrorDisplay(_("Failed to compute results."), waitCursor=True):
            from ImageAugmenterLib.ImageAugmenterUtils import getFilesStructure
            from ImageAugmenterLib.ImageAugmenterValidator import validateForms

            validateForms(self.ui)
            filesStructure = getFilesStructure(self.ui)

            mappedOptions = self.logic.loadPreviewOptions(imagesInputPath=self.ui.imagesInputPath.directory,
                               imgPrefix=self.ui.imgPrefix.text.strip(),
                               maskPrefix=self.ui.maskPrefix.text.strip(),
                               isImgPrefixRegex=self.ui.imageRegexButton.isChecked(),
                               isMaskPrefixRegex=self.ui.maskRegexButton.isChecked(),
                               filesStructure=filesStructure
                               )
            if(len(mappedOptions.keys()) == 0):
                raise ValueError("No samples found with the specified parameters!")
            
            self.previewSettingsDialog.updateOptions(mappedOptions, self.selectedPreviewOptions)

            if self.previewSettingsDialog.exec_() == qt.QDialog.Accepted:
                self.selectedPreviewOptions = self.previewSettingsDialog.getSelectedOptions()
    
    def onImageRexegButton(self):
        from ImageAugmenterLib.UI.ImageAugmenterUIUtils import updateButtonStyle
        updateButtonStyle(self.ui.imageRegexButton, "background-color: rgb(52, 206, 165);" if self.ui.imageRegexButton.isChecked() else "")

    def onMaskRexegButton(self):
        from ImageAugmenterLib.UI.ImageAugmenterUIUtils import updateButtonStyle
        updateButtonStyle(self.ui.maskRegexButton, "background-color: rgb(52, 206, 165);" if self.ui.maskRegexButton.isChecked() else "")

class ImageAugmenterLogic(ScriptedLoadableModuleLogic):
    def __init__(self) -> None:
        """Called when the logic class is instantiated. Can be used for initializing member variables."""
        ScriptedLoadableModuleLogic.__init__(self)
        self.previewNodesList = []

    def getParameterNode(self):
        return ImageAugmenterParameterNode(super().getParameterNode())

    def process(self,
                imagesInputPath: str,
                imgPrefix: str,
                maskPrefix: str,
                isImgPrefixRegex: bool,
                isMaskPrefixRegex: bool,
                outputPath: float,
                filesStructure: str,
                progressBar,
                infoLabel,
                setButtonsEnabled: Callable[[bool], None],
                transformations: list = [],
                device: str = "CPU",
                ) -> None:
        from ImageAugmenterLib.ImageAugmenterDataset import ImageAugmenterDataset
        from ImageAugmenterLib.ImageAugmenterUtils import (
            collectImagesAndMasksList,
            getOriginalCase,
            makeDir,
            splitFilenameAndExtension,
            save,
        )
        from ImageAugmenterLib.ImageAugmenterValidator import (
            validateCollectedImagesAndMasks,
        )

        startTime = time.time()
        logging.info("Processing started")
        infoLabel.setText("Processing started, please wait...")
        imgs, masks = collectImagesAndMasksList(imagesInputPath=imagesInputPath,
                                                imgPrefix=imgPrefix,
                                                maskPrefix=maskPrefix,
                                                isImgPrefixRegex=isImgPrefixRegex,
                                                isMaskPrefixRegex=isMaskPrefixRegex
                                                )

        validationResult = validateCollectedImagesAndMasks(imgs, masks)
        
        if isinstance(validationResult, ValueError):
            setButtonsEnabled(True)
            progressBar.reset()
            infoLabel.setText(validationResult)
            raise validationResult

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

                    currentDir = makeDir(outputPath, caseName, transformName)
                    
                    imgName, imgExtension = splitFilenameAndExtension(imgs[dirIdx], imgPrefix, isImgPrefixRegex)
                    save(img=img.detach().cpu(), path=currentDir,
                         filename=imgName,
                         originalCase=originalCaseImg,
                         extension=imgExtension if imgExtension else "nrrd")

                    if originalCaseMask and msk != None and msk.any():
                        maskName, maskExtension = splitFilenameAndExtension(masks[dirIdx], maskPrefix, isMaskPrefixRegex)
                        save(img=msk.detach().cpu(), path=currentDir,
                             filename=maskName,
                             originalCase=originalCaseMask,
                             extension=maskExtension if maskExtension else "nrrd")


                progressBar.setValue(dirIdx + 1)

            except Exception as e:
                setButtonsEnabled(True)
                progressBar.reset()
                infoLabel.setText(f"{e}")
                raise e

        stopTime = time.time()
        infoLabel.setText(f"Processing completed in {stopTime-startTime:.2f} seconds")
        logging.info(f"Processing completed in {stopTime-startTime:.2f} seconds")

    def preview(self,
                imagesInputPath: str,
                imgPrefix: str,
                maskPrefix: str,
                isImgPrefixRegex: bool,
                isMaskPrefixRegex: bool,
                progressBar,
                infoLabel,
                setButtonsEnabled: Callable[[bool], None],
                selectedPreviewOptions: list,
                transformations: list = [],
                filesStructure: str = "",
                device: str = "CPU",
                ) -> None:

        import SimpleITK as sitk

        from ImageAugmenterLib.ImageAugmenterDataset import ImageAugmenterDataset
        from ImageAugmenterLib.ImageAugmenterUtils import (
            clearScene,
            collectImagesAndMasksList,
            getOriginalCase,
            resetViews,
            showPreview,
        )
        from ImageAugmenterLib.ImageAugmenterValidator import (
            validateCollectedImagesAndMasks,
        )

        startTime = time.time()
        logging.info("Processing started")
        infoLabel.setText("Processing started, please wait...")

        imgs, masks = collectImagesAndMasksList(imagesInputPath=imagesInputPath,
                                                imgPrefix=imgPrefix,
                                                maskPrefix=maskPrefix,
                                                isImgPrefixRegex=isImgPrefixRegex,
                                                isMaskPrefixRegex=isMaskPrefixRegex
                                                )

        validationResult = validateCollectedImagesAndMasks(imgs, masks)
        
        if isinstance(validationResult, ValueError):
            setButtonsEnabled(True)
            progressBar.reset()
            infoLabel.setText(validationResult)
            raise validationResult
        
        if(len(slicer.util.getNodes()) > 0):
            clearScene(self.previewNodesList)
            self.previewNodesList = []
            
        previewIndices = [i for i, path in enumerate(imgs) if path in selectedPreviewOptions] if len(selectedPreviewOptions) > 0 else [0]
        previewImgs = []
        previewMasks = []
        
        if(len(imgs)>0):
            previewImgs = [imgs[i] for i in previewIndices]
            
        if(len(masks)>0):
            previewMasks = [masks[i] for i in previewIndices]
        
        dataset = ImageAugmenterDataset(imgPaths=previewImgs, maskPaths=previewMasks, transformations=transformations, device=device)
        progressBar.setMaximum(len(dataset))

        for dirIdx in range(len(dataset)):
            try:
                transformedImages, transformedMasks = dataset[dirIdx]
                caseName, originalCaseImg = getOriginalCase(previewImgs[dirIdx], filesStructure)

                if transformedMasks:
                    originalCaseMask = sitk.ReadImage(masks[dirIdx])

                    for i in range(len(transformedImages)):
                        imgPack = transformedImages[i]
                        mskPack = transformedMasks[i] if i < len(transformedMasks) else None

                        transformName, img = imgPack
                        _, msk = mskPack

                        imgNodeName = f"{caseName}_{transformName}_img"
                        maskNodeName = f"{caseName}_{transformName}_mask"
                        imgNode, maskNode = showPreview(img=img, originalCaseImg=originalCaseImg, originalCaseMask=originalCaseMask, mask=msk,
                                    imgNodeName=imgNodeName, maskNodeName=maskNodeName)
                        self.previewNodesList.append(imgNode)
                        self.previewNodesList.append(maskNode)
                else:
                    for imgPack in transformedImages:
                        transformName, img = imgPack
                        imgNodeName = f"{caseName}_{transformName}_img"
                        imgNode = showPreview(img, originalCaseImg, imgNodeName=imgNodeName)
                        self.previewNodesList.append(imgNode)

                resetViews()
                progressBar.setValue(dirIdx + 1)

            except Exception as e:
                setButtonsEnabled(True)
                progressBar.reset()
                infoLabel.setText(f"{e}")
                raise e

        stopTime = time.time()
        infoLabel.setText(f"Processing completed in {stopTime-startTime:.2f} seconds")
        logging.info(f"Processing completed in {stopTime-startTime:.2f} seconds")
        
    def loadPreviewOptions(self, 
                           imagesInputPath,
                           imgPrefix,
                           maskPrefix,
                           isImgPrefixRegex: bool,
                           isMaskPrefixRegex: bool,
                           filesStructure) -> dict[str, str]:        
        from ImageAugmenterLib.ImageAugmenterUtils import collectImagesAndMasksList, getCaseName
        
        imgs, masks = collectImagesAndMasksList(imagesInputPath=imagesInputPath,
                                                imgPrefix=imgPrefix,
                                                maskPrefix=maskPrefix,
                                                isImgPrefixRegex=isImgPrefixRegex,
                                                isMaskPrefixRegex=isMaskPrefixRegex
                                                )
        options = {}
        
        for case in imgs:
            options[case] = getCaseName(case, filesStructure)

        return options