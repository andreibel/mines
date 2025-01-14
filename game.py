from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from board import Board

class Game(QMainWindow):
    def __init__(self, rows, cols, num_mines):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines

        self.setWindowTitle("Minesweeper")
        # Adjust window size (extra space for label and buttons)
        self.setGeometry(100, 100, cols * 40, rows * 40 + 100)

        # Main widget and vertical layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)

        # Status label for game messages
        self.status_label = QLabel("Minesweeper Game")
        self.main_layout.addWidget(self.status_label)

        # Create and add the board to the layout
        self.board = Board(rows, cols, num_mines)
        self.main_layout.addWidget(self.board)

        # Create a horizontal layout for the control buttons
        buttons_layout = QHBoxLayout()
        self.main_layout.addLayout(buttons_layout)

        self.next_game_button = QPushButton("Next Game")
        self.next_game_button.clicked.connect(self.next_game)
        buttons_layout.addWidget(self.next_game_button)

        # Connect board cell signal to game end check.
        self.board.cell_revealed_signal.connect(self.check_game_end)

    def check_game_end(self, is_mine):
        # If a mine was revealed, end game as lost.
        if is_mine:
            self.game_over()
        # Else if win condition is met, declare victory.
        elif self.board.check_win_condition():
            self.game_win()

    def game_over(self):
        self.status_label.setText("Game Over! You hit a mine.")
        self.board.reveal_all_cells()
        self.board.setEnabled(False)

    def game_win(self):
        self.status_label.setText("Congratulations! You won!")
        self.board.setEnabled(False)



    def next_game(self):
        """Start a new game (generate a brand-new board)."""
        self.main_layout.removeWidget(self.board)
        self.board.deleteLater()
        self.board = Board(self.rows, self.cols, self.num_mines)
        self.board.cell_revealed_signal.connect(self.check_game_end)
        self.main_layout.insertWidget(1, self.board)
        self.status_label.setText("Minesweeper Game")
        self.status_label.setText("New Game Started!")