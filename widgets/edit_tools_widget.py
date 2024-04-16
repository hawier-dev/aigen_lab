from functools import partial

from PySide6.QtCore import Qt, QRectF, QSize, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QToolButton,
    QFrame,
    QGraphicsOpacityEffect,
    QVBoxLayout,
)
from PySide6.QtGui import QIcon

from constants import surface_color, surface2_color, primary_color
from widgets.slider import Slider


class EditToolsWidget(QFrame):
    slider_value_changed = Signal(int)
    tool_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tools = []
        self.tools_values = []

        self.setStyleSheet(
            # border: 1px solid {surface2_color};
            f"""
            ImageViewTools{{
                background-color: {surface_color};
            }}
            QToolButton{{
                background-color: {surface_color};
                border: none;
                padding: 8px;
            }}
            QToolButton:hover{{
                background-color: {surface2_color};
            }}
            QToolButton:checked{{
                background-color: {primary_color};
            }}
            """
        )
        self.setContentsMargins(10, 10, 10, 10)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.slider = Slider()
        self.slider.valueChanged.connect(self.slider_value_changed)
        self.main_layout.addWidget(self.slider)
        self.main_layout.addSpacing(10)

        self.tools_widget_layout = QHBoxLayout(self)
        self.tools_widget_layout.setSpacing(0)
        self.tools_widget_layout.setContentsMargins(0, 0, 0, 0)

        self.main_layout.addLayout(self.tools_widget_layout)
        self.setLayout(self.main_layout)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(1.0)
        self.setGraphicsEffect(self.opacity_effect)

    def add_tool(self, icon_path, tooltip=None, checkable=True, value="", checked=False):
        tool_button = QToolButton(self)
        tool_button.setCheckable(checkable)
        tool_button.setCursor(Qt.PointingHandCursor)
        tool_button.setIcon(QIcon(icon_path))
        if checkable:
            tool_button.setChecked(checked)
            tool_button.pressed.connect(self.tool_clicked)
            tool_button.pressed.connect(partial(self.tool_changed.emit, value))
        if tooltip:
            tool_button.setToolTip(tooltip)
        tool_button.setIconSize(QSize(24, 24))
        self.tools_widget_layout.addWidget(tool_button)
        self.tools.append(tool_button)
        self.tools_values.append(value)

    def reposition_tool_widget(self, viewport):
        rect = QRectF(viewport.rect())
        tool_widget_width = self.frameGeometry().width()
        tool_widget_height = self.frameGeometry().height()
        new_x = rect.width() / 2 - tool_widget_width / 2
        new_y = rect.height() - tool_widget_height - 30
        self.move(new_x, new_y)

    def tool_clicked(self):
        for tool in self.tools:
            if tool.isChecked():
                tool.setChecked(False)
