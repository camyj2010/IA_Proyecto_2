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
    # print (root)


    # Pa debuggear xd
    # print("Root: ", root.game.player1_pos, root.game.player2_pos, root.type, "-depth", root.depth, '-node_score', root.score)
    # children = tree_to_list(root)
    # for child in children:
       
    #     print(
    #         child.type, 
    #         "-depth", child.depth,
    #         "-j1:", 
    #         child.game.player1_pos, 
    #         child.game.player1_score,
    #         "-j2:", 
    #         child.game.player2_pos, 
    #         child.game.player2_score,
    #         '-node_score', child.score
    #         )
        
    for child in root.children:
       
        if child.score == root.score and child.depth==1:
            # print("POSICION INICIAL: ", root.game.player1_pos)
            # print("Movimiento recomendado:", child.game.player1_pos)
            # print("Score:", child.score)
            # print("Profundidad:", child.depth)
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
                                node.game.player1_score + scale_points(move_points+1, node.depth+1), 
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
                                node.game.player2_score + scale_points(move_points+1, node.depth+1)
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


def scale_points(points, depth):
    '''
    Escala la cantidad de puntos obtenidos segun la profundidad del nodo
    '''
    if depth==0:
        return points * 0
    if depth==1:
        return points * 1
    if depth==2:
        return points * 0.7
    if depth==3:
        return points * 0.4
    if depth==4:
        return points * 0.2
    if depth==5:
        return points * 0.05
    if depth==6:
        return points * 0.01
    return points


def manhattan_distance(position1, position2):
    '''
    Calcula la distancia de manhattan entre dos puntos
    '''
    return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])


def utility_function(player1_pos, player2_pos, board):
    player1_color = player1_pos[0] + player1_pos[1]
    player2_color = player2_pos[0] + player2_pos[1]

    #Distancia de cada punto al jugador 1
    player1_distances = []
    for position in board:
        if position != 0:
            manhattan = manhattan_distance(position, player1_pos)
            if manhattan == 3:
                moves = get_all_moves(player1_pos, player2_pos)
                if position in moves:
                    player1_distances.append(-1)
                else:
                    player1_distances.append(manhattan)
            else:
                player1_distances.append(manhattan)
        else:
            player1_distances.append(0)

    #Distancia de cada punto al jugador 2
    player2_distances = []
    for position in board:
        if position != 0:
            manhattan = manhattan_distance(position, player2_pos)
            if manhattan == 3:
                moves = get_all_moves(player2_pos, player1_pos)
                if position in moves:
                    player2_distances.append(-1)
                else:
                    player2_distances.append(manhattan)
            else:
                player2_distances.append(manhattan)
        else:
            player2_distances.append(0)
    

    #Cantidad de movimientos maxima que se debe hacer el jugador
    # para llegar a un punto dependiendo de su distancia
    distance_scaler = {
        -1: 1,
        0: 1,
        1: 3,
        2: 2,
        3: 3,
        4: 4,
        5: 3,
        6: 4,
        7: 5,
        8: 4,
        9: 5,
        10: 4,
        11: 5,
        12: 4,
        13: 5,
        14: 6
    }
    #Valor del punto divido la distancia del punto al jugador (Se hace para cada punto)
    
    player1_value = sum([(i+1) / distance_scaler[distance] if distance != 0 else 0 for i, distance in enumerate(player1_distances)])
    player2_value = sum([(i+1) / distance_scaler[distance] if distance != 0 else 0 for i, distance in enumerate(player2_distances)])

    return player1_value - player2_value
    


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
        child.score = child.game.player1_score - child.game.player2_score + utility_function(child.game.player1_pos, child.game.player2_pos, child.game.board)
        #print('nodo', child.game.player1_pos, child.game.player2_pos, child.score, child.depth)
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
    game = Game((3, 4), (4, 2), [0, 0, (5, 7), 0, 0, 0, 0], 0, 0)
    # Prueba minimax prof 2
    minimax(game, 2)