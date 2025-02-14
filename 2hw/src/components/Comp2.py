from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QMenu,
)
from PyQt6.QtCore import Qt
from PySide6.QtCore import Slot
from components.Flex import RowLayout, ColLayout, RowWidget, ColWidget


class CountWidget(QWidget):
    @Slot()
    def handle_add(self):
        self.count += 1
        self.label.setNum(self.count)

    @Slot()
    def handle_sub(self):
        self.count -= 1
        self.label.setNum(self.count)

    @Slot()
    def handle_clear(self):
        self.count = 0
        self.label.setNum(self.count)

    def __init__(self):
        super().__init__()
        self.count = 0
        self.label = QLabel(str(self.count))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.add_btn = QPushButton("+")
        self.add_btn.clicked.connect(self.handle_add)
        self.sub_btn = QPushButton("-")
        self.sub_btn.clicked.connect(self.handle_sub)
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.handle_clear)
        self.clear_btn.setContentsMargins(20, 0, 20, 0)

        ctrl_row = RowLayout(self.sub_btn, self.label, self.add_btn)
        ctrl_col = ColLayout(ctrl_row, self.clear_btn)
        self.setLayout(ctrl_col)
