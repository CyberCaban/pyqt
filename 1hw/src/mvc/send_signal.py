from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import Signal, Slot


class Window(QMainWindow):
    closeApp = Signal()

    def __init__(self):
        super().__init__()
        self.closeApp.connect(self.close_by_press)
        self.closeApp.connect(lambda: print('Слот может быть лямбда-функцией'))
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Emit signal')

    def mousePressEvent(self, event):
        self.closeApp.emit()

    @Slot()
    def close_by_press(self):
        print('Я закрываюсь, потому что пользователь нажал на содержимое окна')
        self.close()


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
