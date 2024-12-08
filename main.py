from PyQt6.QtWidgets import QApplication, QWidget
import sys

# Event handler
app = QApplication(sys.argv)

# Make and show window
window = QWidget()
window.show()

# Launch handler
app.exec()