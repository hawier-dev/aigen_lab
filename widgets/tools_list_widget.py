from PySide6.QtCore import Signal
from PySide6.QtWidgets import QListWidget, QListWidgetItem

from widgets.tool_button import ToolButton


class ToolsListWidget(QListWidget):
    tool_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self.tools_widgets = []
        self.currentRowChanged.connect(self.change_tool)

    def add_tool(self, icon, text, spacing=5, func=None):
        tab_widget = ToolButton(icon, text, spacing=spacing)
        tab_widget.set_unselected()
        if func:
            tab_widget.selected.connect(func)
        item = QListWidgetItem()
        item.setSizeHint(tab_widget.sizeHint())

        self.addItem(item)
        self.setItemWidget(item, tab_widget)
        self.tools_widgets.append(tab_widget)

    def change_tool(self, row):
        tab_temp = self.item(row)
        self.setCurrentItem(tab_temp)

        for i, tab_item in enumerate(self.tools_widgets):
            if i == row:
                tab_item.set_selected()
            else:
                tab_item.set_unselected()

        self.tool_changed.emit(row)

    def clear(self):
        super().clear()
        self.tools_widgets = []
