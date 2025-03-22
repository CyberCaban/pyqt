from dataclasses import dataclass
from typing import List, Tuple
import math

@dataclass
class Match:
    x1: int
    y1: int
    x2: int
    y2: int
    is_visible: bool = True

@dataclass
class Puzzle:
    matches: List[Match]
    target_matches_to_remove: int
    description: str
    solution_check: callable
    difficulty: int = 1

class PuzzleModel:
    def __init__(self):
        self.puzzles = self._init_puzzles()
        self.current_puzzle_index = 0
        self.removed_matches = []
    
    def _init_puzzles(self) -> List[Puzzle]:
        puzzles = []
        
        # Puzzle 1: 6 squares to 3 squares
        puzzle1 = Puzzle(
            matches=[
                # Outer square
                Match(100, 100, 200, 100),
                Match(200, 100, 200, 200),
                Match(200, 200, 100, 200),
                Match(100, 200, 100, 100),
                # Inner squares
                Match(100, 100, 150, 150),
                Match(150, 150, 200, 100),
                Match(150, 150, 200, 200),
                Match(150, 150, 100, 200),
            ],
            target_matches_to_remove=3,
            description="Уберите 3 спички, чтобы получить 3 квадрата",
            solution_check=lambda matches: self._check_squares_solution(matches),
            difficulty=1
        )
        puzzles.append(puzzle1)
        
        # Puzzle 2: House to fish
        puzzle2 = Puzzle(
            matches=[
                # House base
                Match(100, 200, 200, 200),
                # House walls
                Match(100, 200, 150, 100),
                Match(200, 200, 150, 100),
                # Roof
                Match(150, 100, 200, 150),
                Match(150, 100, 100, 150),
                # Door
                Match(130, 200, 130, 160),
                Match(170, 200, 170, 160),
                Match(130, 160, 170, 160),
            ],
            target_matches_to_remove=2,
            description="Уберите 2 спички, чтобы превратить дом в рыбу",
            solution_check=lambda matches: self._check_house_to_fish_solution(matches),
            difficulty=2
        )
        puzzles.append(puzzle2)
        
        # Add more puzzles here...
        
        return puzzles
    
    def _check_squares_solution(self, matches: List[Match]) -> bool:
        # Count visible matches that form squares
        visible_matches = [m for m in matches if m.is_visible]
        squares = 0
        
        # Check for 3x3 squares
        for i in range(len(visible_matches)):
            for j in range(i + 1, len(visible_matches)):
                for k in range(j + 1, len(visible_matches)):
                    if self._forms_square(visible_matches[i], visible_matches[j], visible_matches[k]):
                        squares += 1
        
        return squares == 3
    
    def _check_house_to_fish_solution(self, matches: List[Match]) -> bool:
        # Check if the remaining matches form a fish shape
        visible_matches = [m for m in matches if m.is_visible]
        # Implement fish shape checking logic
        return True  # Placeholder
    
    def _forms_square(self, m1: Match, m2: Match, m3: Match) -> bool:
        # Check if three matches form a square
        points = [(m1.x1, m1.y1), (m1.x2, m1.y2),
                 (m2.x1, m2.y1), (m2.x2, m2.y2),
                 (m3.x1, m3.y1), (m3.x2, m3.y2)]
        
        # Check if we have exactly 4 unique points
        unique_points = set(points)
        if len(unique_points) != 4:
            return False
            
        # Check if all sides are equal length
        points_list = list(unique_points)
        lengths = []
        for i in range(4):
            p1 = points_list[i]
            p2 = points_list[(i + 1) % 4]
            length = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
            lengths.append(length)
            
        return all(abs(lengths[0] - l) < 1 for l in lengths)
    
    def get_current_puzzle(self) -> Puzzle:
        return self.puzzles[self.current_puzzle_index]
    
    def remove_match(self, match_index: int) -> bool:
        puzzle = self.get_current_puzzle()
        if not puzzle.matches[match_index].is_visible:
            return False
        puzzle.matches[match_index].is_visible = False
        self.removed_matches.append(match_index)
        return True
    
    def restore_last_match(self) -> bool:
        if not self.removed_matches:
            return False
        match_index = self.removed_matches.pop()
        self.get_current_puzzle().matches[match_index].is_visible = True
        return True
        
    def next_puzzle(self) -> bool:
        if self.current_puzzle_index < len(self.puzzles) - 1:
            self.current_puzzle_index += 1
            self.removed_matches = []
            return True
        return False
        
    def previous_puzzle(self) -> bool:
        if self.current_puzzle_index > 0:
            self.current_puzzle_index -= 1
            self.removed_matches = []
            return True
        return False 