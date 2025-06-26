import os
import pygame as p
from python.chess_graphic import Chess_Graphics
from python.game_state import Game_State

def two_player():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    graphics = Chess_Graphics()
    screen = graphics.create_screen()
    clock = graphics.create_clock()
    
    game_state = Game_State()
    game_state.set_valid_moves()
    move_made = False
    
    running = True
    while running:

        for e in p.event.get():

            if move_made:
                game_state.set_valid_moves()
                game_state.remove_illegal_moves()
                move_made = False

            if e.type == p.QUIT:
                running = False
            
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                clicked_square = graphics.get_sqr(location)
                move_made = game_state.validate_clicked_sqrs(clicked_square)
                graphics.SOUNDS["click"].play()
 
        graphics.draw_board(screen)
        graphics.draw_guidelines(screen, game_state.create_guidelines())
        graphics.draw_pieces(screen, game_state.board)
        
        clock.tick(graphics.MAX_FPS)
        p.display.flip()
    
    p.quit()