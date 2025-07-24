# Sudolo Game - Advanced Sudoku Solver & Generator

<div align="center">
  <img src="https://raw.githubusercontent.com/LazyRobotEngine/sudolo-game/main/assets/sudolo_logo.png" alt="Sudolo Logo" width="200" height="200" style="display: none;">
  <h2>🧩 Solve, Generate, and Master Sudoku Puzzles 🧩</h2>
</div>

## 📋 Overview

Sudolo Game is a feature-rich Sudoku application that combines powerful solving algorithms with an elegant, user-friendly interface. Whether you're a Sudoku beginner or expert, Sudolo offers tools to enhance your puzzle-solving experience with multiple difficulty levels, intelligent hints, and performance metrics.

This application provides both a graphical user interface (GUI) for interactive play and a command-line interface (CLI) for quick solving and automation.

## ✨ Key Features

- **🔍 Advanced Solving Engine**: Efficiently solves any valid Sudoku puzzle using optimized backtracking algorithms
- **🎮 Dual Interface**: Choose between an intuitive GUI or a powerful CLI
- **🎲 Puzzle Generation**: Create new puzzles with customizable difficulty levels (Easy, Medium, Hard)
- **🎯 Intelligent Hint System**: Get strategic hints when you're stuck
- **⏱️ Performance Analytics**: Track solving time and algorithmic steps
- **🔄 Puzzle Validation**: Verify puzzle validity and solution uniqueness
- **📊 Visual Feedback**: Color-coded cells distinguish original clues from your entries and solutions
- **📚 Sample Puzzles**: Practice with built-in puzzles of varying difficulties

## 🖼️ Screenshots

<div align="center">
  <p><i>Run the application to see Sudolo in action!</i></p>
  <p>The GUI features a clean, modern interface with intuitive controls and visual feedback.</p>
</div>

## 🔧 Requirements

- **Python 3.6+**
- **Tkinter** (included with most Python installations)
- **No external dependencies required!**

## 📥 Installation

No complex installation process needed! Simply clone the repository and run the application:

```bash
# Clone the repository
git clone https://github.com/LazyRobotEngine/sudolo-game.git

# Navigate to the project directory
cd sudolo-game

# Run the application
python main.py
```

## 🚀 Usage Guide

### 🖥️ Graphical User Interface (GUI)

Launch the GUI for an interactive experience:

```bash
python main.py
```

### ⌨️ Command-Line Interface (CLI)

For quick solving or automation:

```bash
# Basic CLI usage
python main.py --cli

# Specify difficulty level
python main.py --cli --difficulty easy
python main.py --cli --difficulty medium
python main.py --cli --difficulty hard
```

## 📝 How to Use the GUI

### 🎮 Basic Controls
- **Cell Selection**: Click on any cell to select it
- **Number Entry**: Type a number (1-9) to fill the selected cell
- **Delete Entry**: Press Delete or Backspace to clear a cell

### 🛠️ Features
1. **Solving Puzzles**
   - Enter the puzzle manually or load a sample
   - Click "Solve Puzzle" to find the solution
   - Watch as the solution appears with visual highlighting

2. **Generating New Puzzles**
   - Select your preferred difficulty from the dropdown
   - Click "Generate Puzzle" to create a new challenge
   - Each puzzle is guaranteed to have a unique solution

3. **Getting Assistance**
   - Click "Get Hint" when you're stuck
   - The system will intelligently fill in one cell
   - Use "Check Puzzle" to validate your current progress

4. **Managing the Board**
   - "Clear Board" resets the entire puzzle
   - "Load Sample" provides pre-defined puzzles to practice

## 🧠 How It Works

### 🔍 Solving Algorithm
Sudolo uses an optimized backtracking algorithm that:

1. Identifies empty cells in the puzzle grid
2. Systematically tries numbers 1-9 in each empty cell
3. Validates each placement against Sudoku rules (row, column, and 3x3 box)
4. Recursively attempts to solve the remaining cells
5. Backtracks when an invalid state is reached
6. Continues until a complete solution is found or all possibilities are exhausted

### 🎲 Puzzle Generation
The generator creates puzzles through a sophisticated process:

1. Starts with a completely solved, valid Sudoku board
2. Strategically removes numbers while maintaining puzzle integrity
3. Ensures each puzzle has exactly one solution
4. Adjusts the number of removed cells based on the selected difficulty:
   - Easy: ~35 cells removed
   - Medium: ~45 cells removed
   - Hard: ~55 cells removed

## 📁 Project Structure

```
sudolo-game/
├── main.py              # Application entry point
├── sudoku_solver.py     # Core solving and generation algorithms
├── sudoku_gui.py        # Graphical user interface implementation
└── README.md            # Project documentation
```

## 🔮 Future Enhancements

- **Puzzle Saving/Loading**: Save your progress and return later
- **Timed Challenges**: Test your solving speed against the clock
- **Difficulty Rating**: Precise difficulty ratings beyond basic categories
- **Solving Techniques**: Step-by-step solving using human techniques
- **Themes & Customization**: Personalize your solving experience
- **Leaderboards**: Compare your solving times with others

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Special thanks to all Sudoku enthusiasts and puzzle creators
- Inspired by classic Sudoku solving techniques and modern UI design principles
- Built with ❤️ by [LazyRobotEngine](https://github.com/LazyRobotEngine)
