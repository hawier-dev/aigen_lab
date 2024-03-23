from PySide6.QtWidgets import (
    QPushButton,
    QDialog,
    QVBoxLayout,
    QListWidget,
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

        self.clicked.connect(self.open_model_selector_dialog)

    def open_model_selector_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select a Model")
        layout = QVBoxLayout(dialog)

        list_widget = QListWidget()
        for model in self.models:
            list_widget.addItem(model)
        layout.addWidget(list_widget)

        list_widget.itemDoubleClicked.connect(
            lambda: self.model_selected(dialog, list_widget)
        )

        dialog.exec_()

    def model_selected(self, dialog, list_widget):
        self.select_model(list_widget.currentItem().text())
        dialog.accept()

    def select_model(self, model):
        self.selected_model = model
        self.setText(self.selected_model.split("/")[-1])
        self.model_changed.emit(self.selected_model)
