import ChessBot as cb
import chess as ch
import pygame
from pygame.locals import *
import math

#initialise square display
screen_size = 500 # (X,Y)
piece_size = screen_size//8
SCREEN = pygame.display.set_mode((screen_size, screen_size), RESIZABLE)
pygame.init()

#basic colours
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
BROWN = (184, 139, 74)
LIGHTBROWN = (227, 193, 111)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

#load piece images
piece_imgs = {
    'p': pygame.transform.scale(pygame.image.load('images/black-pawn.png'), (piece_size,piece_size)),
    'n': pygame.transform.scale(pygame.image.load('images/black-knight.png'), (piece_size,piece_size)),
    'b': pygame.transform.scale(pygame.image.load('images/black-bishop.png'), (piece_size,piece_size)),
    'r': pygame.transform.scale(pygame.image.load('images/black-rook.png'), (piece_size,piece_size)),
    'q': pygame.transform.scale(pygame.image.load('images/black-queen.png'), (piece_size,piece_size)),
    'k': pygame.transform.scale(pygame.image.load('images/black-king.png'), (piece_size,piece_size)),
    'P': pygame.transform.scale(pygame.image.load('images/white-pawn.png'), (piece_size,piece_size)),
    'N': pygame.transform.scale(pygame.image.load('images/white-knight.png'), (piece_size,piece_size)),
    'B': pygame.transform.scale(pygame.image.load('images/white-bishop.png'), (piece_size,piece_size)),
    'R': pygame.transform.scale(pygame.image.load('images/white-rook.png'), (piece_size,piece_size)),
    'Q': pygame.transform.scale(pygame.image.load('images/white-queen.png'), (piece_size,piece_size)),
    'K': pygame.transform.scale(pygame.image.load('images/white-king.png'), (piece_size,piece_size)),
}

def resetScreen():
    # Create checkered pattern
    SCREEN.fill(BROWN)
    for x in range(0, 8):
        if (x % 2) == 0:
            for y in range(0, 8, 2):
                pygame.draw.rect(SCREEN, LIGHTBROWN, (x*piece_size, y*piece_size, piece_size, piece_size))
        else:
            for y in range(1, 8, 2):
                pygame.draw.rect(SCREEN, LIGHTBROWN, (x*piece_size, y*piece_size, piece_size, piece_size))

def update(board, highlight_last_move = True):
    # Highlight start and end position of last piece moved
    if highlight_last_move:
        try:
            last_move = board.peek()
            for last_move_index in (last_move.to_square, last_move.from_square):
                x = piece_size * (last_move_index % 8)
                y = piece_size * (7 - last_move_index // 8)
                pygame.draw.rect(SCREEN, RED, pygame.Rect(x, y, piece_size, piece_size))
        except IndexError:
            pass

    # Draw pieces
    for i in range(64):
        piece = board.piece_at(i)
        if piece:
            location = ((i % 8) * piece_size, (7 * piece_size) - (i // 8) * piece_size)
            SCREEN.blit(piece_imgs[str(piece)], location)

    # Draw line borders
    for i in range(1,8):
        pygame.draw.line(SCREEN, WHITE, (0, i * piece_size), (screen_size, i * piece_size))
        pygame.draw.line(SCREEN, WHITE, (i * piece_size, 0), (i * piece_size, screen_size))

    pygame.display.flip()

def main(Board):
    max_depth = 4
    opponent_color = ch.BLACK
    bot_color = ch.WHITE

    resetScreen()
    update(Board)
    pygame.display.set_caption('ACM Chess Bot Workshop')
    index_moves = []

    # Game start
    while True:
        # Bot play
        if Board.turn == bot_color:
            bot = cb.Bot(Board, max_depth, bot_color)
            Board.push(bot.getBestMove())
            resetScreen()
            update(Board)

        # Human play
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN:

                # CTRL + Z = undo
                if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_LCTRL:
                    try:
                        Board.pop()
                        Board.pop()
                        resetScreen() # remove image of last piece moved
                    except IndexError:
                        print("No more moves to undo")

                # R = replay
                if event.key == pygame.K_r:
                    return False

                update(Board)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                resetScreen() #remove previous highlights

                #find which square was clicked and index of it
                square = (math.floor(pos[0] / piece_size), math.floor(pos[1] / piece_size))
                index = (7 - square[1]) * 8 + (square[0])

                # moving a piece
                if index in index_moves:
                    move = moves[index_moves.index(index)]
                    Board.push(move)

                    #reset index and moves
                    index = None
                    index_moves = []
                    update(Board)
                
                # if not moving a piece, highlight and show all moves
                else:   
                    piece = Board.piece_at(index)
                    if piece:
                        TX1 = piece_size * (index % 8)
                        TY1 = piece_size * (7 - index // 8)
                        pygame.draw.rect(SCREEN, GREEN, pygame.Rect(TX1, TY1, piece_size, piece_size), 5)
                        moves = []
                        for move in list(Board.legal_moves):
                            if move.from_square == index:
                                moves.append(move)
                                t = move.to_square
                                #index_moves.append(t)

                                TX1 = piece_size * (t % 8)
                                TY1 = piece_size * (7 - t // 8)

                                #highlight squares it can move to
                                pygame.draw.rect(SCREEN, BLUE, pygame.Rect(TX1, TY1, piece_size, piece_size), 5)

                        index_moves = [m.to_square for m in moves]
                    update(Board, False)

        # if game end
        if Board.outcome():
            print(Board.outcome())
            print(Board)
            break

    # Game end - Wait for user input
    while True:
        # Bot play
        if Board.turn == bot_color:
            bot = cb.Bot(Board, max_depth, bot_color)
            Board.push(bot.getBestMove())
            resetScreen()
            update(Board)

        # Human play
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return False


# (Equivalent to driver.cpp)
# Only runs if played directly from Main.py
# and not if included as a library
if __name__ == "__main__":
    done = False
    while not done:
        newBoard = ch.Board()
        done = main(newBoard)
