"""
Get pixel coordinates (not geographic coordinates) of a location in a raster.
Run the script to activate the tool.
Click a location to see row, column printed to Python console.
Click any other tool to deactivate.
Original source: https://gis.stackexchange.com/a/261538/67365
Modified slightly from the original for compatibility with Python 3 + QGIS 3 - Hannover
"""

from qgis.gui import QgsMapTool
from PyQt5.QtCore import Qt, QPoint
from math import floor

# references to QGIS objects
canvas = iface.mapCanvas()
layer = iface.activeLayer()
data_provider = layer.dataProvider()

# properties to map mouse position to row/col index of the raster in memory
extent = data_provider.extent()
width = data_provider.xSize() if data_provider.capabilities() & data_provider.Size else 1000
height = data_provider.ySize() if data_provider.capabilities() & data_provider.Size else 1000
xres = extent.width() / width
yres = extent.height() / height


class ClickTool(QgsMapTool):
    def __init__(self, canvas, radius=1000 * 10):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.rubberBand = QgsRubberBand(canvas, QgsWkbTypes.PolygonGeometry)  # Rubber band for displaying the circle
        self.rubberBand.setColor(QColor(255, 0, 0, 100))  # Set color and transparency of the rubber band
        self.radius = radius

    def canvasPressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.pos().x()
            y = event.pos().y()

            # clicked position on screen to map coordinates
            point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)

            if extent.xMinimum() <= point.x() <= extent.xMaximum() and \
                    extent.yMinimum() <= point.y() <= extent.yMaximum():
                col = int(floor((point.x() - extent.xMinimum()) / xres))
                row = int(floor((extent.yMaximum() - point.y()) / yres))

                print(f"{row}, {col}")

                # Create circular polygon geometry
                circle_geometry = QgsGeometry.fromPointXY(point).buffer(self.radius, 100)

                # Display the circle on the map
                self.rubberBand.setToGeometry(circle_geometry, None)

    def clearRubberBand(self):
        self.rubberBand.reset()  # Reset the rubber band to clear the geometry

    def deactivate(self):
        self.clearRubberBand()  # Clear the rubber band when deactivating the tool


tool = ClickTool(iface.mapCanvas())
iface.mapCanvas().setMapTool(tool)