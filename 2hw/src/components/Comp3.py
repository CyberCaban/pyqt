from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QMenu,
    QSpinBox,
    QLineEdit,
    QComboBox,
)
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from PySide6.QtCore import Slot
from components.Flex import RowLayout, ColLayout, RowWidget, ColWidget

operations = ["+", "-", "*", "/", "^"]


class CalcWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("Enter first value")
        self.input1.setValidator(QIntValidator())
        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("Enter second value")
        self.input2.setValidator(QIntValidator())
        self.result = QLabel()
        row = RowLayout(self.input1, self.input2)

        self.operation_input = QComboBox()
        self.operation_input.addItems(operations)
        self.operation_input.setStyleSheet(
            """
            QComboBox {
                text-align: center; 
            }
            QComboBox QAbstractItemView {
                text-align: center;
            }
        """
        )
        self.equal_btn = QPushButton("=")
        self.equal_btn.clicked.connect(self.result_animation)
        self.equal_btn.clicked.connect(
            lambda: self.calculate(self.operation_input.currentText())
        )
        main_layout = ColLayout(row, self.operation_input, self.equal_btn, self.result)
        self.setLayout(main_layout)

    def calculate(self, operation):
        try:
            val1 = int(self.input1.text())
            val2 = int(self.input2.text())

            expr = f"{val1} {operation} {val2}"
            if not operation == "^":
                res = f"{expr} = {eval(expr)}"
            else:
                res = f"{val1}<sup>{val2}</sup> = {val1**val2}"
            self.result.setText(res)
        except ValueError:
            self.result.setText("Error: Enter integer")

    @Slot()
    def result_animation(self):
        self.animation = QPropertyAnimation(self.equal_btn, b"geometry")
        self.animation.setDuration(500)
        self.animation.setStartValue(self.equal_btn.geometry())
        self.animation.setEndValue(
            QRect(
                self.equal_btn.x() - 10,
                self.equal_btn.y() - 10,
                self.equal_btn.width() + 20,
                self.equal_btn.height() + 20,
            )
        )
        self.animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        # self.animation.start()
