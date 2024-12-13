import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTreeView, QTextEdit, QMenuBar,
                             QMenu, QToolBar, QPushButton, QSplitter)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Основные настройки окна
        self.setWindowTitle('IDE')
        self.resize(1200, 800)

        # Центральный виджет и основной layout
        central_widget = QWidget()
        main_layout = QHBoxLayout()

        # Сплиттер для изменения размеров областей
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Дерево проекта (слева)
        self.project_tree = QTreeView()
        self.project_tree.setModel(self.create_project_model())
        splitter.addWidget(self.project_tree)

        # Область кода (по центру)
        self.code_editor = QTextEdit()
        splitter.addWidget(self.code_editor)

        # Добавляем сплиттер в основной layout
        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Создаем верхнее меню (тулбар)
        self.create_toolbar()

        # Создаем нижнее меню (терминал)
        self.create_terminal()

        # Применяем темную тему
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3c3f41;
            }
            QTreeView {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3c3f41;
            }
            QToolBar {
                background-color: #3c3f41;
            }
            QPushButton {
                background-color: #365880;
                color: #ffffff;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #4b7399;
            }
        """)

    def create_project_model(self):
        # Создание модели для дерева проекта
        model = QStandardItemModel()
        root = model.invisibleRootItem()

        # Пример структуры проекта
        project = QStandardItem('My Project')
        src_folder = QStandardItem('src')
        py_file = QStandardItem('main.py')

        project.appendRow(src_folder)
        src_folder.appendRow(py_file)

        root.appendRow(project)
        return model

    def create_toolbar(self):
        # Создание верхней панели инструментов
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Кнопка сохранения
        save_btn = QPushButton('Save')
        #save_btn.clicked.connect(self.save_file)
        toolbar.addWidget(save_btn)

        # Кнопка запуска
        run_btn = QPushButton('Run')
        #run_btn.clicked.connect(self.run_code)
        toolbar.addWidget(run_btn)

    def create_terminal(self):
        # Создание терминала
        self.terminal = QTextEdit()
        self.terminal.setMaximumHeight(200)
        self.terminal.setReadOnly(True)

        # Добавляем терминал в нижнюю часть
        dock = QWidget()
        dock_layout = QVBoxLayout()
        dock_layout.addWidget(self.terminal)
        dock.setLayout(dock_layout)

        # Создаем dock виджет для терминала
        #self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dock)

    def save_file(self):
        # Логика сохранения файла
        print("Saving file...")

    def run_code(self):
        # Логика запуска кода
        print("Running code...")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()