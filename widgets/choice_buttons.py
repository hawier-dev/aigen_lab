from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal
from constants import *


class ChoiceButtons(QWidget):
    selection_changed = Signal(str)

    def __init__(self, button_labels):
        super().__init__()
        self.setStyleSheet(
            f"""
            QPushButton{{
                background-color: {surface_color};
                color: {on_surface_color};
                border: 1px solid {surface2_color};
                border-radius: 0px;
                padding: 10px;
            }}
            QPushButton:hover{{
                background-color: {surface2_color};
            }}
            QPushButton:checked{{
                background-color: {primary_color};
                color: {on_primary_color};
                font-weight: bold;
            }}
            """
        )

        self.layout = QVBoxLayout()
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.buttons = []
        self.selected_button = None

        for label in button_labels:
            button = QPushButton(label)
            button.setCheckable(True)
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(self.handle_button_click)
            self.buttons.append(button)
            self.layout.addWidget(button)

        self.buttons[0].click()
        self.setLayout(self.layout)

    def handle_button_click(self):
        clicked_button = self.sender()
        if self.selected_button is not None:
            self.selected_button.setChecked(False)
        clicked_button.setChecked(True)
        self.selected_button = clicked_button
        self.selection_changed.emit(clicked_button.text())

    def get_selected(self):
        return self.selected_button.text()
