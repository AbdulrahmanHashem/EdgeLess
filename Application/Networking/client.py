import socket

from PyQt6.QtGui import QGuiApplication


class Client(socket.socket):
    def __init__(self, fam=socket.AF_INET, ty=socket.SOCK_STREAM):
        super().__init__(fam, ty)
        # Global constants
        self.SERVER_HOST = "192.168.1.111"  # Replace with your server's IP address
        self.SERVER_PORT = 9999
        self.BUFFER_SIZE = 1024*2
        # Create client socket and connect to server

    def connect_now(self, on_connect: (), status_change: ()):
        """ connects to the given server full address """
        try:
            print(f"Attempting to connect to {self.SERVER_HOST}, {self.SERVER_PORT}")
            status_change("Connecting")
            self.connect((self.SERVER_HOST, self.SERVER_PORT))
            on_connect()
            return
        except socket.timeout as timeout:
            print(timeout)
        except Exception as e:
            print(e)

        status_change("Connect")

    def receive_screen_dims(self) -> int:
        s_size = self.recv(self.BUFFER_SIZE).decode()
        c_size = QGuiApplication.primaryScreen().availableGeometry()
        return c_size.width() / int(s_size.split(",")[0])

    def receive(self) -> str:
        try:
            data: str = self.recv(self.BUFFER_SIZE).decode()
            if not data:  # No data received means the client has disconnected
                return ""

            return data
        except Exception as e:
            print(e)

    def disconnect(self, on_disconnect: ()):
        try:
            self.getpeername()
            self.shutdown(socket.SHUT_RDWR) # stop connection
        except Exception as e:
            print("Socket Not Connected")

        self.close()

        on_disconnect()
