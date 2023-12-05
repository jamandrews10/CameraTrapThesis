from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QSizePolicy, QHBoxLayout, QLabel, QComboBox, QStackedWidget, QSpacerItem, QInputDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Signal
import os

# datapoint is a class that holds the pixmap and the labels for each image
class Datapoint(QWidget):
    def __init__(self, id, imageFile, classification, confidence, imageWidget, database, ids, mainWindow):
        super().__init__()
        # Create a widget to hold the image and the text label
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.scrollArea = imageWidget
        self.title = imageFile
        self.database = database
        self.ids = ids
        self.id = id
        self.mainWindow = mainWindow
        self.confirmed = self.database.getRow(self.id)[5]
        # Create the image
        self.originalPixmap = QPixmap(imageFile)
        self.label = ClickableLabel(self, self.scrollArea, self.database, self.id, classification, ids, mainWindow)
        self.pixmap = self.originalPixmap.scaledToWidth(350, Qt.SmoothTransformation)
        self.label.setPixmap(self.pixmap)
        self.layout.addWidget(self.label)
        # Create classification label
        self.textLabel = QLabel()
        self.textLabel.setText(self.confirmed + " " + classification.capitalize() + " (" + str(round(float(confidence) * 100))+ "%)")
        self.textLabel.setStyleSheet("font: 18pt")
        self.textLabel.setFixedHeight(50)
        self.textLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.textLabel)
        self.layout.setAlignment(Qt.AlignCenter)

    # when hovering over the label, show 2 buttons on the image. One to confirm and one to reject
    def enterEvent(self, event):
        self.confirmButton = QPushButton("Confirm")
        self.confirmButton.clicked.connect(self.confirmImage)
        self.rejectButton = QPushButton("Reject")
        self.rejectButton.clicked.connect(self.rejectImage)
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.confirmButton)
        self.buttonLayout.addWidget(self.rejectButton)
        self.buttonWidget = QWidget()
        self.buttonWidget.setLayout(self.buttonLayout)
        # add the buttons to the image
        self.layout.addWidget(self.buttonWidget)
        # animate the label to be bigger
        self.label.setPixmap(self.originalPixmap.scaledToWidth(400, Qt.SmoothTransformation))


    # when the mouse leaves the label, remove the buttons from the layout
    def leaveEvent(self, event):
        self.layout.removeWidget(self.buttonWidget)
        self.buttonWidget.deleteLater()
        self.label.setPixmap(self.originalPixmap.scaledToWidth(350, Qt.SmoothTransformation))

    def confirmImage(self):
        # change the classification of the image to confirmed
        self.database.changeValue(self.id, "CONFIRMED", "Confirmed")
        self.mainWindow.deleteRefreshImages()

    def rejectImage(self):
        # change the classification of the image to rejected
        self.database.changeValue(self.id, "CONFIRMED", "Rejected")
        self.mainWindow.deleteRefreshImages()

class ImageViewer(QMainWindow):
    # PopUp window
    def __init__(self, clickedImage, imageWidget, database, id, ids, mainWindow):
        super().__init__()
        self.database = database
        self.currentId = id
        self.ids = ids
        self.id = id
        self.tags = self.database.getTags(self.id)
        self.mainWindow = mainWindow
        # get every image widget in the library
        self.imagesWidget = imageWidget.children()[0].children()[0].children()
        # get the pixmap of the image that was clicked on
        self.clickedImage = clickedImage
        #create a QstackedWidget to hold 10 previous images and 10 next images
        self.imageStack = QStackedWidget() 
        self.currentIndex = 0
        self.index = 0
        for widget in self.imagesWidget:
            if isinstance(widget, Datapoint):
                # Create a new QLabel
                labelCopy = QLabel()
                # Set its pixmap to be the same as the original label
                labelCopy.setPixmap(widget.originalPixmap.scaledToWidth(800, Qt.SmoothTransformation))
                # add a copy of the label to the stack
                self.imageStack.addWidget(labelCopy)
                # if the label title is the same as the clicked image, set the current index to the index of the label 
                if widget.title == self.clickedImage:
                    # set the index of the stack to the index of the pixmap that was clicked on
                    self.currentIndex = self.index
                self.index += 1
        
        self.initUI()

    def initUI(self):
        # Create the image viewer
        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Create the buttons
        self.yesButton = QPushButton("Yes")
        self.yesButton.clicked.connect(self.confirmImage)
        self.noButton = QPushButton("No animal (false positive))")
        self.noButton.clicked.connect(self.rejectImage)
        self.deleteButton = QPushButton("Delete Image")
        self.deleteButton.clicked.connect(self.deleteImage)
        self.tagButton = QPushButton("Add Tag")
        self.tagButton.clicked.connect(self.addTag)
        self.existingTagButton = QPushButton("Add Existing Tag")
        self.existingTagButton.clicked.connect(self.addExistingTag)
        self.deleteTagButton = QPushButton("Delete Tag")
        self.deleteTagButton.clicked.connect(self.deleteTag)
        # make a drop down list titled not quite and add options
        self.notQuiteList = QComboBox()
        self.notQuiteList.addItems(["Not quite", "deer", "squirrel", "possum", "fox", "mouse", "skunk", "raccoon", "cat", "dog", "bird", "coyote", "rabbit", "weasel", "groundhog"])
        self.notQuiteList.currentTextChanged.connect(self.notQuiteImage)

        # Create the image layout
        self.imageStack.setCurrentIndex(self.currentIndex)

        # create nav buttons
        self.nextButton = QPushButton("Next")
        self.nextButton.clicked.connect(self.nextImage)
        self.prevButton = QPushButton("Previous")
        self.prevButton.clicked.connect(self.prevImage)

        # create the layout
        self.imageLayout = QHBoxLayout()
        spacer1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.imageLayout.addWidget(self.prevButton)
        self.imageLayout.addSpacerItem(spacer1)
        self.imageLayout.addWidget(self.imageStack)
        self.imageLayout.addSpacerItem(spacer2)
        self.imageLayout.addWidget(self.nextButton)

        # Create a label for the classification
        self.classificationLabel = QLabel()
        self.classification = self.database.filterRows("ID", self.currentId)[0][3]
        self.confidence = self.database.filterRows("ID", self.currentId)[0][4]
        self.confirmed = self.database.filterRows("ID", self.currentId)[0][5]
        self.classificationLabel.setText(self.confirmed + " " + self.classification.capitalize() + " (" + str(round(float(self.confidence) * 100))+ "%)" + " " + str(self.tags))

        # Create the button layout
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.yesButton)
        self.buttonLayout.addWidget(self.noButton)
        self.buttonLayout.addWidget(self.notQuiteList)
        self.buttonWidget = QWidget()
        self.buttonWidget.setLayout(self.buttonLayout)
        self.secondaryButtonLayout = QHBoxLayout()
        self.secondaryButtonLayout.addWidget(self.tagButton)
        self.secondaryButtonLayout.addWidget(self.existingTagButton)
        self.secondaryButtonLayout.addWidget(self.deleteTagButton)
        self.secondaryButtonLayout.addWidget(self.deleteButton)
        self.secondaryButtonWidget = QWidget()
        self.secondaryButtonWidget.setLayout(self.secondaryButtonLayout)
        


        # Add the widgets to the window
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.imageLayout)
        self.layout.addWidget(self.classificationLabel)
        self.layout.addWidget(self.buttonWidget)
        self.layout.addWidget(self.secondaryButtonWidget)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    # When the window is closed, delete and refresh images in the library
    def closeEvent(self, event):
        self.mainWindow.deleteRefreshImages()
        super().closeEvent(event)

    def confirmImage(self):
        # change the classification of the image to confirmed
        self.database.changeValue(self.currentId, "CONFIRMED", "Confirmed")
        self.updateClassification()

    def rejectImage(self):
        # change the classification of the image to rejected
        self.database.changeValue(self.currentId, "CONFIRMED", "Rejected")
        self.updateClassification()

    def notQuiteImage(self):
        # if the classification is not quite, change the classification to the selected option and confirm it
        if self.notQuiteList.currentText() != "Not quite":
            self.database.changeValue(self.currentId, "CLASSIFICATION", self.notQuiteList.currentText())
            self.database.changeValue(self.currentId, "CONFIRMED", "Confirmed")
            self.updateClassification()
            # reset the combo box to not quite
            self.notQuiteList.setCurrentIndex(0)
    
    def deleteImage(self):
        # get the row of the image from the database
        row = self.database.getRow(self.currentId)
        # delete the image and cropped image from the directory
        os.remove(row[1])
        os.remove(row[2])
        # delete the image from the database
        self.database.deleteRow(self.currentId)
        # close the image viewer
        self.close()
    
    def addTag(self):
        # open a QInputDialog box to get the tag from the user
        tag, ok = QInputDialog.getText(self, "Add New Tag", "Enter a tag:")
        if ok:
            self.database.addTag(self.currentId, tag)
            self.mainWindow.filteringCombobox.update()
            self.updateClassification()

    def addExistingTag(self):
        # get the list of tags from the database
        tags = self.database.getAllTags()
        # open a QInputDialog box to get the tag from the user
        tag, ok = QInputDialog.getItem(self, "Add Existing Tag", "Select a tag to add:", tags)
        if ok:
            self.database.addTag(self.currentId, tag)
            self.mainWindow.filteringCombobox.update()
            self.updateClassification()

    def deleteTag(self):
        # get the list of tags from the database
        tags = self.database.getTags(self.currentId)
        # open a QInputDialog box to get the tag from the user
        tag, ok = QInputDialog.getItem(self, "Delete Tag", "Select a tag to delete:", tags)
        if ok:
            self.database.deleteTag(self.currentId, tag)
            self.mainWindow.filteringCombobox.update()
            self.updateClassification()

    def nextImage(self):
        # if there is a next image, increment the index and show the next image
        if self.currentIndex < self.imageStack.count() - 1:
            self.currentIndex += 1
            self.imageStack.setCurrentIndex(self.currentIndex)
            idIndex = self.ids.index(self.currentId)
            self.currentId = self.ids[idIndex + 1]
            self.updateClassification()
            
    def prevImage(self):
        # if there is a previous image, decrement the index and show the previous image
        if self.currentIndex > 0:
            self.currentIndex -= 1
            self.imageStack.setCurrentIndex(self.currentIndex)
            idIndex = self.ids.index(self.currentId)
            self.currentId = self.ids[idIndex - 1]
            self.updateClassification()

    def updateClassification(self):
        self.classification = self.database.filterRows("ID", self.currentId)[0][3]
        self.confirmed = self.database.filterRows("ID", self.currentId)[0][5]
        self.tags = self.database.getTags(self.currentId)
        self.classificationLabel.setText(self.confirmed + " " + self.classification.capitalize() + " (" + str(round(float(self.confidence) * 100))+ "%)" + " " + str(self.tags))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        if event.key() == Qt.Key_Right:
            self.nextImage()
        if event.key() == Qt.Key_Left:
            self.prevImage()



class ClickableLabel(QLabel):
    # This class is used to create a clickable label
    clicked = Signal()

    def __init__(self, clickedWidget, imagesWidget, database, id, classification, ids, mainWindow, parent=None):
        super().__init__(parent)
        self.imagesWidget = imagesWidget
        self.clickedImage = clickedWidget.title
        self.database = database
        self.id = id
        self.ids = ids
        self.classification = classification
        self.mainWindow = mainWindow
        
    # when mouse is pressed, call displayImage
    def mousePressEvent(self, event):
        self.clicked.emit()
        self.displayImage(self.clickedImage, self.imagesWidget)

    # when clicking on the label, make an instance of the image viewer
    def displayImage(self, clickedImage, imagesWidget):
        self.imageViewer = ImageViewer(clickedImage, imagesWidget, self.database, self.id, self.ids, self.mainWindow)
        self.imageViewer.show()