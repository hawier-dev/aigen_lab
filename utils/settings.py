import os.path
from os.path import abspath

from PySide6.QtCore import QSettings, QObject, Signal, QStandardPaths

from utils.functions import get_available_devices


class Settings(QObject):
    settings_changed = Signal()

    def __init__(self, organization, application, parent=None):
        super().__init__(parent)
        self.settings = QSettings(organization, application)

    def get_download_location(self):
        return self.settings.value("download_location", "")

    def get_save_location(self):
        return self.settings.value("save_location", "")

    def set_download_location(self, path):
        self.settings.setValue("download_location", path)
        self.settings_changed.emit()

    def set_save_location(self, path):
        self.settings.setValue("save_location", path)
        self.settings_changed.emit()

    def set_default_values(self):
        documents_path = QStandardPaths.writableLocation(
            QStandardPaths.DocumentsLocation
        )
        self.set_download_location(
            abspath(os.path.join(documents_path, "aigenlab", "models"))
        )
        self.set_save_location(
            abspath(os.path.join(documents_path, "aigenlab", "images"))
        )

    def get_device(self):
        return self.settings.value("device", get_available_devices()[0])

    def set_device(self, device):
        self.settings.setValue("device", device)
        self.settings_changed.emit()

    def get_prediction_settings(self):
        return (
            self.settings.value("width", 512),
            self.settings.value("height", 512),
            self.settings.value("steps", 60),
            self.settings.value("guidance_scale", 7.5),
        )

    def set_prediction_settings(self, width, height, steps, guidance_scale):
        self.settings.setValue("width", width)
        self.settings.setValue("height", height)
        self.settings.setValue("steps", steps)
        self.settings.setValue("guidance_scale", guidance_scale)

        self.settings_changed.emit()
