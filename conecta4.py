import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7

def menu():
    print("1. Humano vs IA")
    print("2. IA vs IA")
    opcion = int(input("Elige una opción: "))
    return opcion

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

def crear_tablero():
    tablero = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return tablero

tablero = crear_tablero()
print_board(tablero)
game_over = False
turno = 0

while not game_over:
    # preguntar player 1
    if turno == 0:
       col = int(input("Jugador 1, elige una columna (0-6): "))

       if is_valid_location(tablero, col):
           row = get_next_open_row(tablero, col)
           drop_piece(tablero, row, col, 1)

           if winning_move(tablero, 1):
               print("Jugador 1 gana!")
               game_over = True

    # IA hace su movimiento
    else:
        col = np.random.randint(0,7)
        if is_valid_location(tablero, col):
           row = get_next_open_row(tablero, col)
           drop_piece(tablero, row, col, 2)

           if winning_move(tablero, 2):
               print("Jugador 2 gana!")
               game_over = True
               
    print_board(tablero)

    turno += 1
    turno = turno % 2

