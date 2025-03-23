from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, pyqtSignal
import math


class PuzzleView(QWidget):
    match_clicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_match = None
        self.matches = []
        self.init_ui()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def init_ui(self):
        layout = QVBoxLayout()

        control_panel = QGridLayout()

        self.prev_button = QPushButton("←")
        self.prev_button.clicked.connect(self.prev_button_clicked)
        self.prev_button.setFixedWidth(40)

        self.next_button = QPushButton("→")
        self.next_button.clicked.connect(self.next_button_clicked)
        self.next_button.setFixedWidth(40)

        self.puzzle_label = QLabel()
        self.puzzle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.puzzle_label.setWordWrap(True)

        self.restore_button = QPushButton("Вернуть спичку")
        self.restore_button.clicked.connect(self.restore_button_clicked)

        control_panel.addWidget(self.prev_button, 0, 0)
        control_panel.addWidget(self.puzzle_label, 0, 1)
        control_panel.addWidget(self.next_button, 0, 2)
        control_panel.addWidget(self.restore_button, 0, 3)

        control_panel.setColumnStretch(1, 1)

        layout.addLayout(control_panel)
        layout.addStretch()
        self.setLayout(layout)

    def set_matches(self, matches):
        self.matches = matches
        if self.selected_match is not None:
            if (
                self.selected_match >= len(matches)
                or not matches[self.selected_match].is_visible
            ):
                self.selected_match = None
        self.update()

    def set_puzzle_info(self, description: str, current: int, total: int):
        self.puzzle_label.setText(f"{current}/{total}: {description}")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        for i, match in enumerate(self.matches):
            if match.is_visible:
                if i == self.selected_match:
                    pen = QPen(QColor(255, 0, 0), 4)
                else:
                    pen = QPen(Qt.GlobalColor.black, 3)
                painter.setPen(pen)
                painter.drawLine(match.x1, match.y1, match.x2, match.y2)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            self.select_match_at_position(pos.x(), pos.y())

    def mouseDoubleClickEvent(self, event):
        if (
            event.button() == Qt.MouseButton.LeftButton
            and self.selected_match is not None
        ):
            self.match_clicked.emit(self.selected_match)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            if self.selected_match is not None:
                self.match_clicked.emit(self.selected_match)
        elif event.key() == Qt.Key.Key_Left:
            self.select_previous_match()
        elif event.key() == Qt.Key.Key_Right:
            self.select_next_match()
        else:
            super().keyPressEvent(event)

    def select_match_at_position(self, x, y):
        min_dist = float("inf")
        closest_match = None

        for i, match in enumerate(self.matches):
            if not match.is_visible:
                continue

            dist = self._distance_to_line(x, y, match.x1, match.y1, match.x2, match.y2)
            if dist < min_dist:
                min_dist = dist
                closest_match = i

        if min_dist < 10:
            self.selected_match = closest_match
            self.update()

    def _distance_to_line(self, x, y, x1, y1, x2, y2):
        A = x - x1
        B = y - y1
        C = x2 - x1
        D = y2 - y1

        dot = A * C + B * D
        len_sq = C * C + D * D

        if len_sq == 0:
            return math.sqrt(A * A + B * B)

        param = dot / len_sq

        if param < 0:
            return math.sqrt(A * A + B * B)
        elif param > 1:
            return math.sqrt((x - x2) * (x - x2) + (y - y2) * (y - y2))

        return abs(A * D - C * B) / math.sqrt(len_sq)

    def select_previous_match(self):
        visible_matches = [i for i, m in enumerate(self.matches) if m.is_visible]
        if not visible_matches:
            self.selected_match = None
            self.update()
            return

        if self.selected_match is None:
            self.selected_match = visible_matches[-1]
        else:
            try:
                current_idx = visible_matches.index(self.selected_match)
                self.selected_match = visible_matches[
                    (current_idx - 1) % len(visible_matches)
                ]
            except ValueError:
                self.selected_match = visible_matches[-1]

        self.update()

    def select_next_match(self):
        visible_matches = [i for i, m in enumerate(self.matches) if m.is_visible]
        if not visible_matches:
            self.selected_match = None
            self.update()
            return
        if self.selected_match is None:
            self.selected_match = visible_matches[0]
        else:
            try:
                current_idx = visible_matches.index(self.selected_match)
                self.selected_match = visible_matches[
                    (current_idx + 1) % len(visible_matches)
                ]
            except ValueError:

                self.selected_match = visible_matches[0]
        self.update()

    def restore_button_clicked(self):
        self.match_clicked.emit(-1)

    def prev_button_clicked(self):
        self.match_clicked.emit(-2)

    def next_button_clicked(self):
        self.match_clicked.emit(-3)
