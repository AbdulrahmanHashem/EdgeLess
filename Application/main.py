import sys
from PyQt6.QtWidgets import QApplication

from Application.UserInterface.ClientUI import ClientWindow
from Application.UserInterface.ServerUI import ServerWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    server_window = ServerWindow()
    server_window.show()

    sys.exit(app.exec())


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#
#     client_window = ClientWindow()
#     client_window.show()
#
#     sys.exit(app.exec())
