# game.py

from src.board import Board

class Game:
    def __init__(self, rows=16, columns=16, mines=40):
        self.board = Board(rows, columns, mines)
        self.game_over = False
        self.win = False
        self.first_click = True  # Flag to check if it's the first click

    def reveal_cell(self, x, y):
        if self.game_over:
            return

        if self.first_click:
            self.board.place_mines(x, y)
            self.first_click = False

        cell = self.board.grid[x][y]
        if cell.is_flagged:
            return
        if cell.is_mine:
            cell.reveal()
            self.board.reveal_all_mines()
            self.game_over = True
            self.win = False
        else:
            self.board.reveal_cell(x, y)
            if self.board.is_win():
                self.game_over = True
                self.win = True

    def toggle_flag(self, x, y):
        if self.game_over:
            return
        if self.first_click:
            # Allow flagging before the first click reveals a cell
            self.board.place_mines(x, y)
            self.first_click = False
        self.board.toggle_flag(x, y)

    def chord_cell(self, x, y):
        if self.game_over or self.first_click:
            return
        mine_triggered = self.board.chord_cell(x, y)
        if mine_triggered:
            self.board.reveal_all_mines()
            self.game_over = True
            self.win = False
        else:
            if self.board.is_win():
                self.game_over = True
                self.win = True
