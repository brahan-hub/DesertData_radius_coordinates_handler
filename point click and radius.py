from qgis.core import QgsVectorLayer, QgsFeature, QgsGeometry
from qgis.gui import QgsRubberBand


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