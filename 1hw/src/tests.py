from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMenu,
)
from random import choice

text = [
    "My App",
    "My App",
    "Still My App",
    "Still My App",
    "What on earth",
    "What on earth",
    "This is surprising",
    "This is surprising",
    "Something went wrong",
]


class Window(QMainWindow):
    def __init__(self):
        factor = 500
        super().__init__()
        self.setFixedSize(QSize(factor, factor))
        label = QLabel("helloe")
        label.setMaximumSize(self.width() // 2, 32)
        label.setFont(QFont("FiraCode", 24))
        btn = QPushButton("priva")
        btn.clicked.connect(self.change_text)
        col = QVBoxLayout()
        col.addWidget(label)
        col.addWidget(btn)
        cont = QWidget()
        cont.setLayout(col)
        self.setCentralWidget(cont)

    def change_text(self):
        self.setWindowTitle(choice(text))

    def contextMenuEvent(self, e):
        ctx = QMenu(self)
        rulerAction = QAction("real test", self)
        rulerAction.toggled.connect(lambda x: print("changed!"))
        ctx.addAction(rulerAction)
        ctx.addAction(QAction("test", self))
        ctx.exec(e.globalPos())
        return super().contextMenuEvent(e)


app = QApplication([])
win = Window()
win.show()
app.exec()
