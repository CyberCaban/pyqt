from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QSpinBox,
    QGroupBox
)
from PyQt6.QtCore import pyqtSignal

class EditorToolbox(QWidget):
    # Signals
    description_changed = pyqtSignal(str)
    grid_size_changed = pyqtSignal(int)
    save_clicked = pyqtSignal()
    delete_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Description group
        description_group = QGroupBox("Описание пазла")
        description_layout = QVBoxLayout()
        
        description_label = QLabel("Введите описание задачи:")
        self.description_input = QLineEdit()
        self.description_input.textChanged.connect(self.description_changed.emit)
        
        description_layout.addWidget(description_label)
        description_layout.addWidget(self.description_input)
        description_group.setLayout(description_layout)
        
        # Solution group
        solution_group = QGroupBox("Решение")
        solution_layout = QVBoxLayout()
        
        solution_help = QLabel(
            "Выберите спички правой кнопкой и нажмите пробел, "
            "чтобы добавить в решение"
        )
        solution_help.setWordWrap(True)
        
        solution_label = QLabel("Номера спичек в решении:")
        self.solution_input = QLineEdit()
        self.solution_input.setReadOnly(True)
        
        solution_layout.addWidget(solution_help)
        solution_layout.addWidget(solution_label)
        solution_layout.addWidget(self.solution_input)
        solution_group.setLayout(solution_layout)
        
        # Grid controls group
        grid_group = QGroupBox("Настройки сетки")
        grid_layout = QHBoxLayout()
        
        grid_label = QLabel("Размер:")
        self.grid_size = QSpinBox()
        self.grid_size.setRange(1, 100)
        self.grid_size.setValue(50)
        self.grid_size.valueChanged.connect(self.grid_size_changed.emit)
        
        grid_layout.addWidget(grid_label)
        grid_layout.addWidget(self.grid_size)
        grid_layout.addStretch()
        grid_group.setLayout(grid_layout)
        
        # Action buttons group
        actions_group = QGroupBox("Действия")
        actions_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Сохранить пазл")
        self.save_button.clicked.connect(self.save_clicked.emit)
        
        self.delete_button = QPushButton("Удалить спичку")
        self.delete_button.clicked.connect(self.delete_clicked.emit)
        self.delete_button.setEnabled(False)
        
        actions_layout.addWidget(self.save_button)
        actions_layout.addWidget(self.delete_button)
        actions_group.setLayout(actions_layout)
        
        # Add all groups to main layout
        layout.addWidget(description_group)
        layout.addWidget(solution_group)
        layout.addWidget(grid_group)
        layout.addWidget(actions_group)
        layout.addStretch()
        
        self.setLayout(layout)
        
    def set_solution(self, solution_text: str):
        """Update the solution input text"""
        self.solution_input.setText(solution_text)
        
    def get_description(self) -> str:
        """Get the current description text"""
        return self.description_input.text()
        
    def get_grid_size(self) -> int:
        """Get the current grid size"""
        return self.grid_size.value()
        
    def set_delete_button_enabled(self, enabled: bool):
        """Enable or disable the delete button"""
        self.delete_button.setEnabled(enabled)
        
    def clear(self):
        """Clear all inputs"""
        self.description_input.clear()
        self.solution_input.clear()
        self.delete_button.setEnabled(False) 