from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QMenu,
    QStackedWidget,
)
from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QFont, QPixmap
from PySide6.QtCore import Slot
from components.Comp1 import BigBtn
from components.Comp2 import CountWidget
from components.Comp3 import CalcWidget
from components.Flex import ColWidget


def find_file(rel_path: str):
    return str(Path(__file__).resolve().parent / rel_path)


class Window(QMainWindow):
    def _init_content(self):
        self.cur_content = QStackedWidget()
        self.cur_content.addWidget(BigBtn())
        self.cur_content.addWidget(CountWidget())
        self.cur_content.addWidget(CalcWidget())

    def _init_navbar(self):
        navbar_layout = QHBoxLayout()
        btns = [self._init_btn(num) for num in range(1, 4)]
        for b in btns:
            navbar_layout.addWidget(b)
        navbar = QWidget()
        navbar.setLayout(navbar_layout)
        return navbar

    def _init_btn(self, page: int):
        btn = QPushButton(str(page))
        btn.clicked.connect(lambda: self.navigate(page))
        return btn

    @Slot(int)
    def navigate(self, page: int):
        print(page)
        self.cur_content.setCurrentIndex(page - 1)
        match page:
            case 1:
                self.setWindowTitle("Clickable Button")
            case 2:
                self.setWindowTitle("Count Widget")
            case 3:
                self.setWindowTitle("Calculator")

    def __init__(self):
        super().__init__()
        self.setFont(QFont("Arial", 12))
        self.setWindowTitle("Clickable Button")
        self._init_content()
        navbar = self._init_navbar()

        self.l = QVBoxLayout()
        self.l.addWidget(navbar)
        self.l.addWidget(self.cur_content)

        main_widget = QWidget()
        main_widget.setLayout(self.l)
        self.setCentralWidget(main_widget)
