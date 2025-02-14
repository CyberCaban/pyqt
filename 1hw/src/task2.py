from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QMenu,
)
from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QFont, QPixmap
from models.Book import Book
from components.BookWidget import BookWidget


def find_file(rel_path: str):
    path = str(Path(__file__).resolve().parent / rel_path)
    # print(path)
    return path


class Books(QMainWindow):
    def populate(self):
        library = [
            Book("Cool Book", "John Author", "30", find_file("public/homyak.jpg")),
            Book("very Cool Book", "John Author", "30", find_file("public/kity2.jpg")),
            Book(
                "Cool Book but third time",
                "John Author",
                "30",
                find_file("public/petaHorse.jpg"),
            ),
        ]
        return [BookWidget(x) for x in library]

    def __init__(self):
        super().__init__()
        factor = 400
        self.setMinimumSize(factor, factor)

        l = QHBoxLayout()
        for widget in self.populate():
            l.addWidget(widget)

        main_widget = QWidget()
        main_widget.setLayout(l)
        main_widget.adjustSize()
        self.setCentralWidget(main_widget)
