import socket
import threading

import mouse
import pyautogui


class Server(socket.socket):
    def __init__(self, context, fam=socket.AF_INET, ty=socket.SOCK_STREAM):
        super().__init__(fam, ty)
        # Global constants
        self.HOST = "192.168.1.100"  # Use all available interfaces
        self.PORT = 9999  # Arbitrary non-privileged port
        self.BUFFER_SIZE = 1024
        self.context = context

        self.connected = False

        self.client_socket = None
        self.client_address = None

        self.controller = threading.Event()

        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Enable reuse of the same address

    def run(self):
        try:
            self.bind((self.HOST, self.PORT))  # bind the socket to a local address and port
            self.listen(1)  # Listen for one connection at a time only
            return True
        except Exception as e:
            print(e)
            return False

    def connect_now(self):
        """ Wait for client to connect """
        try:
            # Wait incoming connection and accept it
            self.client_socket, self.client_address = self.accept()

            # Send screen dimensions to client
            SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
            self.client_socket.sendall(f"{SCREEN_WIDTH},{SCREEN_HEIGHT}".encode())

            print(f"Client {self.client_address[0]}:{self.client_address[1]} is connected.")

            # Update server connection state
            self.connected = True

            # Update UI
            self.context.on_connected()
        except Exception as e:
            print(e)

    def send_data(self, data: str):
        """ Mouse event handler """
        try:
            if isinstance(self.client_socket, socket.socket):
                self.client_socket.sendall(data.encode())
                return None
            else:
                print("socket isn't connected")
        except Exception as e:
            print(e)
        print("disconnected")
        self.connected = False
        self.stop()

    def stop(self):
        mouse.unhook_all()
        try:
            self.shutdown(socket.SHUT_RDWR) # stop connection
        except Exception as e:
            print("Socket Not Connected", e)
        self.close()
