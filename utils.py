import random

# Crear tablero de juego al azar
def init_game():
    '''
    Crea un tablero de juego al azar
    '''
    player1_pos = (random.randint(0, 7), random.randint(0, 7))
    player2_pos = (random.randint(0, 7), random.randint(0, 7))
    board = []
    while len(board) < 7:
        slot = (random.randint(0, 7), random.randint(0, 7))
        if slot not in board and slot != player1_pos and slot != player2_pos:
            board.append(slot)

    return player1_pos, player2_pos, board