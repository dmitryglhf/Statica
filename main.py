import sys
import ctypes
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget


class Statica(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Statica')
        self.setWindowIcon(QIcon('source\logo.png'))
        self.setGeometry(300, 300, 600, 400)
        self.show()


if __name__ == '__main__':
    # To set personal AppUserModelID for Statica process
    myappid = 'StaticaID'  # ID
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    ex = Statica()
    sys.exit(app.exec())
