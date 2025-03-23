from dataclasses import dataclass
from typing import List, Tuple, Dict
import math
import json
import os
import uuid

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
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {'puzzles': []}
            
        for puzzle_data in data['puzzles']:
            matches = [Match(**match) for match in puzzle_data['matches']]
            puzzle = Puzzle(
                matches=matches,
                target_matches_to_remove=puzzle_data.get('target_matches_to_remove', 1),
                description=puzzle_data['description'],
                difficulty=puzzle_data.get('difficulty', 1),
                id=puzzle_data.get('id', str(uuid.uuid4())),
                solution=puzzle_data.get('solution', None),
                solution_check=self._check_solution
            )
            puzzles.append(puzzle)
            
        return puzzles
    
    def _save_puzzles(self):
        json_path = os.path.join(os.path.dirname(__file__), 'puzzles.json')
        data = {
            'puzzles': [
                {
                    'matches': [
                        {
                            'x1': match.x1,
                            'y1': match.y1,
                            'x2': match.x2,
                            'y2': match.y2,
                            'is_visible': match.is_visible
                        }
                        for match in puzzle.matches
                    ],
                    'target_matches_to_remove': puzzle.target_matches_to_remove,
                    'description': puzzle.description,
                    'difficulty': puzzle.difficulty,
                    'id': puzzle.id,
                    'solution': puzzle.solution
                }
                for puzzle in self.puzzles
            ]
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_puzzle(self, puzzle_data: Dict):
        # Create a new puzzle ID
        puzzle_id = str(uuid.uuid4())
        
        # Create solution data - convert string of numbers to list of integers
        solution_str = puzzle_data.get('solution', '')
        removed_matches = [int(x.strip()) for x in solution_str.split(',') if x.strip()]
        solution = {
            'removed_matches': removed_matches
        }
        
        # Create new puzzle
        matches = [Match(**match) for match in puzzle_data['matches']]
        new_puzzle = Puzzle(
            matches=matches,
            target_matches_to_remove=len(removed_matches),
            description=puzzle_data['description'],
            difficulty=1,  # Default difficulty for user-created puzzles
            id=puzzle_id,
            solution=solution,
            solution_check=self._check_solution
        )
        
        # Add to puzzles list
        self.puzzles.append(new_puzzle)
        
        # Save to file
        self._save_puzzles()
        
        # Switch to the new puzzle
        self.current_puzzle_index = len(self.puzzles) - 1
    
    def _check_solution(self, matches: List[Match]) -> bool:
        puzzle = self.get_current_puzzle()
        if not puzzle.solution:
            return False
            
        # Convert current removed matches to integers
        current_removed = [int(x) for x in self.removed_matches.get(puzzle.id, [])]
        solution_matches = [int(x) for x in puzzle.solution['removed_matches']]
        
        # Check if the same matches were removed
        if set(current_removed) != set(solution_matches):
            return False
            
        # Check if the correct number of matches were removed
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