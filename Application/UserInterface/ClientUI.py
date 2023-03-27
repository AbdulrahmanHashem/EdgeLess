import threading

import keyboard
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
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
            self.switch.setText("Disconnect")
            self.state.setText(f"{self.client.CLIENT_HOST} : {self.client.CLIENT_PORT}")

            self.start_session()
        else:
            self.switch.setText("Connect")
            self.state.setText(f"")

            # self.stop_session()

    def __init__(self):
        super().__init__()
        self.setup_ui()

        self.switch.clicked.connect(self.toggle)

        self.controller = threading.Event()
        self.controller.set()

        self.mouse_thread = None
        self.connecting_thread = None

        self.client = Client(self)

        self.screen_ratio = 1
        self.last_time = 0.0

    def update_last_time(self, last_time):
        self.last_time = last_time

    def toggle(self):
        if self.client.connected.value is False:
            self.connect()
        else:
            self.disconnect()

    def connect(self):
        self.client.__init__(self)
        if self.connecting_thread is None:
            self.connecting_thread = threading.Thread(target=self.client.connect_now)
            self.connecting_thread.start()

    def disconnect(self):
        self.end_session()

        self.client.disconnect()
        if self.connecting_thread.is_alive():
            self.connecting_thread.join()
        self.connecting_thread = None

    # def toggle_session(self):
    #     if self.controller.is_set():
    #         self.start_session()
    #     else:
    #         self.end_session()

    def start_session(self):
        if self.mouse_thread is None:
            self.controller.clear()
            self.mouse_thread = threading.Thread(target=self.receive_control_events)
            try:
                self.mouse_thread.start()
            except Exception as e:
                print(f"Start Catch : {e}")
        else:
            print(f"Start Error")

    def end_session(self):
        try:
            self.controller.set()
            if self.mouse_thread is not None and self.mouse_thread.is_alive():
                self.mouse_thread.join()
            self.mouse_thread = None
        except Exception as e:
            print(f"End Session Catch : {e}")

    def receive_control_events(self):
        while not self.controller.is_set():
            data = self.client.receive()
            if data:
                if data.__contains__("clo"):
                    self.disconnect()
                elif data.__contains__("new"):
                    for key in official_virtual_keys:
                        keyboard.release(key)

                events = data.split(";")
                for event in events:
                    if not event == "":
                        if event.__contains__("keyboard"):
                            key_press_performer(event, self.last_time, self.update_last_time)
                        else:
                            mouse_event_performer(event, self.screen_ratio)
