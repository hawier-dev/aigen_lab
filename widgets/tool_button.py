import os.path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QSizePolicy, QHBoxLayout, QFrame


class ToolButton(QFrame):
    selected = Signal()

    def __init__(self, icon, text, spacing=5, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setContentsMargins(0, 0, 0, 0)

        self.setStyleSheet(
            "ToolButton{background-color: transparent; border: none; padding: 10px;}"
        )
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.icon_path = icon
        self.gray_icon_path = os.path.splitext(icon)[0] + "_gray.png"

        self.icon_label = QLabel()
        self.icon_label.setPixmap(QPixmap(self.icon_path))

        self.text_label = QLabel(text)
        self.text_label.setStyleSheet(
            "QLabel{font-size: 13px; font-weight: 500; color: #ccc;}"
        )

        layout.addWidget(self.icon_label)
        layout.addSpacing(spacing)
        layout.addWidget(self.text_label)
        layout.addStretch()

        size_policy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.setSizePolicy(size_policy)

    def set_selected(self):
        self.icon_label.setPixmap(QPixmap(self.icon_path))
        self.text_label.setStyleSheet(
            f"QLabel{{font-size: 13px; font-weight: 500; color: #fff; font-weight: bold;}}"
        )

    def set_unselected(self):
        self.icon_label.setPixmap(QPixmap(self.gray_icon_path))
        self.text_label.setStyleSheet(
            f"QLabel{{font-size: 13px; font-weight: 500; color: #ccc;}}"
        )
