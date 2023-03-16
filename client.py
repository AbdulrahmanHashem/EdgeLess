import re
import socket
import sys
import threading
import pyautogui
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication


class Client:
    def __init__(self):
        super().__init__()
        self.controller = threading.Event()
        self.connecting = threading.Event()
        # Global constants
        self.SERVER_HOST = "192.168.1.111"  # Replace with your server's IP address
        self.SERVER_PORT = 9999
        self.BUFFER_SIZE = 1024
        self.screen_ratio = 1
        # Create client socket and connect to server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def handle_mouse_event(self, data):
        """ Mouse event handler """
        x, y, button = data.split(",")
        x = int(x)*self.screen_ratio
        y = int(y)*self.screen_ratio

        # Perform mouse action based on button value
        if button in ["left", "right", "middle"]:
            pyautogui.click(x=x, y=y, button=button)
        elif button == "move":
            pyautogui.moveTo(x=x, y=y, duration=0.1)
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

    def listen_for_mouse_events(self):
        self.client_socket.connect((self.SERVER_HOST, self.SERVER_PORT))
        size = self.client_socket.recv(self.BUFFER_SIZE).decode()
        c_width, c_height = pyautogui.size()
        self.screen_ratio = c_width/int(size.split(",")[0])

        while not self.controller.is_set():
            # self.client_socket.
            data = self.client_socket.recv(self.BUFFER_SIZE).decode()
            if not data:  # No data received means the client has disconnected
                break

            all_data = data.split(";")
            for entry in all_data:
                # check if the test string matches the pattern
                if re.match(r"\w+(,\w+){2}", entry):
                    self.handle_mouse_event(entry)
                    # elif event_type == "keyboard":
                    #     self.handle_keyboard_event(payload)

    def connect(self):
        # Receive data from client and handle mouse and keyboard events
        self.mouse_listener = threading.Thread(target=self.listen_for_mouse_events)
        self.mouse_listener.daemon = True  # Thread dies when main program exits
        try:
            self.mouse_listener.start()
        except Exception:
            print(Exception)

    def stop(self):
        if self.mouse_listener.is_alive() and not self.controller.is_set():
            self.controller.set()
            self.mouse_listener.join()
            self.client_socket.close()
            print(f"disconnected.")


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.switch = QPushButton()
        self.setCentralWidget(self.switch)
        self.switch.setText("Start client")
        self.client = None

        self.switch.clicked.connect(self.toggle_client)

    def toggle_client(self):
        if self.client is None:
            self.switch.setText("Stop")
            self.client = Client()
            self.client.connect()
        else:
            self.switch.setText("Start client")
            self.client.stop()
            self.client = None


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())
