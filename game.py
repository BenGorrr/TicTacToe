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
    turn_counters = 1
    player1_markers = []
    player2_markers = []
    winning_pairs = [
        [0, 1, 2], #horizontal1
        [3, 4, 5], #horizontal2
        [6, 7, 8], #horizontal3
        [0, 3, 6], #vertical1
        [1, 4, 7], #vertical2
        [2, 5, 8], #vertical3
        [0, 4, 8], #diagonal1
        [2, 4, 6], #diagonal2
    ]

    while not done: # game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                #check if mouse click on any squares
                # python 3.8 Walrus Operator
                # if (square := board.selectedSquares(event.pos)):
                square = board.selectedSquares(event.pos)
                if square: #if clicked on square
                    if square not in player1_markers and square not in player2_markers:
                        if turn_counters % 2 != 0: # odd counter = player1's turn
                            player1_markers.append(square)
                        elif turn_counters % 2 == 0: # even counter = player2's turn
                            player2_markers.append(square)

                        # get index of square marker to do winning check
                        p1_markers_index = list(map(board.board_squares.index, player1_markers))
                        p2_markers_index = list(map(board.board_squares.index, player2_markers))

                        for win_pair in winning_pairs: #iterate all the winning pairs
                            #use all() to check if every marker in that win_pair is in the player markers list
                            if all(marker in p1_markers_index for marker in win_pair):
                                print("Player 1 WON!")
                                pygame.draw.rect(board.board_surf, LIGHTGREEN, square)
                            elif all(marker in p2_markers_index for marker in win_pair):
                                print("Player 2 WON!")
                                pygame.draw.rect(board.board_surf, LIGHTGREEN, square)

                        turn_counters += 1 # increment counter for next turn


        # Fill the background with black
        screen.fill((0, 0, 0))
        # blit the board on the screen
        screen.blit(board.board_surf, board.board_surf.get_rect())
        # Draw squares
        # board_squares = drawSquares(board_surf, board_squares)
        board_squares = board.drawSquares()
        board.drawMarker(player1_markers, "o")
        board.drawMarker(player2_markers, "x")
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

    def drawMarker(self, squaresList, marker_type):
        if marker_type == "o":
            for square in squaresList:
                pygame.draw.circle(self.board_surf, WHITE, square.center, self.SQUARE_OFFSET/2 - 15, 4)
        elif marker_type == "x":
            padding = 30
            for square in squaresList:
                pygame.draw.line(self.board_surf, WHITE, (square.left + padding, square.top + padding), (square.right - padding, square.bottom - padding), 4)
                pygame.draw.line(self.board_surf, WHITE, (square.left + padding, square.bottom - padding), (square.right - padding, square.top + padding), 4)



if __name__ == '__main__':
    main()
