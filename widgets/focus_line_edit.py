from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLineEdit


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
