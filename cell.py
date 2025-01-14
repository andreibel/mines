from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QPushButton

class Cell(QPushButton):
    # Signal to request revealing neighbors when a revealed cell is clicked
    reveal_neighbors_signal = pyqtSignal(int, int)

    def __init__(self, x, y):
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
        if event.button() == 1:  # Left click
            # If already revealed, trigger neighbor reveal check
            if self.is_revealed:
                self.reveal_neighbors_signal.emit(self.x, self.y)
            else:
                self.clicked.emit()  # use clicked signal for normal reveal handling
        elif event.button() == 2:  # Right click
            self.toggle_flag()