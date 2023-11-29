from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QSizePolicy, QButtonGroup
from PySide6.QtGui import QIcon
class MenuButtons:
    def __init__ (self, button_texts, text_editor, scroll_area, map):
        """
        Creates the main menu buttons
        param button_texts: list of button texts
        param text_editor: text editor widget
        param scroll_area: scroll area widget
        param map: map widget
        """
        self.map = map
        self.scroll_area = scroll_area
        self.text_editor = text_editor
        self.button_texts = button_texts
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        self.button_group.buttonClicked.connect(self.buttonClicked)

        # Make the main menu buttons
        self.button_layout = QVBoxLayout()

        # Make the library the default interface
        for text in self.button_texts:
            button = QPushButton(text)
            button.setCheckable(True)
            if text == "Library":
                button.setChecked(True)
                self.buttonClicked(button)
            # Set up the style for the buttons
            button.setIcon(QIcon("icons/" + text + ".png"))
            button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
            button.setStyleSheet("border: 0px; min-height: 30px; max-height: 30px; min-width: 100px; text-align: left;")
            self.button_layout.addWidget(button)
            self.button_group.addButton(button)

        # Make the buttons go to the top of the screen
        self.button_layout.addStretch()

        # Add a reload button
        self.reload_button = QPushButton("Reload")
        self.reload_button.setIcon(QIcon("icons/Reload.png"))
        self.reload_button.setStyleSheet("min-height: 30px; max-height: 35px; min-width: 100px;")
        self.button_layout.addWidget(self.reload_button)

        # Add an Export button
        self.export_button = QPushButton("Export")
        self.export_button.setStyleSheet("min-height: 30px; max-height: 35px; min-width: 100px;")
        self.button_layout.addWidget(self.export_button)

        # Create Widget
        self.button_widget = QWidget()
        self.button_widget.setLayout(self.button_layout)        

    def buttonClicked(self, button):
        """
        Defines the behavior of the buttons
        param button: button that was clicked
        """
        self.resetWidgets()
        if button.text() == "Notes":
            button.setStyleSheet("border: 0px; min-height: 30px; max-height: 30px; min-width: 100px; text-align: left; font-weight: bold;")
            self.text_editor.show()
        elif button.text() == "Library":
            button.setStyleSheet("border: 0px; min-height: 30px; max-height: 30px; min-width: 100px; text-align: left; font-weight: bold;")
            self.scroll_area.show()
        elif button.text() == "Cameras":
            button.setStyleSheet("border: 0px; min-height: 30px; max-height: 30px; min-width: 100px; text-align: left; font-weight: bold;")
            self.map.show()

    def resetWidgets(self):
        """
        Resets all widgets
        """
        for btn in self.button_group.buttons():
            btn.setStyleSheet("border: 0px; min-height: 30px; max-height: 30px; min-width: 100px; text-align: left;")
        self.text_editor.hide()
        self.scroll_area.hide()
        self.map.hide()