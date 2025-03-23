from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from .models.puzzle_model import PuzzleModel
from .views.puzzle_view import PuzzleView
from .views.puzzle_editor_view import PuzzleEditorView
from .controllers.puzzle_controller import PuzzleController
from .controllers.puzzle_editor_controller import PuzzleEditorController

class Spichkis(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Create shared model
        self.model = PuzzleModel()
        
        # Create tabs
        tabs = QTabWidget()
        
        # Game tab
        game_view = PuzzleView()
        self.game_controller = PuzzleController(self.model, game_view)
        tabs.addTab(game_view, "Игра")
        
        # Editor tab
        editor_view = PuzzleEditorView()
        self.editor_controller = PuzzleEditorController(self.model, editor_view)
        tabs.addTab(editor_view, "Редактор")
        
        layout.addWidget(tabs)
        self.setLayout(layout)
