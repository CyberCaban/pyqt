from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMenu,
)
from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QFont, QPixmap


class Transparent(QMainWindow):
    def __init__(self):
        super().__init__()
        factor = 100
        self.setBaseSize(factor * 16, factor * 9)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def resizeEvent(self, e):
        newSize = QSize(e.size().width(), int(e.size().width() * 9 / 16))
        self.resize(newSize)
        return super().resizeEvent(e)
