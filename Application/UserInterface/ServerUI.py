import threading

import mouse
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

from Application.EventListeners.mouse_events import listen_to_lc, listen_to_rc, listen_to_mm, listen_to_mc, listen_to_ws
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

        self.start.clicked.connect(self.toggle_server)

        self.mouse_loc = (0, 0)
        self.controller = threading.Event()

    def toggle_server(self) -> None:
        if self.start.text() == "Start Server":
            self.server.__init__()
            self.controller.clear()
            if self.server.run():
                self.address_port.setText(str(self.server.getsockname()))
                self.start.setText("Stop Server")
                self.connect()  # start connecting
        else:
            self.controller.set()
            self.server.stop()
            self.address_port.setText("")
            self.start.setText("Start Server")

    def connect(self) -> None:
        def on_connected():
            self.address_port.setText(
                self.address_port.text() + "\n" + "Connected to" + "\n" + str(self.server.client_address[0]) + " : " + str(self.server.client_address[1]))
            self.start_sending()

        connect_thread = threading.Thread(target=lambda: self.server.connect_now(on_connected))
        connect_thread.daemon = True
        try:
            connect_thread.start()
        except Exception as e:
            print(e)

    def start_sending(self) -> None:
        def listen_to_mouse():
            listen_to_lc(self.server.send_data)
            listen_to_rc(self.server.send_data)
            listen_to_mc(self.server.send_data)
            listen_to_ws(self.server.send_data)
            while not self.controller.is_set():
                loc = listen_to_mm(self.mouse_loc)
                # print(self.mouse_loc)
                if loc is not None:
                    self.mouse_loc = mouse.get_position()
                    self.server.send_data(loc)
                    self.controller.wait(0.01)

        if self.server.connected:
            mouse_thread = threading.Thread(target=listen_to_mouse)
            mouse_thread.daemon = True
            try:
                mouse_thread.start()
            except Exception as e:
                print(e)
        else:
            print("Not Connected")
