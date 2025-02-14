from pathlib import Path
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


def find_file(rel_path: str):
    return str(Path(__file__).resolve().parent / rel_path)


class Window(QMainWindow):
    def wrapLabel(self):
        font = QFont("FiraCode", 12, italic=True)
        l = QLabel("Priva " * 20)
        l.setFont(font)
        l.setWordWrap(True)
        l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l.setContentsMargins(110, -10, 0, 0)
        l.setStyleSheet(
            """
            QLabel:hover {
                color: #5E81AC;
            }
        """
        )
        return l

    def biggerLabel(self):
        font = QFont("FiraCode", 24)
        l = QLabel("Hellow")
        l.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        l.setFont(font)
        l.move(QPoint(0, 10))
        l.setContentsMargins(0, 0, 0, 10)
        return l

    def imageLabel(self, size):
        picFile = find_file("public/kity.jpg")
        img = QPixmap(str(picFile))
        l = QLabel()
        l.setScaledContents(True)
        l.setPixmap(img)
        l.setFixedSize(size, size)
        return l

    def resizeEvent(self, a0):
        newH, newW = a0.size().height(), a0.size().width()
        imgH, imgW = self.imgLabel.size().height(), self.imgLabel.width()
        self.imgLabel.move(newW // 2 - imgW // 2, newH // 2 - imgH // 2)
        return super().resizeEvent(a0)

    def __init__(self):
        super().__init__()
        factor = 400
        self.setMinimumSize(factor, factor)
        self.imgLabel = self.imageLabel(factor)
        self.imgLabel.setParent(self)

        label = self.wrapLabel()
        label2 = self.biggerLabel()
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(label2)

        mainWidget = QWidget()
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)