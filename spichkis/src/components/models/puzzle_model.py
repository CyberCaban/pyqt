from dataclasses import dataclass
from typing import List, Tuple, Dict
import math
import json
import os

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
    id: str = ""
    solution: Dict = None

class PuzzleModel:
    def __init__(self):
        self.puzzles = self._load_puzzles()
        self.current_puzzle_index = 0
        self.removed_matches = {} 
        
    def _load_puzzles(self) -> List[Puzzle]:
        puzzles = []
        json_path = os.path.join(os.path.dirname(__file__), 'puzzles.json')
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for puzzle_data in data['puzzles']:
            matches = [Match(**match) for match in puzzle_data['matches']]
            puzzle = Puzzle(
                matches=matches,
                target_matches_to_remove=puzzle_data['target_matches_to_remove'],
                description=puzzle_data['description'],
                difficulty=puzzle_data['difficulty'],
                id=puzzle_data['id'],
                solution=puzzle_data['solution'],
                solution_check=self._check_solution
            )
            puzzles.append(puzzle)
            
        return puzzles
    
    def _check_solution(self, matches: List[Match]) -> bool:
        puzzle = self.get_current_puzzle()
        if not puzzle.solution:
            return False
            
       
        current_removed = self.removed_matches.get(puzzle.id, [])
        if set(current_removed) != set(puzzle.solution['removed_matches']):
            return False
            
       
        if len(current_removed) != puzzle.target_matches_to_remove:
            return False
            
        return True
    
    def get_current_puzzle(self) -> Puzzle:
        return self.puzzles[self.current_puzzle_index]
    
    def remove_match(self, match_index: int) -> bool:
        puzzle = self.get_current_puzzle()
        if not puzzle.matches[match_index].is_visible:
            return False
        puzzle.matches[match_index].is_visible = False
        
       
        if puzzle.id not in self.removed_matches:
            self.removed_matches[puzzle.id] = []
        self.removed_matches[puzzle.id].append(match_index)
        
        return True
    
    def restore_last_match(self) -> bool:
        puzzle = self.get_current_puzzle()
        if puzzle.id not in self.removed_matches or not self.removed_matches[puzzle.id]:
            return False
            
        match_index = self.removed_matches[puzzle.id].pop()
        puzzle.matches[match_index].is_visible = True
        return True
        
    def next_puzzle(self) -> bool:
        if self.current_puzzle_index < len(self.puzzles) - 1:
            self.current_puzzle_index += 1
            return True
        return False
        
    def previous_puzzle(self) -> bool:
        if self.current_puzzle_index > 0:
            self.current_puzzle_index -= 1
            return True
        return False 