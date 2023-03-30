import ctypes
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from Application.UserInterface.MainUI import EdgeLess


if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon("Application/.Resources/EdgeLess_Logo.ico"))

    myappid = 'NTS.EdgeLess.EdgeLess.1.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    edge_less = EdgeLess()
    edge_less.show()

    sys.exit(app.exec())
