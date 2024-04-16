import json
import os
import shutil
import webbrowser

from PySide6.QtCore import Qt, QSize, QPoint
from PySide6.QtGui import QPixmap, QAction, QIcon
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QProgressBar,
    QHBoxLayout,
    QPushButton,
    QMenu,
)

from constants import (
    LOCAL_MODEL_STYLES,
    primary_color,
)
from utils.file_downloader import FileDownloader


class LocalModel(QWidget):
    def __init__(
        self,
        model_id,
        model_path,
        branch,
        model_type,
        total_size=None,
        library=None,
        downloaded=False,
        parent=None,
    ):
        super().__init__(parent)
        self.library = library
        self.total_size = total_size
        self.modelId = model_id
        self.model_path = model_path
        self.branch = branch
        self.downloaded = downloaded
        self.model_type = model_type
        self.downloading = False
        self.setFixedHeight(80)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(LOCAL_MODEL_STYLES)

        self.layout = QVBoxLayout(self)

        self.top_layout = QHBoxLayout()

        self.user_logo_label = QLabel()
        self.user_logo_label.setFixedSize(18, 18)
        self.user_logo_label.setPixmap(QPixmap("assets/model.png"))

        model_label_layout = QVBoxLayout()
        model_label_layout.setSpacing(1)
        self.model_label = QLabel(self.modelId)
        self.model_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.model_type_label = QLabel(self.model_type)
        self.model_type_label.setStyleSheet("font-size: 12px; color: #ccc;")
        model_label_layout.addWidget(self.model_label)
        model_label_layout.addWidget(self.model_type_label)
        self.model_size_label = QLabel("")
        if total_size is not None:
            self.model_size_label.setText(self.total_size)
        self.model_size_label.setStyleSheet(
            "font-size: 12px; font-weight: bold; color: #ccc;"
        )

        self.manage_button = QPushButton()
        self.manage_button.setCursor(Qt.PointingHandCursor)
        self.manage_button.setFixedSize(18, 18)
        manage_icon = QIcon("assets/manage.png")
        self.manage_button.setIcon(manage_icon)
        self.manage_button.setIconSize(QSize(16, 16))
        self.manage_button.setStyleSheet("border: none;")
        self.manage_button.clicked.connect(self.show_manage_menu)

        self.download_button = QPushButton("   Download")
        self.download_button.setFixedSize(120, 36)
        self.download_button.setCursor(Qt.PointingHandCursor)
        self.download_button.setIcon(QIcon(QPixmap("assets/download_icon.png")))
        self.download_button.setIconSize(QSize(14, 14))
        self.download_button.pressed.connect(self.start_download)

        self.cancel_button = QPushButton("")
        self.cancel_button.setFixedSize(36, 36)
        self.cancel_button.setCursor(Qt.PointingHandCursor)
        self.cancel_button.setIcon(QIcon(QPixmap("assets/cancel.png")))
        self.cancel_button.setIconSize(QSize(14, 14))
        self.cancel_button.pressed.connect(self.cancel_download)
        self.cancel_button.hide()

        self.top_layout.addWidget(self.user_logo_label)
        self.top_layout.addLayout(model_label_layout)
        # self.top_layout.addWidget(self.model_status)
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.model_size_label)
        self.top_layout.addWidget(self.cancel_button)
        if self.downloaded:
            self.top_layout.addWidget(self.manage_button)
        else:
            self.model_size_label.setText("")
            self.top_layout.addWidget(self.download_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setFixedHeight(20)
        self.progress_bar.hide()

        self.layout.addStretch()
        self.layout.addLayout(self.top_layout)
        self.layout.addSpacing(5)
        self.layout.addWidget(self.progress_bar)
        self.layout.addStretch()

    def show_manage_menu(self):
        manage_menu = QMenu()

        open_location_action = QAction("Open location", self)
        open_location_action.triggered.connect(self.open_location)
        manage_menu.addAction(open_location_action)

        if self.downloading:
            cancel_download_action = QAction("Cancel download", self)
            cancel_download_action.triggered.connect(self.cancel_download)
            manage_menu.addAction(cancel_download_action)
        elif self.downloading == False and self.downloaded == True:
            remove_model_action = QAction("Remove model", self)
            remove_model_action.triggered.connect(self.remove_model)
            manage_menu.addAction(remove_model_action)

        manage_menu.exec_(
            self.manage_button.mapToGlobal(QPoint(0, self.manage_button.height()))
        )

    def open_location(self):
        try:
            webbrowser.open(self.model_path)
        except Exception as e:
            print(f"Error opening model location: {e}")

    def remove_model(self):
        self.library.remove_model(self)

    def cancel_download(self):
        self.downloader.cancel_download()

    def download_cancelled(self):
        self.model_size_label.setText("Cleaning up...")
        try:
            shutil.rmtree(self.model_path)
        except Exception as e:
            print(f"Error cleaning up model: {e}")
        self.set_downloading(False)

    def set_downloading(self, downloading):
        self.downloading = downloading
        if self.downloading:
            self.progress_bar.show()
            self.cancel_button.show()
            self.download_button.hide()
            self.model_size_label.setText("Waiting...")
        else:
            self.progress_bar.hide()
            self.cancel_button.hide()
            if self.downloaded:
                self.model_size_label.setText(self.total_size)
            else:
                self.download_button.show()
                self.model_size_label.setText("")

    def update_progress(self, model_id, value_str, maximum_str, value):
        self.model_size_label.setText(f"{value_str} / {maximum_str}")
        self.progress_bar.setValue(value)
        self.total_size = maximum_str

    def start_download(self):
        self.set_downloading(True)
        self.downloader = FileDownloader(
            self.modelId,
            self.branch,
            self.model_path,
        )
        self.downloader.download_complete.connect(self.download_finished)
        self.downloader.progress_updated.connect(self.update_progress)
        self.downloader.download_cancelled.connect(self.download_cancelled)
        self.downloader.start()

    def download_finished(self, model_id):
        self.downloaded = True
        self.set_downloading(False)
        model_info_path = os.path.join(self.model_path, "info.json")
        model_info_data = {
            "downloaded": True,
            "size": self.total_size,
            "name": self.modelId,
            "branch": self.branch,
            "model_type": self.model_type,
        }
        with open(model_info_path, "w") as json_file:
            json.dump(model_info_data, json_file, indent=4)
