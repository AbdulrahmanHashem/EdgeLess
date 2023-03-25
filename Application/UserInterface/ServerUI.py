import threading
import keyboard

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

from Application.EventListeners.keyboard_events import KeyboardHandler
from Application.EventListeners.mouse_events import MouseHandler
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

        self.start.clicked.connect(self.toggle_server)

        # make a server instance
        self.server = Server(self)

        self.mouse_loc = (0, 0)
        self.controller = threading.Event()

        self.keyboard_handler = KeyboardHandler(self)
        self.mouse_handler = MouseHandler(self)

        keyboard.add_hotkey("ctrl+shift", self.start_session)

    def update_mouse_loc(self, xy):
        self.mouse_loc = xy

    def on_connected(self):
        self.address_port.setText(
            self.address_port.text() +
            "\n" +
            "Connected to" +
            "\n" +
            str(self.server.client_address[0]) + " : " + str(self.server.client_address[1]))

    def toggle_server(self) -> None:
        if self.start.text() == "Start Server":
            # Reset
            self.server.__init__(self)
            self.controller.clear()

            if self.server.run():
                # Start Connecting.
                self.connect()

                # Update UI.
                self.address_port.setText(str(self.server.getsockname()))
                self.start.setText("Stop Server")
        else:
            try:
                # Start Connecting.
                self.server.send_data("close")
                self.controller.set()
                self.server.stop()

                # Update UI.
                self.address_port.setText("")
                self.start.setText("Start Server")
            except Exception as e:
                print(e)

    def connect(self) -> None:
        connect_thread = threading.Thread(target=self.server.connect_now)
        connect_thread.daemon = True
        try:
            connect_thread.start()
        except Exception as e:
            print(e)

    def start_session(self) -> None:
        def listen_to_controls():
            self.keyboard_handler.start_keyboard()
            self.mouse_handler.start_mouse()
            while not self.controller.is_set():
                pass

        """ --------------------------- """
        if self.server.connected:
            mouse_thread = threading.Thread(target=listen_to_controls)
            mouse_thread.daemon = True
            try:
                mouse_thread.start()
            except Exception as e:
                print(e)
        else:
            print("Not Connected")
