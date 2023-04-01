from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QMouseEvent, QKeyEvent
from PyQt6.QtCore import QObject
import sys

class EventFilter(QObject):
    def eventFilter(self, obj, event):
        # if event.type() == QMouseEvent.Type.MouseButtonPress:
        #     return True
        # elif event.type() == QMouseEvent.Type.MouseButtonRelease:
        #     return True
        if event.type() == QKeyEvent.Type.KeyPress:
            return False
        elif event.type() == QKeyEvent.Type.KeyRelease:
            return True
        return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # window = QWidget()
    filter = EventFilter()
    app.installEventFilter(filter)
    # window.show()
    sys.exit(app.exec())
