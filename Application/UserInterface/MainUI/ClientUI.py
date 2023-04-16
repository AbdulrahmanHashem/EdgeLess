import socket
import threading

import keyboard
from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QHBoxLayout, QSpinBox

from Application.EventListeners.keyboard_events import key_press_performer
from Application.EventListeners.mouse_events import mouse_event_performer
from Application.Networking.client import Client
from Application.UserInterface.LoggingUI.Logging import log_to_logging_file


class ClientWindow(QWidget):
    def setup_ui(self):
        # Set Main Layout
        self.setLayout(self.main_v_layout)

        # Adding Main Components.
        self.main_v_layout.addWidget(self.state, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_v_layout.addLayout(self.H_layout)
        self.main_v_layout.addWidget(self.switch, alignment=Qt.AlignmentFlag.AlignCenter)

        # Adding id and port Widgets to the H Layout.
        self.H_layout.addWidget(self.id)
        self.H_layout.addWidget(self.port)

        # Setup Port and ID Widgets Settings.
        self.port.setMinimum(0)
        self.port.setMaximum(65535)
        self.port.setValue(9999)

        text = ""
        for i in socket.gethostbyname_ex(socket.gethostname())[2][-1].split(".")[0:3]:
            text = text + f"{i}."
        self.id.setText(text)
        self.id.setMaximumSize(210, 26)

    def on_connected(self, new):
        if new is None:
            """ On Connected None"""
            self.switch.setText("Connecting")
            self.state.setText(f"Attempting to connect to {self.client.HOST}, {self.client.PORT}")

        elif new:
            """ On Connected True"""
            self.switch.setText("Disconnect")
            self.state.setText(f"{self.client.HOST} : {self.client.PORT}")

            self.start_session()

        else:
            """ On Connected False"""
            self.switch.setText("Connect")
            self.state.setText(f"")

    def __init__(self, parent):
        super().__init__()
        self.master_window = parent

        # initialize UI Components.
        self.main_v_layout = QVBoxLayout()
        self.H_layout = QHBoxLayout()

        self.state = QLabel("")

        self.id = QTextEdit()
        self.port = QSpinBox()

        self.switch = QPushButton("Connect")

        self.setup_ui()    # Setup UI components.

        self.mouse_thread = None
        self.connecting_thread = None

        self.client = Client(self)

        self.last_time = 0.0
        self.last_pressed = ""

        self.controller = threading.Event()

        self.switch.clicked.connect(self.toggle)

    def toggle(self):
        if self.client.connected.value is False:
            if self.client.client_disconnection is True:
                self.mouse_thread.join()
                self.client.client_disconnection = False

            self.connect()
        else:
            self.disconnect()

    def connect(self):
        self.client.__init__(self)
        self.connecting_thread = threading.Thread(target=self.client.connect_now)
        self.connecting_thread.start()

    def disconnect(self):
        self.controller.set()
        self.client.disconnect()

    def start_session(self):
        try:
            self.controller.clear()
            self.mouse_thread = threading.Thread(target=self.receive_control_events)
            self.mouse_thread.start()
        except Exception as e:
            log_to_logging_file(f"Start Catch : {e}") if self.master_window.settings.get_setting(
                "Logging") else None

    def receive_control_events(self):
        try:
            zero = ""
            while not self.controller.is_set():
                data = self.client.receive()

                if data == "" or data.__contains__("clo"):
                    self.client.client_disconnection = True
                    self.disconnect()
                    self.release_shortcut()
                    return

                elif "new" in data:
                    sign, x, y, new_shortcut = data.split(",|")
                    self.master_window.settings.update_setting("Session Start", new_shortcut)
                    self.release_shortcut()
                    zero = [x, y]

                if data:
                    events = data.split(";|")
                    for event in events:
                        if not event == "":
                            if event.__contains__("keyboard"):
                                key_press_performer(event, self)
                            else:
                                mouse_event_performer(event, zero, self)
        except Exception as e:
            log_to_logging_file(f"Receive Control Events Catch : {e}") if self.master_window.settings.get_setting(
                "Logging") else None

    def release_shortcut(self):
        shortcut = self.master_window.settings.get_setting("Session Start").split("+")
        for sc in shortcut:
            keyboard.release(sc)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.disconnect()
        super().closeEvent(a0)
