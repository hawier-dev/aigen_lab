from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel

from constants import surface_color


class AppBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(f"QWidget{{background: {surface_color}; padding: 10px;}}")
        self.setFixedHeight(40)
        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.title_label = QLabel("AIGen Lab")
        self.content_layout.addWidget(self.title_label)

        self.setLayout(self.content_layout)
