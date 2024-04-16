from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel

from constants import surface_color


class AppBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"QWidget{{background: {surface_color}; padding: 0px;}}")
        self.setFixedHeight(40)
        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap("assets/logo24.png"))
        self.title_label = QLabel("AIGen Lab")
        self.title_label.setStyleSheet("font-weight: bold;")
        self.content_layout.addSpacing(15)
        self.content_layout.addWidget(self.logo_label)
        self.content_layout.addStretch()

        self.setLayout(self.content_layout)
