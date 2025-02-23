from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from components.Flex import *
from components.Comp1 import Seasons
from components.Comp2 import ProductSelector
from components.Comp3 import AgeCalc

win_titles = ["SeasonsRadio", "ShoppingCart", "AgeCalculator"]


class Window(QMainWindow):
    pages_num = len(win_titles)

    def _init_content(self):
        self.content = QStackedWidget()
        self.content.addWidget(Seasons())
        self.content.addWidget(ProductSelector())
        self.content.addWidget(AgeCalc())

    def _init_btn(self, page: int):
        btn = QPushButton(str(page))
        btn.clicked.connect(lambda: self.navigate(page))
        return btn

    def _init_navbar(self):
        self.setWindowTitle(win_titles[0])
        btns = [self._init_btn(num) for num in range(1, self.pages_num + 1)]
        navbar_layout = RowLayout(*btns)
        navbar = QWidget()
        navbar.setLayout(navbar_layout)
        return navbar

    def navigate(self, page: int):
        self.content.setCurrentIndex(page - 1)
        self.setWindowTitle(win_titles[page - 1])

    def __init__(self):
        super().__init__()
        self._init_content()
        navbar = self._init_navbar()
        layout = ColLayout(navbar, self.content)
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
