# This Python file uses the following encoding: utf-8
import sys
import os
import re
from datetime import datetime
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QScrollArea, QLabel, QGridLayout

import databaseClass 
from datapointClass import Datapoint
from mapWidgetClass import  MapWidget
from textEditorClass import TextEditorWidget
from qBoxClasses import SortBox, FilterBox
from menuButtonsClass import MenuButtons

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow


class MainWindow(QMainWindow):
    """
    This class is the main window of the application.
    """
    def __init__(self, conn, parent=None):
        """
        Constructor of the class.
        param conn: connection to the database
        param parent: parent of the class
        """
        super().__init__(parent)
        self.database = conn
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.createTextEditor()
        self.createScrollAreas()
        self.createMap()
        self.createMenuButtons()
        self.setupComboBoxes()
        self.displayImages(self.database)

        self.setupUI()

    def setupComboBoxes(self):
        """
        Sets up combo boxes behavior to refresh images every time they are changed
        """
        self.sorting_combobox.currentTextChanged.connect(self.deleteRefreshImages)
        self.filtering_combobox.currentTextChanged.connect(self.deleteRefreshImages)

    def createMenuButtons(self):
        """
        Creates the main menu buttons
        """
        self.menu_buttons = MenuButtons(["Library", "Cameras", "Notes"], self.text_editor, self.scroll_area, self.map)

    def createMap(self):
        """
        Creates the map interface
        """
        self.map = MapWidget().image_scroll_area

    def createTextEditor(self):
        """
        Creates the text editor interface
        """
        text_widget = TextEditorWidget()
        self.text_editor = text_widget.text_editor
        self.log_path = text_widget.log_path

    def createScrollAreas(self):
        """
        Creates the scroll areas for the library interface
        """
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.sorting_combobox = SortBox()
        self.filtering_combobox = FilterBox()
        self.scroll_area.hide()
        self.lib_layout = QVBoxLayout()

    def closeEvent(self, event):
        """
        When the window is closed, save the text in the text editor to the log file
        param event: event to close the window
        """
        with open(self.log_path, 'w') as file:
            file.write(self.text_editor.toPlainText())
        # Call the parent class’s existing closeEvent
        super().closeEvent(event)

    def getImageFiles(self, database, sort, filter):
        """
        Gets the image files from the database
        param database: database connection
        param sort: sort option
        param filter: filter option
        return: list of image files
        """
        filter_case = {
            "CameraA": "CAMERA",
            "CameraB": "CAMERA",
            "CameraC": "CAMERA",
            "night": "DAYNIGHT",
            "day": "DAYNIGHT",
            "Confirmed": "CONFIRMED",
            "Rejected": "CONFIRMED",
            "Pending": "CONFIRMED",
            "Tag1": "TAGS",
            "Tag2": "TAGS",
            "Tag3": "TAGS",
            "Tag4": "TAGS",
            "Tag5": "TAGS",
            "None": "*"
        }
        sort_case = {
            "Species A-Z": False,
            "Species Z-A": True,
            "Oldest to Latest": "DATETIME",

        }
        filterd = database.filterRows(filter_case[filter], filter)
        if sort == "Latest to Oldest":
            # sort by time
            sorted = database.sortRows(filterd, "DATETIME", True)
        elif sort == "Oldest to Latest":
            sorted = database.sortRows(filterd, "DATETIME", False)
        else:
            sorted = database.sortRows(filterd, "CLASSIFICATION", sort_case[sort])
        # only keep the [id, image path, classification] from the database
        sorted = list(map(lambda x: [x[0], x[1], x[3]], sorted))
        return sorted


    def createHeaderAndGrid(self, date):
        """
        Creates the header for the library interface
        param date: date of the header
        return: grid layout
        """
        header = QLabel(str(date))
        self.lib_layout.addWidget(header)
        grid = QGridLayout()
        self.lib_layout.addLayout(grid)
        return grid

    def addImageToGrid(self, grid, image_file, row, col, ids):
        """
        Adds an image to the grid
        param grid: grid layout
        param image_file: image file
        param row: row of the grid
        param col: column of the grid
        param ids: list of ids
        """

        # Create a widget to hold the image and the text label
        data_widget = Datapoint(image_file[0], image_file[1], image_file[2], self.scroll_area, self.database, ids, self)

        # Add the widget to the grid
        grid.addWidget(data_widget, row, col)

    def displayImages(self, databse):
        """
        Displays the images in the library
        param database: database connection
        """

        # Create a layout for the combo boxes
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.sorting_combobox)
        top_layout.addWidget(self.filtering_combobox)

        # Add the combo box layout to the main layout
        self.lib_layout.addLayout(top_layout)  
        self.lib_layout.setContentsMargins(0, 0, 0, 0)
        self.refreshImages()

        # Create a widget to hold the library layout
        widget = QWidget()
        widget.setLayout(self.lib_layout)
        self.scroll_area.setWidget(widget)

    

    def refreshImages(self):
        """
        Refreshes the images in the library
        """
        print("refreshing images")
        image_files = self.getImageFiles(self.database, self.sorting_combobox.currentText(), self.filtering_combobox.currentText())
        current_ids = list(map(lambda x: x[0], image_files))
        print("currently displaying: ", image_files)

        current_date = None
        grid = None
        row = col = 0

        for image_file in image_files:
            date = datetime.fromtimestamp(os.path.getmtime(image_file[1])).date()

            # Add a date header everytime the date changes
            if date != current_date:
                current_date = date
                grid = self.createHeaderAndGrid(current_date)
                row = col = 0

            self.addImageToGrid(grid, image_file, row, col, current_ids)

            # allows 3 images per row for presentation purposes
            col += 1
            if col > 2:
                col = 0
                row += 1

    def deleteRefreshImages(self):
        """
        Deletes and refreshes the images in the library
        """
        print("refreshing images")
        image_files = self.getImageFiles(self.database, self.sorting_combobox.currentText(), self.filtering_combobox.currentText())
        current_ids = list(map(lambda x: x[0], image_files))
        print("currently displaying: ", image_files)

        # Delete all datapoints and labels from the library
        for widget in self.scroll_area.children()[0].children()[0].children():
            if isinstance(widget, Datapoint):
                widget.deleteLater()
            elif isinstance(widget, QLabel):
                widget.deleteLater()

        current_date = None
        grid = None
        row = col = 0

        for image_file in image_files:
            date = datetime.fromtimestamp(os.path.getmtime(image_file[1])).date()

            # Add a date header everytime the date changes
            if date != current_date:
                current_date = date
                grid = self.createHeaderAndGrid(current_date)
                row = col = 0

            self.addImageToGrid(grid, image_file, row, col, current_ids)

            # TEMPORARY: allows 3 images per row for presentation purposes
            col += 1
            if col > 2:
                col = 0
                row += 1

    def setupUI(self):
        """
        Setup the user interface
        """
        button_widget = self.menu_buttons.button_widget

        main_layout = QHBoxLayout()
        main_layout.addWidget(button_widget)
        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(self.text_editor)
        main_layout.addWidget(self.map)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

def connect():
    """
    Creates a connection to the database
    """
    myData = databaseClass.DataBase()
    myData.connect()
    print(myData)
    return myData

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myData = connect()
    widget = MainWindow(myData)
    widget.show()
    sys.exit(app.exec())


