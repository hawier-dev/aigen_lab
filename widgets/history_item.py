import os
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QCursor
from PySide6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QFrame,
)

from constants import surface2_color, surface3_color, surface4_color, surface_color


class HistoryItem(QFrame):
    clicked = Signal(str, list)

    def __init__(self, prompt_name, settings, image_path, date, parent=None):
        super().__init__(parent)
        self.prompt_name = prompt_name
        self.settings = settings
        self.image_path = image_path
        self.date = date

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.styles = f"""
            QFrame {{
                border-bottom: 1px solid {surface2_color};
                background-color: {surface_color};
            }}
            QLabel {{
                border: none;
            }}
            QFrame:hover {{
                background-color: {surface4_color};
            }}
        """
        self.setStyleSheet(self.styles)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        # Prompt name
        self.top_layout = QHBoxLayout()
        self.prompt_label = QLabel(self.prompt_name)
        self.prompt_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.date_label = QLabel(self.date)
        self.date_label.setStyleSheet("font-size: 12px; color: #777;")
        self.top_layout.addWidget(self.prompt_label)
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.date_label)

        self.settings_layout = QHBoxLayout()
        for setting in self.settings:
            setting_widget = QLabel(f"{setting[0]}: {setting[1]}")
            setting_widget.setStyleSheet(
                f"padding: 2px; border: 1px solid {surface3_color}; font-size: 12px;"
            )
            self.settings_layout.addWidget(setting_widget)

        self.settings_layout.addStretch()

        self.layout.addLayout(self.top_layout)
        self.layout.addLayout(self.settings_layout)

        # Image
        self.image_label = QLabel()
        if os.path.exists(self.image_path):
            pixmap = QPixmap(self.image_path).scaled(100, 100, Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)
            self.image_label.setFixedSize(100, 100)
        else:
            self.image_label.setText("Image not found")
            self.image_label.setStyleSheet(f"font-size: 12px; color: {surface2_color};")

        self.layout.addWidget(self.image_label)

        self.setLayout(self.layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.image_path, self.settings)
            event.accept()
        else:
            event.ignore()

    def enterEvent(self, event):
        self.setStyleSheet(
            f"""
            QFrame {{
                border-bottom: 1px solid {surface2_color};
                background-color: {surface2_color};
            }}
            QLabel {{
                border: none;
            }}
        """
        )

    def leaveEvent(self, event):
        self.setStyleSheet(self.styles)
