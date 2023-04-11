from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QMouseEvent
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QStyle, QSizePolicy, QLabel

from Application.UserInterface import SettingsUI


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