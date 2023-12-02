from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QSizePolicy, QHBoxLayout, QLabel, QComboBox, QStackedWidget, QSpacerItem, QInputDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Signal
import os

# datapoint is a class that holds the pixmap and the labels for each image
class Datapoint(QWidget):
    def __init__(self, id, image_file, classification, confidence, image_widget, database, ids, main_window):
        super().__init__()
        # Create a widget to hold the image and the text label
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.scroll_area = image_widget
        self.title = image_file
        self.database = database
        self.ids = ids
        self.id = id
        self.main_window = main_window
        self.confirmed = self.database.getRow(self.id)[5]
        # Create the image
        self.original_pixmap = QPixmap(image_file)
        self.label = ClickableLabel(self, self.scroll_area, self.database, self.id, classification, ids, main_window)
        self.pixmap = self.original_pixmap.scaledToWidth(350, Qt.SmoothTransformation)
        self.label.setPixmap(self.pixmap)
        self.layout.addWidget(self.label)
        # Create classification label
        self.text_label = QLabel()
        self.text_label.setText(self.confirmed + " " + classification.capitalize() + " (" + str(round(float(confidence) * 100))+ "%)")
        self.text_label.setStyleSheet("font: 18pt")
        self.text_label.setFixedHeight(50)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.text_label)
        self.layout.setAlignment(Qt.AlignCenter)

    # when hovering over the label, show 2 buttons on the image. One to confirm and one to reject
    def enterEvent(self, event):
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.confirm_image)
        self.reject_button = QPushButton("Reject")
        self.reject_button.clicked.connect(self.reject_image)
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.confirm_button)
        self.button_layout.addWidget(self.reject_button)
        self.button_widget = QWidget()
        self.button_widget.setLayout(self.button_layout)
        # add the buttons to the image
        self.layout.addWidget(self.button_widget)
        # animate the label to be bigger
        self.label.setPixmap(self.original_pixmap.scaledToWidth(400, Qt.SmoothTransformation))


    # when the mouse leaves the label, remove the buttons from the layout
    def leaveEvent(self, event):
        self.layout.removeWidget(self.button_widget)
        self.button_widget.deleteLater()
        self.label.setPixmap(self.original_pixmap.scaledToWidth(350, Qt.SmoothTransformation))

    def confirm_image(self):
        # change the classification of the image to confirmed
        self.database.changeValue(self.id, "CONFIRMED", "Confirmed")
        self.main_window.deleteRefreshImages()

    def reject_image(self):
        # change the classification of the image to rejected
        self.database.changeValue(self.id, "CONFIRMED", "Rejected")
        self.main_window.deleteRefreshImages()

class ImageViewer(QMainWindow):
    # PopUp window
    def __init__(self, clicked_image, image_widget, database, id, ids, main_window):
        super().__init__()
        self.database = database
        self.current_id = id
        self.ids = ids
        self.id = id
        self.tags = self.database.getTags(self.id)
        self.main_window = main_window
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
        self.no_button = QPushButton("No animal (false positive))")
        self.no_button.clicked.connect(self.reject_image)
        self.delete_button = QPushButton("Delete Image")
        self.delete_button.clicked.connect(self.delete_image)
        self.tag_button = QPushButton("Add Tag")
        self.tag_button.clicked.connect(self.add_tag)
        self.existing_tag_button = QPushButton("Add Existing Tag")
        self.existing_tag_button.clicked.connect(self.add_existing_tag)
        self.delete_tag_button = QPushButton("Delete Tag")
        self.delete_tag_button.clicked.connect(self.delete_tag)
        # make a drop down list titled not quite and add options
        self.not_quite_list = QComboBox()
        self.not_quite_list.addItems(["Not quite", "deer", "squirrel", "possum", "fox", "mouse", "skunk", "raccoon", "cat", "dog", "bird", "coyote", "rabbit", "weasel", "groundhog"])
        self.not_quite_list.currentTextChanged.connect(self.not_quite_image)

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
        self.confidence = self.database.filterRows("ID", self.current_id)[0][4]
        self.confirmed = self.database.filterRows("ID", self.current_id)[0][5]
        self.classification_label.setText(self.confirmed + " " + self.classification.capitalize() + " (" + str(round(float(self.confidence) * 100))+ "%)" + " " + str(self.tags))

        # Create the button layout
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.yes_button)
        self.button_layout.addWidget(self.no_button)
        self.button_layout.addWidget(self.not_quite_list)
        self.button_widget = QWidget()
        self.button_widget.setLayout(self.button_layout)
        self.secondary_button_layout = QHBoxLayout()
        self.secondary_button_layout.addWidget(self.tag_button)
        self.secondary_button_layout.addWidget(self.existing_tag_button)
        self.secondary_button_layout.addWidget(self.delete_tag_button)
        self.secondary_button_layout.addWidget(self.delete_button)
        self.secondary_button_widget = QWidget()
        self.secondary_button_widget.setLayout(self.secondary_button_layout)
        


        # Add the widgets to the window
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.image_layout)
        self.layout.addWidget(self.classification_label)
        self.layout.addWidget(self.button_widget)
        self.layout.addWidget(self.secondary_button_widget)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    # When the window is closed, delete and refresh images in the library
    def closeEvent(self, event):
        self.main_window.deleteRefreshImages()
        super().closeEvent(event)

    def confirm_image(self):
        # change the classification of the image to confirmed
        self.database.changeValue(self.current_id, "CONFIRMED", "Confirmed")
        self.update_classification()

    def reject_image(self):
        # change the classification of the image to rejected
        self.database.changeValue(self.current_id, "CONFIRMED", "Rejected")
        self.update_classification()

    def not_quite_image(self):
        # if the classification is not quite, change the classification to the selected option and confirm it
        if self.not_quite_list.currentText() != "Not quite":
            self.database.changeValue(self.current_id, "CLASSIFICATION", self.not_quite_list.currentText())
            self.database.changeValue(self.current_id, "CONFIRMED", "Confirmed")
            self.update_classification()
            # reset the combo box to not quite
            self.not_quite_list.setCurrentIndex(0)
    
    def delete_image(self):
        # get the row of the image from the database
        row = self.database.getRow(self.current_id)
        # delete the image and cropped image from the directory
        os.remove(row[1])
        os.remove(row[2])
        # delete the image from the database
        self.database.deleteRow(self.current_id)
        # close the image viewer
        self.close()
    
    def add_tag(self):
        # open a QInputDialog box to get the tag from the user
        tag, ok = QInputDialog.getText(self, "Add New Tag", "Enter a tag:")
        if ok:
            self.database.addTag(self.current_id, tag)
            self.main_window.filtering_combobox.update()
            self.update_classification()

    def add_existing_tag(self):
        # get the list of tags from the database
        tags = self.database.getAllTags()
        # open a QInputDialog box to get the tag from the user
        tag, ok = QInputDialog.getItem(self, "Add Existing Tag", "Select a tag to add:", tags)
        if ok:
            self.database.addTag(self.current_id, tag)
            self.main_window.filtering_combobox.update()
            self.update_classification()

    def delete_tag(self):
        # get the list of tags from the database
        tags = self.database.getTags(self.current_id)
        # open a QInputDialog box to get the tag from the user
        tag, ok = QInputDialog.getItem(self, "Delete Tag", "Select a tag to delete:", tags)
        if ok:
            self.database.deleteTag(self.current_id, tag)
            self.main_window.filtering_combobox.update()
            self.update_classification()

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
        self.confirmed = self.database.filterRows("ID", self.current_id)[0][5]
        self.tags = self.database.getTags(self.current_id)
        self.classification_label.setText(self.confirmed + " " + self.classification.capitalize() + " (" + str(round(float(self.confidence) * 100))+ "%)" + " " + str(self.tags))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        if event.key() == Qt.Key_Right:
            self.next_image()
        if event.key() == Qt.Key_Left:
            self.prev_image()



class ClickableLabel(QLabel):
    # This class is used to create a clickable label
    clicked = Signal()

    def __init__(self, clicked_widget, images_widget, database, id, classification, ids, main_window, parent=None):
        super().__init__(parent)
        self.images_widget = images_widget
        self.clicked_image = clicked_widget.title
        self.database = database
        self.id = id
        self.ids = ids
        self.classification = classification
        self.main_window = main_window
        
    # when mouse is pressed, call display_image
    def mousePressEvent(self, event):
        self.clicked.emit()
        self.display_image(self.clicked_image, self.images_widget)

    # when clicking on the label, make an instance of the image viewer
    def display_image(self, clicked_image, images_widget):
        self.image_viewer = ImageViewer(clicked_image, images_widget, self.database, self.id, self.ids, self.main_window)
        self.image_viewer.show()