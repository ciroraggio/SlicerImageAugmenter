import qt

class PreviewCheckboxDialog(qt.QDialog):
    def __init__(self, parent=None):
        super(PreviewCheckboxDialog, self).__init__(parent)
        self.setWindowTitle("ImageAugmenter")

        mainDialogLayout = qt.QVBoxLayout(self)
        
        centralWidgetLayout = qt.QHBoxLayout()
        mainDialogLayout.addLayout(centralWidgetLayout)

        centralWidget = qt.QWidget()
        centralWidgetLayout.addWidget(centralWidget)

        self.previewDialogLayout = qt.QVBoxLayout(centralWidget)

        self.scrollArea = qt.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollWidget = qt.QWidget()
        self.scrollLayout = qt.QVBoxLayout(self.scrollWidget)
        self.scrollArea.setStyleSheet("QScrollArea { border: none; }") 
        self.scrollArea.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Preferred)
        self.scrollArea.setWidget(self.scrollWidget)
        self.previewDialogLayout.addWidget(self.scrollArea)

        label = qt.QLabel("Samples on which the preview will be generated, if nothing is selected, the first sample will be used by default.")
        label.setWordWrap(True)  
        label.setSizePolicy(qt.QSizePolicy.Preferred, qt.QSizePolicy.Maximum)
        
        self.scrollLayout.addWidget(label)
        self.checkboxStates = {}
        self.checkboxes = {}

        self.buttonLayout = qt.QHBoxLayout()
        self.previewDialogLayout.addStretch()
        self.previewDialogLayout.addLayout(self.buttonLayout)

        self.leftButtonLayout = qt.QHBoxLayout()
        self.buttonLayout.addLayout(self.leftButtonLayout)
        self.leftButtonLayout.addStretch()

        selectAllButton = qt.QPushButton("Select All")
        selectAllButton.clicked.connect(self.selectAllCheckboxes)
        selectAllButton.setStyleSheet("background-color: #d1ecf1;")  
        self.leftButtonLayout.addWidget(selectAllButton)

        resetButton = qt.QPushButton("Reset")
        resetButton.clicked.connect(self.resetCheckboxes)
        resetButton.setStyleSheet("background-color: #f8d7da;")  
        self.leftButtonLayout.addWidget(resetButton)

        self.rightButtonLayout = qt.QHBoxLayout()
        self.buttonLayout.addStretch()
        self.buttonLayout.addLayout(self.rightButtonLayout)

        applyButton = qt.QPushButton("Apply")
        applyButton.clicked.connect(lambda: self.accept())
        applyButton.setStyleSheet("background-color: rgb(52, 206, 165);")
        self.rightButtonLayout.addWidget(applyButton)
        
    def updateOptions(self, options: dict[str, str], selectedOptions: list[str] = None):
        """
        Dynamically updates dialog options.
        :param options: {original_path: description} like dict
        :param selectedOptions: list of original_path of the checkbox to keep the previous state
        """
        for checkbox in list(self.checkboxes.keys()):
            self.scrollLayout.removeWidget(checkbox)
            checkbox.setParent(None)

        self.checkboxes.clear()
        self.checkboxStates.clear()

        for original_path, option in options.items():
            checkbox = qt.QCheckBox(option)
            self.checkboxes[checkbox] = original_path

            self.scrollLayout.addWidget(checkbox)

            checkbox.stateChanged.connect(self.updateCheckboxState)

            self.checkboxStates[original_path] = False

        if selectedOptions:
            for checkbox, original_path in self.checkboxes.items():
                if original_path in selectedOptions:
                    checkbox.setChecked(True)
                    self.checkboxStates[original_path] = True

        self.scrollLayout.addStretch()

    def updateCheckboxState(self):
        for checkbox, original_path in self.checkboxes.items():
            self.checkboxStates[original_path] = checkbox.isChecked()

    def selectAllCheckboxes(self):
        for checkbox in self.checkboxes.keys():
            checkbox.setChecked(True)

    def resetCheckboxes(self):
        for checkbox in self.checkboxes.keys():
            checkbox.setChecked(False)

    def getSelectedOptions(self):
        return [key for key, value in self.checkboxStates.items() if value]