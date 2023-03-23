import threading

import mouse
from PyQt6.QtWidgets import QMainWindow, QPushButton

from Application.EventListeners.keyboard_events import key_press_performer
from Application.EventListeners.mouse_events import mouse_event_performer
from Application.Networking.client import Client


class ClientWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.switch = QPushButton()
        self.setCentralWidget(self.switch)
        self.switch.setText("Connect")

        self.switch.clicked.connect(self.connect)

        self.controller = threading.Event()

        self.client = Client()
        self.screen_ratio = 1
        self.last_time = 0.0

    def update_last_time(self, last_time):
        self.last_time = last_time

    def connect(self):
        def status_change(status_string: str):
            self.switch.setText(status_string)

        def on_connect():
            self.switch.setText("Disconnect")
            # self.client.settimeout(0)
            self.screen_ratio = self.client.receive_screen_dims()
            self.start()

        self.client.__init__()
        connect = threading.Thread(
            target=lambda: self.client.connect_now(on_connect, status_change)
            if
            self.switch.text() == "Connect"
            else
            self.client.disconnect(lambda: self.switch.setText("Connect"))
        )
        connect.daemon = True
        connect.start()

    def start(self):
        mouse_thread = threading.Thread(target=self.receive_mouse_events)
        mouse_thread.daemon = True
        mouse_thread.start()

    def receive_mouse_events(self):
        while not self.controller.is_set():
            data = self.client.receive()
            if data:
                if data.strip().__contains__("clo"):
                    self.client.send("ok")
                    self.client.disconnect(lambda: self.switch.setText("Connect"))

                all_data = data.split(";")
                for entry in all_data:
                    if not entry == "":
                        if entry.__contains__("keyboard"):
                            key_press_performer(entry, self.last_time, self.update_last_time)
                        else:
                            mouse_event_performer(entry, self.screen_ratio)
