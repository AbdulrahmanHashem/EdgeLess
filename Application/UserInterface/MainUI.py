from PyQt6 import QtGui
from PyQt6.QtCore import Qt
# from PyQt6.QtCore import Qt
from PyQt6.QtGui import QWindowStateChangeEvent
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QRadioButton

from Application.UserInterface.ClientUI import ClientWindow
from Application.UserInterface.ServerUI import ServerWindow
import pystray
from PIL import Image

from Application.AppSettings import AppSettings


class EdgeLess(QMainWindow):
    def __init__(self):
        super().__init__()
        # main window setting
        self.setWindowTitle("Edge Less")
        self.setMinimumWidth(450)
        self.setMinimumHeight(250)
        self.setMaximumWidth(450)
        self.setMaximumHeight(250)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.H_layout = QHBoxLayout()
        self.main_widget.setLayout(self.H_layout)

        self.settings = AppSettings()  # settings Window

        self.create_radio_buttons_group()               # Radio Buttons             |*|   |
        self.create_client_and_server_controls_group()  # Client & Server Controls  | |***|

        self.server.clicked.connect(lambda: self.toggle_app_service(False, True))
        self.client.clicked.connect(lambda: self.toggle_app_service(True, False))

        if self.settings.get_setting("mode") == 1:
            self.server.click()
        else:
            self.client.click()

    def create_radio_buttons_group(self):
        self.radio_buttons_group = QVBoxLayout()
        self.H_layout.addLayout(self.radio_buttons_group)

        self.server = QRadioButton("Server")
        self.server.setChecked(True)
        self.radio_buttons_group.addWidget(self.server, alignment=Qt.AlignmentFlag.AlignTop)

        self.client = QRadioButton("Client")
        self.radio_buttons_group.addWidget(self.client, alignment=Qt.AlignmentFlag.AlignTop)

    def create_client_and_server_controls_group(self):
        self.c_and_s_controls_group = QVBoxLayout()
        self.c_and_s_controls_group.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.H_layout.addLayout(self.c_and_s_controls_group)

        self.server_window = ServerWindow(self)
        self.c_and_s_controls_group.addWidget(self.server_window)

        self.client_window = ClientWindow(self)
        self.c_and_s_controls_group.addWidget(self.client_window)
        self.client_window.setEnabled(False)

    def toggle_app_service(self, client: bool, server: bool):
        self.client_window.setEnabled(client)
        self.server_window.setEnabled(server)

        if server:
            self.settings.update_setting("mode", 1)
        else:
            self.settings.update_setting("mode", 2)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.server_window.disconnect()
        self.client_window.disconnect()
        super().closeEvent(a0)

    def event(self, event):
        if isinstance(event, QWindowStateChangeEvent):
            if self.windowState() & Qt.WindowState.WindowMinimized:
                self.hide()

                def show(icon, menu):
                    self.showNormal()
                    icon.stop()

                def close():
                    self.close()
                    icon.stop()

                image = Image.open("Resources/EdgeLess_Logo.ico")
                menu = pystray.Menu(pystray.MenuItem('Show', show), pystray.MenuItem('Exit', close))
                icon = pystray.Icon('EdgeLess', image, "EdgeLess", menu=menu, doubleclick=show)
                icon.run()
        return super().event(event)
