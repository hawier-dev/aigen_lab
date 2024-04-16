from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit, QFileDialog
from PySide6.QtCore import Qt, Signal

from constants import *
from widgets.focus_line_edit import FocusLineEdit


class PathPicker(QFrame):
    textChanged = Signal(str)

    def __init__(self, placeholder="", mode="dir", extensions=[], parent=None):
        super().__init__(parent)
        self.setLineWidth(1)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setContentsMargins(10, 2, 2, 2)
        self.setFixedHeight(35)
        self.setCursor(Qt.PointingHandCursor)

        self.mode = mode
        self.extensions = extensions

        self.active = False
        self.normal_style = LINE_EDIT_STYLES
        self.hover_style = LINE_EDIT_HOVER_STYLES
        self.active_style = LINE_EDIT_ACTIVE_STYLES

        self.setStyleSheet(self.normal_style)
        self.setCursor(Qt.PointingHandCursor)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Label with the bold letter
        self.label = QLabel("Select path")
        self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label.setStyleSheet(
            f"""
                font-weight: bold;
                font-size: 12px;
                color: {primary_color};
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
        if self.mode == "dir":
            directory = QFileDialog.getExistingDirectory(self, "Select Directory")
            if directory:
                self.setText(directory)
                self.textChanged.emit(directory)
        elif self.mode == "file":
            filter = "Files ("
            for ext in self.extensions:
                filter += f"*.{ext} "
            filter += ")"
            file, _ = QFileDialog.getOpenFileName(self, "Select File", filter=filter)
            if file:
                self.setText(file)
                self.textChanged.emit(file)

        return super().mousePressEvent(event)

    def on_active(self):
        self.active = True
        self.line_edit.setCursor(Qt.IBeamCursor)
        self.setStyleSheet(self.active_style)

    def on_normal(self):
        self.active = False
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
