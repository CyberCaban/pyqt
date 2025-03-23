from PyQt6.QtWidgets import (
    QWidget, 
    QPushButton, 
    QVBoxLayout, 
    QHBoxLayout,
    QGridLayout, 
    QLabel,
    QLineEdit,
    QSpinBox,
    QMessageBox
)
from PyQt6.QtGui import QPainter, QPen, QColor, QFont
from PyQt6.QtCore import Qt, pyqtSignal, QPoint
import math
from dataclasses import dataclass

@dataclass
class Match:
    x1: int
    y1: int
    x2: int
    y2: int
    is_visible: bool = True

class PuzzleEditorView(QWidget):
    puzzle_saved = pyqtSignal(list, str, str)  # matches, description, solution

    def __init__(self, parent=None):
        super().__init__(parent)
        self.matches = []
        self.selected_match = None
        self.is_drawing = False
        self.start_pos = None
        self.current_pos = None
        self.solution_matches = set()  # Indices of matches that are part of the solution
        self.init_ui()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def init_ui(self):
        layout = QVBoxLayout()

        # Control panel
        control_panel = QGridLayout()

        # Description input
        description_label = QLabel("Описание:")
        self.description_input = QLineEdit()
        
        # Solution help label
        solution_help = QLabel("Решение (выберите спички правой кнопкой и нажмите пробел, чтобы добавить в решение)")
        solution_help.setWordWrap(True)
        
        # Solution input (readonly, will be filled automatically)
        solution_label = QLabel("Номера спичек в решении:")
        self.solution_input = QLineEdit()
        self.solution_input.setReadOnly(True)

        # Save button
        self.save_button = QPushButton("Сохранить пазл")
        self.save_button.clicked.connect(self.save_puzzle)

        # Delete button
        self.delete_button = QPushButton("Удалить спичку")
        self.delete_button.clicked.connect(self.delete_selected_match)
        self.delete_button.setEnabled(False)

        # Grid size controls
        grid_controls = QHBoxLayout()
        grid_label = QLabel("Размер сетки:")
        self.grid_size = QSpinBox()
        self.grid_size.setRange(1, 100)
        self.grid_size.setValue(50)
        self.grid_size.valueChanged.connect(self.update)
        grid_controls.addWidget(grid_label)
        grid_controls.addWidget(self.grid_size)
        grid_controls.addStretch()

        # Add widgets to control panel
        control_panel.addWidget(description_label, 0, 0)
        control_panel.addWidget(self.description_input, 0, 1, 1, 2)
        control_panel.addWidget(solution_help, 1, 0, 1, 3)
        control_panel.addWidget(solution_label, 2, 0)
        control_panel.addWidget(self.solution_input, 2, 1, 1, 2)
        control_panel.addWidget(self.save_button, 3, 0)
        control_panel.addWidget(self.delete_button, 3, 1)
        
        # Add layouts to main layout
        layout.addLayout(control_panel)
        layout.addLayout(grid_controls)
        layout.addStretch()
        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw grid
        grid_size = self.grid_size.value()
        pen = QPen(QColor(200, 200, 200), 1)
        painter.setPen(pen)
        
        for x in range(0, self.width(), grid_size):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), grid_size):
            painter.drawLine(0, y, self.width(), y)

        # Draw existing matches
        font = QFont()
        font.setPointSize(10)
        painter.setFont(font)

        for i, match in enumerate(self.matches):
            # Draw match
            if i == self.selected_match:
                pen = QPen(QColor(255, 0, 0), 4)
            elif i in self.solution_matches:
                pen = QPen(QColor(0, 255, 0), 4)  # Green for solution matches
            else:
                pen = QPen(Qt.GlobalColor.black, 3)
            painter.setPen(pen)
            painter.drawLine(match.x1, match.y1, match.x2, match.y2)
            
            # Draw match number
            center_x = (match.x1 + match.x2) / 2
            center_y = (match.y1 + match.y2) / 2
            painter.setPen(QPen(Qt.GlobalColor.blue))
            painter.drawText(int(center_x), int(center_y), str(i))

        # Draw match being created
        if self.is_drawing and self.start_pos and self.current_pos:
            pen = QPen(QColor(0, 0, 255), 3)
            painter.setPen(pen)
            painter.drawLine(self.start_pos, self.current_pos)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Start drawing new match
            self.is_drawing = True
            self.start_pos = self.snap_to_grid(event.pos())
            self.current_pos = self.start_pos
            self.selected_match = None
            self.delete_button.setEnabled(False)
        elif event.button() == Qt.MouseButton.RightButton:
            # Select existing match
            pos = event.pos()
            self.select_match_at_position(pos.x(), pos.y())
            self.delete_button.setEnabled(self.selected_match is not None)

    def mouseMoveEvent(self, event):
        if self.is_drawing:
            self.current_pos = self.snap_to_grid(event.pos())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.is_drawing:
            end_pos = self.snap_to_grid(event.pos())
            # Only add match if it has some length
            if self.start_pos != end_pos:
                self.matches.append(Match(
                    self.start_pos.x(),
                    self.start_pos.y(),
                    end_pos.x(),
                    end_pos.y()
                ))
            self.is_drawing = False
            self.start_pos = None
            self.current_pos = None
            self.update()

    def snap_to_grid(self, pos):
        grid_size = self.grid_size.value()
        x = round(pos.x() / grid_size) * grid_size
        y = round(pos.y() / grid_size) * grid_size
        return QPoint(x, y)

    def select_match_at_position(self, x, y):
        min_dist = float("inf")
        closest_match = None

        for i, match in enumerate(self.matches):
            dist = self._distance_to_line(x, y, match.x1, match.y1, match.x2, match.y2)
            if dist < min_dist:
                min_dist = dist
                closest_match = i

        if min_dist < 10:
            self.selected_match = closest_match
        else:
            self.selected_match = None
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

    def delete_selected_match(self):
        if self.selected_match is not None:
            # Remove from solution if it was there
            if self.selected_match in self.solution_matches:
                self.solution_matches.remove(self.selected_match)
            # Adjust solution indices for matches after the deleted one
            new_solution = set()
            for idx in self.solution_matches:
                if idx > self.selected_match:
                    new_solution.add(idx - 1)
                else:
                    new_solution.add(idx)
            self.solution_matches = new_solution
            
            # Remove match
            self.matches.pop(self.selected_match)
            self.selected_match = None
            self.delete_button.setEnabled(False)
            
            # Update solution input
            self._update_solution_input()
            self.update()

    def save_puzzle(self):
        description = self.description_input.text()
        if not description:
            QMessageBox.warning(self, "Ошибка", "Введите описание пазла")
            return
            
        if not self.solution_matches:
            QMessageBox.warning(self, "Ошибка", "Добавьте хотя бы одну спичку в решение")
            return
            
        if not self.matches:
            QMessageBox.warning(self, "Ошибка", "Добавьте спички в пазл")
            return
            
        solution = ",".join(map(str, sorted(self.solution_matches)))
        self.puzzle_saved.emit(self.matches, description, solution)
        
        # Clear form
        self.matches = []
        self.solution_matches = set()
        self.description_input.clear()
        self.solution_input.clear()
        self.selected_match = None
        self.delete_button.setEnabled(False)
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete and self.selected_match is not None:
            self.delete_selected_match()
        elif event.key() == Qt.Key.Key_Space and self.selected_match is not None:
            # Toggle match in solution
            if self.selected_match in self.solution_matches:
                self.solution_matches.remove(self.selected_match)
            else:
                self.solution_matches.add(self.selected_match)
            self._update_solution_input()
            self.update()
        else:
            super().keyPressEvent(event)
            
    def _update_solution_input(self):
        self.solution_input.setText(", ".join(map(str, sorted(self.solution_matches)))) 