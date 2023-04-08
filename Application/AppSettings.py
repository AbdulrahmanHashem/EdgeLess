import json
import os

from PyQt6.QtWidgets import QWidget

DefaultSettings: dict = {
    "mode": 1,  # 1 = Server 2 = Client
    "session_start": "ctrl+*",
    "BUFFER_SIZE": 2048
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

    def load_settings(self):
        try:
            self._settings = json.load(open(Settings_File))
        except Exception as e:
            print(f"Loading Settings Catch : {e}")

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
