from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QHBoxLayout,
)

from constants import SETTINGS_STYLES


class SettingsTab(QWidget):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.setStyleSheet(SETTINGS_STYLES)
        self.settings = settings

        self.layout = QVBoxLayout(self)

        self.download_location_label = QLabel("Download Location for Models:")
        self.layout.addWidget(self.download_location_label)

        self.download_location_layout = QHBoxLayout()
        self.download_location_edit = QLineEdit()
        self.download_location_edit.setText(self.settings.get_download_location())
        self.download_location_edit.setReadOnly(True)
        self.browse_button = QPushButton("Browse...")
        self.download_location_layout.addWidget(self.download_location_edit)
        self.download_location_layout.addWidget(self.browse_button)
        self.layout.addLayout(self.download_location_layout)

        self.save_location_label = QLabel("Save Location for Photos:")
        self.layout.addWidget(self.save_location_label)

        self.save_location_layout = QHBoxLayout()
        self.save_location_edit = QLineEdit()
        self.save_location_edit.setText(self.settings.get_save_location())
        self.save_location_edit.setReadOnly(True)
        self.save_browse_button = QPushButton("Browse...")
        self.save_location_layout.addWidget(self.save_location_edit)
        self.save_location_layout.addWidget(self.save_browse_button)
        self.layout.addLayout(self.save_location_layout)

        self.layout.addStretch()

        self.browse_button.clicked.connect(self.open_folder_dialog)
        self.save_browse_button.clicked.connect(self.open_save_folder_dialog)
        self.setLayout(self.layout)

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, "Select Download Folder for Models"
        )
        if folder_path:
            self.download_location_edit.setText(folder_path)
            self.settings.set_download_location(folder_path)

    def open_save_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, "Select Save Folder for Photos"
        )
        if folder_path:
            self.save_location_edit.setText(folder_path)
            self.settings.set_save_location(folder_path)
