import threading
import time

import keyboard

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
            self.address_port.setText(str(self.server.getsockname()))
            self.start.setText("Stop Server")
        elif new:
            self.address_port.setText(
                self.address_port.text() +
                "\n" +
                "   Connected to" +
                "\n" +
                str(self.server.client_address[0]) + " : " + str(self.server.client_address[1]))

            keyboard.add_hotkey("ctrl+*", self.toggle_session)
        else:
            self.address_port.setText("")
            self.start.setText("Start Server")

            try:
                if self.server.connected.value:
                    keyboard.unhook_all_hotkeys()
            except Exception as e:
                print(f"'On Connected' Callback.Unhook All Hotkeys Catch : {e}")

    def __init__(self):
        super().__init__()
        self.setup_ui()

        # make a server instance
        self.server = Server(self)

        self.keyboard_handler = KeyboardHandler(self)
        self.mouse_handler = MouseHandler(self)
        self.mouse_loc = (0, 0)

        self.session = threading.Event()
        self.session.set()

        self.connect_thread = None
        self.mouse_thread = None

        self.start.clicked.connect(self.toggle_server)

    def update_mouse_loc(self, xy):
        self.mouse_loc = xy

    def toggle_server(self) -> None:
        if self.server.connected.value is False:
            self.connect()
        else:
            self.disconnect()

    def connect(self) -> None:
        if self.server.run():
            # self.controller.clear()
            # self.session.clear()

            if self.connect_thread is None:
                self.connect_thread = threading.Thread(target=self.server.connect_now)
                try:
                    self.connect_thread.start()
                except Exception as e:
                    print(e)
            else:
                print("UI Connect Bug")
        else:
            print("UI Connect Error : server run error")

    def disconnect(self):
        # Start Connecting.
        try:
            self.end_session()
            if self.server.connected.value is not False:
                # self.controller.set()
                self.server.send_data("close")

                self.server.stop()

                if self.connect_thread is not None and self.connect_thread.is_alive():
                    self.connect_thread.join()

                self.connect_thread = None
        except Exception as e:
            print(f"Disconnect Catch : {e}")

    def toggle_session(self):
        if self.session.is_set():
            self.start_session()
        else:
            self.end_session()

    def start_listening_to_controls(self):
        self.keyboard_handler.start_keyboard()
        self.mouse_handler.start_mouse()
        while not self.session.is_set():
            pass

    def stop_listening_to_controls(self):
        self.keyboard_handler.stop_keyboard()
        self.mouse_handler.stop_mouse()

    def start_session(self) -> None:
        if not self.server.connected:
            print("Session Start Error : Not Connected")
            return
        elif self.mouse_thread is not None:
            print("Session Start Error : Mouse thread not rest")
            return

        try:
            self.session.clear()
            self.mouse_thread = threading.Thread(target=self.start_listening_to_controls)
            self.mouse_thread.start()
            print("Session Start")
        except Exception as e:
            print(f"Session Start Catch : {e}")

    def end_session(self):
        try:
            self.stop_listening_to_controls()

            self.session.set()  # stop session loops

            if self.mouse_thread is not None and self.mouse_thread.is_alive():
                self.mouse_thread.join()
            self.mouse_thread = None
            print("Session End")
        except Exception as e:
            print(f"End Session Catch : {e}")

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.disconnect()
        super().closeEvent(a0)

