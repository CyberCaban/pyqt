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


class BigBtn(QWidget):
    @Slot()
    def handle_input(self):
        if self.btn.isChecked():
            self.label.setText("НАЖАТА!!!")
        else:
            self.label.setText("Отпущена")

    def __init__(self):
        super().__init__()
        l = QVBoxLayout()
        self.label = QLabel("Отпущена")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn = QPushButton("Click me!")
        self.btn.setCheckable(True)
        self.btn.clicked.connect(self.handle_input)
        l.addWidget(self.btn)
        l.addWidget(self.label)
        self.setLayout(l)
