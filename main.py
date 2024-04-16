import sys
import locale

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase, QPalette, QColor, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow

from constants import *
from screens.main_screen import MainScreen


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        locale.setlocale(locale.LC_ALL, "")

        self.setWindowTitle("AIGen Lab")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = MainScreen()
        self.setCentralWidget(self.tabs)


def load_custom_fonts():
    font_paths = {
        "bold": "fonts/Inter-Bold.ttf",
        "light": "fonts/Inter-Light.ttf",
        "medium": "fonts/Inter-Medium.ttf",
        "regular": "fonts/Inter-Regular.ttf",
        "semibold": "fonts/Inter-SemiBold.ttf",
    }

    for weight, path in font_paths.items():
        QFontDatabase.addApplicationFont(path)


def setup_palette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(*hex_to_rgb(background_color)))
    palette.setColor(QPalette.WindowText, QColor(*hex_to_rgb(on_background_color)))
    palette.setColor(QPalette.Base, QColor(*hex_to_rgb(surface_color)))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(*hex_to_rgb(primary_color)))
    palette.setColor(QPalette.HighlightedText, Qt.black)

    return palette


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/logo.png"))
    app.setPalette(setup_palette())
    load_custom_fonts()
    app.setStyleSheet(STYLESHEETS)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
