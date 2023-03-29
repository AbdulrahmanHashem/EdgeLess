from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import Qt

from Application.UserInterface.ClientUI import ClientWindow
from Application.UserInterface.ServerUI import ServerWindow


class EdgeLess(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edge Less")
        self.setMinimumWidth(350)
        self.setMinimumHeight(250)

        self.main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.main_widget)

        self.H_layout = QtWidgets.QHBoxLayout()
        self.main_widget.setLayout(self.H_layout)

        # radio_buttons_group
        self.radio_buttons_group = QtWidgets.QVBoxLayout()
        self.H_layout.addLayout(self.radio_buttons_group)

        self.server = QtWidgets.QRadioButton("Server")
        self.server.setChecked(True)
        self.radio_buttons_group.addWidget(self.server, alignment=Qt.AlignmentFlag.AlignTop)

        self.client = QtWidgets.QRadioButton("Client")
        self.radio_buttons_group.addWidget(self.client, alignment=Qt.AlignmentFlag.AlignTop)

        # client_and_server_controls_group
        self.c_and_s_controls_group = QtWidgets.QVBoxLayout()
        self.c_and_s_controls_group.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.H_layout.addLayout(self.c_and_s_controls_group)

        self.server_window = ServerWindow()
        self.c_and_s_controls_group.addWidget(self.server_window)

        self.client_window = ClientWindow()
        self.c_and_s_controls_group.addWidget(self.client_window)
        self.client_window.setEnabled(False)

        #
        self.server.clicked.connect(lambda: self.toggle_app_service(False, True))
        self.client.clicked.connect(lambda: self.toggle_app_service(True, False))

    def toggle_app_service(self, client: bool, server: bool):
        self.client_window.setEnabled(client)
        self.server_window.setEnabled(server)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.server_window.disconnect()
        self.client_window.disconnect()
        super().closeEvent(a0)

