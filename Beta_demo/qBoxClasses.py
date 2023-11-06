from PySide6.QtWidgets import  QComboBox
class FilterBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addItems(["None", "CameraA", "CameraB", "CameraC", "night", "day", "Confirmed", "Rejected", "Pending", "Tag1", "Tag2", "Tag3", "Tag4", "Tag5"])

class SortBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addItems(["Latest to Oldest", "Oldest to Latest", "Species A-Z", "Species Z-A"])