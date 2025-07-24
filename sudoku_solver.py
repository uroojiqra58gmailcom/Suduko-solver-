"""
Sudoku Solver - Core Logic Module
This module contains the core logic for solving and generating Sudoku puzzles.
"""
import random
import copy
import time
from typing import List, Tuple, Optional, Set


class SudokuSolver:
    """
    A class that handles Sudoku puzzle solving and generation.
    Uses backtracking algorithm for solving puzzles.
    """
    
    def __init__(self, board: List[List[int]] = None):
        """
        Initialize the Sudoku solver with an optional board.
        
        Args:
            board: A 9x9 grid representing the Sudoku puzzle. 
                  0 represents empty cells.
        """
        if board:
            self.board = board
        else:
            self.board = [[0 for _ in range(9)] for _ in range(9)]
        
        # Track solving metrics
        self.steps = 0
        self.start_time = 0
        self.solve_time = 0
    
    def is_valid(self, num: int, pos: Tuple[int, int]) -> bool:
        """
        Check if placing a number at the specified position is valid.
        
        Args:
            num: The number to check (1-9)
            pos: The position (row, col) to check
            
        Returns:
            True if the placement is valid, False otherwise
        """
        row, col = pos
        
        # Check row
        for x in range(9):
            if self.board[row][x] == num and col != x:
                return False
                
        # Check column
        for x in range(9):
            if self.board[x][col] == num and row != x:
                return False
        
        # Check 3x3 box
        box_x = col // 3
        box_y = row // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.board[i][j] == num and (i, j) != pos:
                    return False
                    
        return True
    
    def find_empty(self) -> Optional[Tuple[int, int]]:
        """
        Find an empty cell in the board.
        
        Returns:
            The position (row, col) of an empty cell, or None if no empty cells exist
        """
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None
    
    def solve(self) -> bool:
        """
        Solve the Sudoku puzzle using backtracking algorithm.
        
        Returns:
            True if a solution was found, False otherwise
        """
        self.steps = 0
        self.start_time = time.time()
        
        result = self._solve_backtrack()
        
        self.solve_time = time.time() - self.start_time
        return result
    
    def _solve_backtrack(self) -> bool:
        """
        Internal recursive backtracking algorithm to solve the puzzle.
        
        Returns:
            True if a solution was found, False otherwise
        """
        self.steps += 1
        
        # Find an empty cell
        empty = self.find_empty()
        if not empty:
            return True  # Puzzle is solved
            
        row, col = empty
        
        # Try placing digits 1-9
        for num in range(1, 10):
            if self.is_valid(num, (row, col)):
                # Place the number if valid
                self.board[row][col] = num
                
                # Recursively try to solve the rest
                if self._solve_backtrack():
                    return True
                    
                # If we get here, the current placement didn't work
                # Backtrack by resetting the cell
                self.board[row][col] = 0
                
        # No solution found with current configuration
        return False
    
    def is_valid_board(self) -> bool:
        """
        Check if the current board configuration is valid.
        
        Returns:
            True if the board is valid, False otherwise
        """
        # Check each cell
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    # Temporarily set cell to 0 to check if its value is valid
                    num = self.board[i][j]
                    self.board[i][j] = 0
                    if not self.is_valid(num, (i, j)):
                        self.board[i][j] = num  # Restore value
                        return False
                    self.board[i][j] = num  # Restore value
        return True
    
    def count_solutions(self, max_solutions: int = 2) -> int:
        """
        Count the number of solutions for the current board.
        Stops counting after max_solutions is reached.
        
        Args:
            max_solutions: Maximum number of solutions to count
            
        Returns:
            The number of solutions (up to max_solutions)
        """
        solutions = [0]  # Use a list to allow modification in nested function
        
        def backtrack() -> bool:
            # Find an empty cell
            empty = self.find_empty()
            if not empty:
                solutions[0] += 1
                return solutions[0] >= max_solutions
                
            row, col = empty
            
            # Try placing digits 1-9
            for num in range(1, 10):
                if self.is_valid(num, (row, col)):
                    # Place the number if valid
                    self.board[row][col] = num
                    
                    # Recursively try to solve the rest
                    if backtrack():
                        self.board[row][col] = 0
                        return True
                        
                    # Backtrack
                    self.board[row][col] = 0
            
            return False
        
        # Create a copy of the board to restore later
        original_board = copy.deepcopy(self.board)
        
        # Count solutions
        backtrack()
        
        # Restore the original board
        self.board = original_board
        
        return solutions[0]
    
    def generate_puzzle(self, difficulty: str = "medium") -> None:
        """
        Generate a new Sudoku puzzle with the specified difficulty.
        
        Args:
            difficulty: The difficulty level ("easy", "medium", "hard")
        """
        # Clear the board
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        
        # Fill the diagonal 3x3 boxes (these can be filled independently)
        for i in range(0, 9, 3):
            self._fill_box(i, i)
        
        # Solve the rest of the board
        self._solve_backtrack()
        
        # Create a fully solved board
        solved_board = copy.deepcopy(self.board)
        
        # Remove numbers based on difficulty
        self._remove_numbers(difficulty)
        
        return solved_board
    
    def _fill_box(self, row: int, col: int) -> None:
        """
        Fill a 3x3 box with random numbers.
        
        Args:
            row: The starting row of the box
            col: The starting column of the box
        """
        nums = list(range(1, 10))
        random.shuffle(nums)
        
        index = 0
        for i in range(3):
            for j in range(3):
                self.board[row + i][col + j] = nums[index]
                index += 1
    
    def _remove_numbers(self, difficulty: str) -> None:
        """
        Remove numbers from the solved board to create a puzzle.
        
        Args:
            difficulty: The difficulty level ("easy", "medium", "hard")
        """
        # Define difficulty levels
        difficulty_levels = {
            "easy": 35,      # 35 cells to remove (46 remain)
            "medium": 45,    # 45 cells to remove (36 remain)
            "hard": 55       # 55 cells to remove (26 remain)
        }
        
        # Default to medium if invalid difficulty provided
        cells_to_remove = difficulty_levels.get(difficulty.lower(), 45)
        
        # Get all cell positions
        all_cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(all_cells)
        
        # Keep track of the current board
        current_board = copy.deepcopy(self.board)
        
        # Remove cells one by one
        removed = 0
        for row, col in all_cells:
            if removed >= cells_to_remove:
                break
                
            # Remember the value
            backup = self.board[row][col]
            self.board[row][col] = 0
            
            # Make a copy of the current board
            board_copy = copy.deepcopy(self.board)
            
            # Check if the board still has a unique solution
            if self.count_solutions() == 1:
                removed += 1
            else:
                # If not, restore the value
                self.board[row][col] = backup
    
    def get_board(self) -> List[List[int]]:
        """
        Get the current board.
        
        Returns:
            A copy of the current board
        """
        return copy.deepcopy(self.board)
    
    def set_board(self, board: List[List[int]]) -> None:
        """
        Set the board to a new configuration.
        
        Args:
            board: A 9x9 grid representing the Sudoku puzzle
        """
        self.board = copy.deepcopy(board)
    
    def get_solve_metrics(self) -> Tuple[int, float]:
        """
        Get metrics from the last solve operation.
        
        Returns:
            A tuple containing (steps, solve_time)
        """
        return (self.steps, self.solve_time)
    
    def print_board(self) -> None:
        """
        Print the current board to the console in a readable format.
        """
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - -")
                
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")
                    
                if j == 8:
                    print(self.board[i][j])
                else:
                    print(str(self.board[i][j]) + " ", end="")


def get_sample_puzzle(difficulty: str = "medium") -> List[List[int]]:
    """
    Get a sample puzzle of the specified difficulty.
    
    Args:
        difficulty: The difficulty level ("easy", "medium", "hard")
        
    Returns:
        A 9x9 grid representing a Sudoku puzzle
    """
    puzzles = {
        "easy": [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ],
        "medium": [
            [0, 0, 0, 2, 6, 0, 7, 0, 1],
            [6, 8, 0, 0, 7, 0, 0, 9, 0],
            [1, 9, 0, 0, 0, 4, 5, 0, 0],
            [8, 2, 0, 1, 0, 0, 0, 4, 0],
            [0, 0, 4, 6, 0, 2, 9, 0, 0],
            [0, 5, 0, 0, 0, 3, 0, 2, 8],
            [0, 0, 9, 3, 0, 0, 0, 7, 4],
            [0, 4, 0, 0, 5, 0, 0, 3, 6],
            [7, 0, 3, 0, 1, 8, 0, 0, 0]
        ],
        "hard": [
            [0, 0, 0, 6, 0, 0, 4, 0, 0],
            [7, 0, 0, 0, 0, 3, 6, 0, 0],
            [0, 0, 0, 0, 9, 1, 0, 8, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 0, 1, 8, 0, 0, 0, 3],
            [0, 0, 0, 3, 0, 6, 0, 4, 5],
            [0, 4, 0, 2, 0, 0, 0, 6, 0],
            [9, 0, 3, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 1, 0, 0]
        ]
    }
    
    return puzzles.get(difficulty.lower(), puzzles["medium"])


if __name__ == "__main__":
    # Example usage of the solver in CLI mode
    print("Sudoku Solver - CLI Mode")
    print("------------------------")
    
    # Create a solver with a sample puzzle
    puzzle = get_sample_puzzle("medium")
    solver = SudokuSolver(puzzle)
    
    print("Original puzzle:")
    solver.print_board()
    
    print("\nSolving...")
    if solver.solve():
        steps, time_taken = solver.get_solve_metrics()
        print(f"\nSolved in {steps} steps and {time_taken:.4f} seconds:")
        solver.print_board()
    else:
        print("\nNo solution exists!")
