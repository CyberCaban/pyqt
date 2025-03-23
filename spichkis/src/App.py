from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from components.Flex import *
from components.Spichkis import Spichkis

win_titles = ["Main Window"]


class Window(QMainWindow):
    def _init_content(self):
        self.content = Spichkis()
        layout = ColLayout(self.content)
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        self.setMinimumHeight(500)
        self.setMinimumWidth(600)

    def __init__(self):
        super().__init__()
        self._init_content()
