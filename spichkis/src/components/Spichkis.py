from PyQt6.QtWidgets import QWidget, QVBoxLayout
from .models.puzzle_model import PuzzleModel
from .views.puzzle_view import PuzzleView
from .controllers.puzzle_controller import PuzzleController

class Spichkis(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Создаем компоненты MVC
        model = PuzzleModel()
        view = PuzzleView()
        self.controller = PuzzleController(model, view)
        
        layout.addWidget(view)
        self.setLayout(layout)
