import sys
from PyQt6.QtWidgets import QApplication
from task1 import Window


def main():
    app = QApplication([])
    win = Window()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()