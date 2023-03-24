import threading
import keyboard

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

from Application.EventListeners.keyboard_events import KeyboardHandler
from Application.EventListeners.mouse_events import listen_to_all_clicks_and_wheel
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

        self.keyboard_handler = KeyboardHandler(self)
        keyboard.add_hotkey("ctrl+shift", self.keyboard_handler.on_switch)

    def toggle_server(self) -> None:
        if self.start.text() == "Start Server":
            self.server.__init__()
            self.controller.clear()
            if self.server.run():
                self.address_port.setText(str(self.server.getsockname()))
                self.start.setText("Stop Server")
                self.connect()  # start connecting
        else:
            try:
                self.server.send_data("close")
                self.controller.set()
                self.server.stop()
                self.address_port.setText("")
                self.start.setText("Start Server")
            except Exception as e:
                print(e)

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
        def update_mouse_loc(xy):
            self.mouse_loc = xy

        def listen_to_controls():
            while not self.controller.is_set():
                listen_to_all_clicks_and_wheel(self.server.send_data, self.mouse_loc, update_mouse_loc)

                # listen_for_all_keys(self.server.send_data)
                self.controller.wait()

        if self.server.connected:
            mouse_thread = threading.Thread(target=listen_to_controls)
            mouse_thread.daemon = True
            try:
                mouse_thread.start()
            except Exception as e:
                print(e)
        else:
            print("Not Connected")
