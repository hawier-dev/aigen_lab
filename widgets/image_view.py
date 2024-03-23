from PySide6.QtCore import Qt, QEvent, QPoint
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QMessageBox
from PySide6.QtGui import QPixmap, QPainter, QMouseEvent
from PySide6.QtGui import QBrush, QColor

from constants import *


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

        self.setMouseTracking(True)
        self.image_item = None

    def display_image(self, image_path):
        pixmap = QPixmap(image_path)
        if self.image_item is not None:
            self.scene.removeItem(self.image_item)
        self.image_item = self.scene.addPixmap(pixmap)
        self.fitInView(self.image_item, Qt.KeepAspectRatio)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.image_created = True
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

    def wheelEvent(self, event):
        if self.image_created:
            factor = 1.2
            if event.angleDelta().y() > 0:
                scaleFactor = factor
            else:
                scaleFactor = 1.0 / factor
            self.scale(scaleFactor, scaleFactor)
