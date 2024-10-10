# cell.py

class Cell:
    def __init__(self, x, y):
        self.x = x  # Row position
        self.y = y  # Column position
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def reveal(self):
        if not self.is_flagged and not self.is_revealed:
            self.is_revealed = True
            return True
        return False

    def toggle_flag(self):
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged

    def set_mine(self):
        self.is_mine = True

    def set_adjacent_mines(self, count):
        self.adjacent_mines = count
