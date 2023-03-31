import socket

from Application.Utils.Observation import Observable


class Server(socket.socket):
    HOST = str(socket.gethostbyname_ex(socket.gethostname())[2][-1])  # Use all available interfaces
    PORT = 9999  # Arbitrary non-privileged port
    BUFFER_SIZE = 1024 * 2

    def __init__(self, context, fam=socket.AF_INET, ty=socket.SOCK_STREAM):
        super().__init__(fam, ty)
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Enable reuse of the same address
        self.context = context

        self.HOST = self.context.address.text()
        self.PORT = self.context.port.value()

        # connection state
        self.connected = Observable()
        self.connected.add_observer(self.context.on_connected)

        self.client_socket = None
        self.client_address = None
        self.last_sent = ""
        self.client_disconnection = False

    def run(self):
        try:
            self.__init__(self.context)
            self.bind((self.HOST, self.PORT))  # bind the socket to a local address and port
            self.listen(1)  # Listen for one connection at a time only
            return True
        except Exception as e:
            print(f"Server Run Catch : {e}")
            return False

    def connect_now(self):
        """ Wait for client to connect """
        try:
            self.connected.value = None
            self.client_socket, self.client_address = self.accept()
            self.connected.value = True

        except Exception as e:
            print(f"Server 'Connect Now' Catch : {e}"
                  f"\n      You Likely Stopped the Server Before a Successful Connection")
            self.context.disconnect()
            return None

    def send_data(self, data: str):
        """ Mouse event handler """
        try:
            if self.connected.value:
                self.client_socket.sendall(data.encode())
                self.last_sent = data
                return True
        except Exception as e:
            print(f"Send Data Catch : {e}")
            self.client_disconnection = True
            self.context.disconnect()
            return False

    def stop(self):
        try:
            self.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print(f"Server Shutdown Catch : {e}")

        try:
            self.close()
            self.connected.value = False
            print("Server Closed Gracefully")
        except Exception as e:
            print(f"Server Stop Catch: {e}")
