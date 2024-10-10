# board.py

import random
from src.cell import Cell

class Board:
    def __init__(self, rows, columns, mines):
        self.rows = rows
        self.columns = columns
        self.total_mines = mines
        self.grid = [[Cell(x, y) for y in range(columns)] for x in range(rows)]
        self.mines_placed = False  # Flag to check if mines are placed

    def place_mines(self, exclude_x, exclude_y):
        """
        Place mines on the board, excluding the cell at (exclude_x, exclude_y)
        """
        all_positions = [(x, y) for x in range(self.rows) for y in range(self.columns)]
        exclude_positions = [(exclude_x, exclude_y)]
        # Optionally exclude adjacent cells
        # for dx in (-1, 0, 1):
        #     for dy in (-1, 0, 1):
        #         nx, ny = exclude_x + dx, exclude_y + dy
        #         if 0 <= nx < self.rows and 0 <= ny < self.columns:
        #             exclude_positions.append((nx, ny))

        available_positions = [pos for pos in all_positions if pos not in exclude_positions]
        mines_to_place = self.total_mines

        random.shuffle(available_positions)
        for _ in range(mines_to_place):
            x, y = available_positions.pop()
            self.grid[x][y].set_mine()

        self._calculate_adjacent_mines()
        self.mines_placed = True

    def _calculate_adjacent_mines(self):
        for x in range(self.rows):
            for y in range(self.columns):
                cell = self.grid[x][y]
                if not cell.is_mine:
                    count = self._count_adjacent_mines(x, y)
                    cell.set_adjacent_mines(count)

    def _count_adjacent_mines(self, x, y):
        count = 0
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.rows) and (0 <= ny < self.columns):
                    if self.grid[nx][ny].is_mine:
                        count += 1
        return count

    def reveal_cell(self, x, y):
        cell = self.grid[x][y]
        if cell.reveal():
            if cell.adjacent_mines == 0 and not cell.is_mine:
                # Recursively reveal adjacent cells
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = x + dx, y + dy
                        if (0 <= nx < self.rows) and (0 <= ny < self.columns):
                            neighbor = self.grid[nx][ny]
                            if not neighbor.is_revealed and not neighbor.is_mine:
                                self.reveal_cell(nx, ny)

    def toggle_flag(self, x, y):
        cell = self.grid[x][y]
        cell.toggle_flag()

    def is_win(self):
        for row in self.grid:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True

    def reveal_all_mines(self):
        for row in self.grid:
            for cell in row:
                if cell.is_mine:
                    cell.reveal()

    def chord_cell(self, x, y):
        cell = self.grid[x][y]
        if not cell.is_revealed or cell.is_mine:
            return False  # Cannot chord on unrevealed or mine cells

        # Count flagged adjacent cells
        flagged_count = 0
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.rows) and (0 <= ny < self.columns):
                    neighbor = self.grid[nx][ny]
                    if neighbor.is_flagged:
                        flagged_count += 1

        if flagged_count == cell.adjacent_mines:
            # Reveal all adjacent unflagged and unrevealed cells
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    if (0 <= nx < self.rows) and (0 <= ny < self.columns):
                        neighbor = self.grid[nx][ny]
                        if not neighbor.is_flagged and not neighbor.is_revealed:
                            neighbor.reveal()
                            if neighbor.is_mine:
                                return True  # Mine revealed, game over
                            elif neighbor.adjacent_mines == 0:
                                self.reveal_cell(nx, ny)
        return False  # Chording action completed without hitting a mine
