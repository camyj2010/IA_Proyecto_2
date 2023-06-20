from copy import deepcopy

class Game():
    def __init__(self, player1_pos, player2_pos, board, player1_score, player2_score):
        self.board = board                      # Lista de casillas que dan puntos
        self.player1_pos = player1_pos          # Posicion del jugador 1
        self.player2_pos = player2_pos          # Posicion del jugador 2
        self.player1_score = player1_score      # Puntaje del jugador 1
        self.player2_score = player2_score      # Puntaje del jugador 2


class Node():
    score = None

    def __init__(self, game, type, depth=0, parent=None, children=None):
        self.game = game                                            # Objeto Game
        self.parent = parent                                        # Nodo padre
        self.type = type                                            # Tipo de nodo (max o min)
        self.children = children if children is not None else []    # Lista de nodos hijos
        self.depth = depth                                          # Profundidad del nodo
        if type == 'max':
            self.score = -100000
        elif type == 'min':
            self.score = 100000


def minimax(game, depth):
    '''
    Crea el arbol de minimax y retorna el mejor movimiento
    '''
    board = game.board
    player1_pos = game.player1_pos
    player2_pos = game.player2_pos

    root = Node(game, 'max')
    create_tree(root, depth)
    update_minimax_tree(root)
    print (root)


    # Pa debuggear xd
    # print("Root: ", root.game.player1_pos, root.game.player2_pos, root.type, "-depth", root.depth, '-node_score', root.score)
    for child in root.children:
       
        print(
            child.type, 
            "-depth", child.depth,
            "-j1:", 
            child.game.player1_pos, 
            child.game.player1_score,
            "-j2:", 
            child.game.player2_pos, 
            child.game.player2_score,
            '-node_score', child.score
            )
        
    for child in root.children:
       
        if child.score == root.score and child.depth==1:
            print("POSICION INICIAL: ", root.game.player1_pos)
            print("Movimiento recomendado:", child.game.player1_pos)
            print("Score:", child.score)
            print("Profundidad:", child.depth)
            return child.game.player1_pos


def create_tree(node, depth):
    '''
    Crea el arbol de minimax
    '''
    if depth == 0:
        return

    if node.type == 'max':  # Movimientos del jugador 1
        moves = get_all_moves(node.game.player1_pos, node.game.player2_pos)    # Obtiene todos los movimientos posibles
        for move in moves:
            board_copy = deepcopy(node.game.board) # Copia profunda del tablero
            move_points = check_move(board_copy, move)   # Verifica si el movimiento garantiza puntos
            # Si hay puntos
            if move_points is not None:
                board_copy[move_points] = 0 # Elimina la casilla que da puntos
                new_game = Game(move, 
                                node.game.player2_pos, 
                                board_copy, 
                                node.game.player1_score + move_points + 1, 
                                node.game.player2_score
                                )
            # Si no hay puntos
            else:
                new_game = Game(move, 
                                node.game.player2_pos,
                                node.game.board, 
                                node.game.player1_score, 
                                node.game.player2_score)
                
            new_node = Node(new_game, 'min', node.depth + 1, node)
            node.children.append(new_node)
            create_tree(new_node, depth - 1)

    elif node.type == 'min': # Movimientos del jugador 2
        moves = get_all_moves(node.game.player2_pos, node.game.player1_pos)    # Obtiene todos los movimientos posibles
        for move in moves:
            board_copy = deepcopy(node.game.board) # Copia profunda del tablero
            move_points = check_move(board_copy, move)   # Verifica si el movimiento garantiza puntos
            # Si hay puntos
            if move_points:
                board_copy[move_points] = 0 # Elimina la casilla que da puntos
                new_game = Game(node.game.player1_pos, 
                                move, 
                                board_copy, 
                                node.game.player1_score, 
                                node.game.player2_score + move_points + 1
                                )
            # Si no hay puntos
            else:
                new_game = Game(node.game.player1_pos, 
                                move, 
                                node.game.board, 
                                node.game.player1_score, 
                                node.game.player2_score
                                )
            new_node = Node(new_game, 'max', node.depth + 1, node)
            node.children.append(new_node)
            create_tree(new_node, depth - 1)


def tree_to_list(node):
    '''
    Convierte el arbol de minimax en una lista
    '''
    tree_list = []

    for child in node.children:
        tree_list.append(child)
        tree_list += tree_to_list(child)

    return tree_list


def update_minimax_tree(node):
    '''
    Actualiza el arbol de minimax con los puntajes
    de cada nodo
    '''
    children = tree_to_list(node)

    max_depth = 0
    for child in children:
        if child.depth > max_depth:
            max_depth = child.depth

    # Recorro los nodos y actualizo solo los de profundidad maxima
    # (En este punto no se como incluir la parte que dijo 
    # el profe de que una casilla con puntos que se consigue 
    # antes vale mas que tomarla despues)
    for child in children:
        child.score = child.game.player1_score - child.game.player2_score
    
    while max_depth > 0:
        for child in children:
            if child.depth == max_depth:
                if child.parent.type == 'max':
                    child.parent.score = max(child.parent.score, child.score)
                elif child.parent.type == 'min':
                    child.parent.score = min(child.parent.score, child.score)

        max_depth -= 1


def check_move(board, move):
    '''
    Verifica si el movimiento garantiza puntos, de ser así, retorna
    el indice de la casilla que da puntos
    '''
    for index, point in enumerate(board):
        if point == move:
            # Se retorna el indice en la lista
            # El indice indica los puntos que da la casilla 
            # (se le tiene que sumar 1 para que sea de 1 a 7)
            return index
    return None


def get_all_moves(position,position2):
    '''
    Retorna todos los posibles movimientos de un caballo en una posicion dada
    '''
    moves = []
    x = position[0]
    y = position[1]
    #x2= position2[0]
    #y2=position2[1]


    if x - 1 >= 0 and x - 1 <= 7 :
        if y - 2 >= 0 and y - 2 <= 7:
            if position2!=(x-1,y-2):
             moves.append((x - 1, y - 2))
        if y + 2 >= 0 and y + 2 <= 7:
            if position2!=(x-1,y+2):
             moves.append((x - 1, y + 2))

    if x + 1 >= 0 and x + 1 <= 7:
        if y - 2 >= 0 and y - 2 <= 7:
             if position2!=(x+1,y-2):
                moves.append((x + 1, y - 2))
        if y + 2 >= 0 and y + 2 <= 7:
             if position2!=(x+1,y+2):
                moves.append((x + 1, y + 2))

    if x - 2 >= 0 and x - 2 <= 7 :
        if y - 1 >= 0 and y - 1 <= 7:
            if position2!=(x-2,y-1):
                moves.append((x - 2, y - 1))
        if y + 1 >= 0 and y + 1 <= 7:
             if position2!=(x-2,y+1):
                moves.append((x - 2, y + 1))

    if x + 2 >= 0 and x + 2 <= 7 :
        if y - 1 >= 0 and y - 1 <= 7:
             if position2!=(x+2,y-1):
                moves.append((x + 2, y - 1))
        if y + 1 >= 0 and y + 1 <= 7:
             if position2!=(x+2,y+1):
                moves.append((x + 2, y + 1))

    return moves



if __name__ == '__main__':
    # Juego inicial
    game = Game((0, 0), (7, 7), [(1, 2), (4, 3), (4, 7), (4, 1), (6, 5), (5, 6), (2, 1)])
    # Prueba minimax prof 2
    minimax(game, 2)