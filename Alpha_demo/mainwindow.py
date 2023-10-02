# This Python file uses the following encoding: utf-8
import sys
import os
from datetime import datetime
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QSizePolicy, QHBoxLayout, QButtonGroup, QTextEdit, QScrollArea, QSplitter, QLabel, QGridLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
# databaseInput establishes "conn", a connection to an already filled database that can be iterated through with "cursor"
# cursor = conn.execute("SELECT id, imagePath, croppedPath, class from PATHS")#
import databaseInput

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, conn, parent=None):
        super().__init__(parent)
        self.database = conn
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.create_menu_buttons()
        self.create_text_editor()
        self.create_scroll_areas()
        self.create_library()

        self.setup_ui()

    def create_menu_buttons(self):
        # Create main menu buttons as a group and connect them to their functionalities
        self.button_texts = ["Library", "Projects", "Species", "Cameras", "Notes"]
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        self.button_group.buttonClicked.connect(self.on_button_clicked)

    def create_library(self):
        # Create the library interface
        self.image = QPixmap("/Users/yassine/TrapCam/Cameras.png")
        self.image_label = QLabel()
        self.image_label.setPixmap(self.image)
        self.image_label.hide()

        # Create a QScrollArea instance for the image and set the image_label as its widget
        self.image_scroll_area = QScrollArea()
        self.image_scroll_area.setWidgetResizable(True)
        self.image_scroll_area.setWidget(self.image_label)
        self.image_scroll_area.hide()

        self.display_images(self.database)

    def create_text_editor(self):
        # Create the notes text edit area from a log file
        self.text_editor = QTextEdit()

        # Open log.txt in a given directory or create it if it does not exist
        self.log_path = "/Users/yassine/TrapCam/Notes/log.txt"
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w'): pass

        # Read the file and start the editing on a newline
        with open(self.log_path, 'r') as file:
            content = file.read()
        if content and content[-1] != "\n":
            content += "\n"

        self.text_editor.setText(content)

    def create_scroll_areas(self):
        # Create different scroll areas for other menues as temporary placeholders
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.hide()

        self.scroll_area2 = QScrollArea()
        self.scroll_area2.setWidgetResizable(True)
        self.scroll_area2.hide()

        self.scroll_area3 = QScrollArea()
        self.scroll_area3.setWidgetResizable(True)
        self.scroll_area3.hide()

    def closeEvent(self, event):
        # Save edits to log.txt when the app is closed
        with open(self.log_path, 'w') as file:
            file.write(self.text_editor.toPlainText())
        # Call the parent class’s existing closeEvent
        super().closeEvent(event)

    def get_image_files(self, database):
        # Obtain an image to display in the library
        paths = []
        cursor = database.execute("SELECT id, imagePath, croppedPath, class from PATHS")
        for row in cursor:
            paths.append(row[1])
        return paths
        #return [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.lower().endswith(('.png'))]

    def create_header_and_grid(self, layout, date):
        # Creates the grid that populates the Library interface
        header = QLabel(str(date))
        layout.addWidget(header)
        grid = QGridLayout()
        layout.addLayout(grid)
        return grid

    def add_image_to_grid(self, grid, image_file, row, col):
        # Creates scaled QPixmap images to add to the grid
        # pull the classification of the image from database
        sql = "SELECT class FROM PATHS WHERE imagePath = '" + image_file + "'"
        classification = self.database.execute(sql).fetchall()[0][0]

        # Create a widget to hold the image and the text label
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Create the image
        pixmap = QPixmap(image_file)
        pixmap = pixmap.scaledToWidth(350, Qt.SmoothTransformation)
        label = QLabel()
        label.setPixmap(pixmap)
        layout.addWidget(label)

        # Create classification label
        text_label = QLabel()
        text_label.setText(classification)
        text_label.setFixedHeight(50)
        layout.addWidget(text_label)

        # Add the widget to the grid
        grid.addWidget(widget, row, col)

    def display_images(self, databse):
        # add images to grid
        image_files = self.get_image_files(self.database)
        image_files.sort(key=os.path.getmtime, reverse=True)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        current_date = None
        grid = None
        row = col = 0

        for image_file in image_files:
            date = datetime.fromtimestamp(os.path.getmtime(image_file)).date()

            # Add a date header everytime the date changes
            if date != current_date:
                current_date = date
                grid = self.create_header_and_grid(layout, current_date)
                row = col = 0

            self.add_image_to_grid(grid, image_file, row, col)

            # TEMPORARY: allows 3 images per row for presentation purposes
            col += 1
            if col > 2:
                col = 0
                row += 1

        widget = QWidget()
        widget.setLayout(layout)
        self.scroll_area.setWidget(widget)

    def setup_ui(self):
        # Build the UI
        button_layout = self.create_buttons()
        button_widget = QWidget()
        button_widget.setLayout(button_layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(button_widget)
        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(self.scroll_area2)
        main_layout.addWidget(self.scroll_area3)
        main_layout.addWidget(self.text_editor)
        main_layout.addWidget(self.image_scroll_area)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_buttons(self):
        # Make the main menu buttons
        button_layout = QVBoxLayout()

        # Make the library the default interface
        for text in self.button_texts:
            button = QPushButton(text)
            button.setCheckable(True)
            if text == "Library":
                button.setChecked(True)
                self.on_button_clicked(button)
            # Set up the style for the buttons
            button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
            button.setStyleSheet("padding: 10px; min-height: 30px; max-height: 30px; min-width: 100px; text-align: left;")
            button_layout.addWidget(button)
            self.button_group.addButton(button)

        # Make the buttons go to the top of the screen
        button_layout.addStretch()

        return button_layout

    def on_button_clicked(self, button):
        # Define button behavior
        self.reset_all_widgets()
        button.setStyleSheet("padding: 10px; min-height: 30px; max-height: 30px; min-width: 100px; text-align: left; font-weight: bold;")
        if button.text() == "Notes":
            self.text_editor.show()
        elif button.text() == "Library":
            self.scroll_area.show()
        elif button.text() == "Cameras":
            self.image_scroll_area.show()
        elif button.text() == "Species":
            self.scroll_area2.show()
        elif button.text() == "Projects":
            self.scroll_area3.show()

    def reset_all_widgets(self):
        # Resets all widgets
        for btn in self.button_group.buttons():
            btn.setStyleSheet("padding: 10px; min-height: 30px; max-height: 30px; min-width: 100px; text-align: left;")
        self.text_editor.hide()
        self.scroll_area.hide()
        self.scroll_area2.hide()
        self.scroll_area3.hide()
        self.image_scroll_area.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow(databaseInput.conn)
    widget.show()
    sys.exit(app.exec())
    conn.commit()
    conn.close()
