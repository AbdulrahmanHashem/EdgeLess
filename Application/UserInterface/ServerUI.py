import threading
import time

import keyboard
import pyautogui

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import Qt

from Application.EventListeners.keyboard_events import KeyboardHandler
from Application.EventListeners.mouse_events import MouseHandler
from Application.Networking.server import Server


class ServerWindow(QtWidgets.QMainWindow):
    def setup_ui(self):
        main_widget = QtWidgets.QWidget()
        v_layout = QtWidgets.QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        self.address_port = QtWidgets.QLabel("")
        v_layout.addWidget(self.address_port, alignment=Qt.AlignmentFlag.AlignCenter)

        self.start = QtWidgets.QPushButton("Start Server")
        v_layout.addWidget(self.start, alignment=Qt.AlignmentFlag.AlignCenter)

    def on_connected(self, new):
        if new is None:
            """ On Connected None"""
            self.address_port.setText(str(self.server.getsockname()))
            self.start.setText("Stop Server")

        elif new:
            """ On Connected True"""
            SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
            self.server.send_data(f"{SCREEN_WIDTH},{SCREEN_HEIGHT}")

            self.address_port.setText(
                self.address_port.text() +
                "\n" +
                "   Connected to" +
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

        # make a server instance
        self.server = Server(self)

        self.keyboard_handler = KeyboardHandler(self)
        self.mouse_handler = MouseHandler(self)

        self.session = threading.Event()

        self.connect_thread: threading.Thread
        self.mouse_thread: threading.Thread

        self.start.clicked.connect(self.toggle_server)

    def toggle_server(self) -> None:
        if self.server.connected.value is False:

            if self.server.client_disconnection:
                self.mouse_thread.join()
                self.connect_thread.join()
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
        self.stop_listening_to_controls()
        if self.server.client_disconnection is False:
            self.server.send_data("close")
        self.server.stop()

    def start_listening_to_controls(self):
        self.keyboard_handler.start_keyboard()
        self.mouse_handler.start_mouse()

        while not self.session.is_set():
            pass

    def stop_listening_to_controls(self):
        self.keyboard_handler.stop_keyboard()
        self.mouse_handler.stop_mouse()
        self.session.set()
        # keyboard.add_hotkey("ctrl+*", self.start_session)

    def start_session(self) -> None:
        if not self.server.connected.value:
            print("Session Start Error : Not Connected")
            return

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

