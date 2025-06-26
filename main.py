import os
import pygame
import pygame.freetype
from pygame.sprite import Sprite, RenderUpdates
from pygame.rect import Rect
from enum import Enum
import sys
# from python.game_modes.one_player import one_player
from python.game_modes.two_player import two_player
# from python.game_modes.puzzle_mode import puzzle_mode

# Colors
BLUE = (106, 159, 181)
WHITE = (255, 255, 255)
DARK_BLUE = (70, 130, 180)
GREEN = (34, 139, 34)
PURPLE = (128, 0, 128)
RED = (220, 20, 60)
LIGHT_GRAY = (200, 200, 200)

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    TWO_PLAYER = 1
    # VS_AI = 2
    # PUZZLES = 3

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """Returns surface with text written on"""
    font = pygame.freetype.SysFont("Pixel", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

class UIElement(Sprite):
    """A user interface element that can be added to a surface"""

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        """
        Args:
            center_position - tuple (x, y)
            text - string of text to write
            font_size - int
            bg_rgb (background colour) - tuple (r, g, b)
            text_rgb (text colour) - tuple (r, g, b)
            action - GameState enum value
        """
        self.mouse_over = False
        self.action = action

        # Create the default image
        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        # Create the image that shows when mouse is over the element
        highlighted_image = create_surface_with_text(
            text=text, font_size=int(font_size * 1.2), text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        # Add both images and their rects to lists
        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        # Call the init method of the parent sprite class
        super().__init__()

    # Properties that vary the image and its rect when the mouse is over the element
    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        """Updates the element's appearance depending on the mouse position
        and returns the button's action if clicked.
        """
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """Draws element onto a surface"""
        surface.blit(self.image, self.rect)

def create_gradient_background(screen, color1, color2):
    """Create a gradient background"""
    height = screen.get_height()
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (screen.get_width(), y))

def game_loop(screen, buttons, title_text=None):
    """Handles game loop until an action is returned by a button"""
    clock = pygame.time.Clock()
    
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    return GameState.QUIT
                elif event.key == pygame.K_1:
                    return GameState.TWO_PLAYER
        
        # Create gradient background
        create_gradient_background(screen, (240, 248, 255), (200, 220, 240))
        
        # Draw title if provided
        if title_text:
            
            # Draw subtitle
            subtitle_font = pygame.freetype.SysFont("Arial", 32)
            subtitle_surface, _ = subtitle_font.render("Choose Your Game Mode", (100, 100, 100))
            subtitle_rect = subtitle_surface.get_rect(center=(screen.get_width() // 2, 160))
            screen.blit(subtitle_surface, subtitle_rect)

        # Update and check buttons
        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action

        # Draw buttons
        buttons.draw(screen)
        
        # Draw keyboard shortcuts
        shortcut_font = pygame.freetype.SysFont("Arial", 18)
        shortcuts = [
            "Keyboard Shortcuts:",
            "Press 1 - Two Players",
            "Press ESC/Q - Quit"
        ]
        
        y_start = screen.get_height() - 80
        for i, shortcut in enumerate(shortcuts):
            color = (50, 50, 50) if i == 0 else (100, 100, 100)
            shortcut_surface, _ = shortcut_font.render(shortcut, color)
            shortcut_rect = shortcut_surface.get_rect(center=(screen.get_width() // 2, y_start + i * 20))
            screen.blit(shortcut_surface, shortcut_rect)
        
        pygame.display.flip()
        clock.tick(60)

def title_screen(screen):
    """Display the main menu title screen"""
    # Create buttons
    start_btn = UIElement(
        center_position=(screen.get_width() // 2, 280),
        font_size=32,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Two Players",
        action=GameState.TWO_PLAYER,
    )
    
    # Commented out other game modes
    # vs_ai_btn = UIElement(
    #     center_position=(screen.get_width() // 2, 360),
    #     font_size=32,
    #     bg_rgb=GREEN,
    #     text_rgb=WHITE,
    #     text="VS Computer",
    #     action=GameState.VS_AI,
    # )
    
    # puzzle_btn = UIElement(
    #     center_position=(screen.get_width() // 2, 440),
    #     font_size=32,
    #     bg_rgb=PURPLE,
    #     text_rgb=WHITE,
    #     text="Chess Puzzles",
    #     action=GameState.PUZZLES,
    # )
    
    quit_btn = UIElement(
        center_position=(screen.get_width() // 2, 380),
        font_size=32,
        bg_rgb=RED,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,
    )

    # buttons = RenderUpdates(start_btn, vs_ai_btn, puzzle_btn, quit_btn)
    buttons = RenderUpdates(start_btn, quit_btn)

    return game_loop(screen, buttons, "Python Chess")

def play_two_player(screen):
    """Launch two player mode and handle return"""
    pygame.quit()
    try:
        two_player()
    except Exception as e:
        print(f"Error starting two player game: {e}")
    
    # Reinitialize pygame after returning from game
    pygame.init()
    return GameState.TITLE

# Commented out other game modes
# def play_vs_ai(screen):
#     """Launch AI mode and handle return"""
#     pygame.quit()
#     try:
#         one_player()
#     except Exception as e:
#         print(f"Error starting AI game: {e}")
#     
#     pygame.init()
#     return GameState.TITLE

# def play_puzzles(screen):
#     """Launch puzzle mode and handle return"""
#     pygame.quit()
#     try:
#         puzzle_mode()
#     except Exception as e:
#         print(f"Error starting puzzle mode: {e}")
#     
#     pygame.init()
#     return GameState.TITLE

def main():
    """Main game loop handling different states"""
    # Set working directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    pygame.init()
    screen = pygame.display.set_mode((512, 512))
    pygame.display.set_caption("Chess Game - Main Menu")
    
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        elif game_state == GameState.TWO_PLAYER:
            game_state = play_two_player(screen)

        # elif game_state == GameState.VS_AI:
        #     game_state = play_vs_ai(screen)

        # elif game_state == GameState.PUZZLES:
        #     game_state = play_puzzles(screen)

        elif game_state == GameState.QUIT:
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()