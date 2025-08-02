from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem, QGraphicsPixmapItem
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPen, QBrush, QColor, QPainter, QFont, QPolygonF, QPixmap
import math
import networkx as nx
import os


class NetworkCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.pc_icon = os.path.abspath("assets/pc.png")
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

        # Participant management
        self.participants = {}  # id -> {item, position, name}
        self.connections = {}   # (id_from, id_to) -> {line, arrows}

        # NetworkX graph for layout calculation
        self.graph = nx.Graph()
        self.layout_scale = 300  # Scale factor for layout positioning

        # PC dimensions (square)
        self.pc_size = 100

    def _draw_grid(self):
        """Draw a grid background"""
        pen = QPen(QColor(200, 200, 200), 1)
        grid_size = 50

        scene_rect = self.scene.sceneRect()

        # Vertical lines
        x = scene_rect.left()
        while x <= scene_rect.right():
            line = self.scene.addLine(x, scene_rect.top(), x, scene_rect.bottom(), pen)
            line.setZValue(-1)
            x += grid_size

        # Horizontal lines
        y = scene_rect.top()
        while y <= scene_rect.bottom():
            line = self.scene.addLine(scene_rect.left(), y, scene_rect.right(), y, pen)
            line.setZValue(-1)
            y += grid_size

    def add_participant(self, id: str, name: str):
        """Add a participant to the network"""
        if id in self.participants:
            return

        # Add node to NetworkX graph
        self.graph.add_node(id)

        # Create PC image
        pixmap = QPixmap(self.pc_icon)
        if pixmap.isNull():
            # Fallback to square if image not found
            pc_item = QGraphicsRectItem(0, 0, self.pc_size, self.pc_size)
            pc_item.setBrush(QBrush(QColor(100, 150, 200)))
            pc_item.setPen(QPen(QColor(50, 100, 150), 2))
        else:
            # Scale image to desired size
            scaled_pixmap = pixmap.scaled(self.pc_size, self.pc_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            pc_item = QGraphicsPixmapItem(scaled_pixmap)

        # Create text for name (top)
        name_text = QGraphicsTextItem(name)
        name_text.setFont(QFont("Arial", 10, QFont.Weight.Bold))

        # Create text for ID (bottom)
        id_text = QGraphicsTextItem(id)
        id_text.setFont(QFont("Arial", 8))

        # Store participant info (position will be set later)
        self.participants[id] = {
            'pc_item': pc_item,
            'name_text': name_text,
            'id_text': id_text,
            'position': QPointF(0, 0),
            'name': name
        }

        # Add to scene
        self.scene.addItem(pc_item)
        self.scene.addItem(name_text)
        self.scene.addItem(id_text)

        # Recalculate layout for all participants
        self._update_layout()

    def _update_layout(self):
        """Update positions of all participants using NetworkX spring layout"""
        if len(self.participants) == 0:
            return

        if len(self.participants) == 1:
            # Single node, place at center
            positions = {list(self.participants.keys())[0]: (0, 0)}
        else:
            # Use spring layout for multiple nodes
            positions = nx.spring_layout(
                self.graph,
                k=2,  # Optimal distance between nodes
                iterations=50,  # Number of iterations for positioning
                scale=self.layout_scale,  # Scale the layout
                center=(0, 0)  # Center the layout
            )

        # Update participant positions
        for participant_id, (x, y) in positions.items():
            if participant_id in self.participants:
                position = QPointF(x, y)
                participant = self.participants[participant_id]

                # Update position
                participant['position'] = position
                participant['pc_item'].setPos(position)
                participant['name_text'].setPos(position.x() + 10, position.y() - 25)
                participant['id_text'].setPos(position.x() + 10, position.y() + self.pc_size + 5)

        # Update connection positions
        self._update_connections()

    def _update_connections(self):
        """Update all connection positions after layout change"""
        # Store connection data before clearing
        connection_data = {}
        for (from_id, to_id), connection in self.connections.items():
            # Count arrows to determine if bidirectional
            connection_data[(from_id, to_id)] = len(connection['arrows'])

        # Remove existing connection graphics
        for connection in self.connections.values():
            self.scene.removeItem(connection['line'])
            for arrow in connection['arrows']:
                self.scene.removeItem(arrow)

        # Clear connections
        self.connections.clear()

        # Recreate connections with new positions
        for (from_id, to_id), arrow_count in connection_data.items():
            if from_id in self.participants and to_id in self.participants:
                # Create the connection
                self._create_new_connection(from_id, to_id)

                # If there were 2 arrows (bidirectional), add the reverse
                if arrow_count == 2:
                    self._add_reverse_arrow(from_id, to_id)

    def add_connection(self, id_from, id_to):
        """Add a connection between two participants"""
        # Check if participants exist
        if id_from not in self.participants or id_to not in self.participants:
            return

        # Add edge to NetworkX graph
        self.graph.add_edge(id_from, id_to)

        # Check if exact connection exists
        if (id_from, id_to) in self.connections:
            return

        # Check if reverse connection exists
        reverse_key = (id_to, id_from)
        if reverse_key in self.connections:
            self._add_reverse_arrow(id_to, id_from)
        else:
            self._create_new_connection(id_from, id_to)

        self._update_layout()

    def _create_new_connection(self, id_from, id_to):
        """Create a new connection line with arrow"""
        # Calculate connection points at rectangle borders
        from_pos, to_pos = self._calculate_border_points(id_from, id_to)

        # Create line with 50% transparency
        line = QGraphicsLineItem(from_pos.x(), from_pos.y(), to_pos.x(), to_pos.y())
        line_color = QColor(50, 50, 50, 128)  # 128 = 50% transparency
        line.setPen(QPen(line_color, 2))

        # Create arrow
        arrow = self._create_arrow(from_pos, to_pos)

        self.scene.addItem(line)
        if arrow:
            self.scene.addItem(arrow)

        # Store connection
        self.connections[(id_from, id_to)] = {
            'line': line,
            'arrows': [arrow] if arrow else []
        }

    def _add_reverse_arrow(self, existing_from, existing_to):
        """Add reverse arrow to existing connection for bidirectional flow"""
        if (existing_from, existing_to) not in self.connections:
            return

        connection = self.connections[(existing_from, existing_to)]

        # Calculate reverse direction points
        to_pos, from_pos = self._calculate_border_points(existing_from, existing_to)

        # Create arrow for reverse direction
        reverse_arrow = self._create_arrow(from_pos, to_pos)
        if reverse_arrow:
            self.scene.addItem(reverse_arrow)
            connection['arrows'].append(reverse_arrow)

    def _calculate_border_points(self, id_from, id_to):
        """Calculate connection points at the borders of rectangles"""
        from_participant = self.participants[id_from]
        to_participant = self.participants[id_to]

        # Get rectangle centers
        from_center = QPointF(
            from_participant['position'].x() + self.pc_size / 2,
            from_participant['position'].y() + self.pc_size / 2
        )
        to_center = QPointF(
            to_participant['position'].x() + self.pc_size / 2,
            to_participant['position'].y() + self.pc_size / 2
        )

        # Calculate direction vector
        dx = to_center.x() - from_center.x()
        dy = to_center.y() - from_center.y()
        length = math.sqrt(dx*dx + dy*dy)

        if length == 0:
            return from_center, to_center

        # Normalize direction
        dx /= length
        dy /= length

        # Calculate border points
        half_size = self.pc_size / 2
        from_border = QPointF(
            from_center.x() + dx * half_size,
            from_center.y() + dy * half_size
        )
        to_border = QPointF(
            to_center.x() - dx * half_size,
            to_center.y() - dy * half_size
        )

        return from_border, to_border

    def _create_arrow(self, from_pos, to_pos):
        """Create an arrow polygon pointing from from_pos to to_pos"""
        # Calculate arrow direction
        dx = to_pos.x() - from_pos.x()
        dy = to_pos.y() - from_pos.y()
        length = math.sqrt(dx*dx + dy*dy)

        if length == 0:
            return None

        # Normalize direction
        dx /= length
        dy /= length

        # Arrow dimensions
        arrow_length = 15
        arrow_width = 8

        # Calculate arrow position (at the end of the line)
        arrow_tip = to_pos
        arrow_base = QPointF(
            to_pos.x() - dx * arrow_length,
            to_pos.y() - dy * arrow_length
        )

        # Create arrow polygon with 50% transparency
        arrow_points = [
            arrow_tip,
            QPointF(arrow_base.x() - dy * arrow_width, arrow_base.y() + dx * arrow_width),
            QPointF(arrow_base.x() + dy * arrow_width, arrow_base.y() - dx * arrow_width)
        ]

        arrow_polygon = QPolygonF(arrow_points)
        arrow_color = QColor(50, 50, 50, 128)  # 128 = 50% transparency
        arrow_item = self.scene.addPolygon(arrow_polygon,
                                          QPen(arrow_color, 1),
                                          QBrush(arrow_color))

        return arrow_item

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

    def clear_canvas(self):
        """Clear all participants and connections from the canvas"""
        # Remove all participant graphics from scene
        for participant in self.participants.values():
            self.scene.removeItem(participant['pc_item'])
            self.scene.removeItem(participant['name_text'])
            self.scene.removeItem(participant['id_text'])

        # Remove all connection graphics from scene
        for connection in self.connections.values():
            self.scene.removeItem(connection['line'])
            for arrow in connection['arrows']:
                self.scene.removeItem(arrow)

        # Clear data structures
        self.participants.clear()
        self.connections.clear()

        # Reset NetworkX graph
        self.graph.clear()
