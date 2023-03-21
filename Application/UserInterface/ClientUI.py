import sys
import threading
import pyautogui
from PyQt6.QtWidgets import QMainWindow, QPushButton, QApplication

from Application.Networking.client import Client


class ClientWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.switch = QPushButton()
        self.setCentralWidget(self.switch)
        self.switch.setText("Connect")

        self.switch.clicked.connect(self.connect)

        self.controller = threading.Event()
        self.connecting = threading.Event()

        self.client = Client()
        self.screen_ratio = 1

        # ssize = self.recv(self.BUFFER_SIZE).decode()
        # csize = QGuiApplication.primaryScreen().availableGeometry()
        # self.screen_ratio = csize.width()/int(size.split(",")[0])

    def connect(self):
        def on_connect():
            self.switch.setText("Disconnect")

        def on_disconnect():
            self.switch.setText("Connect")

        self.client.__init__()
        connect = threading.Thread(
            target=lambda:
            self.client.connect_now(on_connect)
            if
            self.switch.text() == "Connect"
            else
            self.client.disconnect(on_disconnect)
        )

        connect.daemon = True
        connect.start()

    def listen_for_mouse_events(self):
        while not self.controller.is_set():
            pass

    def handle_mouse_event(self, data):
        """ Mouse event handler """
        x, y, button = data.split(",")
        x = int(x) * self.screen_ratio
        y = int(y) * self.screen_ratio

        # # Perform mouse action based on button value
        # if button in ["left", "right", "middle"]:
        #     pyautogui.click(x=x, y=y, button=button)
        # elif button == "move":
        #     pyautogui.moveTo(x=x, y=y, duration=0.1)
