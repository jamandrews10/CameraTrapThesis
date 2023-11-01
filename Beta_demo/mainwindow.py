# This Python file uses the following encoding: utf-8
import sys
import os
import re
from datetime import datetime
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QSizePolicy, QHBoxLayout, QButtonGroup, QTextEdit, QScrollArea, QSplitter, QLabel, QGridLayout, QComboBox, QStackedWidget, QSpacerItem
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QUrl, Signal
# databaseInput establishes "conn", a connection to an already filled database that can be iterated through with "cursor"
# cursor = conn.execute("SELECT id, imagePath, croppedPath, class from PATHS")#
#import databaseInput
import databaseClass

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

# create a connection to the database
def connect():
    myData = databaseClass.DataBase()
    myData.clear()
    myData.addRow(['alphaUncropped/IMG_0075.png', 'alphaCropped/IMG_0075.JPG___crop00_md_v5a.0.0.pt.png', 'possum', 'Confirmed', 'CameraB', 'Night', ["tag1", "tag2"]])
    myData.addRow(['alphaUncropped/IMG_0314.png', 'alphaCropped/IMG_0314.JPG___crop00_md_v5a.0.0.pt.png', 'deer', 'Rejected', 'CameraA', 'Night', ["tag2", "tag3"]])
    myData.addRow(['alphaUncropped/IMG_0462.png', 'alphaCropped/IMG_0462.JPG___crop00_md_v5a.0.0.pt.png', 'fox', 'Confirmed', 'CameraC', 'Night', ["tag1", "tag2"]])
    myData.addRow(['alphaUncropped/IMG_0273.png', 'alphaCropped/IMG_0273.JPG___crop00_md_v5a.0.0.pt.png', 'squirrel', 'Rejected', 'CameraA', 'Day', ["tag1", "tag5"]])

    # Printing the database
    print(myData)

    return myData


# datapoint is a class that holds the pixmap and the labels for each image
class Datapoint(QWidget):
    def __init__(self, id, image_file, classification, image_widget, database, ids):
        super().__init__()
        # Create a widget to hold the image and the text label
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.scroll_area = image_widget
        self.title = image_file
        self.database = database
        self.ids = ids
        self.id = id
        # Create the image
        self.original_pixmap = QPixmap(image_file)
        self.label = ClickableLabel(self, self.scroll_area, self.database, self.id, classification, ids)
        self.pixmap = self.original_pixmap.scaledToWidth(350, Qt.SmoothTransformation)
        self.label.setPixmap(self.pixmap)
        self.layout.addWidget(self.label)
        # Create classification label
        self.text_label = QLabel()
        self.text_label.setText(classification)
        self.text_label.setFixedHeight(50)
        self.layout.addWidget(self.text_label)

class ClickableLabel(QLabel):
    # This class is used to create a clickable label
    clicked = Signal()

    def __init__(self, clicked_widget, images_widget, database, id, classification, ids, parent=None):
        super().__init__(parent)
        self.images_widget = images_widget
        self.clicked_image = clicked_widget.title
        self.database = database
        self.id = id
        self.ids = ids
        self.classification = classification

    # when mouse is pressed, call display_image
    def mousePressEvent(self, event):
        self.clicked.emit()
        self.display_image(self.clicked_image, self.images_widget)

    # when clicking on the label, make an instance of the image viewer, a class
    # that displays the image in a separate window and allows for navigation between images
    # this is done by passing the pixmap of the label to the image viewer and the widget that holds
    # the other images
    def display_image(self, clicked_image, images_widget):
        self.image_viewer = ImageViewer(clicked_image, images_widget, self.database, self.id, self.ids)
        self.image_viewer.show()

class ImageViewer(QMainWindow):
    # PopUp window
    def __init__(self, clicked_image, image_widget, database, id, ids):
        super().__init__()
        self.database = database
        self.current_id = id
        self.ids = ids
        # get every image widget in the library
        self.images_widget = image_widget.children()[0].children()[0].children()
        # get the pixmap of the image that was clicked on
        self.clicked_image = clicked_image
        #create a QstackedWidget to hold 10 previous images and 10 next images
        self.image_stack = QStackedWidget() 
        self.current_index = 0
        self.index = 0
        for widget in self.images_widget:
            if isinstance(widget, Datapoint):
                # Create a new QLabel
                label_copy = QLabel()
                # Set its pixmap to be the same as the original label
                label_copy.setPixmap(widget.original_pixmap.scaledToWidth(800, Qt.SmoothTransformation))
                # add a copy of the label to the stack
                self.image_stack.addWidget(label_copy)
                # if the label title is the same as the clicked image, set the current index to the index of the label 
                if widget.title == self.clicked_image:
                    # set the index of the stack to the index of the pixmap that was clicked on
                    self.current_index = self.index
                self.index += 1
        
        self.initUI()

    def initUI(self):
        # Create the image viewer
        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Create the buttons
        self.yes_button = QPushButton("Yes")
        self.yes_button.clicked.connect(self.confirm_image)
        self.no_button = QPushButton("No")
        self.no_button.clicked.connect(self.reject_image)
        self.not_quite_button = QPushButton("Not Quite")
        self.not_quite_button.clicked.connect(self.not_quite_image)

        # Create the image layout
        self.image_stack.setCurrentIndex(self.current_index)

        # create nav buttons
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_image)
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.prev_image)

        # create the layout
        self.image_layout = QHBoxLayout()
        spacer1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.image_layout.addWidget(self.prev_button)
        self.image_layout.addSpacerItem(spacer1)
        self.image_layout.addWidget(self.image_stack)
        self.image_layout.addSpacerItem(spacer2)
        self.image_layout.addWidget(self.next_button)

        # Create a label for the classification
        self.classification_label = QLabel()
        self.classification = self.database.filterRows("ID", self.current_id)[0][3]
        self.confirmed = self.database.filterRows("ID", self.current_id)[0][4]
        self.classification_label.setText("Classification: " + self.classification + " " + self.confirmed)

        # Create the button layout
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.yes_button)
        self.button_layout.addWidget(self.no_button)
        self.button_layout.addWidget(self.not_quite_button)
        self.button_widget = QWidget()
        self.button_widget.setLayout(self.button_layout)

        # Add the widgets to the window
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.image_layout)
        self.layout.addWidget(self.classification_label)
        self.layout.addWidget(self.button_widget)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def confirm_image(self):
        # change the classification of the image to confirmed
        self.database.changeValue(self.current_id, "CONFIRMED", "Confirmed")
        self.update_classification()

    def reject_image(self):
        # change the classification of the image to rejected
        self.database.changeValue(self.current_id, "CONFIRMED", "Rejected")
        self.update_classification()

    def not_quite_image(self):
        # doesn't do anything yet
        pass

    def next_image(self):
        # if there is a next image, increment the index and show the next image
        if self.current_index < self.image_stack.count() - 1:
            self.current_index += 1
            self.image_stack.setCurrentIndex(self.current_index)
            id_index = self.ids.index(self.current_id)
            self.current_id = self.ids[id_index + 1]
            self.update_classification()
            
    def prev_image(self):
        # if there is a previous image, decrement the index and show the previous image
        if self.current_index > 0:
            self.current_index -= 1
            self.image_stack.setCurrentIndex(self.current_index)
            id_index = self.ids.index(self.current_id)
            self.current_id = self.ids[id_index - 1]
            self.update_classification()

    def update_classification(self):
        self.classification = self.database.filterRows("ID", self.current_id)[0][3]
        self.confirmed = self.database.filterRows("ID", self.current_id)[0][4]
        self.classification_label.setText("Classification: " + self.classification + " " + self.confirmed)

class MapWidget:
    def __init__(self):
        # Create the map interface
        self.web_view = QWebEngineView()
        self.web_view.load(QUrl('https://www.google.com/maps/@43.0526155,-75.4039179,16z?entry=ttu'))

        # Create a QScrollArea instance for the web view and set the web_view as its widget
        self.image_scroll_area = QScrollArea()
        self.image_scroll_area.setWidgetResizable(True)
        self.image_scroll_area.setWidget(self.web_view)
        self.image_scroll_area.hide()


class TextEditorWidget:
    def __init__(self):
        # Create the notes text edit area from a log file
        self.text_editor = QTextEdit()

        # Get the directory of the current script
        dir_path = os.path.dirname(os.path.realpath(__file__))

        # Create log.txt in the same directory as the current script
        self.log_path = os.path.join(dir_path, "log.txt")
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w'): pass

        # Read the file and start the editing on a newline
        with open(self.log_path, 'r') as file:
            content = file.read()
        if content and content[-1] != "\n":
            content += "\n"

        # Add timestamp to each new line
        lines = content.split("\n")
        for i in range(len(lines)):
            if lines[i] != "" and not re.match(r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}: ", lines[i]):
                lines[i] = datetime.now().strftime("%m/%d/%Y %H:%M:%S: ") + lines[i]
        content = "\n".join(lines)
        self.text_editor.setText(content)

class FilterBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addItems(["None", "CameraA", "CameraB", "CameraC", "Night", "Confirmed", "Rejected", "Day", "Tag1", "Tag2", "Tag3", "Tag4", "Tag5"])

class SortBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addItems(["None", "Species A-Z", "Species Z-A"])


class MenuButtons:
    def __init__ (self, button_texts, text_editor, scroll_area, map):
        # Create main menu buttons as a group and connect them to their functionalities
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
            button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
            button.setStyleSheet("padding: 10px; min-height: 30px; max-height: 30px; min-width: 100px; text-align: left;")
            self.button_layout.addWidget(button)
            self.button_group.addButton(button)

        # Make the buttons go to the top of the screen
        self.button_layout.addStretch()

        # Create Widget
        self.button_widget = QWidget()
        self.button_widget.setLayout(self.button_layout)

    def buttonClicked(self, button):
        # Define button behavior
        self.resetWidgets()
        if button.text() == "Notes":
            self.text_editor.show()
        elif button.text() == "Library":
            self.scroll_area.show()
        elif button.text() == "Cameras":
            self.map.show()

    def resetWidgets(self):
        # Resets all widgets
        for btn in self.button_group.buttons():
            btn.setStyleSheet("padding: 10px; min-height: 30px; max-height: 30px; min-width: 100px; text-align: left;")
        self.text_editor.hide()
        self.scroll_area.hide()
        self.map.hide()


class MainWindow(QMainWindow):
    def __init__(self, conn, parent=None):
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

    # Set up combo boxes behavior to refresh images every time they are changed
    def setupComboBoxes(self):
        self.sorting_combobox.currentTextChanged.connect(self.deleteRefreshImages)
        self.filtering_combobox.currentTextChanged.connect(self.deleteRefreshImages)

    def createMenuButtons(self):
        # Create main menu buttons as a group and connect them to their functionalities
        self.menu_buttons = MenuButtons(["Library", "Cameras", "Notes"], self.text_editor, self.scroll_area, self.map)

    def createMap(self):
        # Create the map interface
        self.map = MapWidget().image_scroll_area

    def createTextEditor(self):
        # Create the notes text edit area from a log file
        text_widget = TextEditorWidget()
        self.text_editor = text_widget.text_editor
        self.log_path = text_widget.log_path

    def createScrollAreas(self):
        # Create different scroll areas for other menues as temporary placeholders
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.sorting_combobox = SortBox()
        self.filtering_combobox = FilterBox()
        self.scroll_area.hide()
        self.lib_layout = QVBoxLayout()

    def closeEvent(self, event):
        # Save edits to log.txt when the app is closed
        with open(self.log_path, 'w') as file:
            file.write(self.text_editor.toPlainText())
        # Call the parent class’s existing closeEvent
        super().closeEvent(event)

    def getImageFiles(self, database, sort, filter):
        # How do we filter for tags?
        filter_case = {
            "CameraA": "CAMERA",
            "CameraB": "CAMERA",
            "CameraC": "CAMERA",
            "Night": "DAYNIGHT",
            "Day": "DAYNIGHT",
            "Confirmed": "CONFIRMED",
            "Rejected": "CONFIRMED",
            "Tag1": "TAGS",
            "Tag2": "TAGS",
            "Tag3": "TAGS",
            "Tag4": "TAGS",
            "Tag5": "TAGS",
            "None": "*"
        }
        sort_case = {
            "Species A-Z": False,
            "Species Z-A": True
        }
        filterd = database.filterRows(filter_case[filter], filter)
        if sort == "None":
            sorted = filterd
        else:
            sorted = database.sortRows(filterd, "CLASSIFICATION", sort_case[sort])
        # only keep the [id, image path, classification] from the database
        sorted = list(map(lambda x: [x[0], x[1], x[3]], sorted))
        return sorted


    def createHeaderAndGrid(self, date):
        # Creates the grid that populates the Library interface
        header = QLabel(str(date))
        self.lib_layout.addWidget(header)
        grid = QGridLayout()
        self.lib_layout.addLayout(grid)
        return grid

    def addImageToGrid(self, grid, image_file, row, col, ids):
        # Creates scaled QPixmap images to add to the grid

        # Create a widget to hold the image and the text label
        data_widget = Datapoint(image_file[0], image_file[1], image_file[2], self.scroll_area, self.database, ids)

        # Add the widget to the grid
        grid.addWidget(data_widget, row, col)

    def displayImages(self, databse):
        # add images to grid
        # image_files = self.getImageFiles(self.database)
        # image_files.sort(key=os.path.getmtime, reverse=True)

        # Create a layout for the combo boxes
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.sorting_combobox)
        top_layout.addWidget(self.filtering_combobox)
    
        self.lib_layout.addLayout(top_layout)  # Add the combo box layout to the main layout

        self.lib_layout.setContentsMargins(0, 0, 0, 0)

        self.refreshImages()

        widget = QWidget()
        widget.setLayout(self.lib_layout)
        self.scroll_area.setWidget(widget)

        print(self.scroll_area.children()[0].children()[0].children())
    

    def refreshImages(self):
        # Refreshes the images in the library
        #self.scroll_area.takeWidget().deleteLater()
        print("refreshing images")
        # image_files = [[id, path, classification], [id, path, classification]
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

            # TEMPORARY: allows 3 images per row for presentation purposes
            col += 1
            if col > 2:
                col = 0
                row += 1

    def deleteRefreshImages(self):
        # Refreshes the images in the library
        #self.scroll_area.takeWidget().deleteLater()
        print("refreshing images")
        # image_files = [[id, path, classification], [id, path, classification]
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
        # Build the UI
        button_widget = self.menu_buttons.button_widget

        main_layout = QHBoxLayout()
        main_layout.addWidget(button_widget)
        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(self.text_editor)
        main_layout.addWidget(self.map)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myData = connect()
    widget = MainWindow(myData)
    widget.show()
    sys.exit(app.exec())
    conn.commit()
    conn.close()

