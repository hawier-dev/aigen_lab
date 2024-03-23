from PySide6.QtWidgets import QFrame, QLineEdit, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from constants import *


class FocusLineEdit(QLineEdit):
    focus_in = Signal()
    focus_out = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focus_in.emit()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.focus_out.emit()


class LabeledLineEdit(QFrame):
    textChanged = Signal(str)

    def __init__(self, label_text, placeholder="", parent=None):
        super().__init__(parent)
        self.setLineWidth(1)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setContentsMargins(10, 2, 2, 2)
        self.active = False
        self.normal_style = f"""
            QFrame{{
                background-color: {surface_color};
                color: {on_surface_color};
                border: 1px solid {surface2_color};
                border-radius: 0px;
            }}
            QLineEdit{{
                border: none;
                padding: 5px;
                font-size: 13px;
                background-color: {surface_color};
            }}
            QLabel{{
                border: none;
            }}
        """

        self.hover_style = f"""
            QFrame{{
                background-color: {surface2_color};
                color: {on_surface_color}; 
                border: 1px solid {surface2_color};
                border-radius: 0px;
            }}
            QLineEdit{{
                border: none;
                padding: 5px;
                font-size: 13px;
                background-color: {surface2_color}; 
            }}
            QLabel{{
                border: none;
            }}
        """

        self.active_style = f"""
            QFrame{{
                background-color: {surface_color};
                color: {on_surface_color}; 
                border: 1px solid {primary_color};
                border-radius: 0px;
            }}
            QLineEdit{{
                border: none;
                padding: 5px;
                font-size: 13px;
                background-color: {surface_color}; 
            }}
            QLabel{{
                border: none;
            }}
        """
        self.setStyleSheet(self.normal_style)
        self.setCursor(Qt.PointingHandCursor)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Label with the bold letter
        self.label = QLabel(label_text)
        self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label.setStyleSheet(
            """
                font-weight: bold;
                font-size: 12px;
                color: #aaa;
            """
        )

        self.line_edit = FocusLineEdit(placeholder)
        self.line_edit.setContentsMargins(0, 0, 0, 0)
        self.line_edit.focus_in.connect(self.on_active)
        self.line_edit.focus_out.connect(self.on_normal)
        self.line_edit.setCursor(Qt.PointingHandCursor)
        self.line_edit.textChanged.connect(self.textChanged)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line_edit)

        self.setLayout(self.layout)

    def enterEvent(self, event):
        if not self.active:
            self.setStyleSheet(self.hover_style)
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.active:
            self.setStyleSheet(self.normal_style)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.line_edit.setFocus()
        return super().mousePressEvent(event)

    def on_active(self):
        self.active = True
        self.setCursor(Qt.IBeamCursor)
        self.line_edit.setCursor(Qt.IBeamCursor)
        self.setStyleSheet(self.active_style)

    def on_normal(self):
        self.active = False
        self.setCursor(Qt.PointingHandCursor)
        self.line_edit.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(self.normal_style)

    def text(self):
        return self.line_edit.text()

    def setText(self, text):
        self.line_edit.setText(text)

    def setPlaceholderText(self, text):
        self.line_edit.setPlaceholderText(text)

    def setValidator(self, validator):
        self.line_edit.setValidator(validator)
