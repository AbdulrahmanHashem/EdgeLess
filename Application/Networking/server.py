import socket
import threading
import time
from inspect import Traceback

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

        self.client_disconnect = False
        # connection state
        self.connected = Observable()
        self.connected.value = False
        self.connected.add_observer(self.context.on_connected)

        self.client_socket = None
        self.client_address = None
        self.last_sent = ""

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
            # Wait incoming connection and accept it
            try:
                self.connected.value = None
                self.client_socket, self.client_address = self.accept()
            except Exception as e:
                print(f"Server 'Connect Now' Catch : {e}"
                      f"\n      You Likely Stopped the Server Before a Successful Connection")
                return None

            # print(self.client_socket)
            print(f"Client {self.client_address[0]}:{self.client_address[1]} is connected.")

            # Update server connection state
            self.connected.value = True

            self.send_screen_dims()
        except Exception as e:
            self.connected.value = False
            print(f"Server 'Connect Now' Unknown Catch : {e}")

    def send_screen_dims(self):
        # Send screen dimensions to client
        SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
        self.send_data(f"{SCREEN_WIDTH},{SCREEN_HEIGHT}")

    def send_data(self, data: str):
        """ Mouse event handler """
        try:
            if isinstance(self.client_socket, socket.socket) and self.connected.value:
                self.client_socket.sendall(data.encode())
                self.last_sent = data
                return None
            else:
                if data != "close":
                    print("Sending Data Error : Socket Is Not Connected or It's Destroyed")
        except socket.error:
            print("Server Disconnected Shutdown Now")
            # self.context.session.set()
            self.context.disconnect()
            self.client_disconnect = True
            self.context.require_rest()
        except Exception as e:
            print(f"Sending Data Catch : {e}")
            if self.connected.value:
                self.context.disconnect()

    def stop(self):
        try:
            if self.connected.value:
                # stop connection
                self.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            if self.last_sent != "close":
                print(f"Server Shutdown Catch : {e}")

        try:
            self.close()
            self.connected.value = False
            print("Server Closed Gracefully")
        except Exception as e:
            print(f"Server Stop Catch: {e}")
