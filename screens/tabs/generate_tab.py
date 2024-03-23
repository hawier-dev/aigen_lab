import os

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QLineEdit,
    QSizePolicy,
    QProgressBar,
)
from PySide6.QtGui import QPixmap, QIcon, QMovie
from PySide6.QtCore import Qt, QSize, QThreadPool, QPropertyAnimation

from constants import (
    PROMPT_LAYOUT_STYLE,
    surface3_color,
)
from utils.predictor import Predictor
from utils.worker import ImageGenerationTask
from widgets.configuration_bar import ConfigurationBar
from widgets.image_view import ImageView
from widgets.scrolling_prompts import ScrollingPrompts


class GenerateTab(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.predictor = Predictor(
            r"C:\Users\mbady\Documents\aigenlab\models\stable-diffusion-v1-5",
            self.settings.get_save_location(),
        )

        # thread pool for background tasks
        self.thread_pool = QThreadPool()
        self.setContentsMargins(0, 0, 0, 0)

        # Main layout setup
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.center_layout = QVBoxLayout()
        self.center_layout.setSpacing(0)

        # Image placeholder setup
        self.image_viewer = ImageView()
        self.image_viewer.setAlignment(Qt.AlignCenter)
        self.image_viewer.set_placeholder_background()
        self.image_viewer.setStyleSheet("QWidget{border: none;}")
        self.center_layout.addWidget(self.image_viewer)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumHeight(2)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setTextVisible(False)

        self.center_layout.addSpacing(3)
        self.center_layout.addWidget(self.progress_bar)

        # Prompt input area setup
        self.prompt_center_layout = QHBoxLayout()
        self.prompt_center_layout.setContentsMargins(0, 0, 0, 6)
        self.prompt_widget = QWidget()
        self.prompt_widget.setStyleSheet(
            f"QWidget{{border: 1px solid {surface3_color};}}"
        )
        self.prompt_widget.setFixedHeight(52)
        self.prompt_widget.setStyleSheet(PROMPT_LAYOUT_STYLE)
        self.prompt_layout = QHBoxLayout()
        self.prompt_layout.setContentsMargins(10, 0, 10, 0)

        # Text input for prompts
        self.prompt_text_edit = QLineEdit()
        self.prompt_text_edit.setPlaceholderText("Enter prompt here...")
        self.prompt_text_edit.returnPressed.connect(self.generate_image)

        # Generate button setup
        self.generate_button = QPushButton("Generate")
        self.generate_button.setCursor(Qt.PointingHandCursor)
        self.generate_button.setFixedSize(100, 40)
        self.generate_button.setIconSize(QSize(30, 30))
        self.generate_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Loading animation setup
        self.movie = QMovie("assets/spinner.gif")
        self.movie.frameChanged.connect(self.update_spinner_button)

        self.prompt_layout.addWidget(self.prompt_text_edit)
        self.prompt_layout.addWidget(self.generate_button)
        self.prompt_widget.setLayout(self.prompt_layout)
        self.prompt_center_layout.addWidget(self.prompt_widget)

        self.center_layout.addLayout(self.prompt_center_layout)
        self.layout.addLayout(self.center_layout)

        # Configuration bar
        self.configuration_bar = ConfigurationBar()
        self.configuration_bar.model_changed.connect(self.load_pipeline)
        self.layout.addWidget(self.configuration_bar, alignment=Qt.AlignRight)

        self.generate_button.clicked.connect(self.generate_image)

        self.predictor.pipeline_loaded.connect(self.configuration_bar.stop_animation)

        self.setLayout(self.layout)

    def load_pipeline(self, model_id):
        self.configuration_bar.start_animation()
        self.predictor.load_pipeline(model_id)

    def generate_image(self):
        self.start_animation()
        prompt = self.prompt_text_edit.text()
        task = ImageGenerationTask(
            self.settings.get_save_location(),
            prompt,
            self.configuration_bar.image_width,
            self.configuration_bar.image_height,
            self.configuration_bar.steps,
            self.configuration_bar.guidance_scale,
            self.configuration_bar.style,
            self.predictor,
        )
        task.signals.finished.connect(self.display_image)
        task.signals.error.connect(self.report_error)
        task.signals.progress.connect(self.update_progress)
        self.thread_pool.start(task)

    def update_models(self, models):
        self.configuration_bar.update_models(models)

    def update_progress(self, value: int):
        self.progress_bar.setValue(value)

    def display_image(self, image_path):
        if os.path.exists(image_path):
            self.image_viewer.display_image(image_path)
        else:
            self.image_viewer.set_placeholder_background()

        self.stop_animation()
        self.progress_bar.setValue(0)

    def start_animation(self):
        self.generate_button.setText("")
        self.generate_button.setFixedSize(40, 40)
        self.movie.start()
        self.generate_button.setEnabled(False)

    def stop_animation(self):
        self.generate_button.setText("Generate")
        self.generate_button.setFixedSize(120, 40)
        self.movie.stop()
        self.generate_button.setEnabled(True)
        self.generate_button.setIcon(QIcon())

    def update_spinner_button(self):
        self.generate_button.setIcon(self.movie.currentPixmap())

    def report_error(self, e):
        print(f"Error: {e}")
        self.stop_animation()
        self.progress_bar.setValue(0)
