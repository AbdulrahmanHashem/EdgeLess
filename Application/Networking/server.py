import socket
import threading
import pyautogui
from mouse import MoveEvent


class Server(socket.socket):
    def __init__(self, fam=socket.AF_INET, ty=socket.SOCK_STREAM):
        super().__init__(fam, ty)
        # Global constants
        self.HOST = socket.gethostbyname_ex(socket.gethostname())[2][3]  # Use all available interfaces
        self.PORT = 9999  # Arbitrary non-privileged port
        self.BUFFER_SIZE = 1024
        self.connected = False

        self.client_socket = None
        self.client_address = None

        self.controller = threading.Event()

        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Enable reuse of the same address

    def run(self):
        try:
            self.bind((self.HOST, self.PORT))  # bind the socket to a local address and port
            self.listen(1)  # Listen for one connection at a time only
            return True
        except Exception as e:
            print(e)
            return False

    def connect_now(self, on_connected):
        """ Wait for client to connect """
        try:
            self.client_socket, self.client_address = self.accept()
            SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
            self.client_socket.sendall(f"{SCREEN_WIDTH},{SCREEN_HEIGHT}".encode())  # Send screen dimensions to client
            print(f"Client {self.client_address[0]}:{self.client_address[1]} is connected.")
            self.connected = True
            on_connected()
        except Exception as e:
            print(e)

    def send_data(self, data: str):
        """ Mouse event handler """
        try:
            if isinstance(self.client_socket, socket.socket):
                self.client_socket.sendall(data.encode())
                return None
            else:
                print("socket isn't connected")
        except Exception as e:
            print(e)
        print("disconnected")
        self.connected = False

    def stop(self):
        try:
            self.shutdown(socket.SHUT_RDWR) # stop connection
        except Exception as e:
            print("Socket Not Connected", e)

        self.close()
