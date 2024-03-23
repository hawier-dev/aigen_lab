from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIntValidator, QDoubleValidator, QMovie
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QFrame,
    QComboBox,
)

from constants import surface_color
from utils.resolution_validator import ResolutionValidator
from widgets.choice_buttons import ChoiceButtons
from widgets.labeled_line_edit import LabeledLineEdit
from widgets.model_selector import ModelSelector
from widgets.title_label import TitleLabel


class ConfigurationBar(QWidget):
    model_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.setContentsMargins(10, 10, 0, 10)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(
            f"ConfigurationBar{{background: {surface_color};}} QFrame{{background: {surface_color};}}"
        )
        self.setMaximumWidth(240)

        self.image_width = 512
        self.image_height = 512
        self.steps = 60
        self.guidance_scale = 7.5
        self.style = "Normal"

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        # QScrollArea
        self.scroll_area = QScrollArea()
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area_frame = QFrame()
        self.scroll_area.setWidget(self.scroll_area_frame)
        self.main_layout.addWidget(self.scroll_area)

        self.settings_layout = QVBoxLayout(self.scroll_area_frame)
        self.settings_layout.setContentsMargins(0, 0, 10, 0)

        # Model selector
        self.model_selector_label = TitleLabel("Model Selector:")
        self.model_selector = ModelSelector()
        self.model_selector.setCursor(Qt.PointingHandCursor)
        self.model_selector.model_changed.connect(self.model_changed)

        self.settings_layout.addWidget(self.model_selector_label)
        self.settings_layout.addWidget(self.model_selector)

        self.pipeline_loading_widget = QWidget()
        self.pipeline_loading_widget.setContentsMargins(0, 0, 0, 0)
        self.pipeline_loading_layout = QHBoxLayout()
        self.pipeline_loading_layout.setContentsMargins(0, 0, 0, 0)
        self.movie = QMovie("assets/spinner.gif")
        self.movie.setScaledSize(QSize(24, 24))
        self.movie.frameChanged.connect(self.update_spinner)

        self.loading_animation = QLabel()
        self.loading_animation.setMovie(self.movie)
        self.loading_animation.setAlignment(Qt.AlignCenter)
        self.loading_animation.setFixedSize(24, 24)

        self.loading_label = QLabel("Loading pipeline")
        self.loading_label.setStyleSheet(
            "color: white; font-weight: bold; font-size: 13px;"
        )
        self.pipeline_loading_layout.addWidget(self.loading_animation)
        self.pipeline_loading_layout.addWidget(self.loading_label)
        self.pipeline_loading_widget.setLayout(self.pipeline_loading_layout)
        self.pipeline_loading_widget.hide()

        self.settings_layout.addSpacing(5)
        self.settings_layout.addWidget(self.pipeline_loading_widget)
        self.settings_layout.addSpacing(5)

        # Image Resolution Setting
        self.resolution_label = TitleLabel("Image Resolution:")
        self.resolution_layout = QHBoxLayout()
        self.width_input = LabeledLineEdit("W :", str(self.image_width))
        self.width_input.setValidator(QIntValidator(8, 4096))
        self.width_input.textChanged.connect(self.apply_parameters)

        self.height_input = LabeledLineEdit("H :", str(self.image_height))
        self.height_input.setValidator(QIntValidator(8, 4096))
        self.height_input.textChanged.connect(self.apply_parameters)
        self.resolution_layout.addWidget(self.width_input)
        self.resolution_layout.addWidget(self.height_input)

        self.settings_layout.addWidget(self.resolution_label)
        self.settings_layout.addLayout(self.resolution_layout)

        self.settings_layout.addSpacing(10)

        # Num Inference Steps Setting
        self.steps_label = TitleLabel("Num Inference Steps:")
        self.steps_input = LabeledLineEdit("STEPS :", str(self.steps))
        self.steps_input.setValidator(QIntValidator(1, 1000))
        self.steps_input.textChanged.connect(self.apply_parameters)
        self.settings_layout.addWidget(self.steps_label)
        self.settings_layout.addWidget(self.steps_input)

        self.settings_layout.addSpacing(10)

        # Guidance Scale Setting
        self.guidance_label = TitleLabel("Guidance Scale:")
        self.guidance_scale_input = LabeledLineEdit("SCALE :", str(self.guidance_scale))
        self.guidance_scale_input.setValidator(QDoubleValidator(0.0, 100.0, 2))
        self.guidance_scale_input.textChanged.connect(self.apply_parameters)
        self.settings_layout.addWidget(self.guidance_label)
        self.settings_layout.addWidget(self.guidance_scale_input)

        self.settings_layout.addSpacing(10)

        # Image Style Setting
        self.style_label = TitleLabel("Image Style:")
        self.style_buttons = ChoiceButtons(
            ["Normal", "Realistic", "Cartoon", "Artistic", "Minimalist"]
        )
        self.style_buttons.selection_changed.connect(self.apply_parameters)
        self.settings_layout.addWidget(self.style_label)
        self.settings_layout.addWidget(self.style_buttons)

        self.settings_layout.addStretch()

    def update_spinner(self):
        self.loading_animation.setMovie(self.movie)

    def start_animation(self):
        self.pipeline_loading_widget.show()
        self.movie.start()

    def stop_animation(self):
        self.pipeline_loading_widget.hide()
        self.movie.stop()

    def apply_parameters(self):
        self.image_width = int(self.width_input.text())
        self.image_height = int(self.height_input.text())
        self.steps = int(self.steps_input.text())
        self.guidance_scale = float(self.guidance_scale_input.text())
        self.style = self.style_buttons.get_selected()

    def update_models(self, models):
        temp_models = [model.modelId for model in models]
        self.model_selector.models = temp_models
        try:
            if self.model_selector.selected_model not in temp_models:
                self.model_selector.select_model(temp_models[0])

        except IndexError:
            pass
