import threading

import keyboard
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
from keyboard._winkeyboard import official_virtual_keys

from Application.EventListeners.keyboard_events import key_press_performer
from Application.EventListeners.mouse_events import mouse_event_performer
from Application.Networking.client import Client


class ClientWindow(QtWidgets.QMainWindow):
    def setup_ui(self):
        main_widget = QtWidgets.QWidget()
        v_layout = QtWidgets.QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        self.state = QtWidgets.QLabel("")
        v_layout.addWidget(self.state, alignment=Qt.AlignmentFlag.AlignCenter)

        self.switch = QtWidgets.QPushButton("Connect")
        v_layout.addWidget(self.switch, alignment=Qt.AlignmentFlag.AlignCenter)

    def on_connected(self, new):
        if new is None:
            self.switch.setText("Connecting")
            self.state.setText(f"Attempting to connect to {self.client.CLIENT_HOST}, {self.client.CLIENT_PORT}")

        elif new:
            s_size = self.client.receive()
            self.screen_ratio = QGuiApplication.primaryScreen().availableGeometry().width() / int(s_size.split(",")[0])

            self.switch.setText("Disconnect")
            self.state.setText(f"{self.client.CLIENT_HOST} : {self.client.CLIENT_PORT}")

            self.start_session()

        else:
            self.switch.setText("Connect")
            self.state.setText(f"")

    def __init__(self):
        super().__init__()
        self.setup_ui()

        self.mouse_thread = None
        self.connecting_thread = None

        self.client = Client(self)

        self.screen_ratio = 1
        self.last_time = 0.0
        self.last_pressed = ""

        self.controller = threading.Event()

        self.switch.clicked.connect(self.toggle)

    def toggle(self):
        if self.client.connected.value is False:
            self.connect()
        else:
            self.disconnect()

    def connect(self):
        if self.client.client_disconnection is True:
            self.mouse_thread.join()
            self.client.client_disconnection = False
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
            print(f"Start Catch : {e}")

    def receive_control_events(self):
        while not self.controller.is_set():
            data = self.client.receive()
            if data:
                events = data.split(";")
                for event in events:
                    if not event == "":
                        if event.__contains__("keyboard"):
                            key_press_performer(event, self)
                        else:
                            mouse_event_performer(event, self.screen_ratio)

    def release_shortcut(self):
        keyboard.release("ctrl")
        keyboard.release("*")

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.disconnect()
        super().closeEvent(a0)

