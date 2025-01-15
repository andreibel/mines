from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QPushButton

class Cell(QPushButton):
    """
    Represents a cell in a Minesweeper-like grid game.
    
    Each cell can either contain a mine or a number indicating the count of adjacent mines. 
    It tracks its state (revealed, flagged, etc.) and handles user interactions 
    such as clicking (to reveal the cell) and right-clicking (to toggle between flagged states).
    """

    def __init__(self, x, y):
        """
        Initializes a Cell instance with its grid coordinates, state variables, and style.
    
        :param x: The row index of the cell on the grid.
        :param y: The column index of the cell on the grid.
        """
        super().__init__()
        self.x = x  # cell's row coordinate
        self.y = y  # cell's column coordinate
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0
        self.setFixedSize(40, 40)  # set cell size
        self.setStyleSheet("background-color: lightgray;")  # initial color

    def reveal(self):
        """
        Reveals the cell by updating its state and appearance.
        
        If the cell is flagged, the action is ignored. If the cell contains a mine, 
        it's marked as a bomb. Otherwise, it displays the count of adjacent mines 
        (if applicable) or is left blank. The cell is disabled upon reveal.
        """
        # Avoid revealing if cell is flagged
        if self.is_flagged:
            return

        self.is_revealed = True

        if self.is_mine:
            self.setText("💣")
            self.setStyleSheet("background-color: red;")
        else:
            # If there are adjacent mines, display the count; otherwise blank.
            self.setText(str(self.adjacent_mines) if self.adjacent_mines > 0 else "")
            self.setStyleSheet("background-color: white;color:black;")
        self.setEnabled(False)  # disable further clicks after revealed

    def toggle_flag(self):
        """
        Toggles the flagged state of the cell.
        
        Flags can only be set or removed on un-revealed cells. Flagged cells are displayed 
        with a flag icon and a distinct style, while un-flagged cells revert to their original style.
        """
        # Only toggle flag on unrevealed cell
        if self.is_revealed:
            return

        if self.is_flagged:
            self.is_flagged = False
            self.setText("")
            self.setStyleSheet("background-color: lightgray;")
        else:
            self.is_flagged = True
            self.setText("🚩")
            self.setStyleSheet("background-color: yellow;")

    def mousePressEvent(self, event: QMouseEvent):
        """
        Handles mouse press events on the cell.
        
        :param event: The mouse event that triggered the method.
        
        A left-click (button 1) triggers the clicked signal, 
        typically used to reveal the cell. A right-click (button 2) toggles the flag state.
        """
        if event.button() == 1:  # Left click
            self.clicked.emit()  # use clicked signal for normal reveal handling
        elif event.button() == 2:  # Right click
            self.toggle_flag()