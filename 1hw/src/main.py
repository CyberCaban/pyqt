from PyQt6.QtWidgets import QApplication
from window import Transparent
from hw import Window


def main():
    app = QApplication([])
    # win = Transparent()
    win = Window()
    win.show()
    app.exec()
