import socket

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

        self.client_disconnection = False

    def connect_now(self):
        """ connects to the given server full address """
        try:
            self.connected.value = None
            self.connect((self.CLIENT_HOST, self.CLIENT_PORT))
            self.connected.value = True
            return
        except Exception as e:
            print(f"Connect Now Catch : {e}"
                  f"\n      You Likely Stopped the Client Before a Successful Connection")
            self.connected.value = False

    def receive(self) -> str:
        try:
            data: str = self.recv(self.BUFFER_SIZE).decode()
            if data == "" or data.__contains__("clo"):
                self.client_disconnection = True
                self.context.disconnect()
                self.context.release_shortcut()

                return ""
            elif data.__contains__("new"):
                self.context.release_shortcut()

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
            print(f"Disconnect Shutdown Catch : {e}")

        try:
            self.close()
            self.connected.value = False
        except Exception as e:
            print(f"Disconnect Close Catch : {e}")
