from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from constants import SETTINGS_STYLES
from utils.functions import get_available_devices
from widgets.option_selector import OptionSelector
from widgets.path_picker import PathPicker
from widgets.title_label import TitleLabel


class SettingsTab(QWidget):
    device_changed = Signal(str)

    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.setStyleSheet(SETTINGS_STYLES)
        self.settings = settings
        self.devices = get_available_devices()

        self.layout = QVBoxLayout(self)

        self.download_location_label = TitleLabel("Download Location for Models:")
        self.download_location_edit = PathPicker()
        self.download_location_edit.setText(self.settings.get_download_location())
        self.layout.addWidget(self.download_location_label)
        self.layout.addWidget(self.download_location_edit)
        self.layout.addSpacing(10)

        self.save_location_label = TitleLabel("Save Location for Photos:")
        self.save_location_edit = PathPicker()
        self.save_location_edit.setText(self.settings.get_save_location())
        self.layout.addWidget(self.save_location_label)
        self.layout.addWidget(self.save_location_edit)
        self.layout.addSpacing(10)

        self.device_label = TitleLabel("Device:")
        self.device_select = OptionSelector("Select Device")
        self.device_select.option_changed.connect(self.on_device_changed)
        self.device_select.set_options([device[0] for device in self.devices])
        self.device_select.select_option(self.get_current_device()[0])

        self.layout.addWidget(self.device_label)
        self.layout.addWidget(self.device_select)
        self.layout.addSpacing(10)
        self.layout.addStretch()

        self.setLayout(self.layout)

    def get_device_ref(self, name):
        for device in self.devices:
            if device[0] == name:
                return device[1]

    def get_device_name(self, ref):
        for device in self.devices:
            if device[1] == ref:
                return device[0]

    def get_current_device(self):
        device_ref = self.settings.get_device()
        device_name = self.get_device_name(device_ref)

        if device_name is not None:
            return [device_name, device_ref]
        else:
            return self.devices[0]

    def on_device_changed(self, device):
        device_ref = self.get_device_ref(device)
        self.settings.set_device(device_ref)
        self.device_changed.emit(device_ref)
