import io
import folium
from folium.plugins import MousePosition
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QScrollArea
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QInputDialog
class MapWidget(QScrollArea):
    """
    This class is a QScrollArea that is used to display a map of the area
    """
    def __init__(self):
        super().__init__()

        self.webView = QWebEngineView()
        self.markers = self.getMarkers()
        self.refreshMarkers()
        
        self.setWidgetResizable(True)
        # add the web view to the scroll area
        self.stack = QVBoxLayout()
        self.stack.addWidget(self.webView)
        self.buttons = QHBoxLayout()
        # add buttons to the scroll area
        self.addButton = QPushButton("Add Marker")
        self.removeButton = QPushButton("Remove Marker")
        self.addButton.clicked.connect(self.addMarker)
        self.removeButton.clicked.connect(self.removeMarker)
        self.buttons.addWidget(self.addButton)
        self.buttons.addWidget(self.removeButton)
        self.stack.addLayout(self.buttons)

        self.setLayout(self.stack)
        
    def addMarker(self):
        """
        Adds a marker to the map
        """
        text, ok = QInputDialog.getText(self, "Add Marker", "Enter a name for the marker:")
        if ok:
            x_coord, x_ok = QInputDialog.getDouble(self, "Add Marker", "Enter the x coordinate (optional):", decimals = 6)
            y_coord, y_ok = QInputDialog.getDouble(self, "Add Marker", "Enter the y coordinate (optional):", decimals = 6)
            
            # if the user does not input anything, use m.location
            if not x_ok: x_coord = self.m.location[1]
            if not y_ok: y_coord = self.m.location[0]
            
            # add a marker to the list of markers
            self.markers.append([y_coord, x_coord, text])
            self.refreshMarkers()


    def removeMarker(self):
        """
        Removes a marker from the map
        """
        markerNames = []
        for marker in self.markers:
            markerNames.append(marker[2])
        markerName, ok = QInputDialog.getItem(self, "Remove Marker", "Select a marker to remove:", markerNames)
        if ok:
            # remove the marker from the map
            for marker in self.markers:
                if marker[2] == markerName:
                    self.markers.remove(marker)
                    break
            self.refreshMarkers()
        


    def getMarkers(self):
        """
        Retrieves/creates a list of markers from a file in the project folder
        @Returns a two dimensional array containg lists for each marker
        containing the latitude, longitude, and name of the marker
        """
        try:
            with open("Program/markers.txt", 'r') as file:
                content = file.read()
            if content and content[-1] != "\n":
                content += "\n"
            lines = content.split("\n")
            output = []
            for line in lines:
                if line != "":
                    # convert numbers from strings to floats and text to strings
                    line = line.split(",")
                    line[0] = float(line[0])
                    line[1] = float(line[1])
                    line[2] = str(line[2])
                    output.append(line)
            return output
        except:
            with open("Program/markers.txt", 'w') as file:
                pass
            return []
        
    def refreshMarkers(self):
        # clear the map of all markers
        # Create the map interface
        coordinate = (43.044641, -75.406852)
        self.m = folium.Map(
        	zoom_start = 17,
        	location = coordinate
        )
        
        # Define the formatter function for the mouse position
        formatter = "function(num) {return L.Util.formatNum(num, 6) + ' º ';};"

        # Add the MousePosition plugin to the map
        MousePosition(
            position="topright",
            separator=" | ",
            empty_string="NaN",
            lng_first=True,
            num_digits=20,
            prefix="Coordinates:",
            lat_formatter=formatter,
            lng_formatter=formatter,
        ).add_to(self.m)


        for marker in self.markers:
            folium.Marker([marker[0], marker[1]], draggable=True, popup=marker[2]).add_to(self.m)
        # save map data to data object
        self.data = io.BytesIO()
        self.m.save(self.data, close_file=False)
        # update the map
        self.webView.setHtml(self.data.getvalue().decode())
        