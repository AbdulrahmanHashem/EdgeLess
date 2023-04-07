from PyQt6.QtWidgets import QWidget

DefaultSettings = {"a": "b"}


class SettingsUI(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.settings: dict = DefaultSettings

    def reset(self) -> None:
        self.settings = DefaultSettings

    def update_settings(self, key, value):
        self.settings[key] = value
