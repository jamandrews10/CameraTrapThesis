from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QSizePolicy, QHBoxLayout, QLabel, QComboBox, QStackedWidget, QSpacerItem, QInputDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Signal
import os

class Datapoint(QWidget):
    """
    This class is a widget that holds the image and the classification label for each image in the library.
    """
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

    def enterEvent(self, event):
        """
        When the mouse enters the label, add the confirm and reject buttons to the image.
        """
        self.confirmButton = QPushButton("Confirm")
        self.confirmButton.clicked.connect(self.confirmImage)
        self.rejectButton = QPushButton("Reject")
        self.rejectButton.clicked.connect(self.rejectImage)
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.confirmButton)
        self.buttonLayout.addWidget(self.rejectButton)
        self.buttonWidget = QWidget()
        self.buttonWidget.setLayout(self.buttonLayout)
        self.layout.addWidget(self.buttonWidget)
        self.label.setPixmap(self.originalPixmap.scaledToWidth(400, Qt.SmoothTransformation))

    def leaveEvent(self, event):
        """ 
        When the mouse leaves the label, remove the confirm and reject buttons from the image.
        """
        self.layout.removeWidget(self.buttonWidget)
        self.buttonWidget.deleteLater()
        self.label.setPixmap(self.originalPixmap.scaledToWidth(350, Qt.SmoothTransformation))

    def confirmImage(self):
        """
        Change the classification of the image to confirmed.
        """
        self.database.changeValue(self.id, "CONFIRMED", "Confirmed")
        self.mainWindow.deleteRefreshImages()

    def rejectImage(self):
        """
        Change the classification of the image to rejected.
        """
        self.database.changeValue(self.id, "CONFIRMED", "Rejected")
        self.mainWindow.deleteRefreshImages()

class ImageViewer(QMainWindow):
    """
    This class is a window that displays the image that was clicked on in the library.
    """
    def __init__(self, clickedImage, imageWidget, database, id, ids, mainWindow):
        super().__init__()
        self.database = database
        self.currentId = id
        self.ids = ids
        self.id = id
        self.tags = self.database.getTags(self.id)
        self.mainWindow = mainWindow
        self.imagesWidget = imageWidget.children()[0].children()[0].children()
        self.clickedImage = clickedImage
        self.imageStack = QStackedWidget() 
        self.currentIndex = 0
        self.index = 0
        for widget in self.imagesWidget:
            if isinstance(widget, Datapoint):
                labelCopy = QLabel()
                labelCopy.setPixmap(widget.originalPixmap.scaledToWidth(800, Qt.SmoothTransformation))
                self.imageStack.addWidget(labelCopy)
                if widget.title == self.clickedImage:
                    self.currentIndex = self.index
                self.index += 1
        
        self.initUI()

    def initUI(self):
        """
        Create the image viewer window
        """
        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 800, 600)

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

        self.notQuiteList = QComboBox()
        self.notQuiteList.addItems(["Not quite", "deer", "squirrel", "possum", "fox", "mouse", "skunk", "raccoon", "cat", "dog", "bird", "coyote", "rabbit", "weasel", "groundhog"])
        self.notQuiteList.currentTextChanged.connect(self.notQuiteImage)

        self.imageStack.setCurrentIndex(self.currentIndex)

        self.nextButton = QPushButton("Next")
        self.nextButton.clicked.connect(self.nextImage)
        self.prevButton = QPushButton("Previous")
        self.prevButton.clicked.connect(self.prevImage)

        self.imageLayout = QHBoxLayout()
        spacer1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.imageLayout.addWidget(self.prevButton)
        self.imageLayout.addSpacerItem(spacer1)
        self.imageLayout.addWidget(self.imageStack)
        self.imageLayout.addSpacerItem(spacer2)
        self.imageLayout.addWidget(self.nextButton)

        self.classificationLabel = QLabel()
        self.classification = self.database.filterRows("ID", self.currentId)[0][3]
        self.confidence = self.database.filterRows("ID", self.currentId)[0][4]
        self.confirmed = self.database.filterRows("ID", self.currentId)[0][5]
        self.classificationLabel.setText(self.confirmed + " " + self.classification.capitalize() + " (" + str(round(float(self.confidence) * 100))+ "%)" + " " + str(self.tags))

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
        
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.imageLayout)
        self.layout.addWidget(self.classificationLabel)
        self.layout.addWidget(self.buttonWidget)
        self.layout.addWidget(self.secondaryButtonWidget)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def closeEvent(self, event):
        """
        When the window is closed, delete and refresh images in the library
        """
        self.mainWindow.deleteRefreshImages()
        super().closeEvent(event)

    def confirmImage(self):
        """
        Change the classification of the image to confirmed
        """
        self.database.changeValue(self.currentId, "CONFIRMED", "Confirmed")
        self.updateClassification()

    def rejectImage(self):
        """
        Change the classification of the image to rejected
        """
        self.database.changeValue(self.currentId, "CONFIRMED", "Rejected")
        self.updateClassification()

    def notQuiteImage(self):
        """
        Change the classification of the image
        """
        if self.notQuiteList.currentText() != "Not quite":
            self.database.changeValue(self.currentId, "CLASSIFICATION", self.notQuiteList.currentText())
            self.database.changeValue(self.currentId, "CONFIRMED", "Confirmed")
            self.updateClassification()
            self.notQuiteList.setCurrentIndex(0)
    
    def deleteImage(self):
        """
        Delete the image from the library and directory
        """
        row = self.database.getRow(self.currentId)
        os.remove(row[1])
        os.remove(row[2])
        self.database.deleteRow(self.currentId)
        self.close()
    
    def addTag(self):
        """
        Add a tag to the image
        """
        tag, ok = QInputDialog.getText(self, "Add New Tag", "Enter a tag:")
        if ok:
            self.database.addTag(self.currentId, tag)
            self.mainWindow.filteringCombobox.update()
            self.updateClassification()

    def addExistingTag(self):
        """
        Add an existing tag to the image
        """
        tags = self.database.getAllTags()
        tag, ok = QInputDialog.getItem(self, "Add Existing Tag", "Select a tag to add:", tags)
        if ok:
            self.database.addTag(self.currentId, tag)
            self.mainWindow.filteringCombobox.update()
            self.updateClassification()

    def deleteTag(self):
        """
        Delete a tag from the image
        """
        tags = self.database.getTags(self.currentId)
        tag, ok = QInputDialog.getItem(self, "Delete Tag", "Select a tag to delete:", tags)
        if ok:
            self.database.deleteTag(self.currentId, tag)
            self.mainWindow.filteringCombobox.update()
            self.updateClassification()

    def nextImage(self):
        """
        If there is a next image, increment the index and show the next image
        """
        if self.currentIndex < self.imageStack.count() - 1:
            self.currentIndex += 1
            self.imageStack.setCurrentIndex(self.currentIndex)
            idIndex = self.ids.index(self.currentId)
            self.currentId = self.ids[idIndex + 1]
            self.updateClassification()
            
    def prevImage(self):
        """
        If there is a previous image, decrement the index and show the previous image
        """
        if self.currentIndex > 0:
            self.currentIndex -= 1
            self.imageStack.setCurrentIndex(self.currentIndex)
            idIndex = self.ids.index(self.currentId)
            self.currentId = self.ids[idIndex - 1]
            self.updateClassification()

    def updateClassification(self):
        """
        Update the classification label
        """
        self.classification = self.database.filterRows("ID", self.currentId)[0][3]
        self.confirmed = self.database.filterRows("ID", self.currentId)[0][5]
        self.tags = self.database.getTags(self.currentId)
        self.classificationLabel.setText(self.confirmed + " " + self.classification.capitalize() + " (" + str(round(float(self.confidence) * 100))+ "%)" + " " + str(self.tags))

    def keyPressEvent(self, event):
        """
        When the right arrow key is pressed, show the next image
        When the left arrow key is pressed, show the previous image
        When the escape key is pressed, close the window
        """
        if event.key() == Qt.Key_Escape:
            self.close()
        if event.key() == Qt.Key_Right:
            self.nextImage()
        if event.key() == Qt.Key_Left:
            self.prevImage()



class ClickableLabel(QLabel):
    """
    This class is a label that emits a signal when it is clicked on.
    """
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
        
    def mousePressEvent(self, event):
        """
        When the label is clicked on, emit the signal and display the image in the image viewer
        """
        self.clicked.emit()
        self.displayImage(self.clickedImage, self.imagesWidget)

    def displayImage(self, clickedImage, imagesWidget):
        """
        Display the image in the image viewer
        """
        self.imageViewer = ImageViewer(clickedImage, imagesWidget, self.database, self.id, self.ids, self.mainWindow)
        self.imageViewer.show()