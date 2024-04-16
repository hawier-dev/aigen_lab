from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt, QRect, QPoint, Signal, QSize
from PySide6.QtGui import QPainter, QPen, QColor, QMouseEvent

from constants import (
    primary_color,
    surface_color,
    surface3_color,
    on_primary_color,
    primary_variant_color,
)
from utils.animations import OpacityAnimation


class Slider(QWidget):
    valueChanged = Signal(int)

    def __init__(self, parent=None):
        super(Slider, self).__init__(parent)
        self.minimum = 1
        self.maximum = 200
        self.value = 50
        self.handle_radius = 10
        self.margin = 2
        self.pressed = False
        self.handle_position = 0
        self.setFixedHeight(20)

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor(surface3_color))
        painter.setPen(pen)
        painter.setBrush(QColor(surface_color))

        # Draw the slider track
        track_height = 4
        track_rect = QRect(
            self.handle_radius + self.margin,
            (self.height() - track_height) // 2,
            self.width() - 2 * (self.handle_radius + self.margin),
            track_height,
        )
        painter.drawRect(track_rect)

        # Draw the handle
        self.handle_position = (
            self.margin
            + self.handle_radius
            + (self.value - self.minimum)
            / (self.maximum - self.minimum)
            * (self.width() - 2 * (self.handle_radius + self.margin))
        )
        handle_rect = QRect(
            self.handle_position - self.handle_radius,
            (self.height() - 2 * self.handle_radius) // 2,
            2 * self.handle_radius,
            2 * self.handle_radius,
        )
        painter.setBrush(QColor(primary_color))
        painter.drawEllipse(handle_rect)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.pressed = True
            self.updateValue(event.x())

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.pressed:
            self.updateValue(event.x())

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.pressed = False

    def updateValue(self, x):
        track_rect = self.rect().adjusted(
            self.handle_radius + self.margin, 0, -(self.handle_radius + self.margin), 0
        )
        value = (x - track_rect.left()) / track_rect.width() * (
            self.maximum - self.minimum
        ) + self.minimum
        self.setValue(value)

    def setValue(self, value):
        value = int(min(max(value, self.minimum), self.maximum))
        if value != self.value:
            self.value = value
            self.valueChanged.emit(self.value)
            self.update()

    def setRange(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum
        self.update()

    def sizeHint(self):
        return QSize(200, 40)
