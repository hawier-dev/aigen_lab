from functools import partial

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
    QListWidget,
    QListWidgetItem,
    QStatusBar,
    QLabel,
)

from constants import LINK_STYLE, waiting_color, correct_color
from screens.tabs.generate_tab import GenerateTab
from screens.tabs.history_tab import HistoryTab
from screens.tabs.models_tab import ModelsTab
from screens.tabs.settings_tab import SettingsTab
from utils.settings import Settings
from widgets.app_bar import AppBar
from widgets.snack_bar import Snackbar
from widgets.tool_button import ToolButton
from widgets.tools_list_widget import ToolsListWidget


class MainScreen(QWidget):
    def __init__(self, parent=None):
        super(MainScreen, self).__init__(parent)
        self.tabs_items = []
        self.settings = Settings("dev.hawier", "AIGen Lab")
        self.settings.set_default_values()

        self.tasks = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.app_bar = AppBar()

        content_layout = QHBoxLayout()

        self.tab_list_view = ToolsListWidget()
        self.tab_list_view.setStyleSheet("ToolsListWidget{padding:10px;}")
        self.tab_list_view.setSpacing(5)
        self.tab_list_view.setFixedWidth(160)
        self.tab_list_view.tool_changed.connect(self.change_tab)

        self.tab_list_view.add_tool("assets/generate.png", "Create")
        self.tab_list_view.add_tool("assets/model.png", "Library")
        self.tab_list_view.add_tool("assets/history.png", "History")
        self.tab_list_view.add_tool("assets/settings.png", "Settings")

        self.generate_tab = GenerateTab(self.settings)
        self.generate_tab.generated_image.connect(self.load_history)
        self.models_tab = ModelsTab(self.settings)
        self.models_tab.models_changed.connect(self.generate_tab.update_models)
        self.models_tab.initialize_models_from_folder()
        self.models_tab.initialize_models()
        self.history_tab = HistoryTab()
        self.load_history()
        self.history_tab.item_clicked.connect(self.load_history_item)

        self.settings_tab = SettingsTab(self.settings)
        self.settings_tab.device_changed.connect(self.generate_tab.update_device)

        self.tabs_content = QStackedWidget()
        self.tabs_content.setContentsMargins(0, 0, 0, 0)
        self.tabs_content.addWidget(self.generate_tab)
        self.tabs_content.addWidget(self.models_tab)
        self.tabs_content.addWidget(self.history_tab)
        self.tabs_content.addWidget(self.settings_tab)

        content_layout.addWidget(self.tab_list_view)
        content_layout.addWidget(self.tabs_content)

        layout.addWidget(self.app_bar)
        layout.addLayout(content_layout)

        self.setLayout(layout)
        self.tab_list_view.change_tool(0)

    def load_history(self):
        self.history_tab.load_history_items(self.settings.get_save_location())

    def change_tab(self, index):
        tab_index = index
        self.tabs_content.setCurrentIndex(tab_index)

    def load_history_item(self, prompt, settings):
        self.tab_list_view.change_tool(0)
        self.generate_tab.load_history_item(prompt, settings)

    def show_snackbar(self, group, addition):
        if group == "library_add":
            snackbar = Snackbar(
                f"Added to <a href='action' style='{LINK_STYLE}'>library</a>: {addition}",
                self,
            )
            snackbar.link_clicked.connect(partial(self.tab_list_view.change_tool, 2))

        snackbar.show()
