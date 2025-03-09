from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from components.Flex import *
from components.TrigPlot import TrigPlot
from components.TreesPlot import TreesPlot
from components.HurricanesPlot import HurricanesPlot

win_titles = ["Main Window"]


class Window(QMainWindow):
    def _init_content(self):
        tabs = [
            {"component": TrigPlot(), "name": "Trigonometric Functions"},
            {"component": TreesPlot(), "name": "Trees Data"},
            {"component": HurricanesPlot(), "name": "Hurricanes Data"},
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
