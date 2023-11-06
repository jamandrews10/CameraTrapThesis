from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QScrollArea
from PySide6.QtCore import QUrl
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