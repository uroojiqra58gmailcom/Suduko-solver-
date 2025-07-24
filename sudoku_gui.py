"""
Sudoku Solver - GUI Module
This module provides a graphical user interface for the Sudoku solver.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
from typing import List, Tuple, Optional, Callable

from sudoku_solver import SudokuSolver, get_sample_puzzle


class SudokuCell(tk.Frame):
    """
    A custom widget representing a single Sudoku cell.
    """
    def __init__(self, master, row: int, col: int, value: int = 0, 
                 readonly: bool = False, callback: Callable = None):
        """
        Initialize a Sudoku cell.
        
        Args:
            master: The parent widget
            row: The row index (0-8)
            col: The column index (0-8)
            value: The initial value (0 for empty)
            readonly: Whether the cell is part of the initial puzzle
            callback: Function to call when the cell is clicked
        """
        super().__init__(master, width=60, height=60, 
                        highlightthickness=1, highlightbackground="#CCCCCC")
        
        self.row = row
        self.col = col
        self.value = value
        self.readonly = readonly
        self.callback = callback
        self.selected = False
        
        # Create the label to display the value
        self.label = tk.Label(self, text="", font=("Arial", 20), 
                             width=2, height=1)
        self.label.pack(expand=True, fill=tk.BOTH)
        
        # Set initial value
        self.set_value(value)
        
        # Bind click event
        self.label.bind("<Button-1>", self._on_click)
        self.bind("<Button-1>", self._on_click)
    
    def _on_click(self, event):
        """Handle click events on the cell."""
        if self.callback:
            self.callback(self.row, self.col)
    
    def set_value(self, value: int):
        """Set the cell's value."""
        self.value = value
        
        if value == 0:
            self.label.config(text="")
        else:
            self.label.config(text=str(value))
            
        # Update appearance based on whether it's readonly
        if self.readonly and value != 0:
            self.label.config(fg="#000000", font=("Arial", 20, "bold"))
        else:
            self.label.config(fg="#0066CC", font=("Arial", 20))
    
    def select(self):
        """Mark the cell as selected."""
        self.selected = True
        self.config(highlightthickness=2, highlightbackground="#FF0000")
    
    def deselect(self):
        """Mark the cell as not selected."""
        self.selected = False
        self.config(highlightthickness=1, highlightbackground="#CCCCCC")
    
    def is_selected(self) -> bool:
        """Check if the cell is selected."""
        return self.selected
    
    def is_readonly(self) -> bool:
        """Check if the cell is readonly."""
        return self.readonly
    
    def set_readonly(self, readonly: bool):
        """Set whether the cell is readonly."""
        self.readonly = readonly
        self.set_value(self.value)  # Update appearance


class SudokuBoard(tk.Frame):
    """
    A widget representing the entire Sudoku board.
    """
    def __init__(self, master):
        """Initialize the Sudoku board."""
        super().__init__(master, bg="#FFFFFF", padx=5, pady=5)
        
        self.cells = []
        self.selected_cell = None
        
        # Create the grid of cells
        for i in range(9):
            row = []
            for j in range(9):
                cell = SudokuCell(self, i, j, callback=self._on_cell_click)
                
                # Position the cell
                cell.grid(row=i, column=j, padx=(3 if j % 3 == 0 else 1), 
                         pady=(3 if i % 3 == 0 else 1))
                
                row.append(cell)
            self.cells.append(row)
        
        # Bind keyboard events
        self.master.bind("<Key>", self._on_key_press)
    
    def _on_cell_click(self, row: int, col: int):
        """Handle cell click events."""
        # Deselect the previously selected cell
        if self.selected_cell:
            prev_row, prev_col = self.selected_cell
            self.cells[prev_row][prev_col].deselect()
        
        # Select the new cell
        self.cells[row][col].select()
        self.selected_cell = (row, col)
    
    def _on_key_press(self, event):
        """Handle keyboard events."""
        if not self.selected_cell:
            return
            
        row, col = self.selected_cell
        cell = self.cells[row][col]
        
        # Ignore input for readonly cells
        if cell.is_readonly():
            return
            
        # Handle number keys (1-9)
        if event.char.isdigit() and event.char != '0':
            cell.set_value(int(event.char))
        
        # Handle delete/backspace
        elif event.keysym in ('Delete', 'BackSpace'):
            cell.set_value(0)
    
    def get_board(self) -> List[List[int]]:
        """Get the current board state."""
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                row.append(self.cells[i][j].value)
            board.append(row)
        return board
    
    def set_board(self, board: List[List[int]], readonly_mask: List[List[bool]] = None):
        """
        Set the board state.
        
        Args:
            board: A 9x9 grid of values
            readonly_mask: A 9x9 grid indicating which cells are readonly
        """
        for i in range(9):
            for j in range(9):
                value = board[i][j]
                
                # Determine if the cell should be readonly
                readonly = False
                if readonly_mask:
                    readonly = readonly_mask[i][j]
                elif value != 0:
                    readonly = True
                
                # Update the cell
                self.cells[i][j].set_value(value)
                self.cells[i][j].set_readonly(readonly)
        
        # Clear selection
        if self.selected_cell:
            row, col = self.selected_cell
            self.cells[row][col].deselect()
            self.selected_cell = None
    
    def clear_board(self):
        """Clear the board."""
        for i in range(9):
            for j in range(9):
                self.cells[i][j].set_value(0)
                self.cells[i][j].set_readonly(False)
        
        # Clear selection
        if self.selected_cell:
            row, col = self.selected_cell
            self.cells[row][col].deselect()
            self.selected_cell = None
    
    def highlight_solution(self, original_board: List[List[int]], 
                          solved_board: List[List[int]]):
        """
        Highlight the solution by showing filled cells in a different color.
        
        Args:
            original_board: The original board before solving
            solved_board: The solved board
        """
        for i in range(9):
            for j in range(9):
                if original_board[i][j] == 0 and solved_board[i][j] != 0:
                    # This is a cell that was filled by the solver
                    self.cells[i][j].set_value(solved_board[i][j])
                    self.cells[i][j].label.config(fg="#009900")  # Green color


class SudokuGUI:
    """
    The main GUI application for the Sudoku solver.
    """
    def __init__(self, root):
        """
        Initialize the Sudoku GUI.
        
        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        # Set theme and style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure button styles
        self.style.configure('TButton', font=('Arial', 12))
        self.style.configure('Accent.TButton', background='#4CAF50', foreground='white')
        
        # Create the solver
        self.solver = SudokuSolver()
        
        # Create the main frame
        self.main_frame = ttk.Frame(root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create the title
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(title_frame, text="Sudoku Solver", 
                               font=("Arial", 24, "bold"))
        title_label.pack()
        
        # Create the board
        self.board = SudokuBoard(self.main_frame)
        self.board.pack(pady=10)
        
        # Create the controls
        self.create_controls()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, 
                              font=("Arial", 10), anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Initialize with a sample puzzle
        self.load_sample_puzzle("medium")
    
    def create_controls(self):
        """Create the control buttons and options."""
        # Control frame
        control_frame = ttk.Frame(self.main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        # Difficulty selection
        difficulty_frame = ttk.Frame(control_frame)
        difficulty_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))
        
        ttk.Label(difficulty_frame, text="Difficulty:", 
                 font=("Arial", 12)).pack(side=tk.LEFT, padx=(0, 10))
        
        self.difficulty_var = tk.StringVar(value="Medium")
        difficulties = ["Easy", "Medium", "Hard"]
        
        difficulty_menu = ttk.Combobox(difficulty_frame, 
                                      textvariable=self.difficulty_var,
                                      values=difficulties, width=10, 
                                      state="readonly")
        difficulty_menu.pack(side=tk.LEFT)
        
        # Button frame
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X)
        
        # Create a grid for buttons (2x3)
        for i in range(2):
            button_frame.columnconfigure(i, weight=1)
        
        # Solve button
        solve_btn = ttk.Button(button_frame, text="Solve Puzzle", 
                              command=self.solve_puzzle, style='Accent.TButton')
        solve_btn.grid(row=0, column=0, padx=5, pady=5, sticky=tk.EW)
        
        # Generate button
        generate_btn = ttk.Button(button_frame, text="Generate Puzzle", 
                                 command=self.generate_puzzle)
        generate_btn.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # Clear button
        clear_btn = ttk.Button(button_frame, text="Clear Board", 
                              command=self.clear_board)
        clear_btn.grid(row=1, column=0, padx=5, pady=5, sticky=tk.EW)
        
        # Check button
        check_btn = ttk.Button(button_frame, text="Check Puzzle", 
                              command=self.check_puzzle)
        check_btn.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # Load sample button
        sample_btn = ttk.Button(button_frame, text="Load Sample", 
                               command=lambda: self.load_sample_puzzle(
                                   self.difficulty_var.get().lower()))
        sample_btn.grid(row=2, column=0, padx=5, pady=5, sticky=tk.EW)
        
        # Hint button
        hint_btn = ttk.Button(button_frame, text="Get Hint", 
                             command=self.get_hint)
        hint_btn.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)
    
    def solve_puzzle(self):
        """Solve the current puzzle."""
        # Get the current board
        board = self.board.get_board()
        
        # Create a copy of the original board
        original_board = [row[:] for row in board]
        
        # Set the board in the solver
        self.solver.set_board(board)
        
        # Check if the board is valid
        if not self.solver.is_valid_board():
            messagebox.showerror("Invalid Puzzle", 
                               "The current puzzle configuration is invalid.")
            return
        
        # Update status
        self.status_var.set("Solving puzzle...")
        self.root.update_idletasks()
        
        # Solve in a separate thread to avoid freezing the UI
        def solve_thread():
            # Solve the puzzle
            start_time = time.time()
            solved = self.solver.solve()
            solve_time = time.time() - start_time
            
            # Update the UI in the main thread
            self.root.after(0, lambda: self._handle_solve_result(
                solved, original_board, solve_time))
        
        threading.Thread(target=solve_thread).start()
    
    def _handle_solve_result(self, solved: bool, original_board: List[List[int]], 
                            solve_time: float):
        """Handle the result of the solve operation."""
        if solved:
            # Get the solved board
            solved_board = self.solver.get_board()
            steps, _ = self.solver.get_solve_metrics()
            
            # Update the board
            self.board.highlight_solution(original_board, solved_board)
            
            # Update status
            self.status_var.set(
                f"Solved in {solve_time:.2f} seconds and {steps} steps.")
            
            messagebox.showinfo("Success", 
                              f"Puzzle solved in {solve_time:.2f} seconds and {steps} steps!")
        else:
            self.status_var.set("Failed to solve puzzle.")
            messagebox.showerror("Error", "No solution exists for this puzzle!")
    
    def generate_puzzle(self):
        """Generate a new puzzle with the selected difficulty."""
        difficulty = self.difficulty_var.get().lower()
        
        # Update status
        self.status_var.set(f"Generating {difficulty} puzzle...")
        self.root.update_idletasks()
        
        # Generate in a separate thread
        def generate_thread():
            # Generate the puzzle
            solved_board = self.solver.generate_puzzle(difficulty)
            
            # Get the generated puzzle
            board = self.solver.get_board()
            
            # Update the UI in the main thread
            self.root.after(0, lambda: self._handle_generate_result(board))
        
        threading.Thread(target=generate_thread).start()
    
    def _handle_generate_result(self, board: List[List[int]]):
        """Handle the result of the generate operation."""
        # Update the board
        self.board.set_board(board)
        
        # Update status
        difficulty = self.difficulty_var.get()
        self.status_var.set(f"Generated a new {difficulty} puzzle.")
    
    def clear_board(self):
        """Clear the board."""
        self.board.clear_board()
        self.status_var.set("Board cleared.")
    
    def check_puzzle(self):
        """Check if the current puzzle is valid and has a unique solution."""
        # Get the current board
        board = self.board.get_board()
        
        # Set the board in the solver
        self.solver.set_board(board)
        
        # Check if the board is valid
        if not self.solver.is_valid_board():
            messagebox.showerror("Invalid Puzzle", 
                               "The current puzzle configuration is invalid.")
            return
        
        # Count solutions
        solutions = self.solver.count_solutions()
        
        if solutions == 0:
            messagebox.showinfo("Check Result", 
                              "The puzzle has no solutions.")
        elif solutions == 1:
            messagebox.showinfo("Check Result", 
                              "The puzzle is valid and has a unique solution.")
        else:
            messagebox.showinfo("Check Result", 
                              f"The puzzle has multiple solutions ({solutions}).")
    
    def load_sample_puzzle(self, difficulty: str):
        """Load a sample puzzle of the specified difficulty."""
        # Get a sample puzzle
        board = get_sample_puzzle(difficulty)
        
        # Update the board
        self.board.set_board(board)
        
        # Update status
        self.status_var.set(f"Loaded a {difficulty} sample puzzle.")
    
    def get_hint(self):
        """Provide a hint by filling in one cell."""
        # Get the current board
        board = self.board.get_board()
        
        # Find empty cells
        empty_cells = []
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    empty_cells.append((i, j))
        
        if not empty_cells:
            messagebox.showinfo("Hint", "The board is already complete!")
            return
        
        # Set the board in the solver
        self.solver.set_board(board)
        
        # Check if the board is valid
        if not self.solver.is_valid_board():
            messagebox.showerror("Invalid Puzzle", 
                               "The current puzzle configuration is invalid.")
            return
        
        # Solve the puzzle
        if not self.solver.solve():
            messagebox.showerror("Error", "No solution exists for this puzzle!")
            return
        
        # Get the solved board
        solved_board = self.solver.get_board()
        
        # Choose a random empty cell to fill
        import random
        row, col = random.choice(empty_cells)
        
        # Update the cell
        self.board.cells[row][col].set_value(solved_board[row][col])
        self.board.cells[row][col].set_readonly(True)
        self.board.cells[row][col].label.config(fg="#009900")  # Green color
        
        # Update status
        self.status_var.set(f"Hint provided at cell ({row+1}, {col+1}).")


if __name__ == "__main__":
    # Create the root window
    root = tk.Tk()
    
    # Create the GUI
    app = SudokuGUI(root)
    
    # Start the main loop
    root.mainloop()
