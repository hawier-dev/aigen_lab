from PySide6.QtWidgets import QLabel


class TitleLabel(QLabel):
    def __init__(self, title: str):
        super().__init__(title)
        self.setStyleSheet("font-size: 13px; font-weight: bold;")
        self.setFixedHeight(30)
