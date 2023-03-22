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
        mouse_thread = threading.Thread(target=self.receive_mouse_events())
        mouse_thread.daemon = True
        mouse_thread.start()

    def receive_mouse_events(self):
        while not self.controller.is_set():
            data = self.client.receive()

            if data.strip().__contains__("clo"):
                self.client.send("ok")
                self.client.disconnect(lambda: self.switch.setText("Connect"))

            all_data = data.split(";")
            for entry in all_data:
                if not entry == "":
                    self.handle_mouse_event(entry)
                    self.controller.wait(0.01)
                # check if the test string matches the pattern

    def handle_mouse_event(self, data):
        """ Mouse event handler """
        # button, x, y, t = data.split(",")

        # Perform mouse action based on button value
        if data.__contains__("Move"):
            button, x, y, t = data.split(",")
            x = int(x) * self.screen_ratio
            y = int(y) * self.screen_ratio
            mouse.play([mouse.MoveEvent(x=x, y=y, time=t)], 0)
        elif data.__contains__("Button"):
            button, x, y, t = data.split(",")
            try:
                mouse.play([mouse.ButtonEvent(event_type=x.strip(), button=y.strip(), time=t)], 0)
            except Exception as e:
                print(e)
        else:
            button, delta, t = data.split(",")
            try:
                mouse.play([mouse.WheelEvent(delta=delta.strip(), time=t.strip())])
            except Exception as e:
                print(e)