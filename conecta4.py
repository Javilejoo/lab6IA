import random
import numpy as np
import pygame
import sys
import math

Blue = (0,0,255)
Black = (0,0,0)
Red = (255,0,0)
Yellow = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

HUMAN = 0
AI = 1

HUMAN_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4
EMPTY = 0

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
def score_position(tablero, piece):
    score = 0
    # Score horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(tablero[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            # four in a row
            if window.count(piece) == 4:
                score += 100
            # three in a row
            elif window.count(piece) == 3 and window.count(EMPTY) == 1:
                score += 10

    # Score vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(tablero[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            if window.count(piece) == 4:
                score += 100
            elif window.count(piece) == 3 and window.count(EMPTY) == 1:
                score += 10

    return score

def get_valid_locations(tablero):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(tablero, col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(tablero, piece):
    valid_locations = get_valid_locations(tablero)
    best_score = 0
    best_col = random.choice(valid_locations)
    
    for col in valid_locations:
        row = get_next_open_row(tablero, col)
        temp_board = tablero.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col



def draw_board(tablero):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, Blue, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, Black, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)


    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if tablero[r][c] == HUMAN_PIECE:
                pygame.draw.circle(screen, Red, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif tablero[r][c] == AI_PIECE:
                pygame.draw.circle(screen, Yellow, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

    pygame.display.update()

tablero = crear_tablero()
print_board(tablero)
game_over = False


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

turno = random.randint(HUMAN, AI)

while not game_over:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, Black, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turno == HUMAN:
                pygame.draw.circle(screen, Red, (posx, int(SQUARESIZE/2)), RADIUS)
            
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, Black, (0,0, width, SQUARESIZE))
            if turno == HUMAN:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(tablero, col):
                    row = get_next_open_row(tablero, col)
                    drop_piece(tablero, row, col, HUMAN_PIECE)

                    if winning_move(tablero, HUMAN_PIECE):
                        label = myfont.render("Jugador 1 gana!!", 1, Red)
                        screen.blit(label, (40,10))
                        game_over = True


                    turno += 1
                    turno = turno % 2
                    print_board(tablero) 
                    draw_board(tablero)


    # IA hace su movimiento
    if turno == AI and not game_over:
        #col = random.randint(0, COLUMN_COUNT-1)
        col = pick_best_move(tablero, AI_PIECE)
                
        if is_valid_location(tablero, col):
            pygame.time.wait(500)
            row = get_next_open_row(tablero, col)
            drop_piece(tablero, row, col, AI_PIECE)

            if winning_move(tablero, AI_PIECE):
                label = myfont.render("Jugador 2 gana!!", 2, Yellow)
                screen.blit(label, (40,10))
                game_over = True

            print_board(tablero) 
            draw_board(tablero)

            turno += 1
            turno = turno % 2

    if game_over:
        pygame.time.wait(3000)
    