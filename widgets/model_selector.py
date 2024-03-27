from functools import partial

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QPushButton,
    QMenu,
    QApplication,
)
from PySide6.QtCore import Signal

from constants import surface_color, on_surface_color, surface2_color, surface3_color


class ModelSelector(QPushButton):
    model_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__("Select Model", parent)
        self.models = []
        self.selected_model = None
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {surface_color};
                color: {on_surface_color};
                border: 1px solid {surface2_color};
                border-radius: 0px;
                padding: 10px;
                font-size: 13px;
            }}
            QPushButton::hover {{
                background-color: {surface2_color};
            }}
            QPushButton::pressed {{
                background-color: {surface3_color};
            }}
            """
        )

        self.clicked.connect(self.show_model_selector_menu)

    def show_model_selector_menu(self):
        menu = QMenu(self)
        for model in self.models:
            action = QAction(model, self)
            action.triggered.connect(partial(self.select_model, model))
            menu.addAction(action)
        menu.exec_(self.mapToGlobal(self.rect().bottomLeft()))

    def select_model(self, model):
        self.selected_model = model
        self.setText(self.selected_model.split("/")[-1])
        self.model_changed.emit(self.selected_model)
