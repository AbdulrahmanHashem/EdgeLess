import socket
import threading

import keyboard
import pyautogui

from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from Application.EventListeners.keyboard_events import KeyboardHandler
from Application.EventListeners.mouse_events import MouseHandler
from Application.Networking.server import Server


class ServerWindow(QWidget):
    def setup_ui(self):
        v_layout = QVBoxLayout()
        self.setLayout(v_layout)

        self.addresses = QLabel(str(socket.gethostbyname_ex(socket.gethostname())[2]))
        v_layout.addWidget(self.addresses, alignment=Qt.AlignmentFlag.AlignCenter)

        self.address_port = QLabel("")
        v_layout.addWidget(self.address_port, alignment=Qt.AlignmentFlag.AlignCenter)

        self.start = QPushButton("Start Server")
        v_layout.addWidget(self.start, alignment=Qt.AlignmentFlag.AlignCenter)

    def on_connected(self, new):
        if new is None:
            """ On Connected None"""
            self.address_port.setText(str(self.server.getsockname()))
            self.start.setText("Stop Server")

        elif new:
            """ On Connected True"""
            self.address_port.setText(
                self.address_port.text() +
                "\n" +
                "   Connected to " +
                "\n" +
                str(self.server.client_address[0]) + " : " + str(self.server.client_address[1]))

            keyboard.add_hotkey("ctrl+*", self.start_session)

        else:
            """ On Connected False"""
            self.address_port.setText("")
            self.start.setText("Start Server")

    def __init__(self):
        super().__init__()
        self.setup_ui()

        self.server = Server(self)

        self.keyboard_handler = KeyboardHandler(self)
        self.mouse_handler = MouseHandler(self)

        self.session = threading.Event()

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
            return print("UI Connect Error : server run error")

        if self.server.connected.value:
            return print("UI Connect Error : Server Is Still Connected")

        try:
            self.connect_thread = threading.Thread(target=self.server.connect_now)
            self.connect_thread.start()
        except Exception as e:
            return print(f"UI Connect Catch : {e}")

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

        while not self.session.is_set():
            pass

    def stop_listening_to_controls(self):
        if keyboard._hotkeys.__contains__("ctrl+*"):
            keyboard.remove_hotkey("ctrl+*")

        self.session.set()
        self.mouse_handler.stop_mouse()
        self.keyboard_handler.stop_keyboard()

        keyboard.add_hotkey("ctrl+*", self.start_session)

    def start_session(self) -> None:
        if self.keyboard_handler.session_on and self.mouse_handler.session_on:
            self.stop_listening_to_controls()

        if (self.keyboard_handler.session_on and self.mouse_handler.session_on) is False:
            if not self.server.connected.value:
                print("Session Start Error : Not Connected")
                return
            if self.mouse_thread is not None:
                self.mouse_thread.join()

            try:
                self.session.clear()
                self.mouse_thread = threading.Thread(target=self.start_listening_to_controls)
                self.mouse_thread.start()
                print("Session Start")

            except Exception as e:
                print(f"Session Start Catch : {e}")

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.disconnect()
        super().closeEvent(a0)

