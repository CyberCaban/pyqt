from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(1000)
        self.setMinimumHeight(1000)
        label = QLabel(self)
        image = QPixmap('clocks.png')
        image = image.scaledToHeight(200)
        label.setPixmap(image)
        label.setMinimumWidth(image.size().width())
        label.setMinimumHeight(image.size().height())


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
