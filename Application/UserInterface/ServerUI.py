import socket
import threading

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from Application.Networking.server import Server


class ServerWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        main_widget = QtWidgets.QWidget()
        v_layout = QtWidgets.QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # address:port text
        self.address_port = QtWidgets.QLabel("")
        v_layout.addWidget(self.address_port, alignment=Qt.AlignmentFlag.AlignCenter)

        # server start button
        self.start = QtWidgets.QPushButton("Start Server")
        v_layout.addWidget(self.start, alignment=Qt.AlignmentFlag.AlignCenter)

        # make a server instance
        self.server = Server()
        # socket.gethostbyname(socket.gethostname())

        self.start.clicked.connect(self.toggle_server)
        # address_port.setText(str(server.getsockname()))

    def toggle_server(self):
        if self.start.text() == "Start Server":
            self.server.__init__()
            if self.server.run():
                self.address_port.setText(str(self.server.getsockname()))
                self.start.setText("Stop Server")
                self.connect()  # start connecting
        else:
            self.server.stop()
            self.address_port.setText("")
            self.start.setText("Start Server")

    def connect(self):
        def on_connected():
            self.address_port.setText(
                self.address_port.text() + "\n" + self.server.client_socket + " : " + self.server.client_address)
        mouse_thread = threading.Thread(target=lambda: self.server.connect_now(on_connected))
        mouse_thread.daemon = True
        try:
            mouse_thread.start()
        except Exception as e:
            print(e)
