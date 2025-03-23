from ..models.puzzle_model import PuzzleModel

class PuzzleEditorController:
    def __init__(self, model: PuzzleModel, view):
        self.model = model
        self.view = view
        self.view.puzzle_saved.connect(self.save_puzzle)
        
    def save_puzzle(self, matches, description, solution):
        # Convert matches to the format expected by the model
        puzzle_data = {
            "matches": [
                {
                    "x1": match.x1,
                    "y1": match.y1,
                    "x2": match.x2,
                    "y2": match.y2,
                    "is_visible": match.is_visible
                }
                for match in matches
            ],
            "description": description,
            "solution": solution
        }
        self.model.add_puzzle(puzzle_data) 