from functools import partial

from PySide6.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QGraphicsEllipseItem,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor, QCursor, QImage

from utils.animations import OpacityAnimation


class ImageView(QGraphicsView):
    def __init__(self, parent=None):
        super(ImageView, self).__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setRubberBandSelectionMode(Qt.IntersectsItemShape)
        self.image_created = False
        self.edit_mode = False

        self.drawing = False
        self.drawing_layer = None
        self.drawing_pixmap_item = None
        self.brush_indicator = None
        self.last_point = None

        self.brush_size = 50
        self.pen = QPen(QColor("red"), self.brush_size)
        self.pen.setCapStyle(Qt.RoundCap)
        self.pen.setBrush(QColor("red"))
        self.mode = "add"

        self.setMouseTracking(True)
        self.image_item = None

    def change_tool(self, tool):
        self.mode = tool

    def resizeEvent(self, event):
        super(ImageView, self).resizeEvent(event)

    def display_image(self, image_path):
        pixmap = QPixmap(image_path)
        if self.image_item is not None:
            self.scene.removeItem(self.image_item)
        self.image_item = self.scene.addPixmap(pixmap)

        image_width = pixmap.width()
        image_height = pixmap.height()

        self.scene.setSceneRect(0, 0, image_width, image_height)

        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

        if self.edit_mode:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.image_created = True
        self.show()

        self.drawing_layer = QPixmap(image_width, image_height)
        self.drawing_layer.fill(Qt.transparent)
        self.drawing_pixmap_item = QGraphicsPixmapItem(self.drawing_layer)
        self.drawing_pixmap_item.setZValue(10)
        self.drawing_pixmap_item.setOpacity(0.6)
        self.scene.addItem(self.drawing_pixmap_item)

        self.brush_indicator = QGraphicsEllipseItem(
            0, 0, self.brush_size, self.brush_size
        )
        self.brush_indicator.setPen(QPen(QColor("black"), 1))
        self.brush_indicator.setZValue(15)
        self.scene.addItem(self.brush_indicator)

        if not self.edit_mode:
            self.brush_indicator.setVisible(False)

        self.last_point = None
        self.drawing = False
        self.show()

    def set_placeholder_background(self):
        self.image_created = False
        self.setDragMode(QGraphicsView.NoDrag)
        placeholder_html = f"""
        <html>
            <body>
                <p style="text-align: center; font-size: 18px; font-family: inter;">To generate an image, enter a prompt and click 
                <span style='color: #4251f5; font-weight: bold;'>Generate</span>.</p>
            </body>
        </html>
        """
        if self.image_item is not None:
            self.scene.removeItem(self.image_item)
            self.image_item = None
        self.scene.clear()

        text_item = self.scene.addText("")
        text_item.setPos(10, 10)
        text_item.setTextWidth(260)
        text_item.document().setHtml(placeholder_html)

    def save_mask(self):
        if not self.drawing_layer:
            return

        mask = QImage(self.drawing_layer.size(), QImage.Format_ARGB32)
        mask.fill(Qt.black)

        for x in range(self.drawing_layer.width()):
            for y in range(self.drawing_layer.height()):
                if self.drawing_layer.pixelColor(x, y).alpha() > 0:
                    mask.setPixelColor(x, y, QColor(Qt.white))

        mask.save(f"c:/Users/mbady/Desktop/mask.png")

    def mousePressEvent(self, event):
        if self.image_created and event.button() == Qt.LeftButton and self.edit_mode:
            self.drawing = True
            self.last_point = self.mapToScene(event.pos())
            event.accept()

    def mouseMoveEvent(self, event):
        if self.image_created and self.drawing and self.last_point is not None:
            painter = QPainter(self.drawing_layer)
            painter.setPen(self.pen)

            if self.mode == "remove":
                painter.setCompositionMode(QPainter.CompositionMode_Clear)

            current_point = self.mapToScene(event.pos())
            painter.drawLine(self.last_point, current_point)
            painter.end()

            self.drawing_pixmap_item.setPixmap(self.drawing_layer)
            self.last_point = current_point
            event.accept()

        if self.brush_indicator is not None:
            scenePos = self.mapToScene(event.pos())
            self.brush_indicator.setPos(
                scenePos.x() - self.brush_size / 2, scenePos.y() - self.brush_size / 2
            )
            self.brush_indicator.show()

        super(ImageView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.image_created and event.button() == Qt.LeftButton:
            self.drawing = False
            self.last_point = None
            event.accept()

    def set_brush_size(self, size):
        self.brush_size = size
        self.pen.setWidth(size)
        self.brush_indicator.setRect(0, 0, size, size)

    def set_edit_mode(self, mode):
        self.edit_mode = mode
        if mode:
            self.setDragMode(QGraphicsView.NoDrag)

        else:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.setCursor(Qt.ArrowCursor)

            if self.drawing_layer is not None:
                self.drawing_layer.fill(Qt.transparent)
                self.drawing_pixmap_item.setPixmap(self.drawing_layer)


    def wheelEvent(self, event):
        if self.image_created:
            factor = 1.1
            if event.angleDelta().y() > 0:
                scale_factor = factor
            else:
                scale_factor = 1.0 / factor
            self.scale(scale_factor, scale_factor)
