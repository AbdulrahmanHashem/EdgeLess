from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QWindowStateChangeEvent, QMouseEvent, QIcon, QRegion, QAction
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QRadioButton, QLabel, QPushButton, \
    QStyle, QSizePolicy, QFrame

from Application.UserInterface.ClientUI import ClientWindow
from Application.UserInterface.ServerUI import ServerWindow
import pystray
from PIL import Image

from Application.AppSettings import AppSettings
from Application.UserInterface.SettingsUI import SettingsUI


class EdgeLess(QMainWindow):
    def __init__(self):
        super().__init__()
        # main window setting
        self.initialize_ui()

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.H_layout = QHBoxLayout()
        self.main_widget.setLayout(self.H_layout)

        self.settings = AppSettings()  # settings Window

        self.create_radio_buttons_group()               # Radio Buttons             |*|   |
        self.create_client_and_server_controls_group()  # Client & Server Controls  | |***|

        self.server.clicked.connect(lambda: self.toggle_app_service(False, True))
        self.client.clicked.connect(lambda: self.toggle_app_service(True, False))

        if self.settings.get_setting("mode") == 1:
            self.server.click()
        else:
            self.client.click()

        # self.rect().width()
        # self.rect().height()
        # region = QRegion(
        #     int(-(self.rect().width() * 0.5)),
        #     0,
        #     int(self.rect().width()),
        #     int(self.rect().height()),
        #     QRegion.RegionType.Ellipse)
        # self.setMask(region)

    def initialize_ui(self):
        self.setWindowTitle("Edge Less")

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        title_bar = CustomTitleBar(self)
        self.setMenuWidget(title_bar)

    def create_radio_buttons_group(self):
        self.radio_buttons_group = QVBoxLayout()
        self.H_layout.addLayout(self.radio_buttons_group)

        self.server = QRadioButton("Server")
        self.server.setChecked(True)
        self.radio_buttons_group.addWidget(self.server, alignment=Qt.AlignmentFlag.AlignTop)

        self.client = QRadioButton("Client")
        self.radio_buttons_group.addWidget(self.client, alignment=Qt.AlignmentFlag.AlignTop)

    def create_client_and_server_controls_group(self):
        self.c_and_s_controls_group = QVBoxLayout()
        self.c_and_s_controls_group.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.H_layout.addLayout(self.c_and_s_controls_group)

        self.server_window = ServerWindow(self)
        self.c_and_s_controls_group.addWidget(self.server_window)

        self.client_window = ClientWindow(self)
        self.c_and_s_controls_group.addWidget(self.client_window)
        self.client_window.setEnabled(False)

    def toggle_app_service(self, client: bool, server: bool):
        self.client_window.setEnabled(client)
        self.server_window.setEnabled(server)

        if server:
            self.settings.update_setting("mode", 1)
        else:
            self.settings.update_setting("mode", 2)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.server_window.disconnect()
        self.client_window.disconnect()
        super().closeEvent(a0)

    def event(self, event):
        if isinstance(event, QWindowStateChangeEvent):
            if self.windowState() & Qt.WindowState.WindowMinimized:
                self.hide()

                def show(icon, menu):
                    self.showNormal()
                    icon.stop()

                def close():
                    self.close()
                    icon.stop()

                image = Image.open("Resources/EdgeLess_Logo.ico")
                menu = pystray.Menu(pystray.MenuItem('Show', show), pystray.MenuItem('Exit', close))
                icon = pystray.Icon('EdgeLess', image, "EdgeLess", menu=menu, doubleclick=show)
                icon.run()
        return super().event(event)


class CustomTitleBar(QWidget):
    """A custom title bar widget"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.offset_x = 0
        self.offset_y = 0

        self.settings_ui = None

        self.setMinimumHeight(30)

        # Add Main Layout
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Add Left Layout
        self.add_left_layout()

        # Add a button to minimize the window
        self.minimize_button = QPushButton()
        self.main_layout.addWidget(self.minimize_button)
        self.minimize_button.clicked.connect(self.parent.showMinimized)

        self.minimize_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMinButton))
        self.minimize_button.setFixedWidth(30)
        self.minimize_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.minimize_button.setStyleSheet("""
        QPushButton { border: 0px; }
        QPushButton:hover { background-color: #838383; } """)

        # Add a button to close the window
        self.close_button = QPushButton()
        self.main_layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self.parent.close)

        self.close_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarCloseButton))
        self.close_button.setFixedWidth(40)
        self.close_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.close_button.setStyleSheet("""
        QPushButton { border: 0px; } 
        QPushButton:hover { background-color: #ff6347; } """)

    def add_left_layout(self):
        # Add Left Layout
        self.left_layout = QHBoxLayout()
        self.main_layout.addLayout(self.left_layout)
        self.left_layout.setContentsMargins(5, 0, 0, 0)
        self.left_layout.setSpacing(5)

        # add a program icon
        self.label = QLabel()
        self.icon = QIcon("Resources/EdgeLess_Logo.ico")
        self.pixmap = self.icon.pixmap(25, 25)
        self.label.setPixmap(self.pixmap)
        self.left_layout.addWidget(self.label)

        # add menus/buttons
        self.settings_act = QPushButton("Settings")
        self.left_layout.addWidget(self.settings_act)
        self.settings_act.clicked.connect(self.open_settings)

        self.settings_act.setFixedWidth(60)
        self.settings_act.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.settings_act.setStyleSheet(""" 
        QPushButton { border: 0px; border-radius: 5px; } 
        QPushButton:hover { background-color: #838383; } """)

        # Add a label to display the window title
        self.title_label = QLabel(self.parent.windowTitle())
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_layout.addWidget(self.title_label, Qt.AlignmentFlag.AlignVCenter)

    def open_settings(self):
        if isinstance(self.settings_ui, SettingsUI):
            self.settings_ui.showNormal()
        else:
            self.settings_ui = SettingsUI(self.parent)
            self.settings_ui.show()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Handle mouse press events on the title bar"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.offset_x = event.globalPosition().x() - self.window().geometry().topLeft().x()
            self.offset_y = event.globalPosition().y() - self.window().geometry().topLeft().y()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Handle mouse move events on the title bar"""
        if event.buttons() & Qt.MouseButton.LeftButton:
            # Move the window by the same offset as the mouse movement
            self.window().move(int(event.globalPosition().x() - self.offset_x), int(event.globalPosition().y() - self.offset_y))
