import socket
import sys
import threading
import pyautogui
import keyboard
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import QtWidgets

# Send screen dimensions to client
# client_socket.sendall(f"{SCREEN_WIDTH},{SCREEN_HEIGHT}".encode())


class Server:
    def __init__(self):
        self.controller = threading.Event()
        # Global constants
        self.HOST = ''  # Use all available interfaces
        self.PORT = 80  # Arbitrary non-privileged port
        self.BUFFER_SIZE = 1024

        # Create server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Enable reuse of the same address
        # self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)  # Enable reuse of the same address

        self.server_socket.bind((self.HOST, self.PORT))  # bind the socket to a local address and port
        # self.server_socket.setblocking(False)  # set the socket to non-blocking mode
        self.server_socket.listen(5)  # Listen for one connection at a time only
        print(f"Server started and listening on port {self.PORT}...")

        # Wait for client to connect
        self.client_socket, self.client_address = self.server_socket.accept()
        print(f"Client {self.client_address[0]}:{self.client_address[1]} is connected.")

        self.xa = 0
        self.ya = 0

    def handle_mouse_event(self, x, y, button):
        """ Mouse event handler """
        data = f"{x},{y},{button};"
        # message = data
        self.client_socket.sendall(data.encode())

    # # Keyboard event handler
    # def handle_keyboard_event(self, event_type, key, action):
    #     data = f"{key},{action}"
    #     message = f"{event_type}:{data}"
    #     self.client_socket.sendall(message.encode())

    def listen_for_mouse_events(self):
        """ Start mouse event listener thread """
        self.controller.clear()
        while not self.controller.is_set():
            # left_button, right_button, middle_button = pyautogui.mouseDown()
            #
            # # Listen for left mouse button press and release
            # if left_button:
            #     handle_mouse_event("mouse", x, y, "left")
            #     while pyautogui.mouseDown()[0]:
            #         pass
            #
            # # Listen for right mouse button press and release
            # if right_button:
            #     handle_mouse_event("mouse", x, y, "right")
            #     while pyautogui.mouseDown()[1]:
            #         pass
            #
            # # Listen for middle mouse button press and release
            # if middle_button:
            #     handle_mouse_event("mouse", x, y, "middle")
            #     while pyautogui.mouseDown()[2]:
            #         pass

            # Listen for mouse movement
            # print(self.xa, self.ya, "location")

            new_x, new_y = pyautogui.position()
            if new_x != self.xa or new_y != self.ya:
                self.xa, self.ya = new_x, new_y
                print(new_x, new_y, "location")
                self.handle_mouse_event(new_x, new_y, "move")
                self.controller.wait(0.09)

    # def listen_for_keyboard_events(self):
    #     while not self.controller.is_set():
    #         event = keyboard.read_event()
    #         key = event.name
    #         action = event.event_type
    #
    #         # Special keys need to be handled differently
    #         if key in ["ctrl", "alt", "shift", "win"]:
    #             key = key.upper()
    #
    #         self.handle_keyboard_event("keyboard", key, action)

    def run(self):
        """ Mouse listener threads """
        self.mouse_listener = threading.Thread(target=self.listen_for_mouse_events)
        self.mouse_listener.daemon = True  # Thread dies when main program exits
        try:
            self.mouse_listener.start()
        except Exception:
            print(Exception)

        # self.keyboard_listener = threading.Thread(target=self.listen_for_keyboard_events)
        # self.keyboard_listener.daemon = True  # Thread dies when main program exits
        # try:
        #     self.keyboard_listener.start()
        # except Exception:
        #     print(Exception)
    def stop(self):
        if self.mouse_listener.is_alive() and not self.controller.is_set():
            self.controller.set()
            self.mouse_listener.join()
            # self.keyboard_listener.join()

            print(f"Client {self.client_address[0]}:{self.client_address[1]} has disconnected.")
            self.client_socket.close()
            self.server_socket.close()


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.switch = QtWidgets.QPushButton()
        self.setCentralWidget(self.switch)

        self.switch.setText("Start server")
        self.switch.setMinimumWidth(200)

        self.server = None
        self.switch.clicked.connect(self.toggle_server)

    def toggle_server(self):
        if self.server is None:
            self.switch.setText("Stop")
            self.server = Server()
            self.server.run()
        else:
            self.switch.setText("Start server")
            self.server.stop()
            self.server = None


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())


