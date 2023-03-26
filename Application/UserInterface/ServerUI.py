import threading
import keyboard

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

from Application.EventListeners.keyboard_events import KeyboardHandler
from Application.EventListeners.mouse_events import MouseHandler
from Application.Networking.server import Server


class ServerWindow(QtWidgets.QMainWindow):
    def setup_ui(self):
        main_widget = QtWidgets.QWidget()
        v_layout = QtWidgets.QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        self.address_port = QtWidgets.QLabel("")
        v_layout.addWidget(self.address_port, alignment=Qt.AlignmentFlag.AlignCenter)

        self.start = QtWidgets.QPushButton("Start Server")
        v_layout.addWidget(self.start, alignment=Qt.AlignmentFlag.AlignCenter)

    def on_connected(self, new):
        if new:
            self.address_port.setText(
                self.address_port.text() +
                "\n" +
                "   Connected to" +
                "\n" +
                str(self.server.client_address[0]) + " : " + str(self.server.client_address[1]))

            keyboard.add_hotkey("ctrl+shift", self.start_session)

        elif new is None:
            self.address_port.setText(str(self.server.getsockname()))
            self.start.setText("Stop Server")
        else:
            # Update UI.
            self.address_port.setText("")
            self.start.setText("Start Server")

            try:
                keyboard.unhook_all_hotkeys()
            except Exception as e:
                print(f"Update UI Catch : {e}")

    def __init__(self):
        super().__init__()
        self.setup_ui()

        self.start.clicked.connect(self.toggle_server)

        # make a server instance
        self.server = Server(self)
        self.server.connected.add_observer(self.update_ui)

        self.mouse_loc = (0, 0)
        self.controller = threading.Event()

        self.keyboard_handler = KeyboardHandler(self)
        # self.mouse_handler = MouseHandler(self)

        self.connect_thread = None
        self.mouse_thread = None

    def update_mouse_loc(self, xy):
        self.mouse_loc = xy

    def toggle_server(self) -> None:
        if self.server.connected.value is False:
            # Reset
            self.server.__init__(self)
            self.controller.clear()
            self.connect()
        else:
            self.disconnect()

    def connect(self) -> None:
        if self.server.run():
            if self.connect_thread is None:
                self.connect_thread = threading.Thread(target=self.server.connect_now)
                try:
                    self.connect_thread.start()
                except Exception as e:
                    print(e)
            else:
                print("UI Connect Bug")
        else:
            print("server run error")

    def disconnect(self):
        # Start Connecting.
        try:
            if self.server.connected.value:
                self.server.send_data("close")
            self.controller.set()
            self.server.stop()
            self.connect_thread.join()
            self.connect_thread = None
        except Exception as e:
            print(f"Disconnect Catch : {e}")

    def listen_to_controls(self):
        self.keyboard_handler.start_keyboard()
        # self.mouse_handler.start_mouse()
        while not self.controller.is_set():
            pass

    def start_session(self) -> None:
        if self.server.connected:
            if self.mouse_thread is None:
                self.mouse_thread = threading.Thread(target=self.listen_to_controls)
                try:
                    self.mouse_thread.start()

                    print("Session Start")
                except Exception as e:
                    print(f"Session Start Catch : {e}")
            else:
                print("Session Start Error : Mouse thread not rest")
        else:
            print("Session Start Error : Not Connected")

    def end_session(self):
        try:
            self.controller.set()
            self.mouse_thread.join()
            self.mouse_thread = None

            print("Session End")
        except Exception as e:
            print(f"End Session Catch : {e}")