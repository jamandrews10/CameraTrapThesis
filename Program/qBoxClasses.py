from PySide6.QtWidgets import  QComboBox
class FilterBox(QComboBox):
    """
    This class is a QComboBox that is used to filter the images in the main window.
    """
    def __init__(self, database, parent=None):
        super().__init__(parent)
        self.database = database
        self.cameras = self.database.getAllCameras()
        self.tags = self.database.getAllTags()
        self.addItems(["No Filter"])
        self.addItems(self.cameras)
        self.addItems(["night", "day", "Confirmed", "Rejected", "Pending"])
        self.addItems(self.tags)
    
    def update(self):
        """
        Updates the filter box with the current cameras and tags.
        """
        self.cameras = self.database.getAllCameras()
        self.tags = self.database.getAllTags()
        self.clear()
        self.addItems(["No Filter"])
        self.addItems(self.cameras)
        self.addItems(["night", "day", "Confirmed", "Rejected", "Pending"])
        self.addItems(self.tags)

class SortBox(QComboBox):
    """
    This class is a QComboBox that is used to sort the images in the main window.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addItems(["Latest to Oldest", "Oldest to Latest", "Highest Confidence", "Lowest Confidence", "Species A-Z", "Species Z-A"])