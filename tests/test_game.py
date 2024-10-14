# tests/test_game.py

import unittest
from src.game import Game

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game(rows=5, columns=5, mines=5)

    def test_first_click_safe(self):
        self.game.reveal_cell(0, 0)
        self.assertFalse(self.game.first_click)
        self.assertFalse(self.game.board.grid[0][0].is_mine)

    def test_reveal_cell(self):
        self.game.reveal_cell(0, 0)
        self.assertTrue(self.game.board.grid[0][0].is_revealed)

    def test_game_over_on_mine(self):
        # Force a mine at position (1,1)
        self.game.board.grid[1][1].set_mine()
        self.game.board.mines_placed = True  # Indicate that mines have been placed
        self.game.first_click = False  # Indicate that it's not the first click
        self.game.reveal_cell(1, 1)
        self.assertTrue(self.game.game_over)
        self.assertFalse(self.game.win)

    def test_win_game(self):
        self.game.board.place_mines(exclude_x=0, exclude_y=0)
        # Reveal all non-mine cells
        for row in self.game.board.grid:
            for cell in row:
                if not cell.is_mine:
                    cell.reveal()
        self.assertTrue(self.game.board.is_win())
        self.assertFalse(self.game.game_over)
        # Now, attempt to reveal a cell to trigger the win condition in the game
        self.game.reveal_cell(0, 0)
        self.assertTrue(self.game.game_over)
        self.assertTrue(self.game.win)

    def test_toggle_flag(self):
        self.game.toggle_flag(2, 2)
        self.assertTrue(self.game.board.grid[2][2].is_flagged)
        self.game.toggle_flag(2, 2)
        self.assertFalse(self.game.board.grid[2][2].is_flagged)

    def test_chord_cell_no_mine_triggered(self):
        self.game.board.place_mines(exclude_x=2, exclude_y=2)
        cell = self.game.board.grid[2][2]
        cell.reveal()
        # Flag all adjacent mines
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = 2 + dx, 2 + dy
                if 0 <= nx < self.game.board.rows and 0 <= ny < self.game.board.columns:
                    neighbor = self.game.board.grid[nx][ny]
                    if neighbor.is_mine:
                        neighbor.toggle_flag()
        # Perform chording
        self.game.chord_cell(2, 2)
        self.assertFalse(self.game.game_over)

    def test_chord_cell_mine_triggered(self):
        self.game.board.place_mines(exclude_x=2, exclude_y=2)
        cell = self.game.board.grid[2][2]
        cell.reveal()
        # Flag incorrect cells
        self.game.board.grid[1][1].toggle_flag()
        # Perform chording
        self.game.chord_cell(2, 2)
        self.assertTrue(self.game.game_over)
        self.assertFalse(self.game.win)

if __name__ == '__main__':
    unittest.main()
