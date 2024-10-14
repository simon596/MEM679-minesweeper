# game.py

from src.board import Board  # Import the Board class from the src.board module

class Game:
    """
    Represents the Minesweeper game logic.

    The Game class manages the overall game state, including the game board,
    handling user actions such as revealing cells, toggling flags, and chording,
    as well as checking for win or loss conditions.

    Attributes:
        board (Board): The game board containing cells.
        game_over (bool): Indicates if the game has ended.
        win (bool): Indicates if the player has won the game.
        first_click (bool): Indicates if the next move is the first click.
    """

    def __init__(self, rows=16, columns=16, mines=40):
        """
        Initializes a new game with the specified board size and number of mines.

        Args:
            rows (int): Number of rows in the board.
            columns (int): Number of columns in the board.
            mines (int): Number of mines to be placed on the board.
        """
        # Initialize the game board with the given dimensions and mines
        self.board = Board(rows, columns, mines)
        self.game_over = False  # Flag to indicate if the game has ended
        self.win = False        # Flag to indicate if the player has won
        self.first_click = True  # Flag to check if it's the first click

    def reveal_cell(self, x, y):
        """
        Reveals the cell at the given coordinates.

        If the cell is a mine, the game ends with a loss.
        If the cell is not a mine, it reveals the cell and recursively reveals neighboring cells if necessary.
        On the first click, mines are placed on the board avoiding the first clicked cell.

        Args:
            x (int): The row index of the cell.
            y (int): The column index of the cell.
        """
        if self.game_over:
            return  # Do nothing if the game is over

        if self.first_click:
            # On the first click, place the mines, avoiding the first clicked cell
            self.board.place_mines(x, y)
            self.first_click = False

        cell = self.board.grid[x][y]

        if cell.is_flagged:
            return  # Do nothing if the cell is flagged

        if cell.is_mine:
            # If the cell is a mine, reveal it and end the game with a loss
            cell.reveal()
            self.board.reveal_all_mines()  # Reveal all mines on the board
            self.game_over = True
            self.win = False
        else:
            # If the cell is not a mine, reveal it and potentially reveal adjacent cells
            self.board.reveal_cell(x, y)
            if self.board.is_win():
                # Check if the player has revealed all non-mine cells and won the game
                self.game_over = True
                self.win = True

    def toggle_flag(self, x, y):
        """
        Toggles a flag on the cell at the given coordinates.

        Flags are used by the player to mark suspected mines.
        On the first action, mines are placed on the board if this is the first click.

        Args:
            x (int): The row index of the cell.
            y (int): The column index of the cell.
        """
        if self.game_over:
            return  # Do nothing if the game is over

        if self.first_click:
            # Allow flagging before the first click reveals a cell
            self.board.place_mines(x, y)
            self.first_click = False

        self.board.toggle_flag(x, y)  # Toggle the flag state of the cell

    def chord_cell(self, x, y):
        """
        Performs a chord action on the cell at the given coordinates.

        Chording reveals all unrevealed, non-flagged neighboring cells if the number of adjacent flags equals
        the number of adjacent mines. If a mine is revealed during chording, the game ends with a loss.

        Args:
            x (int): The row index of the cell.
            y (int): The column index of the cell.
        """
        if self.game_over or self.first_click:
            return  # Do nothing if the game is over or if it's the first click

        # Perform chording action on the cell
        mine_triggered = self.board.chord_cell(x, y)

        if mine_triggered:
            # If a mine is triggered during chording, reveal all mines and end the game with a loss
            self.board.reveal_all_mines()
            self.game_over = True
            self.win = False
        else:
            if self.board.is_win():
                # Check if the player has revealed all non-mine cells and won the game
                self.game_over = True
                self.win = True
