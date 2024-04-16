from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import QPropertyAnimation, QRect, Qt, QTimer, Signal
from PySide6.QtGui import QFont

from constants import *


class Snackbar(QWidget):
    link_clicked = Signal()

    def __init__(self, message, parent=None, duration=3000):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.text = QLabel(message, self)
        self.text.setFont(QFont("Inter", 10))
        self.text.setOpenExternalLinks(False)
        self.text.linkActivated.connect(self.on_link_clicked)
        self.text.setStyleSheet(
            "QLabel{"
            f"color: {on_surface_color}; "
            f"background-color: {surface3_color}; "
            f"padding: 10px; "
            f"border 1px solid {surface4_color}; "
            "border-radius: 5px;"
            "}"
        )
        self.animation = QPropertyAnimation(self, b"geometry")
        layout = QVBoxLayout()
        layout.addWidget(self.text)
        self.setLayout(layout)
        self.adjustSize()

        # Timer to auto-hide the snackbar
        self.timer = QTimer(self)
        self.timer.setInterval(duration)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hideAnimation)
        self.timer.start()

    def showEvent(self, event):
        screen_width = self.parent().width()
        screen_height = self.parent().height()
        widget_width = self.width()
        widget_height = self.height()
        x_position = int((screen_width - widget_width) / 2)
        y_position_start = screen_height
        y_position_end = screen_height - widget_height - 20

        self.setGeometry(x_position, -widget_height, widget_width, widget_height)
        self.animation.setDuration(500)
        self.animation.setStartValue(
            QRect(x_position, y_position_start, widget_width, widget_height)
        )
        self.animation.setEndValue(
            QRect(x_position, y_position_end, widget_width, widget_height)
        )
        self.animation.start()

    def hideAnimation(self):
        screen_height = self.parent().height()
        widget_height = self.height()
        y_position_end = screen_height - widget_height - 20

        self.animation.setDuration(500)
        self.animation.setStartValue(
            QRect(self.x(), y_position_end, self.width(), widget_height)
        )
        self.animation.setEndValue(
            QRect(self.x(), screen_height, self.width(), widget_height)
        )
        self.animation.finished.connect(self.hide)
        self.animation.start()

    def on_link_clicked(self):
        self.link_clicked.emit()
