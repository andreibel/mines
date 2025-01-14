from PyQt5.QtSql import password
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout
import random

class Cell(QPushButton):
    def __init__(self,x,y):
        super().__init__()
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_opened = False
        self.adjacent_mines = 0
        self.setFixedSize(40,40)
        self.setStyleSheet("background-color: lightgray;")

    def open(self):
        self.is_opened = True
        if self.is_mine:
            self.setText("💣")
        else:
            self.setText(str(self.adjacent_mines) if self.adjacent_mines > 0 else "")
            self.setStyleSheet("background-color: white;")
        self.setEnabled(False)  # Disable the button once revealed

class Board(QWidget):
    def __init__(self, rows, cols, num_mines):
        super().__init__()
        self.cols = cols
        self.rows = rows
        self.num_mines = num_mines
        self.grid_layout = QGridLayout(self)
        self.grid = [[Cell(x, y) for y in range(cols)] for x in range(rows)]
        self.generate_mines()


    def generate_mines(self):
        mines = set()
        while len(mines) < self.num_mines:
            x = random.randint(0, self.cols - 1)
            y = random.randint(0, self.rows - 1)
            mines.add((x, y))
        for i in mines:
            self.grid[i[0]][i[1]].is_mine = True

    def calculate_adjacent_mines(self):
        for i in range(self.cols):
            for j in range(self.rows):
                if self.grid[i][j].is_mine:
                    continue
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
                    x , y = i + dx, j + dy
                    if 0 <= x < self.cols and 0 <= y < self.rows and self.grid[x][y].is_mine:
                        self.grid[x][y].adjacent_mines += 1
                pass
