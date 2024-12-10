import sys
import ctypes
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QWidget
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor, QIcon, QAction
from PyQt6.QtCore import Qt, QRegularExpression


class Statica(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create window
        self.setWindowTitle('Statica')
        self.setWindowIcon(QIcon('source\logo.png'))
        self.setGeometry(300, 300, 800, 600)
        # Center window
        self.center_window()
        # Set font and font size
        self.setFont(QFont("JetBrains Mono", 10))
        # Text editor
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)
        self.text_edit.setTabStopDistance(30)

        # Syntax highlighter
        self.highlighter = PythonHighlighter(self.text_edit.document())


    def center_window(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        # Text formats
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor("lightblue"))
        self.keyword_format.setFontWeight(QFont.Weight.Bold)

        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor("lightgreen"))

        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("gray"))

        # Python keywords
        self.keywords = [
            "False", "None", "True", "and", "as", "assert", "async", "await",
            "break", "class", "continue", "def", "del", "elif", "else", "except",
            "finally", "for", "from", "global", "if", "import", "in", "is",
            "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try",
            "while", "with", "yield"
        ]

    def highlightBlock(self, text):
        # Keywords highlighting
        for keyword in self.keywords:
            pattern = QRegularExpression(r"\b" + keyword + r"\b")
            match = pattern.globalMatch(text)
            while match.hasNext():
                m = match.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), self.keyword_format)

        # String highlighting
        pattern = QRegularExpression(r"(\".*?\"|\'.*?\')")
        match = pattern.globalMatch(text)
        while match.hasNext():
            m = match.next()
            self.setFormat(m.capturedStart(), m.capturedLength(), self.string_format)

        # Comments highlighting
        pattern = QRegularExpression(r"#.*")
        match = pattern.globalMatch(text)
        while match.hasNext():
            m = match.next()
            self.setFormat(m.capturedStart(), m.capturedLength(), self.comment_format)


if __name__ == '__main__':
    # To set personal AppUserModelID for Statica process
    myappid = 'StaticaID'  # ID
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    # Set theme
    app.setStyle('fusion')
    # Code editor class
    editor = Statica()
    editor.show()
    sys.exit(app.exec())
