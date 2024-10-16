# board.py

import random  # Import the random module for shuffling and random selection
from mem679_minesweeper.cell import Cell  # Import the Cell class from the src.cell module

class Board:
    """
    Represents the game board for Minesweeper.

    The Board class manages the grid of cells, handles mine placement, and provides
    methods for revealing cells, toggling flags, and checking game state (win/lose conditions).

    Attributes:
        rows (int): Number of rows in the board.
        columns (int): Number of columns in the board.
        total_mines (int): Total number of mines to be placed on the board.
        grid (list of list of Cell): 2D list representing the grid of cells.
        mines_placed (bool): Flag indicating whether mines have been placed on the board.
    """

    def __init__(self, rows, columns, mines):
        """
        Initializes the Board with the given dimensions and number of mines.

        Args:
            rows (int): Number of rows in the board.
            columns (int): Number of columns in the board.
            mines (int): Number of mines to be placed on the board.
        """
        self.rows = rows
        self.columns = columns
        self.total_mines = mines
        # Create a grid of Cell objects
        self.grid = [[Cell(x, y) for y in range(columns)] for x in range(rows)]
        self.mines_placed = False  # Flag to check if mines are placed

    def place_mines(self, exclude_x, exclude_y):
        """
        Places mines randomly on the board, excluding the cell at (exclude_x, exclude_y).

        This method ensures that the first cell revealed by the player is never a mine,
        enhancing gameplay by avoiding immediate game over on the first click.

        Args:
            exclude_x (int): The row index of the cell to exclude from mine placement.
            exclude_y (int): The column index of the cell to exclude from mine placement.
        """
        # Generate all possible cell positions
        all_positions = [(x, y) for x in range(self.rows) for y in range(self.columns)]
        # Create a list of positions to exclude from mine placement
        exclude_positions = [(exclude_x, exclude_y)]

        # Optionally exclude adjacent cells to the first click to make the game easier
        # Uncomment the following block to exclude adjacent cells
        # for dx in (-1, 0, 1):
        #     for dy in (-1, 0, 1):
        #         nx, ny = exclude_x + dx, exclude_y + dy
        #         if 0 <= nx < self.rows and 0 <= ny < self.columns:
        #             exclude_positions.append((nx, ny))

        # Create a list of available positions for mine placement, excluding the specified cells
        available_positions = [pos for pos in all_positions if pos not in exclude_positions]
        mines_to_place = self.total_mines

        # Randomly shuffle the available positions
        random.shuffle(available_positions)
        # Place mines on the board
        for _ in range(mines_to_place):
            x, y = available_positions.pop()
            self.grid[x][y].set_mine()  # Set the cell at (x, y) as a mine

        # Calculate the number of adjacent mines for each cell
        self._calculate_adjacent_mines()
        self.mines_placed = True  # Set the flag indicating mines have been placed

    def _calculate_adjacent_mines(self):
        """
        Calculates and sets the number of adjacent mines for each cell on the board.

        This method iterates over all cells and, for those that are not mines,
        counts the number of neighboring cells that are mines.
        """
        for x in range(self.rows):
            for y in range(self.columns):
                cell = self.grid[x][y]
                if not cell.is_mine:
                    # Count the number of adjacent mines for this cell
                    count = self._count_adjacent_mines(x, y)
                    cell.set_adjacent_mines(count)  # Set the count in the cell

    def _count_adjacent_mines(self, x, y):
        """
        Counts the number of mines adjacent to the cell at (x, y).

        Args:
            x (int): The row index of the cell.
            y (int): The column index of the cell.

        Returns:
            int: The number of adjacent mines.
        """
        count = 0
        # Iterate over all neighboring positions including diagonals
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = x + dx, y + dy  # Neighboring cell coordinates
                # Skip the cell itself
                if dx == 0 and dy == 0:
                    continue
                # Check if neighboring coordinates are within bounds
                if (0 <= nx < self.rows) and (0 <= ny < self.columns):
                    if self.grid[nx][ny].is_mine:
                        count += 1  # Increment count if neighbor is a mine
        return count

    def reveal_cell(self, x, y):
        """
        Reveals the cell at (x, y). If the cell has zero adjacent mines, recursively reveals neighboring cells.

        Args:
            x (int): The row index of the cell to reveal.
            y (int): The column index of the cell to reveal.
        """
        cell = self.grid[x][y]
        if cell.reveal():
            # If the cell was successfully revealed and has zero adjacent mines
            if cell.adjacent_mines == 0 and not cell.is_mine:
                # Recursively reveal adjacent cells
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = x + dx, y + dy
                        # Skip the cell itself
                        if dx == 0 and dy == 0:
                            continue
                        # Check if neighboring coordinates are within bounds
                        if (0 <= nx < self.rows) and (0 <= ny < self.columns):
                            neighbor = self.grid[nx][ny]
                            if not neighbor.is_revealed and not neighbor.is_mine:
                                # Recursively reveal neighbor
                                self.reveal_cell(nx, ny)

    def toggle_flag(self, x, y):
        """
        Toggles a flag on the cell at (x, y).

        Args:
            x (int): The row index of the cell.
            y (int): The column index of the cell.
        """
        cell = self.grid[x][y]
        cell.toggle_flag()

    def is_win(self):
        """
        Checks if the player has won the game.

        The player wins when all non-mine cells have been revealed.

        Returns:
            bool: True if the player has won, False otherwise.
        """
        for row in self.grid:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False  # There are still non-mine cells to reveal
        return True  # All non-mine cells have been revealed

    def reveal_all_mines(self):
        """
        Reveals all mines on the board.

        This method is typically called when the game is over to display all mine locations.
        """
        for row in self.grid:
            for cell in row:
                if cell.is_mine:
                    cell.reveal()

    def chord_cell(self, x, y):
        """
        Performs the chording action on the cell at (x, y).

        Chording reveals all adjacent unrevealed cells if the number of adjacent flags equals the number of adjacent mines.
        If a mine is revealed during chording (due to incorrect flagging), the method returns True to indicate game over.

        Args:
            x (int): The row index of the cell.
            y (int): The column index of the cell.

        Returns:
            bool: True if a mine was revealed during chording (game over), False otherwise.
        """
        cell = self.grid[x][y]
        if not cell.is_revealed or cell.is_mine:
            return False  # Cannot chord on unrevealed or mine cells

        # Count flagged adjacent cells
        flagged_count = 0
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = x + dx, y + dy
                # Skip the cell itself
                if dx == 0 and dy == 0:
                    continue
                if (0 <= nx < self.rows) and (0 <= ny < self.columns):
                    neighbor = self.grid[nx][ny]
                    if neighbor.is_flagged:
                        flagged_count += 1

        if flagged_count == cell.adjacent_mines:
            # Reveal all adjacent unflagged and unrevealed cells
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    # Skip the cell itself
                    if dx == 0 and dy == 0:
                        continue
                    if (0 <= nx < self.rows) and (0 <= ny < self.columns):
                        neighbor = self.grid[nx][ny]
                        if not neighbor.is_flagged and not neighbor.is_revealed:
                            neighbor.reveal()
                            if neighbor.is_mine:
                                return True  # Mine revealed during chording, game over
                            elif neighbor.adjacent_mines == 0:
                                # Recursively reveal neighboring cells with zero adjacent mines
                                self.reveal_cell(nx, ny)
        return False  # Chording action completed without hitting a mine
