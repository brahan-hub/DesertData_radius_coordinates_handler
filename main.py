from qgis.core import QgsProject, QgsPointXY
from qgis.gui import QgsMapToolEmitPoint
from qgis.PyQt.QtCore import pyqtSignal

class CoordinateCaptureTool(QgsMapToolEmitPoint):
    clicked = pyqtSignal(float, float)
    
    def __init__(self, canvas, layer):
        self.canvas = canvas
        self.layer = layer
        super().__init__(self.canvas)
    
    def canvasReleaseEvent(self, event):
        point = self.toMapCoordinates(event.pos())
        if self.layer.extent().contains(QgsPointXY(point)):
            self.clicked.emit(point.x(), point.y())
            print(f"Clicked coordinate: {point.x()}, {point.y()}")
        else:
            print("Clicked outside the map bounds.")

# Get the map canvas
canvas = iface.mapCanvas()

# Get the first raster layer (assuming you have one loaded)
layer = None
for lyr in QgsProject.instance().mapLayers().values():
    if lyr.type() == QgsMapLayer.RasterLayer:
        layer = lyr
        break

if layer is not None:
    # Create and set the tool
    tool = CoordinateCaptureTool(canvas, layer)
    canvas.setMapTool(tool)

    # Connect the clicked signal to a function
    def handle_click(x, y):
        print(f"Clicked coordinate: {x}, {y}")

    tool.clicked.connect(handle_click)

    print("Click on the map to get coordinates.")
else:
    print("No raster layer found.")
