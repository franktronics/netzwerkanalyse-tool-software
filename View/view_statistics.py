from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QPen, QBrush, QColor, QPainter


class NetworkCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Zoom limits
        self.min_zoom = 0.3
        self.max_zoom = 5.0
        self.current_zoom = 1.0

        # Create scene with fixed size
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(-2000, -2000, 4000, 4000)
        self.setScene(self.scene)

        # Draw grid background
        self._draw_grid()

        # Pan variables
        self.last_pan_point = QPointF()
        self.is_panning = False

        # Add a sample PC rectangle
        self._add_sample_pc()

    def _draw_grid(self):
        """Draw a grid background"""
        pen = QPen(QColor(200, 200, 200), 1)
        grid_size = 50

        scene_rect = self.scene.sceneRect()

        # Vertical lines
        x = scene_rect.left()
        while x <= scene_rect.right():
            line = self.scene.addLine(x, scene_rect.top(), x, scene_rect.bottom(), pen)
            line.setZValue(-1)  # Put grid in background
            x += grid_size

        # Horizontal lines
        y = scene_rect.top()
        while y <= scene_rect.bottom():
            line = self.scene.addLine(scene_rect.left(), y, scene_rect.right(), y, pen)
            line.setZValue(-1)  # Put grid in background
            y += grid_size

    def _add_sample_pc(self):
        """Add a simple rectangle representing a PC"""
        rect = QGraphicsRectItem(0, 0, 80, 60)
        rect.setBrush(QBrush(QColor(100, 150, 200)))
        rect.setPen(QPen(QColor(50, 100, 150), 2))
        rect.setPos(100, 100)
        self.scene.addItem(rect)

    def wheelEvent(self, event):
        """Handle zoom with mouse wheel"""
        zoom_factor = 1.15
        if event.angleDelta().y() > 0:
            new_zoom = self.current_zoom * zoom_factor
            if new_zoom <= self.max_zoom:
                self.scale(zoom_factor, zoom_factor)
                self.current_zoom = new_zoom
        else:
            new_zoom = self.current_zoom / zoom_factor
            if new_zoom >= self.min_zoom:
                self.scale(1 / zoom_factor, 1 / zoom_factor)
                self.current_zoom = new_zoom

    def mousePressEvent(self, event):
        """Handle mouse press for panning"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_panning = True
            self.last_pan_point = event.position()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Handle mouse move for panning"""
        if self.is_panning:
            delta = event.position() - self.last_pan_point
            # Convert to scene coordinates for proper panning
            h_bar = self.horizontalScrollBar()
            v_bar = self.verticalScrollBar()

            h_bar.setValue(h_bar.value() - int(delta.x()))
            v_bar.setValue(v_bar.value() - int(delta.y()))

            self.last_pan_point = event.position()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Handle mouse release to stop panning"""
        if event.button() == Qt.MouseButton.LeftButton and self.is_panning:
            self.is_panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)


class ViewStatistics(QWidget):
    
    #Constructor for centerApplication viewLStatistics
    def __init__(self):
        super().__init__()
        self._initUI()
    

    #initialize the centerApplication viewStatistics
    def _initUI(self):
        layout = QVBoxLayout()

        # Network canvas for visualization
        self.network_canvas = NetworkCanvas()
        self.network_canvas.add_participant(id = "00:11:22:33:44:55", name = "PC1")
        self.network_canvas.add_participant(id = "66:77:88:99:AA:BB", name = "PC2")
        self.network_canvas.add_connection(if_from = "00:11:22:33:44:55", id_to = "66:77:88:99:AA:BB")
        layout.addWidget(self.network_canvas)

        self.setLayout(layout)
