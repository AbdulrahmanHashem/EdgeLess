import socket
import threading
import pyautogui


class Server(socket.socket):
    def __init__(self, fam=socket.AF_INET, ty=socket.SOCK_STREAM):
        super().__init__(fam, ty)
        # Global constants
        self.HOST = socket.gethostbyname(socket.gethostname())  # Use all available interfaces
        self.PORT = 9999  # Arbitrary non-privileged port
        self.BUFFER_SIZE = 1024
        self.client_socket, self.client_address = "", ""

        self.controller = threading.Event()

        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Enable reuse of the same address
        # SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
        # self.client_socket.sendall(f"{SCREEN_WIDTH},{SCREEN_HEIGHT}".encode())  # Send screen dimensions to client

    def run(self):
        try:
            self.bind((self.HOST, self.PORT))  # bind the socket to a local address and port
            self.listen(1)  # Listen for one connection at a time only
            return True
        except Exception as e:
            print(e)
            return False

    def connect_now(self, on_connected):
        """ Wait for client to connect """
        try:
            self.client_socket, self.client_address = self.accept()
            print(f"Client {self.client_address[0]}:{self.client_address[1]} is connected.")
            on_connected()
        except Exception as e:
            print(e)

    def send_data(self, data):
        """ Mouse event handler """
        if isinstance(self.client_socket, socket.socket):
            self.client_socket.sendall(data.encode())
        else:
            print("socket isn't connected")

    def stop(self):
        try:
            self.getpeername()
            self.shutdown(socket.SHUT_RDWR) # stop connection
        except Exception as e:
            print("Socket Not Connected")

        self.close()


# import socket
# import typing
# import PyQt6.sip
# from PyQt6.QtCore import QDataStream, QIODevice, QByteArray
# from PyQt6.QtNetwork import QTcpServer, QTcpSocket, QHostAddress, QAbstractSocket, QNetworkProxy
#
# class Server(QTcpServer):
#     def __init__(self):
#         super().__init__()
#         self.current_client_socket = None
#
#     def start_server(self):
#         # listen for incoming connections
#         if not self.listen(QHostAddress.SpecialAddress, 1234): # set in settings
#             print("Error: could not start server")
#             exit(1)
#
#     def accept_new_connection(self) -> 'QTcpSocket':
#         self.current_client_socket = self.nextPendingConnection()
#         return self.current_client_socket
#
#     def create_data_stream(self):
#         return QDataStream(self.current_client_socket)
#
#     def receive_from_stream(self, stream: QDataStream):
#         # receive data from the client
#         data = QByteArray()
#         stream.startTransaction()
#         stream >> data
#         if not stream.commitTransaction():
#             print("Error: could not receive data from client")
#             return "Error: could not receive data from client"
#         else:
#             return data.data()
#
#
#     def send_through_stream(self, stream: QDataStream, data: str):
#         # send data back to the client
#         stream.startTransaction()
#         stream << data
#         stream.commitTransaction()
#
#     def hasPendingConnections(self) -> bool:
#         return super().hasPendingConnections()
#
#     def waitForNewConnection(self, msecs: int = ...) -> typing.Tuple[bool, bool]:
#         return super().waitForNewConnection(msecs)
#
#     def setSocketDescriptor(self, socketDescriptor: PyQt6.sip.voidptr) -> bool:
#         return super().setSocketDescriptor(socketDescriptor)
#
#     def socketDescriptor(self) -> PyQt6.sip.voidptr:
#         return super().socketDescriptor()
#
#     def setMaxPendingConnections(self, numConnections: int) -> None:
#         super().setMaxPendingConnections(numConnections)
#
#     def isListening(self) -> bool:
#         return super().isListening()
#
#     def errorString(self) -> str:
#         return super().errorString()
#
#     def serverError(self) -> QAbstractSocket.SocketError:
#         return super().serverError()
#
#     def close(self) -> None:
#         super().close()
