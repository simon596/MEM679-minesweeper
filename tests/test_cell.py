# tests/test_cell.py

import unittest
from src.cell import Cell

class TestCell(unittest.TestCase):
    def test_cell_initialization(self):
        cell = Cell(0, 0)
        self.assertEqual(cell.x, 0)
        self.assertEqual(cell.y, 0)
        self.assertFalse(cell.is_mine)
        self.assertFalse(cell.is_revealed)
        self.assertFalse(cell.is_flagged)
        self.assertEqual(cell.adjacent_mines, 0)

    def test_set_mine(self):
        cell = Cell(0, 0)
        cell.set_mine()
        self.assertTrue(cell.is_mine)

    def test_toggle_flag(self):
        cell = Cell(0, 0)
        cell.toggle_flag()
        self.assertTrue(cell.is_flagged)
        cell.toggle_flag()
        self.assertFalse(cell.is_flagged)

    def test_reveal(self):
        cell = Cell(0, 0)
        result = cell.reveal()
        self.assertTrue(result)
        self.assertTrue(cell.is_revealed)

    def test_reveal_flagged_cell(self):
        cell = Cell(0, 0)
        cell.toggle_flag()
        result = cell.reveal()
        self.assertFalse(result)
        self.assertFalse(cell.is_revealed)

    def test_set_adjacent_mines(self):
        cell = Cell(0, 0)
        cell.set_adjacent_mines(3)
        self.assertEqual(cell.adjacent_mines, 3)

if __name__ == '__main__':
    unittest.main()
