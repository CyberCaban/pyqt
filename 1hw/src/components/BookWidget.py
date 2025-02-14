from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMenu,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QFont, QPixmap
from models.Book import Book


class BookWidget(QWidget):
    def _init_self(self):
        self.setContentsMargins(10, 5, 10, 5)
        self.setStyleSheet(
            """
            QWidget {
                background-color: #444444;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
                           """
        )

    def _init_label(self, text: str):
        l = QLabel(text)
        l.setAlignment(Qt.AlignmentFlag.AlignTop)
        l.setWordWrap(True)
        l.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        return l

    def set_cover(self, cover_path: str):
        cover_label = QLabel()
        pixmap = QPixmap(cover_path)
        # print(cover_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
            cover_label.setPixmap(pixmap)
            cover_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cover_label.setMinimumSize(pixmap.size())
        else:
            cover_label.setText("Обложка не найдена")
        return cover_label

    def __init__(self, book: Book):
        super().__init__()
        self._init_self()

        layout = QVBoxLayout()
        cover_label = self.set_cover(book.cover_path)
        ls = [
            cover_label,
            name_label := self._init_label(book.name),
            author_label := self._init_label(book.author),
            pages_label := self._init_label(book.page_num),
        ]
        for w in ls:
            layout.addWidget(w)
        self.setLayout(layout)
