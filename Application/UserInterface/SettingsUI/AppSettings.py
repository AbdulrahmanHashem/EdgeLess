import json
import os
from datetime import datetime

from PyQt6.QtWidgets import QWidget

from Application.UserInterface.LoggingUI.Logging import log_to_logging_file

DefaultSettings: dict = {
    "mode": 1,  # 1 = Server 2 = Client
    "Session Start": "ctrl+*",
    "Buffer Size": 2048,
    "Logging": False
}

Settings_File = "Resources/Settings.json"


def make_settings_file() -> bool:
    if os.path.isfile(Settings_File) is False:
        json.dump(DefaultSettings, open(Settings_File, 'w'))
        return True
    else:
        return False


class AppSettings:
    def __init__(self) -> None:
        super().__init__()
        self._settings: dict or None = None
        self.initialize_settings()

        self.logging = self.get_setting("Logging")

    def load_settings(self):
        try:
            self._settings = json.load(open(Settings_File))
        except Exception as e:
            log_to_logging_file(f"Loading Settings Catch : {e}") if self.get_setting("Logging") else None

    def update_settings_file(self) -> bool:
        if os.path.isfile(Settings_File):
            json.dump(self._settings, open(Settings_File, 'w'))
            return True
        else:
            return False

    def initialize_settings(self) -> None:
        if make_settings_file():
            self._settings = DefaultSettings
        else:
            self.load_settings()

    def update_setting(self, key, value):
        self._settings[key] = value
        self.update_settings_file()

    def get_setting(self, key):
        return self._settings[key]
