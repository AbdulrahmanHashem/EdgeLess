import sys
from PyQt6 import QtWidgets
from Application.UserInterface.ServerUI import ServerWindow


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    server_window = ServerWindow()
    server_window.show()

    sys.exit(app.exec())