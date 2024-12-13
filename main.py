import sys
import ctypes
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTreeView, QTextEdit, QTabWidget,
                             QToolBar, QPushButton, QSplitter, QSizePolicy)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import (QStandardItemModel, QStandardItem, QIcon, QFont,
                         QFontDatabase, QColor)
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QPixmap, QPainter


class SvgIcon(QIcon):
    def __init__(self, path, size=24, color="#02d8f6"):
        super().__init__()
        renderer = QSvgRenderer(path)
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()

        self.addPixmap(pixmap)


class CodeEditor(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        first_tab = QTextEdit()
        first_tab.setFont(QFont('JetBrains Mono', 10))
        first_tab.setStyleSheet("""
            background-color: #1f1f1f;
            color: #d4d4d4;
            border: none;
            selection-background-color: #264f78;
        """)

        self.tabs.addTab(first_tab, "Untitled")
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def close_tab(self, index):
        self.tabs.removeTab(index)

        if self.tabs.count() == 0:
            first_tab = QTextEdit()
            first_tab.setFont(QFont('JetBrains Mono', 10))
            first_tab.setStyleSheet("""
                background-color: #1f1f1f;
                color: #d4d4d4;
                border: none;
                selection-background-color: #264f78;
            """)
            self.tabs.addTab(first_tab, "Untitled")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_fonts()
        self.initUI()

    def load_fonts(self):
        inter_fonts = ['Inter Medium.ttf']
        jetbrains_fonts = [
            'JetBrainsMono-Regular.ttf',
            'JetBrainsMono-Medium.ttf'
        ]

        font_dir = os.path.join(os.path.dirname(__file__), 'fonts')

        for font in inter_fonts:
            QFontDatabase.addApplicationFont(os.path.join(font_dir, font))

        for font in jetbrains_fonts:
            QFontDatabase.addApplicationFont(os.path.join(font_dir, font))

    def initUI(self):
        self.setWindowTitle('Statica')
        self.setWindowIcon(QIcon('source\logo.png'))
        self.resize(1200, 600)

        central_widget = QWidget()
        main_layout = QHBoxLayout()

        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.project_tree = QTreeView()
        self.project_tree.setMaximumWidth(250)
        self.project_tree.setModel(self.create_project_model())
        self.project_tree.setIndentation(10)
        self.project_tree.header().hide()
        splitter.addWidget(self.project_tree)

        self.code_editor = CodeEditor()
        splitter.addWidget(self.code_editor)

        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.create_toolbar()

        self.setStyleSheet("""
            * {
                font-family: 'Inter Medium'
            }
            QMainWindow {
                background-color: #252525;
            }
            QWidget {
                background-color: #1e1e1e;
                color: #d4d4d4;
            }
            QTreeView {
                background-color: #252525;
                color: #d4d4d4;
                border: none;
            }
            QToolBar {
                background-color: #252525;
                spacing: 4px;
                border: none;
            }
            QSplitter {
                background-color: #252525;
            }
            QSplitter::handle {
                background-color: #252525;
                width: 2px;
            }
            QPushButton {
                background-color: #252525;
                color: #d4d4d4;
                border: none;
                padding: 5px;
                margin: 5px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #252525;
            }
            QTabWidget::pane {
                background-color: #252525;
                border: none;
            }
            QTabBar::tab {
                background-color: #2c2c2c;
                color: #d4d4d4;
                padding: 5px 10px;
                border: none;
            }
            QTabBar::tab:selected {
                background-color: #3c3c3c;
            }
        """)

    def create_project_model(self):
        model = QStandardItemModel()
        root = model.invisibleRootItem()

        # Получаем текущую директорию
        current_dir = os.getcwd()
        current_dir_name = os.path.basename(current_dir)

        project = QStandardItem(current_dir_name)
        project.setForeground(QColor("#d4d4d4"))
        project.setFont(QFont('Inter Medium', 10))
        
        # Рекурсивная функция для добавления подпапок и файлов
        def add_dir_items(dir_path, parent_item):
            for item in os.listdir(dir_path):
                full_path = os.path.join(dir_path, item)
                
                # Показываем только Python файлы
                if os.path.isfile(full_path) and item.endswith('.py'):
                    file_item = QStandardItem(item)
                    file_item.setForeground(QColor("#569cd6"))
                    file_item.setFont(QFont('Inter Medium', 10))
                    
                    parent_item.appendRow(file_item)
                
                # Добавляем подпапки с рекурсивным просмотром
                elif os.path.isdir(full_path):
                    folder_item = QStandardItem(item)
                    folder_item.setForeground(QColor("#d4d4d4"))
                    folder_item.setFont(QFont('Inter Medium', 10))
                    
                    parent_item.appendRow(folder_item)
                    
                    # Рекурсивно добавляем содержимое подпапки
                    add_dir_items(full_path, folder_item)

        # Добавляем содержимое текущей директории
        add_dir_items(current_dir, project)

        root.appendRow(project)
        return model


    def create_toolbar(self):
        toolbar = QToolBar()
        toolbar.setStyleSheet("QToolBar { border: none; }")
        toolbar.setIconSize(QSize(18, 18))
        self.addToolBar(toolbar)

        icon_dir = os.path.join(os.path.dirname(__file__), 'assets')

        buttons = [
            ('Save', 'disk.svg'),
            ('Open', 'folder.svg'),
            ('Run', 'play.svg')
        ]

        for name, icon in buttons:
            btn = QPushButton()
            btn.setIcon(SvgIcon(os.path.join(icon_dir, icon), 18, "#d4d4d4"))
            btn.setToolTip(name)
            btn.setStyleSheet("""
                QPushButton { 
                    background: none; 
                    border: none; 
                    padding: 4px;
                }
                QPushButton:hover {
                    background-color: #3c3c3c;
                }
            """)
            toolbar.addWidget(btn)

    def save_file(self):
        print("Saving file...")

    def run_code(self):
        print("Running code...")

    def open_file(self):
        print("Opening file...")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    # To set personal AppUserModelID for Statica process
    myappid = 'StaticaID'  # ID
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    main()