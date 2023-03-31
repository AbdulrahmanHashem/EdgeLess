import re
import socket

from Application.Utils.Observation import Observable

rex = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')

class Client(socket.socket):
    CLIENT_HOST = "0.0.0.0"
    CLIENT_PORT = 0
    BUFFER_SIZE = 1024 * 2  # TODO will be moved into the settings window

    def __init__(self, context, fam=socket.AF_INET, ty=socket.SOCK_STREAM):
        super().__init__(fam, ty)
        self.context = context
        self.CLIENT_HOST = self.context.id.toPlainText()
        self.CLIENT_PORT = self.context.port.value()

        self.connected = Observable()
        self.connected.value = False
        self.connected.add_observer(self.context.on_connected)

        self.client_disconnection = False

    def connect_now(self):
        """ connects to the given server full address """
        try:
            if rex.match(self.CLIENT_HOST):
                self.connected.value = None
                self.connect((self.CLIENT_HOST, self.CLIENT_PORT))
                self.connected.value = True
                return
            else:
                print("Incorrect address format")
        except Exception as e:
            print(f"Connect Now Catch : {e}"
                  f"\n      You Likely Stopped the Client Before a Successful Connection")
            self.connected.value = False

    def receive(self) -> str:
        try:
            data: str = self.recv(self.BUFFER_SIZE).decode()
            return data
        except socket.error as e:
            print(f"Receive Catch : {e}")
            self.client_disconnection = True
            self.context.disconnect()
            self.context.release_shortcut()

            return ""

    def disconnect(self):
        try:
            self.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print(f"Client Shutdown Catch : {e}")

        try:
            self.close()
            self.connected.value = False
        except Exception as e:
            print(f"Client Close Catch : {e}")
