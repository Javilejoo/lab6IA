import numpy as np
import random
import pygame
import sys
import math


BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER1 = 0
PLAYER2 = 1

EMPTY = 0
HUMAN_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def evaluate_window(window, piece):
    score = 0
    opp_piece = HUMAN_PIECE
    if piece == HUMAN_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def is_terminal_node(board):
    return winning_move(board, HUMAN_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

'''
is_activated:Boolean para determinar si se activa o no el alpha-beta running (Default True) 
'''
def minimax(board, depth, alpha, beta, maximizingHUMAN, is_activated):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, float("inf"))  # Use float("inf") for consistency
            elif winning_move(board, HUMAN_PIECE):
                return (None, float("-inf"))
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingHUMAN:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False, is_activated)[1]
            if new_score > value:
                value = new_score
                column = col
            if is_activated:  # Update alpha only if Alpha-Beta Pruning is activated
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        return column, value

    else:  # Minimizing HUMAN
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, HUMAN_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True, is_activated)[1]
            if new_score < value:
                value = new_score
                column = col
            if is_activated:  # Update beta only if Alpha-Beta Pruning is activated
                beta = min(beta, value)
                if alpha >= beta:
                    break
        return column, value

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, piece):

    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == HUMAN_PIECE:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

def board_representation(board):
    return board.flatten()

def activated(is_activated):
    if is_activated == 'y':
        return True
    elif is_activated == 'n':
        return False
    


class QLearningAgent:
    def __init__(self, learning_rate=0.1, discount_rate=0.95, exploration_rate=1.0, exploration_decay=0.99, min_exploration_rate=0.01):
        self.learning_rate = learning_rate  # Alpha (α)
        self.discount_rate = discount_rate  # Gamma (γ)
        self.exploration_rate = exploration_rate  # Epsilon (ε)
        self.exploration_decay = exploration_decay
        self.min_exploration_rate = min_exploration_rate
        self.q_table = {}  # Initialize Q-table, potentially with a state representation

    def update_q_table(self, state, action, reward, next_state):
        """
        Update Q-values based on the formula:
        Q(state, action) = Q(state, action) + α * (reward + γ * max(Q(next_state, all actions)) - Q(state, action))
        """
        if state not in self.q_table:
            self.q_table[state] = np.zeros(7)  # Assuming 7 columns
        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(7)

        max_future_q = np.max(self.q_table[next_state])
        current_q = self.q_table[state][action]
        new_q = current_q + self.learning_rate * (reward + self.discount_rate * max_future_q - current_q)
        self.q_table[state][action] = new_q

    def choose_action(self, state, valid_actions):
        """
        Decide an action based on an ε-greedy policy.
        """
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(valid_actions)  # Explore
        else:
            if state not in self.q_table:
                self.q_table[state] = np.zeros(7)
            return np.argmax(self.q_table[state])  # Exploit learned values

    def decay_exploration_rate(self):
        """
        Decay the exploration rate over time, ensuring it never goes below a minimum threshold.
        """
        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)


# menu 
print("+----------------------+")
print("+--Elija preferencias--+")
print("+----------------------+")

print("+----Modo de juego-----+")
print("1. Jugador vs IA\n" + "2. IA vs IA")
pvp = int(input())

print("Incluir alpha-beta running? : y/n")
is_activated = input()

board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER1, PLAYER2)

# crear el agente Q_learning
q_learning_agent = QLearningAgent()

# IA vs Persona
if pvp == 1:
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == PLAYER1:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                #print(event.pos)
                # Ask for Player 1 Input
                if turn == PLAYER1:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, HUMAN_PIECE)

                        if winning_move(board, HUMAN_PIECE):
                            label = myfont.render("Player 1 wins!!", 1, RED)
                            screen.blit(label, (40,10))
                            game_over = True

                        turn += 1
                        turn = turn % 2

                        print_board(board)
                        draw_board(board)


        # # Ask for Player 2 Input
        if turn == PLAYER2 and not game_over:
            # Get the current state of the board for the Q-learning agent
            current_state = board_representation(board)  # You need to implement this function

            # Decide on the best action based on the current policy
            # For simplicity, we're assuming all columns are valid actions
            valid_actions = get_valid_locations(board)  # You likely have this function
            col = q_learning_agent.choose_action(current_state, valid_actions)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                # Check for win condition
                if winning_move(board, AI_PIECE):
                    label = myfont.render("Player 2 wins!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                print_board(board)
                draw_board(board)

                # Update the Q-table based on the action taken and the result
                # This might involve observing the new state and any rewards
                # Example: q_learning_agent.update_q_table(current_state, action, reward, next_state, done)

                turn += 1
                turn = turn % 2


        if game_over:
            pygame.time.wait(3000)

# IA vs IA
elif pvp == 2:
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
        #print(event.pos)
        # # Ask for Player 1 Input
        if turn == PLAYER1 and not game_over:
            # col = random.randint(0, COLUMN_COUNT-1)  # Esto es lo que se reemplazará
            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True, activated(is_activated))  # Calcula el mejor movimiento para el jugador 1 (IA)
            
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, HUMAN_PIECE)  # El jugador 1 (IA) coloca su ficha (roja) en la columna seleccionada

                if winning_move(board, HUMAN_PIECE):
                    label = myfont.render("Player 1 wins!!", 1, RED)
                    screen.blit(label, (40,10))
                    game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

        # # Ask for Player 2 Input
        if turn == PLAYER2 and not game_over:

            #col = random.randint(0, COLUMN_COUNT-1)
            #col = pick_best_move(board, AI_PIECE)
            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True, activated(is_activated))

            if is_valid_location(board, col):
                #pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    label = myfont.render("Player 2 wins!!", 1, YELLOW)
                    screen.blit(label, (40,10))
                    game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(3000)