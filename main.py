import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTreeView, QTextEdit, QTabWidget,
                             QToolBar, QPushButton, QSplitter)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import (QStandardItemModel, QStandardItem, QIcon, QFont,
                         QFontDatabase)
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

        # Вкладки для открытых файлов
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        #self.tabs.tabCloseRequested.connect(self.close_tab)

        # Первая пустая вкладка
        first_tab = QTextEdit()
        first_tab.setFont(QFont('JetBrains Mono', 10))
        first_tab.setStyleSheet("""
            background-color: #1e1e1e;
            color: #d4d4d4;
            border: none;
        """)

        self.tabs.addTab(first_tab, "Untitled")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def close_tab(self, index):
        # Закрытие вкладки
        self.tabs.removeTab(index)

        # Если не осталось вкладок, создаем новую пустую
        if self.tabs.count() == 0:
            first_tab = QTextEdit()
            first_tab.setFont(QFont('JetBrains Mono', 10))
            first_tab.setStyleSheet("""
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: none;
            """)
            self.tabs.addTab(first_tab, "Untitled")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Загрузка шрифтов
        self.load_fonts()

        self.initUI()

    def load_fonts(self):
        # Загрузка шрифтов Inter
        inter_fonts = [
            'Inter_18pt-Medium.ttf'
        ]

        # Загрузка шрифта JetBrains Mono
        jetbrains_fonts = [
            'JetBrainsMono-Regular.ttf',
            'JetBrainsMono-Medium.ttf'
        ]

        # Путь к шрифтам
        font_dir = os.path.join(os.path.dirname(__file__), 'fonts')

        # Загрузка шрифтов Inter
        for font in inter_fonts:
            QFontDatabase.addApplicationFont(os.path.join(font_dir, font))

        # Загрузка шрифтов JetBrains Mono
        for font in jetbrains_fonts:
            QFontDatabase.addApplicationFont(os.path.join(font_dir, font))

    def initUI(self):
        self.setWindowTitle('IDE')
        self.resize(1200, 600)

        # Центральный виджет
        central_widget = QWidget()
        main_layout = QHBoxLayout()

        # Сплиттер для изменения размеров областей
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Дерево проекта (слева, уменьшенная ширина)
        self.project_tree = QTreeView()
        self.project_tree.setMaximumWidth(250)  # Уменьшена ширина
        self.project_tree.setModel(self.create_project_model())
        splitter.addWidget(self.project_tree)

        # Виджет редактора кода
        self.code_editor = CodeEditor()
        splitter.addWidget(self.code_editor)

        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Создаем верхнее меню (тулбар)
        self.create_toolbar()

        # Применяем глобальные стили
        self.setStyleSheet("""
            * {
                font-family: 'Inter', sans-serif;
                font-weight: 400;
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
            }
            QPushButton {
                background-color: #365880;
                color: #ffffff;
                border: none;
                padding: 5px;
                margin: 5px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #4a6984;
            }
        """)

    def create_project_model(self):
        model = QStandardItemModel()
        root = model.invisibleRootItem()

        project = QStandardItem('My Project')
        src_folder = QStandardItem('src')
        py_file = QStandardItem('main.py')

        project.appendRow(src_folder)
        src_folder.appendRow(py_file)

        root.appendRow(project)
        return model

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        icon_dir = os.path.join(os.path.dirname(__file__), 'assets')

        # Кнопки с иконками
        buttons = [
            ('Save', 'disk.svg', self.save_file),
            ('Run', 'play.svg', self.run_code),
            ('Open', 'folder.svg', self.open_file)
        ]

        for name, icon, method in buttons:
            btn = QPushButton()
            btn.setIcon(SvgIcon(os.path.join(icon_dir, icon), 24))
            btn.setToolTip(name)
            #btn.clicked.connect(method)
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
    main()