import sys
import os
basedir = os.path.dirname(__file__)
import re
from datetime import datetime
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QScrollArea, QLabel, QGridLayout

from Program.databaseClass import DataBase
from Program.datapointClass import Datapoint
from Program.mapWidgetClass import  MapWidget
from Program.textEditorClass import TextEditorWidget
from Program.qBoxClasses import SortBox, FilterBox
from Program.menuButtonsClass import MenuButtons

from ui_form import Ui_MainWindow


class TrapCam(QMainWindow):
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
        self.database.checkDeletes()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("TrapCam")
        self.app = app

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
        self.sortingCombobox.currentTextChanged.connect(self.deleteRefreshImages)
        self.filteringCombobox.currentTextChanged.connect(self.deleteRefreshImages)

    def createMenuButtons(self):
        """
        Creates the main menu buttons
        """
        self.menuButtons = MenuButtons(["Library", "Cameras", "Notes"], self.textEditor, self.scrollArea, self.map)
        self.menuButtons.reloadButton.clicked.connect(self.detectRefreshImages)
        self.menuButtons.exportButton.clicked.connect(self.exportCSV)

    def exportCSV(self):
        """
        Exports the data in the library to a csv file
        """
        if self.currentFilter == "*":
            self.database.toCSV()
        else:
            self.database.toCSV(self.currentFilter, self.currentFilterValue)


    def createMap(self):
        """
        Creates the map interface
        """
        self.map = MapWidget()

    def createTextEditor(self):
        """
        Creates the text editor interface
        """
        textWidget = TextEditorWidget()
        self.textEditor = textWidget.textEditor
        self.logPath = textWidget.logPath

    def createScrollAreas(self):
        """
        Creates the scroll areas for the library interface
        """
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.sortingCombobox = SortBox()
        self.filteringCombobox = FilterBox(self.database)
        self.scrollArea.hide()
        self.libLayout = QVBoxLayout()

    def closeEvent(self, event):
        """
        When the window is closed, save the text in the text editor to the log file
        param event: event to close the window
        """
        with open(self.logPath, 'w') as file:
            file.write(self.textEditor.toPlainText())
        with open("Program/markers.txt", 'w') as file:
            file.write("")
            for marker in self.map.markers:
                file.write(str(marker[0]) + "," + str(marker[1]) + "," + marker[2] + "\n")
        super().closeEvent(event)

    def getImageFiles(self, database, sort, filter):
        """
        Gets the image files from the database
        param database: database connection
        param sort: sort option
        param filter: filter option
        return: list of image files
        """
        self.cameras = database.getAllCameras()
        self.tags = database.getAllTags()
        filterCase = {
            **dict.fromkeys(self.cameras, "CAMERA"),
            **dict.fromkeys(self.tags, "TAGS"),
            "night": "DAYNIGHT",
            "day": "DAYNIGHT",
            "Confirmed": "CONFIRMED",
            "Rejected": "CONFIRMED",
            "Pending": "CONFIRMED",
            "No Filter": "*"
        }
        sortCase = {
            "Species A-Z": False,
            "Species Z-A": True,
            "Oldest to Latest": "DATETIME",
            "Highest Confidence" : "CONFIDENCE",
            "Lowest Confidence" : "CONFIDENCE"
        }
        self.currentFilter = filterCase[filter]
        self.currentFilter = filter
        filterd = database.filterRows(filterCase[filter], filter)
        if sort == "Latest to Oldest":
            sorted = database.sortRows(filterd, "DATETIME", True)
        elif sort == "Oldest to Latest":
            sorted = database.sortRows(filterd, "DATETIME", False)
        elif sort == "Highest Confidence":
            sorted = database.sortRows(filterd, "CONFIDENCE", True)
        elif sort == "Lowest Confidence":
            sorted = database.sortRows(filterd, "CONFIDENCE", False)
        else:
            sorted = database.sortRows(filterd, "CLASSIFICATION", sortCase[sort])
        sorted = list(map(lambda x: [x[0], x[1], x[3], x[4]], sorted))
        return sorted

    def convertDate(self, date):
        """
        Converts the date to a string of the format "May 20th, 2021"
        param date: date to convert
        return: string of the date
        """
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                  "October", "November", "December"]
        month = months[date.month - 1]
        day = date.day
        year = date.year
        daySuffix = "th"
        if day == 1 or day == 21 or day == 31:
            daySuffix = "st"
        elif day == 2 or day == 22:
            daySuffix = "nd"
        elif day == 3 or day == 23:
            daySuffix = "rd"
        return month + " " + str(day) + daySuffix + ", " + str(year)
    

    def createHeaderAndGrid(self, date):
        """
        Creates the header for the library interface
        param date: date of the header
        return: grid layout
        """
        header = QLabel(str(self.convertDate(date)))
        header.setStyleSheet("font-weight: bold")
        header.setStyleSheet("font-size: 20px")
        header.setFixedHeight(75)
        self.libLayout.addWidget(header)
        grid = QGridLayout()
        self.libLayout.addLayout(grid)
        return grid

    def addImageToGrid(self, grid, imageFile, row, col, ids):
        """
        Adds an image to the grid
        param grid: grid layout
        param image_file: image file
        param row: row of the grid
        param col: column of the grid
        param ids: list of ids
        """

        dataWidget = Datapoint(imageFile[0], imageFile[1], imageFile[2], imageFile[3], self.scrollArea, self.database, ids, self)

        grid.addWidget(dataWidget, row, col)
        

    def displayImages(self, databse):
        """
        Displays the images in the library
        param database: database connection
        """

        topLayout = QHBoxLayout()
        topLayout.addStretch()
        topLayout.addWidget(self.sortingCombobox)
        topLayout.addWidget(self.filteringCombobox)
        

        self.libLayout.addLayout(topLayout)  
        self.libLayout.setContentsMargins(10, 10, 0, 0)
        self.refreshImages()

        widget = QWidget()
        widget.setLayout(self.libLayout)
        self.scrollArea.setWidget(widget)

    

    def refreshImages(self):
        """
        Refreshes the images in the library
        """
        imageFiles = self.getImageFiles(self.database, self.sortingCombobox.currentText(), self.filteringCombobox.currentText())
        currentIds = list(map(lambda x: x[0], imageFiles))

        currentDate = None
        grid = None
        row = col = 0

        for imageFile in imageFiles:
            date = datetime.fromtimestamp(os.path.getmtime(imageFile[1])).date()

            if date != currentDate:
                currentDate = date
                grid = self.createHeaderAndGrid(currentDate)
                row = col = 0

            self.addImageToGrid(grid, imageFile, row, col, currentIds)

            col += 1
            if col > 2:
                col = 0
                row += 1

    def deleteRefreshImages(self):
        """
        Deletes and refreshes the images in the library
        """
        imageFiles = self.getImageFiles(self.database, self.sortingCombobox.currentText(), self.filteringCombobox.currentText())
        currentIds = list(map(lambda x: x[0], imageFiles))

        for widget in self.scrollArea.children()[0].children()[0].children():
            if isinstance(widget, Datapoint):
                widget.deleteLater()
            elif isinstance(widget, QLabel):
                widget.deleteLater()

        currentDate = None
        grid = None
        row = col = 0

        for imageFile in imageFiles:
            date = datetime.fromtimestamp(os.path.getmtime(imageFile[1])).date()

            if date != currentDate:
                currentDate = date
                grid = self.createHeaderAndGrid(currentDate)
                row = col = 0

            self.addImageToGrid(grid, imageFile, row, col, currentIds)

            col += 1
            if col > 2:
                col = 0
                row += 1
            
    def detectRefreshImages(self):
        self.database.checkDeletes()
        self.database.detectNew("input", "cropped")
        self.filteringCombobox.update()
        self.deleteRefreshImages()

    def setupUI(self):
        """
        Setup the user interface
        """
        buttonWidget = self.menuButtons.buttonWidget

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(buttonWidget)
        mainLayout.addWidget(self.scrollArea)
        mainLayout.addWidget(self.textEditor)
        mainLayout.addWidget(self.map)

        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

def connect():
    """
    Creates a connection to the database
    """
    myData = DataBase()
    myData.connect()
    return myData

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myData = connect()
    widget = TrapCam(myData)
    widget.showMaximized()
    sys.exit(app.exec())


