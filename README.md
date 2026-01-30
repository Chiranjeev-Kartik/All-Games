# Terminal Arcade V3

A collection of classic terminal games with a polished, colorful TUI and persistent statistics.

![Terminal Arcade](https://placehold.co/600x400?text=Terminal+Arcade+V3)

## 🎮 Games Included

1.  **🧩 Sudoku**
    - Classic number puzzle.
    - Fill the 9x9 grid so that each column, each row, and each of the nine 3x3 subgrids contain all of the digits from 1 to 9.

2.  **♟️ Chess vs AI**
    - Play standard chess against a basic AI engine.
    - Features move validation and check/checkmate detection.
    - _Powered by `python-chess`._

3.  **💣 Minesweeper**
    - Classic mine detection game.
    - Clear the board without detonating any hidden mines using clues about the number of neighboring mines.

## ✨ Features

- **Rich TUI**: Beautiful interface using ANSI colors and ASCII art.
- **Stats Tracking**: detailed statistics for wins and games played.
- **Easy Navigation**: Use Arrow keys or Vim keys (if supported) to navigate menus.
- **Cross-Platform**: Designed to work on Windows, macOS, and Linux terminals.

## 🚀 Installation & Usage

### Prerequisites

- Python 3.8+
- Pip

### Setup

1.  **Clone the repository**

    ```bash
    git clone https://github.com/Imposter-zx/All-Games.git
    cd All-Games
    ```

2.  **Install Dependencies**

    ```bash
    pip install -r terminal_games/requirements.txt
    ```

3.  **Run the Arcade**
    ```bash
    python terminal_games/arcade.py
    ```

## 🛠️ Project Structure

```
All Games/
├── terminal_games/
│   ├── arcade.py          # Main launcher
│   ├── chess_game.py      # Chess implementation
│   ├── sudoku.py          # Sudoku implementation
│   ├── minesweeper.py     # Minesweeper implementation
│   ├── arcade_utils.py    # Shared utilities (colors, input)
│   └── input_utils.py     # Input handling
├── README.md              # This file
└── .gitignore
```

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.
