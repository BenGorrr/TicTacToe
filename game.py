# tic tac toe with pygame

#import and initiate pygame
import pygame as pg
import pygame.freetype
import time, random, sys
pg.init()
#import constants from config
from config import *

#Set up drawing window
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Tic Ma Toe')

class Game():
    def __init__(self):
        # window setup
        pg.display.set_caption('Tic Ma Toe')
        self.font = pg.font.Font(None, 32)
        # initiate clock and screen
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.board = Board(600, 600) #create a 600x600 board
        # Rect object for side bar
        self.sideBar_rect = pg.Rect(600, 0, SCREEN_WIDTH - 600, SCREEN_HEIGHT)
        self.turn_counters = 1 # Counters to keep track of which player's turn
        self.player1_name = "Bennie"
        self.player2_name = "Alex"
        self.player1_name_input = False
        self.player2_name_input = False
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
        self.start_time = pg.time.get_ticks()
        self.game_won = (False, None)
        self.game_draw = False

        while 1:
            self.Loop()

    def Loop(self):
        # main game loop
        self.eventLoop()
        self.Draw()
        self.drawName()
        self.blitInfo()
        pg.display.flip()
        self.clock.tick(10)

    def eventLoop(self):
        # event loop for key presses and mouse clicks
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYUP and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYUP and (event.key == pg.K_r or (event.key == pg.K_SPACE and (self.game_won[0] or self.game_draw))):
                main()
            elif event.type == pg.KEYDOWN:
                # Change Player Name
                # if player1 input box is active
                if self.player1_name_input:
                    # if user press enter, unfocus the input box
                    if event.key == pg.K_RETURN:
                        self.player1_name_input = False
                    elif event.key == pg.K_BACKSPACE:
                        self.player1_name = self.player1_name[:-1]
                    else:
                        self.player1_name += event.unicode
                # if player2 input box is active
                elif self.player2_name_input:
                    if event.key == pg.K_RETURN:
                        self.player2_name_input = False
                    elif event.key == pg.K_BACKSPACE:
                        self.player2_name = self.player2_name[:-1]
                    else:
                        self.player2_name += event.unicode

            elif event.type == pg.MOUSEBUTTONUP:
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
                # Change Player Name
                # if user click on player name input box
                if self.player1_rect.collidepoint(event.pos):
                    # toggle the focus of input box
                    if not self.player2_name_input:
                        self.player1_name_input = not self.player1_name_input
                elif self.player2_rect.collidepoint(event.pos):
                    if not self.player1_name_input:
                        self.player2_name_input = not self.player2_name_input

    def blitInfo(self):
        # draw timer, stop when game is done
        if not self.game_won[0] and not self.game_draw:
            self.passed_time = pg.time.get_ticks() - self.start_time
        timer = self.font.render("Time:  " + str(int(self.passed_time/1000))+"s", True, WHITE)
        self.screen.blit(timer, (self.board.board_rect.right + 50, 30))

        if self.game_won[0]:
            # draw winner announcement
            winner_text = self.font.render("Winner", True, GREEN)
            indicator_pos = (self.sideBar_rect.centerx - winner_text.get_width()/2, self.sideBar_rect.centery - 70) if self.isOdd(self.turn_counters) else (self.sideBar_rect.centerx - winner_text.get_width()/2, self.sideBar_rect.centery + 70)
            self.screen.blit(winner_text, indicator_pos)
        elif self.game_draw:
            # draw DRAW announcement
            draw_text = self.font.render("DRAW", True, GREEN)
            indicator_pos = (self.sideBar_rect.centerx - draw_text.get_width()/2, self.sideBar_rect.centery)
            self.screen.blit(draw_text, indicator_pos)
        else:
            # draw indicator for player's turn if game not won
            indicator_pos = (self.sideBar_rect.centerx, self.sideBar_rect.centery - 70) if self.isOdd(self.turn_counters) else (self.sideBar_rect.centerx, self.sideBar_rect.centery + 70)
            pg.draw.circle(self.screen, GREEN, indicator_pos, 7)

    def drawName(self):
        # Show Border color when input is focused
        p1_border_color = GREEN if self.player1_name_input else BLACK
        p2_border_color = GREEN if self.player2_name_input else BLACK

        self.player1_rect = pg.draw.rect(self.screen, p1_border_color, (self.sideBar_rect.left, self.sideBar_rect.centery - 162, self.sideBar_rect.width, 50), 1)
        self.player2_rect = pg.draw.rect(self.screen, p2_border_color, (self.sideBar_rect.left, self.sideBar_rect.centery + 138, self.sideBar_rect.width, 50), 1)

        if self.game_won[0]:
            # set color for name text when game is won
            player1_color = GREEN if self.isOdd(self.turn_counters) else RED
            player2_color = RED if self.isOdd(self.turn_counters) else GREEN
        elif self.game_draw:
            # set color for name text when game is DRAW
            player1_color = WHITE
            player2_color = WHITE
        else:
            # set color for name text
            player1_color = GREEN if self.isOdd(self.turn_counters) else WHITE
            player2_color = WHITE if self.isOdd(self.turn_counters) else GREEN
        player1_text = self.font.render(self.player1_name, True, player1_color)
        text_center_pos = (self.sideBar_rect.centerx - player1_text.get_width()/2, self.sideBar_rect.centery - 150)
        self.screen.blit(player1_text, text_center_pos)
        player2_text = self.font.render(self.player2_name, True, player2_color)
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

class Board():
    def __init__(self, BOARD_WIDTH, BOARD_HEIGHT):
        self.BOARD_WIDTH = BOARD_WIDTH
        self.BOARD_HEIGHT = BOARD_HEIGHT
        self.SQUARE_OFFSET = BOARD_HEIGHT/3
        self.board_surf, self.board_squares = self.create_board()
        self.board_rect = self.board_surf.get_rect()

    def create_board(self):
        # create board surface
        board_surf = pg.Surface((self.BOARD_WIDTH, self.BOARD_HEIGHT))
        board_surf.fill((33, 33, 33))

        board_squares = []
        #first draw of squares to generate the rect obj for each squares
        for row in range(3):
            for column in range(3):
                square = pg.draw.rect(board_surf, WHITE, (column*self.SQUARE_OFFSET, row*self.SQUARE_OFFSET, self.SQUARE_OFFSET, self.SQUARE_OFFSET), 1)
                board_squares.append(square)

        return board_surf, board_squares

    def drawSquares(self):
        for i, square in enumerate(self.board_squares):
            #draw filled squares(width=0)
            pg.draw.rect(self.board_surf, GRAY, square)
            #draw squares with edge lines border(width=1)
            new_square = pg.draw.rect(self.board_surf, WHITE, square, 1)
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
                pg.draw.circle(self.board_surf, WHITE, square.center, self.SQUARE_OFFSET/2 - 15, 4)
        elif marker_type == "x":
            padding = 30
            for square in squaresList:
                pg.draw.line(self.board_surf, WHITE, (square.left + padding, square.top + padding), (square.right - padding, square.bottom - padding), 4)
                pg.draw.line(self.board_surf, WHITE, (square.left + padding, square.bottom - padding), (square.right - padding, square.top + padding), 4)



if __name__ == '__main__':
    main()
