from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from constants import surface_color, surface2_color, on_surface_color, primary_color
from widgets.title_label import TitleLabel
from widgets.tools_list_widget import ToolsListWidget


class RightEditTab(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(
            f"""
            QPushButton{{
                background-color: {surface_color};
                border: 1px solid {surface2_color};
                border-radius: 0px;
                font-weight: 500;
                padding: 10px;
                color: {on_surface_color};
            }}
            QPushButton:hover{{
                background-color: {surface2_color};
            }}
            QPushButton:pressed{{
                background-color: {surface2_color};
            }}
            QPushButton:checked{{
                background-color: {primary_color};
                font-weight: 600;
            }}
            QLabel{{
                background-color: none;
            }}
            ToolButton{{
                background-color: none;
            }}
            """
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addSpacing(10)

        layout.addWidget(TitleLabel("Image Manipulation:"))

        self.resize_button = QPushButton("Resize Image")
        self.resize_button.clicked.connect(self.resize_image)
        layout.addWidget(self.resize_button)

        self.remove_background_button = QPushButton("Remove Background")
        self.remove_background_button.clicked.connect(self.remove_background)
        layout.addWidget(self.remove_background_button)

        layout.addWidget(TitleLabel("Tools:"))

        self.tools_toolbar = ToolsListWidget()
        self.tools_toolbar.setContentsMargins(0, 0, 0, 0)
        self.tools_toolbar.setSpacing(5)

        self.tools_toolbar.add_tool("assets/remove.png", "Remove Objects", spacing=15)

        layout.addWidget(self.tools_toolbar)
        layout.addStretch()

        self.setLayout(layout)

    def resize_image(self):
        print("Zmiana rozmiaru zdjęcia...")

    def remove_background(self):
        print("Usuwanie tła...")

    def remove_objects(self):
        print("Usuwanie obiektów...")
