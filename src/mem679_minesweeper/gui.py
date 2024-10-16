# gui.py

import pygame
import sys
from mem679_minesweeper.game import Game  # Import the Game class from the src package

# Define colors used in the game (RGB values)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
DARK_GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Cell dimensions and margin between cells
CELL_SIZE = 30
MARGIN = 2

# Minimum window dimensions to ensure UI elements are visible
MIN_WINDOW_WIDTH = 400
MIN_WINDOW_HEIGHT = 500

class InputBox:
    """
    A class representing an input box for user text input.

    Attributes:
        rect (pygame.Rect): The rectangle area of the input box.
        color_inactive (tuple): The color when the input box is inactive.
        color_active (tuple): The color when the input box is active.
        color (tuple): The current color of the input box.
        text (str): The text entered by the user.
        font (pygame.font.Font): The font used for rendering text.
        txt_surface (pygame.Surface): The rendered text surface.
        active (bool): Indicates whether the input box is active.
    """

    def __init__(self, x, y, w, h, text=''):
        """
        Initialize the InputBox.

        Args:
            x (int): The x-coordinate of the input box.
            y (int): The y-coordinate of the input box.
            w (int): The width of the input box.
            h (int): The height of the input box.
            text (str): The initial text in the input box.
        """
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = DARK_GRAY
        self.color_active = YELLOW
        self.color = self.color_inactive  # Start with the inactive color
        self.text = text
        self.font = pygame.font.SysFont('arial', 24)
        self.txt_surface = self.font.render(text, True, WHITE)
        self.active = False  # Input box is initially inactive

    def handle_event(self, event):
        """
        Handle events related to the input box.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect
            if self.rect.collidepoint(event.pos):
                self.active = not self.active  # Toggle the active state
            else:
                self.active = False
            # Change the current color of the input box
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    pass  # Ignore Enter key
                elif event.key == pygame.K_BACKSPACE:
                    # Remove last character
                    self.text = self.text[:-1]
                elif event.unicode.isdigit():
                    # Append new character
                    self.text += event.unicode
                # Re-render the text surface with the new text
                self.txt_surface = self.font.render(self.text, True, WHITE)

    def draw(self, screen):
        """
        Draw the input box and text on the screen.

        Args:
            screen (pygame.Surface): The surface to draw on.
        """
        # Draw the text
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Draw the input box rect
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_value(self):
        """
        Get the integer value entered in the input box.

        Returns:
            int or None: The integer value if valid, else None.
        """
        return int(self.text) if self.text.isdigit() else None

class MinesweeperGUI:
    """
    A class representing the graphical user interface for Minesweeper.

    Attributes:
        game (Game): The Minesweeper game logic.
        screen (pygame.Surface): The main display surface.
        font (pygame.font.Font): The font used for rendering text.
        clock (pygame.time.Clock): The game clock to control frame rate.
        running (bool): Indicates whether the game loop is running.
        timer_started (bool): Indicates whether the timer has started.
        start_time (int): The time when the timer started.
        elapsed_time (int): The elapsed time in seconds.
        difficulty_selected (bool): Indicates if a difficulty level has been selected.
        customizing (bool): Indicates if the custom difficulty menu is active.
        input_boxes (list): List of input boxes for custom difficulty.
        error_message (str): Stores error messages for display.
        rows (int): Number of rows in the game board.
        columns (int): Number of columns in the game board.
        mines (int): Number of mines in the game board.
    """

    def __init__(self):
        """
        Initialize the Minesweeper GUI.
        """
        pygame.init()
        self.game = None  # Will initialize later based on difficulty
        # Set up the initial screen with minimum dimensions
        self.screen = pygame.display.set_mode((MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT))
        pygame.display.set_caption('Minesweeper')
        self.font = pygame.font.SysFont('arial', 24)  # Default font for menus
        self.clock = pygame.time.Clock()
        self.running = True  # Main loop control
        self.timer_started = False
        self.start_time = 0
        self.elapsed_time = 0
        self.difficulty_selected = False  # Flag to check if the game has started
        self.customizing = False  # Flag for custom difficulty input mode
        self.input_boxes = []  # Stores input boxes for custom difficulty
        self.error_message = ''  # Error message display

    def run(self):
        """
        The main game loop. Handles switching between menus and game states.
        """
        while self.running:
            self.clock.tick(30)  # Limit the frame rate to 30 FPS
            if not self.difficulty_selected:
                if self.customizing:
                    # Handle custom difficulty menu
                    self.handle_custom_menu_events()
                    self.show_custom_menu()
                else:
                    # Handle start menu
                    self.handle_start_menu_events()
                    self.show_start_menu()
            else:
                # Handle game events and rendering
                self.handle_events()
                self.draw_board()
                self.update_timer()
            # Update the display
            pygame.display.flip()
        # Quit the game when the main loop ends
        pygame.quit()
        sys.exit()

    def handle_start_menu_events(self):
        """
        Handle events in the start menu, such as difficulty selection.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False  # Exit the game
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Define difficulty buttons with their properties
                buttons = [
                    {"label": "Beginner", "rect": pygame.Rect(125, 100, 150, 50), "rows": 9, "cols": 9, "mines": 10},
                    {"label": "Intermediate", "rect": pygame.Rect(125, 170, 150, 50), "rows": 16, "cols": 16, "mines": 40},
                    {"label": "Expert", "rect": pygame.Rect(125, 240, 150, 50), "rows": 16, "cols": 30, "mines": 99},
                    {"label": "Custom", "rect": pygame.Rect(125, 310, 150, 50), "custom": True},
                ]
                # Check if a button was clicked
                for button in buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        if button.get("custom"):
                            # Switch to custom difficulty menu
                            self.customizing = True
                            self.init_custom_menu()
                            return
                        else:
                            # Start game with selected difficulty
                            self.start_game(button["rows"], button["cols"], button["mines"])
                            return

    def show_start_menu(self):
        """
        Display the start menu with difficulty options.
        """
        self.screen.fill(BLACK)
        # Render the title text
        title_text = self.font.render("Select Difficulty", True, WHITE)
        title_rect = title_text.get_rect(center=(200, 50))
        self.screen.blit(title_text, title_rect)

        # Define difficulty buttons without additional properties
        buttons = [
            {"label": "Beginner", "rect": pygame.Rect(125, 100, 150, 50)},
            {"label": "Intermediate", "rect": pygame.Rect(125, 170, 150, 50)},
            {"label": "Expert", "rect": pygame.Rect(125, 240, 150, 50)},
            {"label": "Custom", "rect": pygame.Rect(125, 310, 150, 50)},
        ]

        # Draw buttons and their labels
        for button in buttons:
            pygame.draw.rect(self.screen, DARK_GRAY, button["rect"])
            label = self.font.render(button["label"], True, WHITE)
            label_rect = label.get_rect(center=button["rect"].center)
            self.screen.blit(label, label_rect)

    def init_custom_menu(self):
        """
        Initialize the custom difficulty menu input boxes and reset error messages.
        """
        # Create input boxes for rows, columns, and mines
        self.input_boxes = [
            {"name": "rows", "box": InputBox(200, 100, 150, 40)},
            {"name": "cols", "box": InputBox(200, 160, 150, 40)},
            {"name": "mines", "box": InputBox(200, 220, 150, 40)},
        ]
        self.error_message = ''  # Clear any previous error messages

    def handle_custom_menu_events(self):
        """
        Handle events in the custom difficulty menu, including input and submission.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False  # Exit the game
                return
            # Pass events to input boxes to handle text input
            for box in self.input_boxes:
                box["box"].handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Define the submit button
                submit_button_rect = pygame.Rect(125, 300, 150, 50)
                if submit_button_rect.collidepoint(mouse_pos):
                    # Get input values from the input boxes
                    rows = self.input_boxes[0]["box"].get_value()
                    cols = self.input_boxes[1]["box"].get_value()
                    mines = self.input_boxes[2]["box"].get_value()
                    # Validate inputs
                    if rows and cols and mines:
                        max_mines = (rows * cols) - 1
                        if mines < max_mines:
                            # Start the game with custom settings
                            self.start_game(rows, cols, mines)
                            self.customizing = False  # Exit custom menu
                            return
                        else:
                            # Set error message for too many mines
                            self.error_message = "Too many mines!"
                    else:
                        # Set error message for invalid inputs
                        self.error_message = "Invalid inputs!"

    def show_custom_menu(self):
        """
        Display the custom difficulty menu with input boxes and submit button.
        """
        self.screen.fill(BLACK)
        # Render the title text
        title_text = self.font.render("Custom Difficulty", True, WHITE)
        title_rect = title_text.get_rect(center=(200, 50))
        self.screen.blit(title_text, title_rect)

        # Labels for input boxes
        labels = [
            {"text": "Rows:", "pos": (50, 100)},
            {"text": "Columns:", "pos": (50, 160)},
            {"text": "Mines:", "pos": (50, 220)},
        ]
        # Draw labels next to input boxes
        for label in labels:
            label_surface = self.font.render(label["text"], True, WHITE)
            self.screen.blit(label_surface, label["pos"])

        # Draw input boxes
        for box in self.input_boxes:
            box["box"].draw(self.screen)

        # Draw the submit button
        submit_button_rect = pygame.Rect(125, 300, 150, 50)
        pygame.draw.rect(self.screen, DARK_GRAY, submit_button_rect)
        submit_text = self.font.render("Start Game", True, WHITE)
        submit_text_rect = submit_text.get_rect(center=submit_button_rect.center)
        self.screen.blit(submit_text, submit_text_rect)

        # Display error message if any
        if self.error_message:
            error_text = self.font.render(self.error_message, True, RED)
            self.screen.blit(error_text, (100, 370))

    def start_game(self, rows, cols, mines):
        """
        Initialize and start the game with the given settings.

        Args:
            rows (int): Number of rows in the game board.
            cols (int): Number of columns in the game board.
            mines (int): Number of mines to place on the board.
        """
        # Initialize the game logic
        self.game = Game(rows=rows, columns=cols, mines=mines)
        self.rows = rows
        self.columns = cols
        self.mines = mines

        # Calculate the window size based on board dimensions
        window_width = cols * (CELL_SIZE + MARGIN) + MARGIN
        window_height = rows * (CELL_SIZE + MARGIN) + MARGIN + 100  # Extra space for UI elements

        # Ensure the window is at least the minimum size
        window_width = max(window_width, MIN_WINDOW_WIDTH)
        window_height = max(window_height, MIN_WINDOW_HEIGHT)

        # Set up the display with the new window size
        self.screen = pygame.display.set_mode((window_width, window_height))
        # Adjust font size based on cell size
        self.font = pygame.font.SysFont('arial', CELL_SIZE // 2)
        self.difficulty_selected = True  # Game has started
        self.timer_started = False
        self.elapsed_time = 0

    def handle_events(self):
        """
        Handle events during the game, including user input and game logic.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False  # Exit the game

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if not self.game.game_over:
                    # Game is ongoing
                    if mouse_y < self.rows * (CELL_SIZE + MARGIN) + MARGIN:
                        # Click is within the game board area
                        col = mouse_x // (CELL_SIZE + MARGIN)
                        row = mouse_y // (CELL_SIZE + MARGIN)

                        if 0 <= row < self.rows and 0 <= col < self.columns:
                            # Check for modifier keys
                            modifiers = pygame.key.get_mods()
                            if event.button == 1:  # Left click
                                if modifiers & pygame.KMOD_SHIFT:
                                    # Shift + Left Click performs chording
                                    self.game.chord_cell(row, col)
                                else:
                                    # Reveal the cell
                                    self.game.reveal_cell(row, col)
                                    if not self.timer_started:
                                        # Start the timer on first action
                                        self.timer_started = True
                                        self.start_time = pygame.time.get_ticks()
                            elif event.button == 3:  # Right click
                                # Toggle a flag on the cell
                                self.game.toggle_flag(row, col)
                                if not self.timer_started:
                                    # Start the timer on first action
                                    self.timer_started = True
                                    self.start_time = pygame.time.get_ticks()
                    else:
                        # Check if reset button is clicked
                        reset_button_rect = pygame.Rect(
                            self.screen.get_width() // 2 - 120, self.screen.get_height() - 40, 100, 30
                        )
                        if reset_button_rect.collidepoint(mouse_x, mouse_y):
                            self.reset_game()
                else:
                    # Game is over
                    # Check if "Home" button is clicked
                    home_button_rect = pygame.Rect(
                        self.screen.get_width() // 2 + 20, self.screen.get_height() - 40, 100, 30
                    )
                    if home_button_rect.collidepoint(mouse_x, mouse_y):
                        self.reset_game()

    def draw_board(self):
        """
        Render the game board, cells, and UI elements on the screen.
        """
        self.screen.fill(BLACK)
        # Draw each cell on the board
        for row in range(self.rows):
            for col in range(self.columns):
                cell = self.game.board.grid[row][col]
                rect = pygame.Rect(
                    col * (CELL_SIZE + MARGIN) + MARGIN,
                    row * (CELL_SIZE + MARGIN) + MARGIN,
                    CELL_SIZE,
                    CELL_SIZE
                )
                if cell.is_revealed:
                    if cell.is_mine:
                        # Draw a mine
                        pygame.draw.rect(self.screen, RED, rect)
                        pygame.draw.circle(
                            self.screen, BLACK,
                            rect.center, CELL_SIZE // 2 - 4
                        )
                    else:
                        # Draw a revealed cell
                        pygame.draw.rect(self.screen, GRAY, rect)
                        if cell.adjacent_mines > 0:
                            # Draw the number of adjacent mines
                            text_surface = self.font.render(str(cell.adjacent_mines), True, BLUE)
                            text_rect = text_surface.get_rect(center=rect.center)
                            self.screen.blit(text_surface, text_rect)
                else:
                    # Draw an unrevealed cell
                    pygame.draw.rect(self.screen, DARK_GRAY, rect)
                    if cell.is_flagged:
                        # Draw a flag
                        pygame.draw.polygon(
                            self.screen, RED,
                            [
                                (rect.left + CELL_SIZE // 2, rect.top + CELL_SIZE // 4),
                                (rect.left + 3 * CELL_SIZE // 4, rect.top + CELL_SIZE // 2),
                                (rect.left + CELL_SIZE // 2, rect.top + 3 * CELL_SIZE // 4),
                                (rect.left + CELL_SIZE // 4, rect.top + CELL_SIZE // 2)
                            ]
                        )
                    elif self.game.game_over and cell.is_mine:
                        # Reveal mines after game over
                        pygame.draw.rect(self.screen, RED, rect)
                        pygame.draw.circle(
                            self.screen, BLACK,
                            rect.center, CELL_SIZE // 2 - 4
                        )
        # Draw timer and buttons
        self.draw_timer()
        if self.game.game_over:
            # Draw "Home" button and game over message
            self.draw_home_button()
            self.show_game_over_message()
        else:
            # Draw "Reset" button during the game
            self.draw_reset_button()

    def update_timer(self):
        """
        Update the elapsed time if the timer is running.
        """
        if self.timer_started and not self.game.game_over:
            # Calculate elapsed time in seconds
            self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000

    def draw_timer(self):
        """
        Draw the timer displaying the elapsed time on the screen.
        """
        # Timer background rectangle
        timer_rect = pygame.Rect(10, self.screen.get_height() - 80, 250, 30)
        pygame.draw.rect(self.screen, BLACK, timer_rect)
        # Timer text with units
        timer_text = self.font.render(f"Time: {self.elapsed_time} seconds", True, WHITE)
        # Draw the timer text
        self.screen.blit(timer_text, (15, self.screen.get_height() - 75))

    def draw_reset_button(self):
        """
        Draw the "Reset" button on the screen.
        """
        reset_button_rect = pygame.Rect(
            self.screen.get_width() // 2 - 120, self.screen.get_height() - 40, 100, 30
        )
        pygame.draw.rect(self.screen, DARK_GRAY, reset_button_rect)
        reset_text = self.font.render("Reset", True, WHITE)
        reset_text_rect = reset_text.get_rect(center=reset_button_rect.center)
        self.screen.blit(reset_text, reset_text_rect)

    def draw_home_button(self):
        """
        Draw the "Home" button on the screen after the game is over.
        """
        home_button_rect = pygame.Rect(
            self.screen.get_width() // 2 + 20, self.screen.get_height() - 40, 100, 30
        )
        pygame.draw.rect(self.screen, DARK_GRAY, home_button_rect)
        home_text = self.font.render("Home", True, WHITE)
        home_text_rect = home_text.get_rect(center=home_button_rect.center)
        self.screen.blit(home_text, home_text_rect)

    def reset_game(self):
        """
        Reset the game to the start menu.
        """
        self.difficulty_selected = False
        self.timer_started = False
        self.elapsed_time = 0
        self.customizing = False  # Exit custom difficulty mode
        self.error_message = ''  # Clear any error messages
        # Reset the display to the minimum window size
        self.screen = pygame.display.set_mode((MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT))

    def show_game_over_message(self):
        """
        Display a message indicating whether the player won or lost.
        """
        message_rect = pygame.Rect(0, self.screen.get_height() - 120, self.screen.get_width(), 30)
        pygame.draw.rect(self.screen, BLACK, message_rect)

        if self.game.win:
            # Player won
            message = f"You Win! Time: {self.elapsed_time} seconds"
            color = GREEN
        else:
            # Player lost
            message = "Game Over!"
            color = RED

        # Render the message text
        text_surface = self.font.render(message, True, color)
        text_rect = text_surface.get_rect(center=message_rect.center)
        # Draw the message text
        self.screen.blit(text_surface, text_rect)

def main():
    """
    The main entry point of the game.
    """
    gui = MinesweeperGUI()
    gui.run()

if __name__ == '__main__':
    main()
