from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QApplication, QLineEdit, QWidget, QPushButton, QVBoxLayout
from PySide6.QtCore import Slot


class Window(QWidget):
    # @Slot()
    def handle_input(self):
        if self.__numLineEdit.hasAcceptableInput():
            print("Пользователь ввёл " + self.__numLineEdit.text())
        else:
            print("Пользователь ввёл недопустимое значение")

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ввод числа")
        layout = QVBoxLayout()
        self.__numLineEdit = QLineEdit()
        self.__numLineEdit.setPlaceholderText("Введите число от 1 до 100")
        self.__numLineEdit.setFocus()
        self.__numLineEdit.setValidator(QIntValidator(1, 100))
        layout.addWidget(self.__numLineEdit)
        button = QPushButton("Готово")
        button.clicked.connect(self.handle_input)
        layout.addWidget(button)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
