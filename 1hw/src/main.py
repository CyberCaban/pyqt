from PyQt6.QtWidgets import QApplication
from window import Transparent
from task1 import Window
from task2 import Books


def main():
    app = QApplication([])
    # win = Books()
    win = Window()
    win.show()
    app.exec()

if __name__ == "__main__":
    main()