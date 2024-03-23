import json
import os
import webbrowser
from shutil import rmtree

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
    surface_color,
    surface2_color,
    surface3_color,
)
from utils.file_downloader import FileDownloader


class LocalModel(QWidget):
    def __init__(
        self,
        model_id,
        model_path,
        branch,
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
        self.downloading = False
        self.setFixedHeight(80)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(LOCAL_MODEL_STYLES)

        self.layout = QVBoxLayout(self)

        self.top_layout = QHBoxLayout()

        self.user_logo_label = QLabel()
        self.user_logo_label.setFixedSize(18, 18)
        self.user_logo_label.setPixmap(QPixmap("assets/model.png").scaled(18, 18))

        self.model_label = QLabel(self.modelId)
        self.model_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.model_status = QLabel(self.branch)
        self.model_status.setStyleSheet(
            f"font-size: 11px; "
            f"font-weight: bold; "
            f"color: #fff; "
            f"background-color: {primary_color};"
            "border-radius: 5px; "
            "padding: 2px;"
        )
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
        self.download_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {surface_color};
                color: #fff;
                font-size: 12px;
                font-weight: bold;
                border: 1px solid {surface2_color};
                padding: 5px 10px;
            }}
            QPushButton:hover {{
                background-color: {surface2_color};
            }}
            QPushButton:pressed {{
                background-color: {surface3_color};
            }}
        """
        )
        self.download_button.setFixedSize(120, 36)
        self.download_button.setIcon(QIcon(QPixmap("assets/download_icon.png")))
        self.download_button.setIconSize(QSize(14, 14))
        self.download_button.pressed.connect(self.start_download)

        self.top_layout.addWidget(self.user_logo_label)
        self.top_layout.addWidget(self.model_label)
        # self.top_layout.addWidget(self.model_status)
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.model_size_label)
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
        pass

    def set_downloading(self, downloading):
        self.downloading = downloading
        if self.downloading:
            self.progress_bar.show()
            self.model_size_label.setText("Waiting...")
        else:
            self.progress_bar.hide()
            if self.downloaded:
                self.model_size_label.setText(self.total_size)

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
        self.downloader.start()

    def download_finished(self, model_id):
        self.set_downloading(False)
        self.set_downloaded(True)
        model_info_path = os.path.join(self.model_path, "info.json")
        model_info_data = {
            "downloaded": True,
            "size": self.total_size,
            "name": self.modelId,
            "branch": self.branch,
        }
        with open(model_info_path, "w") as json_file:
            json.dump(model_info_data, json_file, indent=4)
