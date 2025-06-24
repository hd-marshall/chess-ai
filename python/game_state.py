from python.game_rules import Game_Rules

from typing import Dict, Tuple, List

class Game_State:

    def __init__(self) -> None:
        self.clicked_squares : List[Tuple[int, int], Tuple[int, int]] = []

        self.board = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.player_colour : str = "w"
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)

        self.rules = Game_Rules()
        self.white_moves : Dict[Tuple[int, int], List[Tuple[int, int]]] = {}
        self.black_moves : Dict[Tuple[int, int], List[Tuple[int, int]]] = {}

        self.pinned_pieces = []
        self.in_check = False
        self.checkmate = False
        self.stalemate = False
    
    def set_valid_moves(self) -> None:
        self.white_moves = self.create_valid_moves("w")
        self.black_moves = self.create_valid_moves("b")

    def create_valid_moves(self, player_colour: str) -> None:
        valid_moves = {}
        n = len(self.board)
        opponent_colour = "w" if player_colour == "b" else "b"

        for i in range(n):
            for j in range(n):

                if self.board[i][j] != "--" and self.board[i][j][0] == self.player_colour:

                    piece = self.board[i][j][1]
                    start_sqr = (i, j)
                    
                    valid_moves[start_sqr] = []
                    valid_moves[start_sqr].extend(self.rules.get_piece_move(piece, start_sqr, opponent_colour, self.board))
        
        return valid_moves

    def remove_illegal_moves(self) -> None:
        
        player_king = self.white_king_location if self.player_colour == "w" else self.black_king_location
        opponent_moves = self.black_moves if self.player_colour == "w" else self.white_moves

        attacking_pieces = self.rules.square_under_attack(player_king, opponent_moves)

        if len(attacking_pieces) == 1:
            attack_piece = attacking_pieces[0]
            attack_dir = self.rules.square_under_attack_direction(player_king, attacking_pieces, self.board)

            self.rules.single_check(player_king, attack_piece, attack_dir, self.valid_moves)

    def move(self) -> None:
        
        start_row = self.clicked_squares[0][0]
        start_col = self.clicked_squares[0][1]
        end_row = self.clicked_squares[1][0]
        end_col = self.clicked_squares[1][1]

        piece_value = self.board[start_row][start_col]

        self.board[end_row][end_col] = piece_value
        self.board[start_row][start_col] = "--"

        valid_moves = self.white_moves if self.player_colour == "w" else self.black_moves
        valid_moves.clear()

        self.player_colour = "w" if self.player_colour == "b" else "b" 

    def get_valid_move(self, end_sqr) -> bool:

        valid_moves = self.white_moves if self.player_colour == "w" else self.black_moves
        start_sqr = self.clicked_squares[0]
        
        if start_sqr in valid_moves:
            if end_sqr in valid_moves[start_sqr]:
                return True
                
        return False

    def validate_clicked_sqrs(self, location: Tuple[int, int]) -> bool:
        
        row, col = location

        if not self.clicked_squares and self.board[row][col] == "--":
            return False
        
        self.clicked_squares.append(location)

        if self.get_valid_move(location):

            self.clicked_squares.append(location)
            self.move()
            self.clicked_squares.clear()
            return True
        
        else:
            self.clicked_squares.clear()
            self.clicked_squares.append(location)
        
    def create_guidelines(self) -> List[Tuple[int, int]]:

        valid_moves = self.white_moves if self.player_colour == "w" else self.black_moves
        guidelines_squares = []
        
        if len(self.clicked_squares) != 1:
            return guidelines_squares
        
        row, col = self.clicked_squares[0][0], self.clicked_squares[0][1]

        return valid_moves.get((row, col), [])