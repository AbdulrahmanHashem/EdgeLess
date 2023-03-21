import socket

from PyQt6.QtGui import QGuiApplication


class Client(socket.socket):
    def __init__(self, fam=socket.AF_INET, ty=socket.SOCK_STREAM):
        super().__init__(fam, ty)
        # Global constants
        self.SERVER_HOST = "192.168.1.111"  # Replace with your server's IP address
        self.SERVER_PORT = 9999
        self.BUFFER_SIZE = 1024
        # Create client socket and connect to server

    def connect_now(self, on_connect: ()):
        """ connects to the given server full address """
        try:
            self.settimeout(10)
            print(f"Attempting to connect to {self.SERVER_HOST}, {self.SERVER_PORT}")
            self.connect((self.SERVER_HOST, self.SERVER_PORT))
            on_connect()
        except socket.timeout as timeout:
            print(timeout)
            return False
        except Exception as e:
            print(e)
            return False

    def receive(self) -> str:
        data: str = self.recv(self.BUFFER_SIZE).decode()
        if not data:  # No data received means the client has disconnected
            return ""

        print(data)
        return data
        # all_data = data.split(";")
        # for entry in all_data:
        #     # check if the test string matches the pattern
        #     if re.match(r"\w+(,\w+){2}", entry):
        #         self.handle_mouse_event(entry)

    def disconnect(self, on_disconnect: ()):
        try:
            self.getpeername()
            self.shutdown(socket.SHUT_RDWR) # stop connection
        except Exception as e:
            print("Socket Not Connected")

        self.close()

        on_disconnect()
