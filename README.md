# 🧨 Minesweeper in Python

This repository contains a **Minesweeper** game implemented in **Python**, including a command-line version and basic testing infrastructure.

---

## 🗂️ Project Structure
mines/<br/>
|── src/<br/>
│   ├── board.py      # The main board logic (setup, reveal, flag, etc.)<br/>
│   ├── game.py       # Game loop & CLI interactions with the player<br/>
│   └── utils.py      # Utility functions (e.g., display helpers)<br/>
|── tests/<br/>
│   └── test_board.py # Unit tests for board functionality<br/>
|── LICENSE           # Project license (if applicable)<br/>
|── README.md         # This file<br/>

---

## ⚙️ Features

- Initialize a Minesweeper board of custom size (width × height) with a configurable number of mines.
- Reveal tiles, including recursive blank tile expansion.
- Flag/unflag tiles as potential mines.
- Detect end-of-game conditions: win or loss.
- A clean command-line interface for interactive play.
- Unit tests covering core board logic.

---

## 🚀 Getting Started

### Prerequisites

- Python **3.8+** installed
- Optionally: `venv` or another virtual environment tool

### Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/andreibel/mines.git
   cd mines
2. Create & activate a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
4. Install any dependencies (if listed in requirements.txt):
   ```bash
   pip install -r requirements.txt
   
