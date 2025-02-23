from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *


class DraggableWidget(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("background-color: lightblue; border: 1px solid black;")
        self.setFixedSize(100, 50)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.position().toPoint()
            drag = QDrag(self)
            mime_data = QMimeData()
            drag.setMimeData(mime_data)
            drag.exec(Qt.DropAction.MoveAction)


class DragApp(QWidget):
    drag_count = 0

    def _init_label(self, text, bold=False):
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setWordWrap(True)
        if bold:
            label.setStyleSheet("font-weight: bold; font-size: 14px;")
        else:
            label.setStyleSheet("font-size: 12px;")
        return label

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setMinimumSize(400, 400)
        self.separator = QFrame(self)
        self.separator.setFrameShape(QFrame.Shape.HLine)
        self.separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.separator.setStyleSheet("color: black;")

    def mousePressEvent(self, event):
        if event.position().y() < self.height() / 2:
            widget = DraggableWidget(f"Drag Me ({self.drag_count})", self)
            self.drag_count += 1
            widget.move(event.position().toPoint() - QPoint(50, 25))
            widget.show()

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        if event.position().y() >= self.height() / 2:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.position().y() >= self.height() / 2:
            widget = event.source()
            widget.move(event.position().toPoint() - QPoint(50, 25))
            event.accept()
        else:
            event.ignore()

    def resizeEvent(self, event):
        self.separator.setGeometry(0, self.height() // 2, self.width(), 2)
        super().resizeEvent(event)
