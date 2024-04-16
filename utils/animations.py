from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Signal
from PySide6.QtWidgets import QGraphicsOpacityEffect, QWidget


class OpacityAnimation(QPropertyAnimation):
    def __init__(
        self,
        target_widget: QWidget,
        start_value: float,
        end_value: float,
        duration: int = 200,
    ):
        self.opacity_effect = QGraphicsOpacityEffect(target_widget)
        target_widget.setGraphicsEffect(self.opacity_effect)
        super().__init__(self.opacity_effect, b"opacity")

        self.setDuration(duration)
        self.setStartValue(start_value)
        self.setEndValue(end_value)
        self.setEasingCurve(QEasingCurve.InOutQuad)
