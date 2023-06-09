import re
import socket

from Application.UserInterface.LoggingUI.Logging import log_to_logging_file
from Application.Utils.Observation import Observable

rex = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')


class Client(socket.socket):
    HOST = "0.0.0.0"
    PORT = 0

    def __init__(self, context, fam=socket.AF_INET, ty=socket.SOCK_STREAM):
        super().__init__(fam, ty)
        self.context = context
        self.BUFFER_SIZE = self.context.master_window.settings.get_setting("Buffer Size")

        self.connected = Observable()
        self.connected.add_observer(self.context.on_connected)

        self.connected.value = False
        self.client_disconnection = False

    def connect_now(self):
        """ connects to the given server full address """
        try:
            self.HOST = self.context.id.toPlainText()
            self.PORT = self.context.port.value()
            if rex.match(self.HOST):
                self.connected.value = None
                self.connect((self.HOST, self.PORT))
                self.connected.value = True
                return
            else:
                self.context.state.setText("Incorrect Address Format.")
                return
        except Exception as e:
            log_to_logging_file(f"Connect Now Catch : {e}"
                                f"You Likely Stopped the Client Before a Successful Connection") \
                if self.context.master_window.settings.get_setting("Logging") else None
            self.connected.value = False

    def receive(self) -> str:
        try:
            data: str = self.recv(self.BUFFER_SIZE).decode()
            return data
        except socket.error as e:
            log_to_logging_file(f"Receive Catch : {e}") if self.context.master_window.settings.get_setting(
                "Logging") else None
            self.client_disconnection = True
            self.context.disconnect()
            self.context.release_shortcut()

            return ""

    def disconnect(self):
        try:
            self.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            log_to_logging_file(f"Client Shutdown Catch : {e}") if self.context.master_window.settings.get_setting(
                "Logging") else None

        try:
            self.close()
            self.connected.value = False
        except Exception as e:
            log_to_logging_file(f"Client Close Catch : {e}") if self.context.master_window.settings.get_setting(
                "Logging") else None
