import re
import socket

from Application.UserInterface.LoggingUI.Logging import log_to_logging_file
from Application.Utils.Observation import Observable

rex = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')


class Server(socket.socket):
    HOST = "0.0.0.0"
    PORT = 0

    def __init__(self, context, fam=socket.AF_INET, ty=socket.SOCK_STREAM):
        super().__init__(fam, ty)
        self.context = context
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Enable reuse of the same address

        self.connected = Observable()
        self.connected.add_observer(self.context.on_connected)

        self.client_socket = None
        self.client_address = None
        self.client_disconnection = False

    def run(self):
        try:
            self.HOST = self.context.address.text()
            self.PORT = self.context.port.value()
            if rex.match(self.HOST):
                self.__init__(self.context)
                self.bind((self.HOST, self.PORT))  # bind the socket to a local address and port
                self.listen(1)  # Listen for one connection at a time only
                return True
            else:
                self.context.status.setText("Incorrect Address Format.")
                return False
        except Exception as e:
            log_to_logging_file(f"Server Run Catch : {e}") if self.context.master_window.settings.get_setting("Logging") else None
            return False

    def connect_now(self):
        """ Wait for client to connect """
        try:
            self.connected.value = None
            self.client_socket, self.client_address = self.accept()
            self.connected.value = True

        except Exception as e:
            log_to_logging_file(f"Server 'Connect Now' Catch : {e} "
                                f"You Likely Stopped the Server Before a Successful Connection") \
                if self.context.master_window.settings.get_setting("Logging") else None
            self.context.disconnect()
            return None

    def send_data(self, data: str):
        """ Mouse event handler """
        try:
            if self.connected.value:
                self.client_socket.sendall(data.encode())
                return True
        except Exception as e:
            log_to_logging_file(f"Send Data Catch : {e}") if self.context.master_window.settings.get_setting(
                "Logging") else None
            self.client_disconnection = True
            self.context.stop_listening_to_controls()
            return False

    def stop(self):
        try:
            self.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            log_to_logging_file(f"Server Shutdown Catch : {e}") if self.context.master_window.settings.get_setting(
                "Logging") else None

        try:
            self.close()
            self.connected.value = False
            log_to_logging_file("Server Closed Gracefully") if self.context.master_window.settings.get_setting(
                "Logging") else None
        except Exception as e:
            log_to_logging_file(f"Server Stop Catch: {e}") if self.context.master_window.settings.get_setting(
                "Logging") else None
