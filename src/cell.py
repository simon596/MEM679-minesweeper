# cell.py

class Cell:
    """
    Represents a single cell in the Minesweeper game board.

    Each cell can be a mine or not, and keeps track of its state such as whether it has been revealed,
    flagged, or the number of adjacent mines.

    Attributes:
        x (int): The row index of the cell on the board.
        y (int): The column index of the cell on the board.
        is_mine (bool): Indicates whether the cell contains a mine.
        is_revealed (bool): Indicates whether the cell has been revealed.
        is_flagged (bool): Indicates whether the cell has been flagged by the player.
        adjacent_mines (int): The number of mines adjacent to this cell.
    """

    def __init__(self, x, y):
        """
        Initializes a Cell object at a specific position on the board.

        Args:
            x (int): The row index of the cell.
            y (int): The column index of the cell.
        """
        self.x = x  # Row position on the board
        self.y = y  # Column position on the board
        self.is_mine = False       # True if the cell contains a mine
        self.is_revealed = False   # True if the cell has been revealed
        self.is_flagged = False    # True if the cell has been flagged by the player
        self.adjacent_mines = 0    # Number of mines in adjacent cells

    def reveal(self):
        """
        Reveals the cell if it is not flagged and not already revealed.

        Returns:
            bool: True if the cell was successfully revealed, False otherwise.
        """
        if not self.is_flagged and not self.is_revealed:
            self.is_revealed = True
            return True  # Cell was successfully revealed
        return False  # Cell could not be revealed

    def toggle_flag(self):
        """
        Toggles the flagged state of the cell.

        Flags are used by the player to mark suspected mines.
        A cell cannot be flagged if it has already been revealed.
        """
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged  # Toggle the flag state

    def set_mine(self):
        """
        Sets the cell to contain a mine.
        """
        self.is_mine = True  # Mark this cell as a mine

    def set_adjacent_mines(self, count):
        """
        Sets the number of adjacent mines for the cell.

        Args:
            count (int): The number of mines adjacent to this cell.
        """
        self.adjacent_mines = count  # Update the adjacent mines count
