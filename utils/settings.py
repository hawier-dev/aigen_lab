import os.path
from os.path import abspath

from PySide6.QtCore import QSettings, QObject, Signal, QStandardPaths


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
