import json
import os
from os.path import dirname
from shutil import rmtree

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QScrollArea,
    QVBoxLayout,
    QFrame,
    QMessageBox,
)
from utils.file_downloader import FileDownloader
from widgets.local_model import LocalModel
from constants import AVAIABLE_MODELS, surface_color


class ModelsTab(QWidget):
    models_changed = Signal(list)

    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.setContentsMargins(5, 5, 5, 5)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"QWidget{{background: {surface_color};}}")

        self.download_queue = []
        self.settings = settings
        self.currently_downloading = False
        self.models = []

        self.layout = QVBoxLayout()

        self.models_layout = QVBoxLayout()
        self.models_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_frame = QFrame()
        self.scroll_area_frame.setLayout(self.models_layout)
        self.scroll_area.setWidget(self.scroll_area_frame)

        self.layout.addWidget(self.scroll_area)

        self.setLayout(self.layout)

    def initialize_models_from_folder(self):
        models_directory = self.settings.get_download_location()
        for item in os.listdir(models_directory):
            model_path = os.path.join(models_directory, item)
            if os.path.isdir(model_path):
                info_path = os.path.join(model_path, "info.json")
                if os.path.exists(info_path):
                    with open(info_path, "r") as json_file:
                        model_info_data = json.load(json_file)
                        model_info = LocalModel(
                            model_id=model_info_data.get("name", ""),
                            model_path=dirname(info_path),
                            branch=model_info_data.get("branch", "main"),
                            total_size=model_info_data.get("size", "0B"),
                            downloaded=model_info_data.get("downloaded", False),
                            library=self,
                        )
                        self.add_model(model_info, downloading=False)

        self.models_changed.emit(self.models)

    def initialize_models(self):
        current_models = [model.modelId for model in self.models]
        for model in AVAIABLE_MODELS:
            model_id = model.get("name", "")
            if model_id in current_models:
                continue

            model_info = LocalModel(
                model_id=model_id,
                model_path=os.path.join(
                    self.settings.get_download_location(),
                    model_id.split("/")[-1],
                ),
                branch=model.get("branch", "main"),
                total_size=model.get("size", "0B"),
                downloaded=False,
                library=self,
            )
            self.add_model(model_info, downloading=False)

    def add_model(self, local_model, downloading=False, branch="main"):
        local_model.set_downloading(downloading)
        self.models_layout.addWidget(local_model)
        self.models.append(local_model)

    def remove_model(self, local_model):
        reply = QMessageBox.question(
            self,
            "Remove Model",
            "Are you sure you want to remove this model?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            try:
                rmtree(local_model.model_path)
                local_model.setParent(None)
                self.models.remove(local_model)
                local_model.deleteLater()
                self.update_no_models_label_visibility()
            except Exception as e:
                print(f"Error removing model: {e}")

    def update_no_models_label_visibility(self):
        # if self.models:
        #     self.no_models_label.setVisible(False)
        # else:
        #     self.no_models_label.setVisible(True)
        pass

    def add_to_download_queue(self, model_info, branch):
        self.download_queue.append((model_info, branch))
        self.process_next_download()

    def process_next_download(self):
        if self.download_queue and not self.currently_downloading:
            next_model = self.download_queue.pop(0)
            self.start_download(next_model)
