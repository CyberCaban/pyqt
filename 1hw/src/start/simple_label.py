from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(600)
        self.setMinimumHeight(200)
        label = QLabel("Hello World!", self)
        label.setMinimumWidth(self.width())
        label.setMinimumHeight(self.height()/3)
        label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        label.setMargin(10)
        font = QFont("Times", 24, QFont.Bold)
        label.setFont(font)


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
