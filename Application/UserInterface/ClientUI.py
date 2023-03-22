import threading

import mouse
from PyQt6.QtWidgets import QMainWindow, QPushButton

from Application.Networking.client import Client


class ClientWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.switch = QPushButton()
        self.setCentralWidget(self.switch)
        self.switch.setText("Connect")

        self.switch.clicked.connect(self.connect)

        self.controller = threading.Event()
        # self.connecting = threading.Event()

        self.client = Client()
        self.screen_ratio = 1

    def connect(self):
        def status_change(status_string: str):
            self.switch.setText(status_string)

        def on_connect():
            self.switch.setText("Disconnect")
            # self.client.settimeout(0)
            self.screen_ratio = self.client.receive_screen_dims()
            self.start()

        def on_disconnect():
            self.switch.setText("Connect")

        self.client.__init__()
        connect = threading.Thread(
            target=lambda: self.client.connect_now(on_connect, status_change)
            if
            self.switch.text() == "Connect"
            else
            self.client.disconnect(on_disconnect)
        )
        connect.daemon = True
        connect.start()

    def start(self):
        mouse_thread = threading.Thread(target=self.listen_for_mouse_events())
        mouse_thread.daemon = True
        mouse_thread.start()

    def listen_for_mouse_events(self):
        # self.last_pressed = ["", ""]
        while not self.controller.is_set():
            data = self.client.receive()
            all_data = data.split(";")
            for entry in all_data:
                if not entry == "":
                    self.handle_mouse_event(entry)
                    self.controller.wait(0.01)
                # check if the test string matches the pattern

    def handle_mouse_event(self, data):
        """ Mouse event handler """
        # print(f"'{data}'")
        button, x, y = data.split(",")

        # Perform mouse action based on button value
        if button == "MoveEvent":
            x = int(x) * self.screen_ratio
            y = int(y) * self.screen_ratio
            mouse.play([mouse.MoveEvent(x=x, y=y, time=0)], 0)
        elif button == "ButtonEvent":
            try:
                mouse.play([mouse.ButtonEvent(event_type=x.strip(), button=y.strip(), time=0)], 0)
            except Exception as e:
                print(e)
        else:
            try:
                mouse.play([mouse.WheelEvent(x.strip(), y.strip())])
            except Exception as e:
                print(e)