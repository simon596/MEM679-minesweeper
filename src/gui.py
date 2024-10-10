# gui.py

import pygame
import sys
from src.game import Game

# Define colors
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
DARK_GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Cell dimensions
CELL_SIZE = 30
MARGIN = 2

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = DARK_GRAY
        self.color_active = YELLOW
        self.color = self.color_inactive
        self.text = text
        self.font = pygame.font.SysFont('arial', 24)
        self.txt_surface = self.font.render(text, True, WHITE)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state if clicked
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            # Change the color of the input box
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    pass  # Do nothing on Enter key
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.unicode.isdigit():
                    self.text += event.unicode
                # Re-render the text
                self.txt_surface = self.font.render(self.text, True, WHITE)

    def draw(self, screen):
        # Blit the text
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_value(self):
        return int(self.text) if self.text.isdigit() else None

class MinesweeperGUI:
    def __init__(self):
        pygame.init()
        self.game = None  # Will initialize later based on difficulty
        self.screen = pygame.display.set_mode((400, 500))
        pygame.display.set_caption('Minesweeper')
        self.font = pygame.font.SysFont('arial', 24)
        self.clock = pygame.time.Clock()
        self.running = True
        self.timer_started = False
        self.start_time = 0
        self.elapsed_time = 0
        self.difficulty_selected = False
        self.customizing = False  # Flag to check if we're in custom difficulty input mode
        self.input_boxes = []
        self.error_message = ''

    def run(self):
        while self.running:
            self.clock.tick(30)
            if not self.difficulty_selected:
                if self.customizing:
                    self.handle_custom_menu_events()
                    self.show_custom_menu()
                else:
                    self.handle_start_menu_events()
                    self.show_start_menu()
            else:
                self.handle_events()
                self.draw_board()
                self.update_timer()
            pygame.display.flip()
        pygame.quit()
        sys.exit()

    def handle_start_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                buttons = [
                    {"label": "Beginner", "rect": pygame.Rect(125, 100, 150, 50), "rows": 9, "cols": 9, "mines": 10},
                    {"label": "Intermediate", "rect": pygame.Rect(125, 170, 150, 50), "rows": 16, "cols": 16, "mines": 40},
                    {"label": "Expert", "rect": pygame.Rect(125, 240, 150, 50), "rows": 16, "cols": 30, "mines": 99},
                    {"label": "Custom", "rect": pygame.Rect(125, 310, 150, 50), "custom": True},
                ]
                for button in buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        if button.get("custom"):
                            self.customizing = True
                            self.init_custom_menu()
                            return
                        else:
                            self.start_game(button["rows"], button["cols"], button["mines"])
                            return

    def show_start_menu(self):
        self.screen.fill(BLACK)
        title_text = self.font.render("Select Difficulty", True, WHITE)
        title_rect = title_text.get_rect(center=(200, 50))
        self.screen.blit(title_text, title_rect)

        # Difficulty Buttons
        buttons = [
            {"label": "Beginner", "rect": pygame.Rect(125, 100, 150, 50)},
            {"label": "Intermediate", "rect": pygame.Rect(125, 170, 150, 50)},
            {"label": "Expert", "rect": pygame.Rect(125, 240, 150, 50)},
            {"label": "Custom", "rect": pygame.Rect(125, 310, 150, 50)},
        ]

        for button in buttons:
            pygame.draw.rect(self.screen, DARK_GRAY, button["rect"])
            label = self.font.render(button["label"], True, WHITE)
            label_rect = label.get_rect(center=button["rect"].center)
            self.screen.blit(label, label_rect)

    def init_custom_menu(self):
        # Initialize input boxes
        self.input_boxes = [
            {"name": "rows", "box": InputBox(200, 100, 150, 40)},
            {"name": "cols", "box": InputBox(200, 160, 150, 40)},
            {"name": "mines", "box": InputBox(200, 220, 150, 40)},
        ]
        self.error_message = ''

    def handle_custom_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            for box in self.input_boxes:
                box["box"].handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                submit_button_rect = pygame.Rect(125, 300, 150, 50)
                if submit_button_rect.collidepoint(mouse_pos):
                    # Get input values
                    rows = self.input_boxes[0]["box"].get_value()
                    cols = self.input_boxes[1]["box"].get_value()
                    mines = self.input_boxes[2]["box"].get_value()
                    # Validate inputs
                    if rows and cols and mines:
                        max_mines = (rows * cols) - 1
                        if mines < max_mines:
                            self.start_game(rows, cols, mines)
                            self.customizing = False
                            return
                        else:
                            # Show error message
                            self.error_message = "Too many mines!"
                    else:
                        # Show error message
                        self.error_message = "Invalid inputs!"

    def show_custom_menu(self):
        self.screen.fill(BLACK)
        title_text = self.font.render("Custom Difficulty", True, WHITE)
        title_rect = title_text.get_rect(center=(200, 50))
        self.screen.blit(title_text, title_rect)

        # Labels
        labels = [
            {"text": "Rows:", "pos": (50, 100)},
            {"text": "Columns:", "pos": (50, 160)},
            {"text": "Mines:", "pos": (50, 220)},
        ]
        for label in labels:
            label_surface = self.font.render(label["text"], True, WHITE)
            self.screen.blit(label_surface, label["pos"])

        # Draw Input Boxes
        for box in self.input_boxes:
            box["box"].draw(self.screen)

        # Submit Button
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
        # Initialize the game with selected difficulty
        self.game = Game(rows=rows, columns=cols, mines=mines)
        self.rows = rows
        self.columns = cols
        self.mines = mines
        window_width = cols * (CELL_SIZE + MARGIN) + MARGIN
        window_height = rows * (CELL_SIZE + MARGIN) + MARGIN + 50  # Extra space for timer and buttons
        self.screen = pygame.display.set_mode((window_width, window_height))
        self.font = pygame.font.SysFont('arial', CELL_SIZE // 2)
        self.difficulty_selected = True
        self.timer_started = False
        self.elapsed_time = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if not self.game.game_over:
                    # Game is ongoing
                    if mouse_y < self.rows * (CELL_SIZE + MARGIN) + MARGIN:
                        col = mouse_x // (CELL_SIZE + MARGIN)
                        row = mouse_y // (CELL_SIZE + MARGIN)

                        if 0 <= row < self.rows and 0 <= col < self.columns:
                            modifiers = pygame.key.get_mods()
                            if event.button == 1:  # Left click
                                if modifiers & pygame.KMOD_SHIFT:
                                    # Shift + Left Click performs chording
                                    self.game.chord_cell(row, col)
                                else:
                                    self.game.reveal_cell(row, col)
                                    if not self.timer_started:
                                        self.timer_started = True
                                        self.start_time = pygame.time.get_ticks()
                            elif event.button == 3:  # Right click
                                self.game.toggle_flag(row, col)
                                if not self.timer_started:
                                    self.timer_started = True
                                    self.start_time = pygame.time.get_ticks()
                    else:
                        # Check if reset button is clicked
                        reset_button_rect = pygame.Rect(
                            self.screen.get_width() // 2 - 50, self.screen.get_height() - 40, 100, 30
                        )
                        if reset_button_rect.collidepoint(mouse_x, mouse_y):
                            self.reset_game()
                else:
                    # Game is over
                    # Check if "Home" button is clicked
                    home_button_rect = pygame.Rect(
                        self.screen.get_width() // 2 - 50, self.screen.get_height() - 40, 100, 30
                    )
                    if home_button_rect.collidepoint(mouse_x, mouse_y):
                        self.reset_game()

    def draw_board(self):
        self.screen.fill(BLACK)
        # Draw cells
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
                        pygame.draw.rect(self.screen, RED, rect)
                        pygame.draw.circle(
                            self.screen, BLACK,
                            rect.center, CELL_SIZE // 2 - 4
                        )
                    else:
                        pygame.draw.rect(self.screen, GRAY, rect)
                        if cell.adjacent_mines > 0:
                            text_surface = self.font.render(str(cell.adjacent_mines), True, BLUE)
                            text_rect = text_surface.get_rect(center=rect.center)
                            self.screen.blit(text_surface, text_rect)
                else:
                    pygame.draw.rect(self.screen, DARK_GRAY, rect)
                    if cell.is_flagged:
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
            self.draw_home_button()
            self.show_game_over_message()
        else:
            self.draw_reset_button()

    def update_timer(self):
        if self.timer_started and not self.game.game_over:
            self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000

    def draw_timer(self):
        # Timer background
        timer_rect = pygame.Rect(10, self.screen.get_height() - 40, 200, 30)
        pygame.draw.rect(self.screen, BLACK, timer_rect)
        # Timer text with units
        timer_text = self.font.render(f"Time: {self.elapsed_time} seconds", True, WHITE)
        self.screen.blit(timer_text, (15, self.screen.get_height() - 35))

    def draw_reset_button(self):
        reset_button_rect = pygame.Rect(
            self.screen.get_width() // 2 - 50, self.screen.get_height() - 40, 100, 30
        )
        pygame.draw.rect(self.screen, DARK_GRAY, reset_button_rect)
        reset_text = self.font.render("Reset", True, WHITE)
        reset_text_rect = reset_text.get_rect(center=reset_button_rect.center)
        self.screen.blit(reset_text, reset_text_rect)

    def draw_home_button(self):
        home_button_rect = pygame.Rect(
            self.screen.get_width() // 2 - 50, self.screen.get_height() - 40, 100, 30
        )
        pygame.draw.rect(self.screen, DARK_GRAY, home_button_rect)
        home_text = self.font.render("Home", True, WHITE)
        home_text_rect = home_text.get_rect(center=home_button_rect.center)
        self.screen.blit(home_text, home_text_rect)

    def reset_game(self):
        self.difficulty_selected = False
        self.timer_started = False
        self.elapsed_time = 0
        self.customizing = False
        self.error_message = ''
        # Reset to initial screen size
        self.screen = pygame.display.set_mode((400, 500))

    def show_game_over_message(self):
        message_rect = pygame.Rect(0, self.screen.get_height() - 80, self.screen.get_width(), 30)
        pygame.draw.rect(self.screen, BLACK, message_rect)

        if self.game.win:
            message = f"You Win! Time: {self.elapsed_time} seconds"
            color = GREEN
        else:
            message = "Game Over!"
            color = RED

        text_surface = self.font.render(message, True, color)
        text_rect = text_surface.get_rect(center=message_rect.center)
        self.screen.blit(text_surface, text_rect)

def main():
    gui = MinesweeperGUI()
    gui.run()

if __name__ == '__main__':
    main()