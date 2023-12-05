from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QSizePolicy, QButtonGroup
from PySide6.QtGui import QIcon
class MenuButtons:
    def __init__ (self, buttonTexts, textEditor, scrollArea, map):
        """
        Creates the main menu buttons
        param buttonTexts: list of button texts
        param textEditor: text editor widget
        param scrollArea: scroll area widget
        param map: map widget
        """
        self.map = map
        self.scrollArea = scrollArea
        self.textEditor = textEditor
        self.buttonTexts = buttonTexts
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.setExclusive(True)
        self.buttonGroup.buttonClicked.connect(self.buttonClicked)

        # Make the main menu buttons
        self.buttonLayout = QVBoxLayout()

        # Make the library the default interface
        for text in self.buttonTexts:
            button = QPushButton(text)
            button.setCheckable(True)
            if text == "Library":
                button.setChecked(True)
                self.buttonClicked(button)
            # Set up the style for the buttons
            button.setIcon(QIcon("icons/" + text + ".png"))
            button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
            button.setStyleSheet("border: 0px; min-height: 30px; max-height: 30px; min-width: 100px; text-align: left;")
            self.buttonLayout.addWidget(button)
            self.buttonGroup.addButton(button)

        # Make the buttons go to the top of the screen
        self.buttonLayout.addStretch()

        # Add a reload button
        self.reloadButton = QPushButton("Reload")
        self.reloadButton.setIcon(QIcon("icons/Reload.png"))
        self.reloadButton.setStyleSheet("min-height: 30px; max-height: 35px; min-width: 100px;")
        self.buttonLayout.addWidget(self.reloadButton)

        # Add an Export button
        self.exportButton = QPushButton("Export")
        self.exportButton.setStyleSheet("min-height: 30px; max-height: 35px; min-width: 100px;")
        self.buttonLayout.addWidget(self.exportButton)

        # Create Widget
        self.buttonWidget = QWidget()
        self.buttonWidget.setLayout(self.buttonLayout)        

    def buttonClicked(self, button):
        """
        Defines the behavior of the buttons
        param button: button that was clicked
        """
        self.resetWidgets()
        if button.text() == "Notes":
            button.setStyleSheet("border: 0px; min-height: 30px; max-height: 30px; min-width: 100px; text-align: left; font-weight: bold;")
            self.textEditor.show()
        elif button.text() == "Library":
            button.setStyleSheet("border: 0px; min-height: 30px; max-height: 30px; min-width: 100px; text-align: left; font-weight: bold;")
            self.scrollArea.show()
        elif button.text() == "Cameras":
            button.setStyleSheet("border: 0px; min-height: 30px; max-height: 30px; min-width: 100px; text-align: left; font-weight: bold;")
            self.map.show()

    def resetWidgets(self):
        """
        Resets all widgets
        """
        for btn in self.buttonGroup.buttons():
            btn.setStyleSheet("border: 0px; min-height: 30px; max-height: 30px; min-width: 100px; text-align: left;")
        self.textEditor.hide()
        self.scrollArea.hide()
        self.map.hide()