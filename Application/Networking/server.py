import socket
import threading

import mouse
import pyautogui

from Application.Utils.Observation import Observable


class Server(socket.socket):
    # Global constants
    HOST = "192.168.1.100"  # Use all available interfaces
    PORT = 9999  # Arbitrary non-privileged port
    BUFFER_SIZE = 1024

    def __init__(self, context, fam=socket.AF_INET, ty=socket.SOCK_STREAM):
        super().__init__(fam, ty)
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Enable reuse of the same address

        self.context = context

        # connection state
        self.connected = Observable()
        self.connected.value = False
        self.connected.add_observer(self.context.on_connected)

        self.client_socket = None
        self.client_address = None

    def run(self):
        try:
            self.bind((self.HOST, self.PORT))  # bind the socket to a local address and port
            self.listen(1)  # Listen for one connection at a time only
            self.connected.value = None
            return True
        except Exception as e:
            print(f"Running Server : {e}")
            return False

    def connect_now(self):
        """ Wait for client to connect """
        try:
            # Wait incoming connection and accept it
            self.client_socket, self.client_address = self.accept()
            print(self.client_socket)
            print(f"Client {self.client_address[0]}:{self.client_address[1]} is connected.")

            self.send_screen_dims()

            # Update server connection state
            self.connected.value = True
        except Exception as e:
            self.connected.value = False
            print(f"Connecting Catch : {e}")

    def send_screen_dims(self):
        # Send screen dimensions to client
        SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
        self.send_data(f"{SCREEN_WIDTH},{SCREEN_HEIGHT}")

    def send_data(self, data: str):
        """ Mouse event handler """
        try:
            if isinstance(self.client_socket, socket.socket):
                self.client_socket.sendall(data.encode())
                return None
            else:
                print("Sending Data Error : Socket Is Destroyed")
                self.connected.value = False
                self.stop()
        except Exception as e:
            print(f"Sending Data Catch : {e}")

    def stop(self):
        try:
            if self.connected.value:
                # stop connection
                self.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print(f"Shutdown Catch : {e}")

        try:
            self.close()
            self.connected.value = False
        except Exception as e:
            print(f"Close Catch: {e}")
