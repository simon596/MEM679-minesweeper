# tests/test_board.py

import unittest
from src.board import Board

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(rows=5, columns=5, mines=5)

    def test_board_initialization(self):
        self.assertEqual(self.board.rows, 5)
        self.assertEqual(self.board.columns, 5)
        self.assertEqual(self.board.total_mines, 5)
        self.assertFalse(self.board.mines_placed)
        self.assertEqual(len(self.board.grid), 5)
        self.assertEqual(len(self.board.grid[0]), 5)

    def test_place_mines(self):
        self.board.place_mines(exclude_x=0, exclude_y=0)
        self.assertTrue(self.board.mines_placed)
        mine_count = sum(cell.is_mine for row in self.board.grid for cell in row)
        self.assertEqual(mine_count, 5)
        self.assertFalse(self.board.grid[0][0].is_mine)  # Ensure exclude cell is not a mine

    def test_calculate_adjacent_mines(self):
        self.board.place_mines(exclude_x=0, exclude_y=0)
        # Since mines are random, we check that adjacent mines count is between 0 and 5
        for row in self.board.grid:
            for cell in row:
                self.assertGreaterEqual(cell.adjacent_mines, 0)
                self.assertLessEqual(cell.adjacent_mines, 5)

    def test_reveal_cell(self):
        self.board.place_mines(exclude_x=0, exclude_y=0)
        self.board.reveal_cell(0, 0)
        self.assertTrue(self.board.grid[0][0].is_revealed)

    def test_reveal_mine(self):
        # Force a mine at position (1,1)
        self.board.grid[1][1].set_mine()
        self.board.grid[1][1].set_adjacent_mines(0)
        self.board.reveal_cell(1, 1)
        self.assertTrue(self.board.grid[1][1].is_revealed)
        self.assertTrue(self.board.grid[1][1].is_mine)

    def test_toggle_flag(self):
        self.board.toggle_flag(2, 2)
        self.assertTrue(self.board.grid[2][2].is_flagged)
        self.board.toggle_flag(2, 2)
        self.assertFalse(self.board.grid[2][2].is_flagged)

    def test_is_win(self):
        self.board.place_mines(exclude_x=0, exclude_y=0)
        # Reveal all non-mine cells
        for row in self.board.grid:
            for cell in row:
                if not cell.is_mine:
                    cell.reveal()
        self.assertTrue(self.board.is_win())

    def test_reveal_all_mines(self):
        self.board.place_mines(exclude_x=0, exclude_y=0)
        self.board.reveal_all_mines()
        for row in self.board.grid:
            for cell in row:
                if cell.is_mine:
                    self.assertTrue(cell.is_revealed)

    def test_chord_cell(self):
        # Set up a cell with adjacent mines
        self.board.place_mines(exclude_x=2, exclude_y=2)
        cell = self.board.grid[2][2]
        cell.reveal()
        # Flag all adjacent mines
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = 2 + dx, 2 + dy
                if 0 <= nx < self.board.rows and 0 <= ny < self.board.columns:
                    neighbor = self.board.grid[nx][ny]
                    if neighbor.is_mine:
                        neighbor.toggle_flag()
        # Perform chording
        result = self.board.chord_cell(2, 2)
        self.assertFalse(result)  # Should not hit a mine
        # Check that all adjacent non-mine cells are revealed
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = 2 + dx, 2 + dy
                if 0 <= nx < self.board.rows and 0 <= ny < self.board.columns:
                    neighbor = self.board.grid[nx][ny]
                    if not neighbor.is_mine and not neighbor.is_flagged:
                        self.assertTrue(neighbor.is_revealed)

if __name__ == '__main__':
    unittest.main()
