import socket
import threading

import keyboard

from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSpinBox, QLineEdit

from Application.EventListeners.keyboard_events import KeyboardHandler
from Application.EventListeners.mouse_events import MouseHandler
from Application.Networking.server import Server
from Application.UserInterface.LoggingUI.Logging import log_to_logging_file


class ServerWindow(QWidget):
    def enable(self):
        if self.address.isEnabled() and self.port.isEnabled():
            self.address.setEnabled(False)
            self.port.setEnabled(False)
        elif self.address.isEnabled() is False or self.port.isEnabled() is False:
            self.address.setEnabled(True)
            self.port.setEnabled(True)
        else:
            self.address.setEnabled(True)
            self.port.setEnabled(True)

    def setup_ui(self):
        # Setting Main Layout.
        self.setLayout(self.main_v_layout)

        # Adding All Available Addresses.
        self.main_v_layout.addWidget(self.addresses, alignment=Qt.AlignmentFlag.AlignCenter)

        # Adding Server Address layout to the main layout.
        self.main_v_layout.addLayout(self.H_layout)

        # Adding Server Address layout components.
        self.H_layout.addWidget(self.edit)
        self.H_layout.addWidget(self.address)
        self.H_layout.addWidget(self.port)

        # Setting Server Address layout components settings.
        self.edit.setMaximumWidth(50)
        self.edit.clicked.connect(self.enable)

        self.address.setMaximumSize(150, 26)
        self.address.setEnabled(False)
        self.address.editingFinished.connect(lambda: self.address.setEnabled(False))

        self.port.setMinimum(0)
        self.port.setMaximum(65535)
        self.port.setValue(9999)
        self.port.setEnabled(False)
        self.port.editingFinished.connect(lambda: self.port.setEnabled(False))

        # Adding Address text, Status text and Start button to the main layout.
        self.main_v_layout.addWidget(self.status, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_v_layout.addWidget(self.start, alignment=Qt.AlignmentFlag.AlignCenter)

    def on_connected(self, new):
        if new is None:
            """ On Connected None"""
            self.status.setText("Waiting For Connection")
            self.start.setText("Stop Server")

        elif new:
            """ On Connected True"""
            self.status.setText(f"Connected to {self.server.client_address[0]} : {self.server.client_address[1]}")

            shortcut = self.master_window.settings.get_setting("Session Start")
            keyboard.add_hotkey(shortcut, self.start_session)

        else:
            """ On Connected False"""
            self.status.setText("")
            self.start.setText("Start Server")

    def __init__(self, parent):
        super().__init__()
        self.master_window = parent

        self.main_v_layout = QVBoxLayout()
        self.H_layout = QHBoxLayout()
        self.addresses = QLabel(str(socket.gethostbyname_ex(socket.gethostname())[2]))
        self.address = QLineEdit(str(socket.gethostbyname_ex(socket.gethostname())[2][-1]))
        self.port = QSpinBox()
        self.edit = QPushButton("Edit")
        self.start = QPushButton("Start Server")
        self.status = QLabel()

        self.setup_ui()

        self.server = Server(self)

        self.keyboard_handler = KeyboardHandler(self)
        self.mouse_handler = MouseHandler(self)

        self.connect_thread: threading.Thread | None = None
        self.mouse_thread: threading.Thread | None = None

        self.start.clicked.connect(self.toggle_server)

    def toggle_server(self) -> None:
        if self.server.connected.value is False:
            if self.connect_thread is not None:
                self.connect_thread.join()

            if self.server.client_disconnection:
                self.server.client_disconnection = False

            self.connect()
        else:
            self.disconnect()

    def connect(self) -> None:
        if self.server.run() is False:
            return log_to_logging_file("UI Connect Error : server run error") if self.master_window.settings.get_setting(
                "Logging") else None

        if self.server.connected.value:
            return log_to_logging_file("UI Connect Error : Server Is Still Connected") if self.master_window.settings.get_setting(
                "Logging") else None

        try:
            self.connect_thread = threading.Thread(target=self.server.connect_now)
            self.connect_thread.start()
        except Exception as e:
            return log_to_logging_file(f"UI Connect Catch : {e}") if self.master_window.settings.get_setting("Logging") else None

    def disconnect(self):
        self.start.setEnabled(False)
        self.stop_listening_to_controls()
        if self.server.client_disconnection is False:
            self.server.send_data("close")
        self.server.stop()
        self.start.setEnabled(True)

    def start_listening_to_controls(self):
        self.keyboard_handler.start_keyboard()
        self.mouse_handler.start_mouse()

    def stop_listening_to_controls(self):
        shortcut = self.master_window.settings.get_setting("Session Start")

        if keyboard._hotkeys.__contains__(shortcut):
            keyboard.remove_hotkey(shortcut)

        self.keyboard_handler.stop_keyboard()
        self.mouse_handler.stop_mouse()

        keyboard.add_hotkey(shortcut, self.start_session)

    def start_session(self) -> None:
        if self.server.client_disconnection and self.server.connected.value:
            self.disconnect()
            return

        if self.keyboard_handler.session_on and self.mouse_handler.session_on:
            self.stop_listening_to_controls()

        if (self.keyboard_handler.session_on and self.mouse_handler.session_on) is False:
            if not self.server.connected.value:
                log_to_logging_file("Session Start Error : Not Connected") if self.master_window.settings.get_setting(
                    "Logging") else None
                return
            if self.mouse_thread is not None:
                self.mouse_thread.join()

            try:
                self.mouse_thread = threading.Thread(target=self.start_listening_to_controls)
                self.mouse_thread.start()

                log_to_logging_file("Session Start") if self.master_window.settings.get_setting("Logging") else None
            except Exception as e:
                log_to_logging_file(f"Session Start Catch : {e}") if self.master_window.settings.get_setting("Logging") else None

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.disconnect()
        super().closeEvent(a0)
