from game import Game
import sys
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    # Adjust these values for board size and number of mines
    rows, cols, num_mines = 10, 10, 15
    game = Game(rows, cols, num_mines)
    game.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()