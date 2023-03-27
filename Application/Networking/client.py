import socket
from PyQt6.QtGui import QGuiApplication

from Application.Utils.Observation import Observable


class Client(socket.socket):
    CLIENT_HOST = "192.168.1.111"  # Replace with your server's IP address
    CLIENT_PORT = 9999
    BUFFER_SIZE = 1024 * 2

    def __init__(self, context, fam=socket.AF_INET, ty=socket.SOCK_STREAM):
        super().__init__(fam, ty)
        self.context = context

        self.connected = Observable()
        self.connected.value = False
        self.connected.add_observer(self.context.on_connected)

    def connect_now(self):
        """ connects to the given server full address """
        try:
            self.connected.value = None
            self.connect((self.CLIENT_HOST, self.CLIENT_PORT))

            self.context.screen_ratio = self.receive_screen_dims()

            self.connected.value = True
            return
        except Exception as e:
            print(f"Connect Now Catch : {e}"
                  f"\n      You Likely Stopped the Client Before a Successful Connection")
            self.connected.value = False

    def receive_screen_dims(self) -> int:
        try:
            s_size = self.receive()
            c_size = QGuiApplication.primaryScreen().availableGeometry()
            return c_size.width() / int(s_size.split(",")[0])
        except Exception as e:
            print(f"Screen Setup Catch : {e}")

    def receive(self) -> str:
        try:
            data: str = self.recv(self.BUFFER_SIZE).decode()
            if not data:
                return ""

            return data
        except Exception as e:
            print(f"Receive Catch : {e}")
            # self.disconnect()

    def disconnect(self):
        try:
            if self.connected.value:
                self.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print(f"Disconnect Shutdown Catch : {e}")

        try:
            self.close()
        except Exception as e:
            print(f"Disconnect Close Catch : {e}")

        if self.connected.value is not False:
            self.connected.value = False
