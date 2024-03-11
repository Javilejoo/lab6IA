import numpy as np
import pygame
import sys
import math
import random

Blue = (0,0,255)
Black = (0,0,0)
Red = (255,0,0)
Yellow = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

def menu():
    print("1. Humano vs IA")
    print("2. IA vs IA")
    opcion = int(input("Elige una opción: "))
    return opcion

def crear_tablero():
    tablero = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return tablero

def drop_piece(tablero, row, col, piece):
        tablero[row][col] = piece

def is_valid_location(tablero, col):
     return tablero[ROW_COUNT-1][col] == 0

def get_next_open_row(tablero,col):
    for r in range(ROW_COUNT):
         if tablero[r][col] == 0:
             return r

def print_board(tablero):
    print(np.flip(tablero, 0))

def winning_move(tablero, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if tablero[r][c] == piece and tablero[r][c+1] == piece and tablero[r][c+2] == piece and tablero[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if tablero[r][c] == piece and tablero[r+1][c] == piece and tablero[r+2][c] == piece and tablero[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if tablero[r][c] == piece and tablero[r+1][c+1] == piece and tablero[r+2][c+2] == piece and tablero[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if tablero[r][c] == piece and tablero[r-1][c+1] == piece and tablero[r-2][c+2] == piece and tablero[r-3][c+3] == piece:
                return True

def draw_board(tablero):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, Blue, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, Black, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)


    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if tablero[r][c] == 1:
                pygame.draw.circle(screen, Red, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif tablero[r][c] == 2:
                pygame.draw.circle(screen, Yellow, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

    pygame.display.update()

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def is_game_over(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def score_position(board, piece):
    # Implement scoring logic here. For simplicity, return 0.
    # You can improve by checking for potential wins, blocks, etc.
    return 0

# TODO revisar que esté bien
# Función Minmax
def minimax(board, depth, alpha, beta, is_maximizing):
    valid_locations = get_valid_locations(board)
    is_terminal = is_game_over(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else: 
                return (None, 0)
        else: 
            return (None, score_position(board, AI_PIECE))
    if is_maximizing:
        value = float('-inf')
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else: 
        value = float('inf')
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

AI_PIECE = 2
PLAYER_PIECE = 1
EMPTY = 0

tablero = crear_tablero()
print_board(tablero)
game_over = False
turno = 0

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(tablero)
pygame.display.update()
 
myfont = pygame.font.SysFont("monospace", 75)

while not game_over:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, Black, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turno == 0:
                pygame.draw.circle(screen, Red, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, Yellow, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, Black, (0,0, width, SQUARESIZE))
            if turno == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(tablero, col):
                    row = get_next_open_row(tablero, col)
                    drop_piece(tablero, row, col, 1)

                    if winning_move(tablero, 1):
                        label = myfont.render("Jugador 1 gana!!", 1, Red)
                        screen.blit(label, (40,10))
                        game_over = True
            else:
                # Turno de la IA
                col, minimax_score = minimax(tablero, 5, float('-inf'), float('inf'), True)
                if is_valid_location(tablero, col):
                    pygame.time.wait(500)  
                    row = get_next_open_row(tablero, col)
                    drop_piece(tablero, row, col, AI_PIECE)
                    
                    if winning_move(tablero, AI_PIECE):
                        label = myfont.render("AI wins!!", 1, Yellow)
                        screen.blit(label, (40,10))
                        game_over = True
            '''
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))
                
                if is_valid_location(tablero, col):
                    row = get_next_open_row(tablero, col)
                    drop_piece(tablero, row, col, 2)

                    if winning_move(tablero, 2):
                        label = myfont.render("Jugador 2 gana!!", 2, Yellow)
                        screen.blit(label, (40,10))
                        game_over = True  
            '''  

            print_board(tablero) 
            draw_board(tablero)

            turno += 1
            turno = turno % 2

            if game_over:
                pygame.time.wait(3000)