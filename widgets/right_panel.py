from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QSizePolicy,
)

from constants import (
    surface_color,
    primary_color,
    on_surface_color,
    surface2_color,
    surface3_color,
)
from widgets.right_tabs.right_edit_tab import RightEditTab
from widgets.right_tabs.right_generate_tab import RightGenerateTab


class RightPanel(QWidget):
    model_changed = Signal(str)
    on_tab_changed = Signal(int)

    def __init__(self, settings):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(
            f"""
            QWidget{{background: {surface_color};}}
            QTabWidget::pane{{border: none;}}
            QTabBar::tab{{background: {surface_color}; color: {on_surface_color}; border: 1px solid {surface3_color}; padding: 8px;}}
            QTabBar::tab:hover{{background: {surface3_color};}}
            QTabBar::tab:selected{{background: {primary_color}; border: none;}}
            """
        )
        self.setMaximumWidth(250)
        self.settings = settings

        self.model_id = None
        (
            self.image_width,
            self.image_height,
            self.steps,
            self.guidance_scale,
        ) = self.settings.get_prediction_settings()

        self.style = "Normal"

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.tabs = QTabWidget()
        self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tabs.tabBar().setExpanding(True)
        self.tabs.tabBar().setDocumentMode(True)
        self.tabs.tabBar().setCursor(Qt.PointingHandCursor)
        self.tabs.currentChanged.connect(self.on_tab_changed)
        self.main_layout.addWidget(self.tabs)

        self.generate_tab = RightGenerateTab(
            self.image_width, self.image_height, self.steps, self.guidance_scale
        )
        self.generate_tab.model_changed.connect(self.on_model_changed)
        self.generate_tab.apply_parameters.connect(self.apply_parameters)
        self.edit_tab = RightEditTab()

        self.tabs.addTab(self.generate_tab, "Generate")
        self.tabs.addTab(self.edit_tab, "Edit")

    def on_model_changed(self, model_id):
        self.model_id = model_id
        self.model_changed.emit(model_id)

    def start_animation(self):
        self.generate_tab.pipeline_loading_widget.show()
        self.generate_tab.movie.start()

    def stop_animation(self):
        self.generate_tab.pipeline_loading_widget.hide()
        self.generate_tab.movie.stop()

    def apply_parameters(self):
        try:
            self.image_width = int(self.generate_tab.width_input.text())
            self.image_height = int(self.generate_tab.height_input.text())
            self.steps = int(self.generate_tab.steps_input.text())
            self.guidance_scale = float(self.generate_tab.guidance_scale_input.text())
            self.style = self.generate_tab.style_buttons.get_selected()

            self.settings.set_prediction_settings(
                self.image_width,
                self.image_height,
                self.steps,
                self.guidance_scale,
            )

        except ValueError:
            return

    def load_settings_from_list(self, settings):
        self.generate_tab.width_input.setText(str(settings[0][1]))
        self.generate_tab.height_input.setText(str(settings[1][1]))
        self.generate_tab.steps_input.setText(str(settings[2][1]))
        self.generate_tab.guidance_scale_input.setText(str(settings[3][1]))
        self.generate_tab.style_buttons.select_button(settings[4][1])

    def update_models(self, models):
        temp_models = [model.modelId for model in models]
        self.generate_tab.model_selector.set_options(temp_models)
        try:
            if self.generate_tab.model_selector.selected_option not in temp_models:
                self.generate_tab.model_selector.select_option(temp_models[0])

        except IndexError:
            pass
