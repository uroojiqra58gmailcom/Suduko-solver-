"""
Sudoku Solver - Main Application
This is the main entry point for the Sudoku Solver application.
"""
import sys
import tkinter as tk
import argparse

from sudoku_solver import SudokuSolver, get_sample_puzzle
from sudoku_gui import SudokuGUI


def run_cli_mode(difficulty: str = "medium"):
    """
    Run the application in command-line interface mode.
    
    Args:
        difficulty: The difficulty level of the puzzle to solve
    """
    print("Sudoku Solver - CLI Mode")
    print("------------------------")
    
    # Create a solver with a sample puzzle
    puzzle = get_sample_puzzle(difficulty)
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


def run_gui_mode():
    """Run the application in graphical user interface mode."""
    # Create the root window
    root = tk.Tk()
    
    # Create the GUI
    app = SudokuGUI(root)
    
    # Start the main loop
    root.mainloop()


def main():
    """Main entry point for the application."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Sudoku Solver")
    parser.add_argument("--cli", action="store_true", 
                      help="Run in command-line interface mode")
    parser.add_argument("--difficulty", choices=["easy", "medium", "hard"], 
                      default="medium", help="Puzzle difficulty level")
    
    args = parser.parse_args()
    
    # Run in the appropriate mode
    if args.cli:
        run_cli_mode(args.difficulty)
    else:
        run_gui_mode()


if __name__ == "__main__":
    main()
