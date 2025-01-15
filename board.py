from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QGridLayout
from cell import Cell
import random

class Board(QWidget):
    # Signal to notify game if a revealed cell turned out to be a mine (or safe)
    cell_revealed_signal = pyqtSignal(bool)

    def __init__(self, rows, cols, num_mines, parent=None):
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(1)  # small spacing between cells

        # Create a grid of Cell objects
        self.grid = [[Cell(x, y) for y in range(cols)] for x in range(rows)]
        for x in range(rows):
            for y in range(cols):
                cell = self.grid[x][y]
                self.grid_layout.addWidget(cell, x, y)
                # Connect left-click (non-revealed) to reveal_cell call.
                cell.clicked.connect(lambda _, cx=x, cy=y: self.reveal_cell(cx, cy))
                # When a revealed cell is clicked, try to reveal its neighbors.


        self.place_mines()
        self.calculate_adjacent_mines()

    def place_mines(self):
        mines_placed = 0
        while mines_placed < self.num_mines:
            x = random.randint(0, self.rows - 1)
            y = random.randint(0, self.cols - 1)
            cell = self.grid[x][y]
            if not cell.is_mine:
                cell.is_mine = True
                mines_placed += 1

    def calculate_adjacent_mines(self):
        # For each cell that is not a mine, count adjacent mines.
        for x in range(self.rows):
            for y in range(self.cols):
                cell = self.grid[x][y]
                if cell.is_mine:
                    continue

                count = 0
                # Check all eight neighbors
                for dx, dy in [(-1, -1), (-1, 0), (-1, 1),
                               (0, -1),          (0, 1),
                               (1, -1), (1, 0),  (1, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.rows and 0 <= ny < self.cols:
                        if self.grid[nx][ny].is_mine:
                            count += 1
                cell.adjacent_mines = count

    def reveal_cell(self, x, y):
        cell = self.grid[x][y]
        # If already revealed or flagged, do nothing.
        if cell.is_revealed or cell.is_flagged:
            return

        cell.reveal()

        # If a mine is revealed, emit a signal and stop.
        if cell.is_mine:
            self.cell_revealed_signal.emit(True)
            return

        # Emit signal to indicate a safe cell was revealed.
        self.cell_revealed_signal.emit(False)

        # If no adjacent mines, reveal all adjacent cells recursively.
        if cell.adjacent_mines == 0:
            for dx, dy in [(-1, -1), (-1, 0), (-1, 1),
                           (0, -1),          (0, 1),
                           (1, -1), (1, 0),  (1, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.rows and 0 <= ny < self.cols:
                    self.reveal_cell(nx, ny)

    def reveal_neighbors(self, x, y):
        cell = self.grid[x][y]
        if not cell.is_revealed:
            return

        # Count flags around the cell and collect neighbor references.
        flag_count = 0
        neighbors = []
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1),
                       (0, -1),          (0, 1),
                       (1, -1), (1, 0),  (1, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                neighbor = self.grid[nx][ny]
                neighbors.append(neighbor)
                if neighbor.is_flagged:
                    flag_count += 1

        # If the flag count matches the adjacent mines count, reveal all unflagged neighbors.
        if flag_count == cell.adjacent_mines:
            for neighbor in neighbors:
                if not neighbor.is_revealed and not neighbor.is_flagged:
                    self.reveal_cell(neighbor.x, neighbor.y)

    def check_win_condition(self):
        """Return True if all non-mine cells have been revealed."""
        for row in self.grid:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True

    def reveal_all_cells(self):
        """Reveal every cell on the board (useful at game over)."""
        for row in self.grid:
            for cell in row:
                if not cell.is_revealed:
                    cell.reveal()