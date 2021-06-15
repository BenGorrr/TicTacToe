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

# def create_board():
#     BOARD_WIDTH = 600
#     BOARD_HEIGHT = 600
#     SQUARE_OFFSET = BOARD_HEIGHT/3
#     # create board surface
#     board_surf = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
#     board_surf.fill((33, 33, 33))
#
#     board_squares = []
#     #first draw of squares to generate the rect obj for each squares
#     for row in range(3):
#         for column in range(3):
#             square = pygame.draw.rect(board_surf, WHITE, (column*SQUARE_OFFSET, row*SQUARE_OFFSET, SQUARE_OFFSET, SQUARE_OFFSET), 1)
#             board_squares.append(square)
#
#     return board_surf, board_squares

# def drawSquares(board_surf, board_squares):
#     for i, square in enumerate(board_squares):
#         #draw filled squares(width=0)
#         pygame.draw.rect(board_surf, GRAY, square)
#         #draw squares with edge lines border(width=1)
#         new_square = pygame.draw.rect(board_surf, WHITE, square, 1)
#         board_squares[i] = new_square
#
#     return board_squares #return squares to reassign new squares

# def isInSquare(pos, board_squares):
#     for square in board_squares:
#         # if mouse pos is in the square, return the index of the square
#         if square.collidepoint(pos):
#             # return board_squares.index(square)
#             return square #return square rect obj

def main():
    done = False
    clock = pygame.time.Clock()
    # board_surf, board_squares = create_board()
    board = Board(600, 600) #create a 600x600 board

    while not done: # game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                #check if mouse click on any squares
                # square = isInSquare(event.pos, board.board_squares)
                square = board.selectedSquares(event.pos)
                if square: #if clicked on square
                    pygame.draw.rect(board.board_surf, LIGHTGREEN, square)
                    #print(square)
                # python 3.8 Walrus Operator
                # if (square := isInSquare(event.pos, board_squares)):
                #     pygame.draw.rect(board_surf, LIGHTGREEN, square)

        # Fill the background with black
        screen.fill((0, 0, 0))
        # pygame.display.update()
        # blit the board on the screen
        screen.blit(board.board_surf, board.board_surf.get_rect())
        # Draw squares
        # board_squares = drawSquares(board_surf, board_squares)
        board_squares = board.drawSquares()
        pygame.display.flip()
        clock.tick(10)

class Board():
    def __init__(self, BOARD_WIDTH, BOARD_HEIGHT):
        self.BOARD_WIDTH = BOARD_WIDTH
        self.BOARD_HEIGHT = BOARD_HEIGHT
        self.SQUARE_OFFSET = BOARD_HEIGHT/3
        self.board_surf, self.board_squares = self.create_board()

    def create_board(self):
        # create board surface
        board_surf = pygame.Surface((self.BOARD_WIDTH, self.BOARD_HEIGHT))
        board_surf.fill((33, 33, 33))

        board_squares = []
        #first draw of squares to generate the rect obj for each squares
        for row in range(3):
            for column in range(3):
                square = pygame.draw.rect(board_surf, WHITE, (column*self.SQUARE_OFFSET, row*self.SQUARE_OFFSET, self.SQUARE_OFFSET, self.SQUARE_OFFSET), 1)
                board_squares.append(square)

        return board_surf, board_squares

    def drawSquares(self):
        for i, square in enumerate(self.board_squares):
            #draw filled squares(width=0)
            pygame.draw.rect(self.board_surf, GRAY, square)
            #draw squares with edge lines border(width=1)
            new_square = pygame.draw.rect(self.board_surf, WHITE, square, 1)
            self.board_squares[i] = new_square

        return self.board_squares #return squares to reassign new squares

    def selectedSquares(self, pos):
        for square in self.board_squares:
            # if mouse pos is in the square, return the index of the square
            if square.collidepoint(pos):
                # return board_squares.index(square)
                return square #return square rect obj


if __name__ == '__main__':
    main()
