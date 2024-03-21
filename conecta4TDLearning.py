import numpy as np
import random
import inspect
import os
import sys
from kaggle_environments import make, utils, agent


# Función para soltar una pieza en el tablero
def drop_piece(grid, col, piece, config):
    next_grid = grid.copy()
    for row in range(config.rows-1, -1, -1):
        if next_grid[row][col] == 0:
            break
    next_grid[row][col] = piece
    return next_grid

# Función para verificar si la jugada resulta en una victoria
def check_winning_move(obs, config, col, piece):
    grid = np.asarray(obs.board).reshape(config.rows, config.columns)
    next_grid = drop_piece(grid, col, piece, config)
    for row in range(config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(next_grid[row,col:col+config.inarow])
            if window.count(piece) == config.inarow:
                return True
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns):
            window = list(next_grid[row:row+config.inarow,col])
            if window.count(piece) == config.inarow:
                return True
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns-(config.inarow-1)):
            window = list(next_grid[range(row, row+config.inarow), range(col, col+config.inarow)])
            if window.count(piece) == config.inarow:
                return True
    for row in range(config.inarow-1, config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(next_grid[range(row, row-config.inarow, -1), range(col, col+config.inarow)])
            if window.count(piece) == config.inarow:
                return True
    return False

# Agente
def my_agent(obs, config):
    valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
    for col in valid_moves:
        if check_winning_move(obs, config, col, obs.mark):
            return col
    return random.choice(valid_moves)

# Función para escribir el agente en un archivo
def write_agent_to_file(function, file):
    with open(file, "a" if os.path.exists(file) else "w") as f:
        f.write(inspect.getsource(function))
        print(function, "written to", file)



# Escribir el agente en un archivo
write_agent_to_file(my_agent, "submission.py")

# Leer el archivo del agente
submission = utils.read_file("submission.py")
saved_agent = agent.get_last_callable(submission)

# Ejecutar el agente
# Crear el entorno del juego
env = make("connectx", debug=True)
env.run([saved_agent, saved_agent])
print("Success!" if env.state[0].status == env.state[1].status == "DONE" else "Failed...")