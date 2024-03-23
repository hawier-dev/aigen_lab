import random

from PySide6.QtWidgets import QScrollArea, QHBoxLayout, QLabel, QWidget
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QMouseEvent
from constants import surface_color, surface2_color

class ClickableLabel(QLabel):
    clicked = Signal()  

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(
            f"QLabel {{ background-color: {surface_color}; border: none; padding: 5px; }}"
            f"QLabel:hover {{ background-color: {surface2_color}; }}"
        )
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(30)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()  

class ScrollingPrompts(QWidget):
    label_clicked = Signal(str)
    def __init__(self, prompts, parent=None):
        super().__init__(parent)
        self.prompts = random.sample(prompts, len(prompts))
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)
        self.setFixedHeight(30)
        
        self.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)   
        
        self.scroll_widget = QWidget()
        self.scroll_layout = QHBoxLayout(self.scroll_widget)
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.setAlignment(Qt.AlignLeft)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)

        for prompt in self.prompts:
            prompt_label = ClickableLabel(prompt) 
            prompt_label.clicked.connect(lambda prompt=prompt: self.on_label_clicked(prompt)) 
            self.scroll_layout.addWidget(prompt_label)

        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(self.scroll_area)

        self.setup_scrolling()

    def on_label_clicked(self, prompt):
        self.label_clicked.emit(prompt)

    def setup_scrolling(self):
        self.timer = QTimer(self) 
        self.timer.timeout.connect(self.scroll_content)  
        self.timer.start(50) 

    def scroll_content(self):
        value = self.scroll_area.horizontalScrollBar().value() + 1
        max_value = self.scroll_area.horizontalScrollBar().maximum() 
        if value > max_value:
            self.scroll_area.horizontalScrollBar().setValue(0)
        else:
            self.scroll_area.horizontalScrollBar().setValue(value) 

    def enterEvent(self, event):
        self.timer.stop() 

    def leaveEvent(self, event):
        self.timer.start(50) 