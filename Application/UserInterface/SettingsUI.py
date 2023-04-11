from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QKeySequenceEdit, QSpinBox, QVBoxLayout, QGridLayout, QLabel

from Application.Utils.Utils import set_QWidget_content, get_QWidget_content


class SettingsUI(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.settings = parent.settings

        self.settings_widget = {"Session Start": QKeySequenceEdit,
                                "Buffer Size": QSpinBox}

        self.settings_widget_refs = {}

        self.initialize_ui()

        self.fill_settings()

        self.settings_widget_refs["Session Start"].editingFinished.connect(
            lambda: self.settings.update_setting(
                "Session Start",
                get_QWidget_content(self.settings_widget_refs["Session Start"])
            )
        )

        self.settings_widget_refs["Buffer Size"].editingFinished.connect(
            lambda: self.settings.update_setting(
                "Buffer Size",
                get_QWidget_content(self.settings_widget_refs["Buffer Size"])
            )
        )

    def initialize_ui(self):
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

        self.add_settings()

    def add_settings(self):
        for widget_key in self.settings_widget:
            index = list(self.settings_widget.keys()).index(widget_key)

            name_widget = QLabel(widget_key)
            value_widget = self.settings_widget[widget_key]()

            self.main_layout.addWidget(name_widget, index, 0, alignment=Qt.AlignmentFlag.AlignRight)
            self.main_layout.addWidget(value_widget, index, 1)

            if isinstance(value_widget, QSpinBox):
                value_widget.setMaximum(10240)

            self.settings_widget_refs[widget_key] = value_widget

    def fill_settings(self):
        for widget_key in self.settings_widget_refs:
            setting = self.settings.get_setting(widget_key)
            set_QWidget_content(self.settings_widget_refs[widget_key], setting)
