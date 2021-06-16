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
# TODO: Clean up constants Variable to config
class Game():
    def __init__(self):
        # window setup
        pygame.display.set_caption('Tic Ma Toe')
        self.font = pygame.font.Font(None, 32)
        # initiate clock and screen
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.board = Board(600, 600) #create a 600x600 board
        # Rect object for side bar
        self.sideBar_rect = pygame.Rect(600, 0, SCREEN_WIDTH - 600, SCREEN_HEIGHT)
        self.turn_counters = 1 # Counters to keep track of which player's turn
        self.player1_markers = []
        self.player2_markers = []
        self.winning_pairs = [
            [0, 1, 2], # horizontal1
            [3, 4, 5], # horizontal2
            [6, 7, 8], # horizontal3
            [0, 3, 6], # vertical1
            [1, 4, 7], # vertical2
            [2, 5, 8], # vertical3
            [0, 4, 8], # diagonal1
            [2, 4, 6], # diagonal2
        ]
        self.start_time = pygame.time.get_ticks()
        self.game_won = (False, None)
        self.game_draw = False

        while 1:
            self.Loop()

    def Loop(self):
        # TODO: Add input box to change player's name
        # main game loop
        if self.game_won[0]:
            #print(f"Player {str(self.game_won[1])} Won!")
            pass
        self.eventLoop()
        self.Draw()
        self.blitInfo()
        pygame.display.flip()
        self.clock.tick(10)

    def eventLoop(self):
        # event loop for key presses and mouse clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP and (event.key == pygame.K_r or (event.key == pygame.K_SPACE and self.game_won[0])):
                main()
            elif event.type == pygame.MOUSEBUTTONUP:
                #check if mouse click on any squares
                # python 3.8 Walrus Operator
                # if (square := board.selectedSquares(event.pos)):
                square = self.board.selectedSquares(event.pos)
                if square and not self.game_won[0]: #if clicked on square
                    if square not in self.player1_markers and square not in self.player2_markers:
                        if self.turn_counters % 2 != 0: # odd counter = player1's turn
                            self.player1_markers.append(square)
                        elif self.turn_counters % 2 == 0: # even counter = player2's turn
                            self.player2_markers.append(square)

                        # get index of square marker to do winning check
                        p1_markers_index = list(map(self.board.board_squares.index, self.player1_markers))
                        p2_markers_index = list(map(self.board.board_squares.index, self.player2_markers))

                        for win_pair in self.winning_pairs: #iterate all the winning pairs
                            #use all() to check if every marker in that win_pair is in the player markers list
                            if all(marker in p1_markers_index for marker in win_pair):
                                self.game_won = (True, 1)
                                return
                            elif all(marker in p2_markers_index for marker in win_pair):
                                self.game_won = (True, 2)
                                return
                        if len(p1_markers_index) + len(p2_markers_index) == 9:
                            self.game_draw = True
                            return
                        self.turn_counters += 1 # increment counter for next turn

    def blitInfo(self):
        # draw timer, stop when game is done
        if not self.game_won[0] and not self.game_draw:
            self.passed_time = pygame.time.get_ticks() - self.start_time
        timer = self.font.render("Time:  " + str(int(self.passed_time/1000))+"s", True, WHITE)
        self.screen.blit(timer, (self.board.board_rect.right + 50, 30))
        # draw players text
        if self.game_won[0]:
            # set color for name text when game is won
            player1_color = GREEN if self.isOdd(self.turn_counters) else RED
            player2_color = RED if self.isOdd(self.turn_counters) else GREEN
            # draw winner announcement
            winner_text = self.font.render("Winner", True, GREEN)
            indicator_pos = (self.sideBar_rect.centerx - winner_text.get_width()/2, self.sideBar_rect.centery - 70) if self.isOdd(self.turn_counters) else (self.sideBar_rect.centerx - winner_text.get_width()/2, self.sideBar_rect.centery + 70)
            self.screen.blit(winner_text, indicator_pos)
        elif self.game_draw:
            # set color for name text when game is DRAW
            player1_color = WHITE
            player2_color = WHITE
            # draw DRAW announcement
            draw_text = self.font.render("DRAW", True, GREEN)
            indicator_pos = (self.sideBar_rect.centerx - draw_text.get_width()/2, self.sideBar_rect.centery)
            self.screen.blit(draw_text, indicator_pos)
        else:
            # draw indicator for player's turn if game not won
            indicator_pos = (self.sideBar_rect.centerx, self.sideBar_rect.centery - 70) if self.isOdd(self.turn_counters) else (self.sideBar_rect.centerx, self.sideBar_rect.centery + 70)
            pygame.draw.circle(self.screen, GREEN, indicator_pos, 7)
            # set color for name text
            player1_color = GREEN if self.isOdd(self.turn_counters) else WHITE
            player2_color = WHITE if self.isOdd(self.turn_counters) else GREEN
        player1_text = self.font.render("Bennie", True, player1_color)
        text_center_pos = (self.sideBar_rect.centerx - player1_text.get_width()/2, self.sideBar_rect.centery - 150)
        self.screen.blit(player1_text, text_center_pos)
        player2_text = self.font.render("Alex", True, player2_color)
        text_center_pos = (self.sideBar_rect.centerx - player2_text.get_width()/2, self.board.board_rect.centery + 150)
        self.screen.blit(player2_text, text_center_pos)

    def Draw(self):
        # Fill the background with black
        self.screen.fill((0, 0, 0))
        # blit the board on the screen
        self.screen.blit(self.board.board_surf, self.board.board_surf.get_rect())
        # draw squares
        self.board.board_squares = self.board.drawSquares()
        self.board.drawMarker(self.player1_markers, "o")
        self.board.drawMarker(self.player2_markers, "x")

    def isOdd(self, n):
        return n % 2 != 0

def main():
    Game()
"""
def main():
    done = False
    clock = pygame.time.Clock()
    # board_surf, board_squares = create_board()
    board = Board(600, 600) #create a 600x600 board
    turn_counters = 1
    player1_markers = []
    player2_markers = []
    winning_pairs = [
        [0, 1, 2], # horizontal1
        [3, 4, 5], # horizontal2
        [6, 7, 8], # horizontal3
        [0, 3, 6], # vertical1
        [1, 4, 7], # vertical2
        [2, 5, 8], # vertical3
        [0, 4, 8], # diagonal1
        [2, 4, 6], # diagonal2
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
"""
class Board():
    def __init__(self, BOARD_WIDTH, BOARD_HEIGHT):
        self.BOARD_WIDTH = BOARD_WIDTH
        self.BOARD_HEIGHT = BOARD_HEIGHT
        self.SQUARE_OFFSET = BOARD_HEIGHT/3
        self.board_surf, self.board_squares = self.create_board()
        self.board_rect = self.board_surf.get_rect()

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
