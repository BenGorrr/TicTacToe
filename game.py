# tic tac toe with pygame

#import and initiate pygame
import pygame, sys
import pygame.freetype
import time, random
pygame.init()
#import constants from config
from config import *

#Set up drawing window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tic Ma Toe')
#board_surf.blit(screen, board_rect)

def create_board():
    BOARD_WIDTH = 600
    BOARD_HEIGHT = 600
    # create board surface
    board_surf = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
    board_surf.fill((33, 33, 33))
    # draw lines on board surface
    square_offset = BOARD_HEIGHT/3
    lines_pos = [
        ( (0, square_offset), (BOARD_WIDTH, square_offset) ),
        ( (0, square_offset*2), (BOARD_WIDTH, square_offset*2) ),
        ( (square_offset, 0), (square_offset, BOARD_HEIGHT) ),
        ( (square_offset*2, 0), (square_offset*2, BOARD_HEIGHT) ),
    ]
    for line in lines_pos:
        pygame.draw.line(board_surf, (255, 255, 255), line[0], line[1], 1)
    return board_surf



def main():
    clock = pygame.time.Clock()
    board_surf = create_board()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        # Fill the background with black
        screen.fill((0, 0, 0))
        # pygame.display.update()
        # blit the board on the screen
        screen.blit(board_surf, board_surf.get_rect())
        pygame.display.flip()
        clock.tick(10)

if __name__ == '__main__':
    main()
