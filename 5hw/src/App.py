from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from components.Flex import *
from components.Comp1 import NoteApp
from components.Comp2 import ProductApp

win_titles = ["Main Window"]


class Window(QMainWindow):
    def _init_content(self):
        tabs = [
            {"component": NoteApp(), "name": "Note App"},
            {"component": ProductApp(), "name": "Note App"},
        ]
        self.content = QTabWidget()
        self.content.setMovable(True)
        for tab in tabs:
            comp = tab["component"]
            name = tab["name"]
            self.content.addTab(comp, name)

    def __init__(self):
        super().__init__()
        self._init_content()
        layout = ColLayout(self.content)
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
