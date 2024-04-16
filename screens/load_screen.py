from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class LoadingScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Ładowanie")
        self.main_window = main_window

        layout = QVBoxLayout()

        self.logo_label = QLabel(self)
        self.logo_pixmap = QPixmap("mggpaero.jpg")
        self.logo_label.setPixmap(self.logo_pixmap.scaled(300, 300, Qt.KeepAspectRatio))

        self.text_label = QLabel("Ładowanie...")
        self.text_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.text_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.logo_label, 0, Qt.AlignHCenter)
        layout.addWidget(self.text_label)

        self.setLayout(layout)

    def set_label(self, text):
        self.text_label.setText(text)
