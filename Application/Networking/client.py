import socket
from PyQt6.QtGui import QGuiApplication


class Client(socket.socket):
    def __init__(self, context, fam=socket.AF_INET, ty=socket.SOCK_STREAM):
        super().__init__(fam, ty)
        self.context = context
        self.SERVER_HOST = "192.168.1.111"  # Replace with your server's IP address
        self.SERVER_PORT = 9999
        self.BUFFER_SIZE = 1024*2

    def connect_now(self):
        """ connects to the given server full address """
        try:
            print(f"Attempting to connect to {self.SERVER_HOST}, {self.SERVER_PORT}")
            self.context.update_status_change("Connecting")
            self.connect((self.SERVER_HOST, self.SERVER_PORT))
            self.context.on_connect()
            return
        except socket.timeout as timeout:
            print(timeout)
        except Exception as e:
            print(e)

        self.context.update_status_change("Connect")

    def receive_screen_dims(self) -> int:
        s_size = self.recv(self.BUFFER_SIZE).decode()
        c_size = QGuiApplication.primaryScreen().availableGeometry()
        return c_size.width() / int(s_size.split(",")[0])

    def receive(self) -> str:
        try:
            data: str = self.recv(self.BUFFER_SIZE).decode()
            if not data:
                return ""

            return data
        except Exception as e:
            print(e)
            self.disconnect()

    def disconnect(self):
        try:
            self.getpeername()
            self.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print("Socket Not Connected")

        self.close()

        self.context.update_status_change("Connect")
        self.context.controller.set()

