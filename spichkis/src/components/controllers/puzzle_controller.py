from ..models.puzzle_model import PuzzleModel
from ..views.puzzle_view import PuzzleView
from PyQt6.QtWidgets import QMessageBox

class PuzzleController:
    def __init__(self, model: PuzzleModel, view: PuzzleView):
        self.model = model
        self.view = view
        self.init_controller()
        
    def init_controller(self):
        self.view.match_clicked.connect(self.handle_match_click)
        self.update_view()
        
    def handle_match_click(self, match_index: int):
        if match_index == -1:  # Restore signal
            if self.model.restore_last_match():
                self.update_view()
        elif match_index == -2:  # Previous puzzle
            if self.model.previous_puzzle():
                self.update_view()
        elif match_index == -3:  # Next puzzle
            if self.model.next_puzzle():
                self.update_view()
        else:
            if self.model.remove_match(match_index):
                self.update_view()
                self.check_solution()
                
    def update_view(self):
        current_puzzle = self.model.get_current_puzzle()
        self.view.set_matches(current_puzzle.matches)
        self.view.set_puzzle_info(
            current_puzzle.description,
            self.model.current_puzzle_index + 1,
            len(self.model.puzzles)
        )
        
    def check_solution(self):
        puzzle = self.model.get_current_puzzle()
        print(self.model.removed_matches)
        removed_count = len(self.model.removed_matches[puzzle.id])
        
        if removed_count == puzzle.target_matches_to_remove:
            if puzzle.solution_check(puzzle.matches):
                msg = QMessageBox(self.view)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Поздравляем!")
                msg.setText("Головоломка решена правильно!")
                msg.setInformativeText("Хотите перейти к следующей головоломке?")
                msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                
                if msg.exec() == QMessageBox.StandardButton.Yes:
                    if self.model.next_puzzle():
                        self.update_view()
            else:
                QMessageBox.warning(self.view, "Попробуйте еще раз", 
                                  "Решение неверное") 