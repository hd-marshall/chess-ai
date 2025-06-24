import pygame as p
import pygame.mixer as pm

from typing import Tuple, List

class Chess_Graphics:

    def __init__(self) -> None:
        self.WIDTH = 512
        self.HEIGHT = 512
        self.DIMENSION = 8
        self.SQUARE_SIZE = self.HEIGHT // self.DIMENSION
        self.MAX_FPS = 15
        self.IMAGES = {}
        self.load_images()
        self.SOUNDS = {}
        self.load_sounds()

    def load_images(self) -> None:
        """
        Load all the piece images for pygame graphics and store them in the IMAGES dictionary.

        This function iterates through a list of chess piece identifiers, loads each corresponding image 
        from the file system, scales it to the appropriate size, and stores it in the IMAGES dictionary 
        with the piece identifier as the key.

        Parameters:
        None

        Returns:
        None
        """
        pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
        for piece in pieces:
            image_path = f"images/{piece}.png"
            image = p.image.load(image_path)
            self.IMAGES[piece] = p.transform.scale(image, (int(self.SQUARE_SIZE), int(self.SQUARE_SIZE)))

    def load_sounds(self) -> None:
        """
        Load all the all the player interaction game sounds.

        This function stores .wav files in the SOUNDS dictionary with a sound identifier as the key. Finishing by
        iterating through the dictionary changing the sound volume. 

        Parameters:
        None

        Returns:
        None
        """
        pm.init()
        self.SOUNDS['click'] = pm.Sound("sounds/click1.wav")
        self.SOUNDS['error'] = pm.Sound("sounds/click2Error.wav")

        for sound in self.SOUNDS.values():
            sound.set_volume(0.3)
    
    def play_sound(self, sound: bool) -> None:
        """
        Play a game sound based on the player's interaction.

        This function plays a specific sound from the SOUNDS dictionary based on the boolean parameter `sound`.
        If `sound` is True, it plays the "click" sound. Otherwise, it plays the "error" sound.

        Parameters:
        sound (bool): A boolean indicating which sound to play. True for "click", False for "error".

        Returns:
        None
        """
        self.SOUNDS["click" if sound else "error"].play()

    def create_screen(self) -> p:
        """
        Initialize the pygame display and create the game screen.

        This function initialises all imported pygame modules, sets up the display window with the specified
        width and height, and sets the window caption to "Chess: The Game". The created screen is then returned.

        Parameters:
        None

        Returns:
        pygame.Surface: The initialized game screen.
        """

        p.init()
        screen = p.display.set_mode((self.WIDTH, self.HEIGHT))
        p.display.set_caption("Chess: The Game")

        return screen
    
    def create_clock(self) -> p.time.Clock:
        """
        Create and return a new clock object to control the game's frame rate.

        This function initialises a pygame Clock object which can be used to manage 
        the timing and frame rate of the game.

        Parameters:
        None

        Returns:
        p.time.Clock: The initialized clock object.
        """
        clock = p.time.Clock()

        return clock

    def draw_board(self, screen: p.Surface) -> None:
        """
        Draw the chess board on the given screen.

        This function iterates through each square of the board, determining the color 
        based on the position, and draws it on the screen using pygame's drawing 
        functions.

        Parameters:
        screen (pygame.Surface): The screen to draw the board on.

        Returns:
        None
        """
        white = (255, 253, 208)
        black = (139, 69, 19)
        colours = [p.Color(white), p.Color(black)]

        for row in range(self.DIMENSION):
            for column in range(self.DIMENSION):
                colour = colours[(row + column) % 2]
                p.draw.rect(screen, colour, p.Rect(column * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

    def draw_pieces(self, screen: p.Surface, board: List[List[str]]) -> None:
        """
        Draw all the chess pieces on the board.

        This function iterates through each square of the board and draws the 
        appropriate piece image if a piece is present.

        Parameters:
        screen (pygame.Surface): The screen to draw the pieces on.
        board (List[List[str]]): The current state of the chess board.

        Returns:
        None
        """
        for row in range(self.DIMENSION):
            for column in range(self.DIMENSION):
                piece = board[row][column]
                if piece != "--":
                    screen.blit(self.IMAGES[piece], p.Rect(column * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

    def draw_guidelines(self, screen: p.Surface, guideline_list: List[Tuple[int, int]]) -> None:
        """
        Draw guidelines on the chess board to highlight valid moves.
        This function takes a list of valid move positions and draws rectangles
        on the specified squares to visually indicate possible moves to the player.

        Parameters:
        screen (p.Surface): The Pygame surface to draw on.
        guideline_list (List[Tuple[int, int]]): A list of (row, column) tuples representing valid moves.

        Returns:
        None
        """
        highlight_colour = (176, 196, 222, 0.5)

        for position in guideline_list:
            row, column = position
            p.draw.rect(screen, highlight_colour, p.Rect(column * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

    def get_sqr(self, location: Tuple[int, int]) -> Tuple[int, int]:
        """
        Convert a window pixel location to board coordinates.

        This function takes a pixel location from a mouse click and converts it 
        to the corresponding row and column on the chess board.

        Parameters:
        location (Tuple[int, int]): The pixel coordinates of the mouse click.

        Returns:
        Tuple[int, int]: The corresponding (row, column) on the chess board.
        """
        clickRow = int(location[1] // self.SQUARE_SIZE)
        clickColumn = int(location[0] // self.SQUARE_SIZE)

        return (clickRow, clickColumn)