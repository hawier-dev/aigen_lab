import os
import json
import os
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, Signal

from widgets.history_item import HistoryItem
from constants import surface_color


class HistoryTab(QWidget):
    item_clicked = Signal(str, list)

    def __init__(self):
        super().__init__()
        self.setContentsMargins(5, 5, 5, 5)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(
            f"QWidget{{background: {surface_color};}} QListWidget::item{{background: {surface_color};}}"
        )
        layout = QVBoxLayout()
        self.history_list = QListWidget()
        self.history_list.setVerticalScrollMode(QListWidget.ScrollPerPixel)
        self.history_list.verticalScrollBar().setSingleStep(15)
        layout.addWidget(self.history_list)
        self.setLayout(layout)

    def load_history_items(self, directory):
        self.history_list.clear()
        history_items = []

        for folder_name in os.listdir(directory):
            folder_path = os.path.join(directory, folder_name)
            if os.path.isdir(folder_path):
                settings_path = os.path.join(folder_path, "settings.json")
                try:
                    image_path = os.path.join(
                        folder_path,
                        [
                            file
                            for file in os.listdir(folder_path)
                            if file.endswith(".png")
                        ][0],
                    )
                except IndexError:
                    continue

                if os.path.exists(settings_path) and os.path.exists(image_path):
                    with open(settings_path, "r") as file:
                        settings = json.load(file)
                        prompt = settings.get("prompt", "Unknown prompt")
                        date = settings.get("date")
                        settings_filtered = [
                            ["Width", settings.get("width")],
                            ["Height", settings.get("height")],
                            ["Steps", settings.get("steps")],
                            ["Guidance Scale", settings.get("guidance_scale")],
                            ["Style", settings.get("style")],
                        ]
                        history_item_widget = HistoryItem(
                            prompt, settings_filtered, image_path, date
                        )
                        history_item_widget.clicked.connect(self.item_clicked)
                        history_items.append(history_item_widget)

        history_items.sort(key=lambda x: x.date, reverse=True)

        for history_item_widget in history_items:
            list_item = QListWidgetItem(self.history_list)
            list_item.setSizeHint(history_item_widget.sizeHint())
            self.history_list.addItem(list_item)
            self.history_list.setItemWidget(list_item, history_item_widget)
