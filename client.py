import re
import socket
import threading

import pyautogui
from PyQt5.QtWidgets import QMainWindow


class Client(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = threading.Event()
        # Global constants
        self.SERVER_HOST = "192.168.1.100"  # Replace with your server's IP address
        self.SERVER_PORT = 9999
        self.BUFFER_SIZE = 1024

        # Create client socket and connect to server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.SERVER_HOST, self.SERVER_PORT))


    def validate(self, string):
        # define the pattern
        # pattern = r"\w{4,}:\w,\w,\w{4,}"
        pattern = r"\w+(,\w+){2}"

        # check if the test string matches the pattern
        if re.match(pattern, string):
            return True
        else:
            return False


    # Mouse event handler
    def handle_mouse_event(self, data):
        x, y, button = data.split(",")
        x = int(x)
        y = int(y)

        # Perform mouse action based on button value
        if button in ["left", "right", "middle"]:
            pyautogui.click(x=x, y=y, button=button)
        elif button == "move":
            pyautogui.moveTo(x=x, y=y)

    # # Keyboard event handler
    # def handle_keyboard_event(self, data):
    #     key, action = data.split(",")
    #     key = key.strip()
    #     action = action.strip()
    #
    #     # Perform keyboard action based on key and action values
    #     if action == "down":
    #         pyautogui.keyDown(key)
    #     elif action == "up":
    #         pyautogui.keyUp(key)
    #     else:
    #         pyautogui.press(key)
    def connect(self):
        # Receive data from client and handle mouse and keyboard events
            while not self.controller.is_set():
                data = self.client_socket.recv(self.BUFFER_SIZE).decode()
                if not data:  # No data received means the client has disconnected
                    break

                all_data = data.split(";")
                for entry in all_data:
                    if self.validate(entry):
                        print(entry)
                        # event_type, payload = entry.split(":")
                        # if event_type == "mouse":
                        self.handle_mouse_event(entry)
                        # elif event_type == "keyboard":
                        #     self.handle_keyboard_event(payload)

    def stop(self):
        print(f"disconnected.")
        self.client_socket.close()
