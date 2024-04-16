from functools import partial

from PySide6.QtGui import QAction, QFontMetrics
from PySide6.QtWidgets import (
    QPushButton,
    QMenu,
    QApplication,
)
from PySide6.QtCore import Signal, Qt

from constants import surface_color, on_surface_color, surface2_color, surface3_color
from utils.functions import truncate_model_id


class OptionSelector(QPushButton):
    option_changed = Signal(str)

    def __init__(self, text, options=None, mode="normal", parent=None):
        super().__init__(text, parent)
        self.selected_option = None
        self.options = options
        self.mode = mode
        self.setFixedHeight(35)
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {surface_color};
                color: {on_surface_color};
                border: 1px solid {surface2_color};
                border-radius: 0px;
                padding: 0px 10px;
                font-size: 13px;
                text-align: left;
            }}
            QPushButton::hover {{
                background-color: {surface2_color};
            }}
            QPushButton::pressed {{
                background-color: {surface3_color};
            }}
            """
        )

        self.setCursor(Qt.PointingHandCursor)
        self.clicked.connect(self.show_selector)

    def show_selector(self):
        if self.options:
            menu = QMenu(self)
            for option in self.options:
                action = QAction(option, self)
                action.triggered.connect(partial(self.select_option, option))
                menu.addAction(action)
            menu.exec_(self.mapToGlobal(self.rect().bottomLeft()))

    def truncate_text(self, text):
        if len(text) > 26:
            text = text[:26] + "..."

        return text

    def select_option(self, option):
        self.selected_option = option
        if self.mode == "model":
            option = truncate_model_id(option)
        option = self.truncate_text(option)
        self.setText(option)
        self.option_changed.emit(self.selected_option)

    def set_options(self, options):
        self.options = options
