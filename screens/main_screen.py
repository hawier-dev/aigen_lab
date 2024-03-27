from functools import partial

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
    QListWidget,
    QListWidgetItem,
)

from constants import LINK_STYLE
from screens.tabs.generate_tab import GenerateTab
from screens.tabs.history_tab import HistoryTab
from screens.tabs.models_tab import ModelsTab
from screens.tabs.settings_tab import SettingsTab
from utils.settings import Settings
from widgets.app_bar import AppBar
from widgets.snack_bar import Snackbar
from widgets.tab_widget import TabWidget


class MainScreen(QWidget):
    def __init__(self, parent=None):
        super(MainScreen, self).__init__(parent)
        self.tabs_items = []
        self.settings = Settings("dev.hawier", "AIGen Lab")
        self.settings.set_default_values()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.app_bar = AppBar()

        content_layout = QHBoxLayout()

        self.tab_list_view = QListWidget()
        self.tab_list_view.setCursor(Qt.PointingHandCursor)
        self.tab_list_view.setSpacing(5)
        self.tab_list_view.setFixedWidth(160)

        self.add_tab("assets/generate.png", "Generate")
        self.add_tab("assets/model.png", "Library")
        self.add_tab("assets/history.png", "History")
        self.add_tab("assets/settings.png", "Settings")

        self.generate_tab = GenerateTab(self.settings)
        self.models_tab = ModelsTab(self.settings)
        self.models_tab.models_changed.connect(self.generate_tab.update_models)
        self.models_tab.initialize_models_from_folder()
        self.history_tab = HistoryTab()
        self.history_tab.load_history_items(self.settings.get_save_location())
        self.history_tab.item_clicked.connect(self.load_history_item)

        self.tabs_content = QStackedWidget()
        self.tabs_content.setContentsMargins(0, 0, 0, 0)
        self.tabs_content.addWidget(self.generate_tab)
        self.tabs_content.addWidget(self.models_tab)
        self.tabs_content.addWidget(self.history_tab)
        self.tabs_content.addWidget(SettingsTab(self.settings))

        self.tab_list_view.currentItemChanged.connect(self.change_tab)

        content_layout.addWidget(self.tab_list_view)
        content_layout.addWidget(self.tabs_content)

        layout.addWidget(self.app_bar)
        layout.addLayout(content_layout)
        self.setLayout(layout)
        self.change_tab(0)

    def add_tab(self, icon, text):
        tab_widget = TabWidget(icon, text)
        item = QListWidgetItem()
        item.setSizeHint(tab_widget.sizeHint())

        self.tab_list_view.addItem(item)
        self.tab_list_view.setItemWidget(item, tab_widget)
        self.tabs_items.append(tab_widget)

    def change_tab(self, current):
        if isinstance(current, int):
            tab_index = current
            tab_temp = self.tab_list_view.item(current)
        else:
            tab_index = self.tab_list_view.row(current)
            tab_temp = current
        self.tabs_content.setCurrentIndex(tab_index)
        self.tab_list_view.setCurrentItem(tab_temp)

        for i, tab_item in enumerate(self.tabs_items):
            if i == tab_index:
                tab_item.set_selected()
            else:
                tab_item.set_unselected()

    def load_history_item(self, prompt, settings):
        self.change_tab(0)
        self.generate_tab.load_history_item(prompt, settings)

    def show_snackbar(self, group, addition):
        if group == "library_add":
            snackbar = Snackbar(
                f"Added to <a href='action' style='{LINK_STYLE}'>library</a>: {addition}",
                self,
            )
            snackbar.link_clicked.connect(partial(self.change_tab, 2))

        snackbar.show()
