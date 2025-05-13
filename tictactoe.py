"""
Tic Tac Toe Player
"""

import math
import copy

from bigtree import Node

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """


    if terminal(board):
        return "The game is already over"

    x_movements = 0
    o_movements = 0
    for rows in board:
        for cell in rows:
            if cell == X:
                x_movements = x_movements + 1
            elif cell == O:
                o_movements = o_movements + 1

    current_player = None
    if x_movements < o_movements or x_movements == o_movements:
        current_player = X
    else:
        current_player = O

    return current_player

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    empty_cells = 0
    for rows in board:
        for cell in rows:
            if cell == EMPTY:
                empty_cells = empty_cells + 1
    if empty_cells < 1:
        return "The game is already over"

    possible_actions = set()

    for i, rows in enumerate(board):
        for j, cell in enumerate(rows):
            if cell == EMPTY:
                possible_actions.add((i, j))

    return possible_actions

def valid_action_in_board(board, action):
    """Returns if the action is a valid move in a given board"""
    return board[action[0]][action[1]] is None

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if (action is None
        or board is None
        or not isinstance(action, tuple)
        or len(action) != 2
        or action[0] > 2 or action[0] < 0 or not isinstance(action[0], int)
        or action[1] > 2 or action[1] < 0 or not isinstance(action[1], int)
        or not valid_action_in_board(board, action)):

        raise ValueError("The action is not valid")

    current_player = player(board)
    new_board = copy.deepcopy(board)
    row, cell = action
    new_board[row][cell] = current_player

    return new_board

def board_match(board, player):
    for i in range(3):
        # Check rows and columns
        if all(board[i][j] == player for j in range(3)):
            return player
        if all(board[j][i] == player for j in range(3)):
            return player

        # Check diagonals
        if all(board[i][i] == player for i in range(3)):
            return player
        if all(board[i][2 - i] == player for i in range(3)):
            return player

    # IF there's no winner
    return None

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board_match(board, X) is not None:
        return X
    elif board_match(board, O) is not None:
        return O

    # IF there's no winner
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    terminal_board = True
    for rows in board:
        for cell in rows:
            if cell == EMPTY:
                terminal_board = False

    winner_board = None
    if not terminal_board:
        winner_board = winner(board)

    return terminal_board or bool(winner_board)

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    winner_board = winner(board)
    result = None
    if winner_board == X:
        result = 1
    elif winner_board == O:
        result = -1
    else:
        result = 0

    return result

def min_player(board, best_max_value, best_min_value, node):
    heuristic_value = node.heuristic_value + 1

    if terminal(board):
        node.result = utility(board)
        return node

    for i, action in enumerate(actions(board)):
        board_result = result(board, action)

        sub_node = Node(str(i)+O, current_player=X, action=action, board_result=board_result, result= None, heuristic_value= heuristic_value, selected= None, parent= node)

        max_node = max_player(board_result, best_max_value, best_min_value, sub_node)

        sub_node.result = max_node.result

        if max_node.result < best_min_value.result or (max_node.result == best_min_value.result and max_node.heuristic_value < best_min_value.heuristic_value):
            sub_node.selected = 1
            best_min_value = sub_node
        # elif max_node.result > best_min_value.result:
        #     break
    return best_min_value

def max_player(board, best_max_value, best_min_value, node):
    heuristic_value = node.heuristic_value + 1

    if terminal(board):
        node.result = utility(board)
        return node

    for i, action in enumerate(actions(board)):
        board_result = result(board, action)

        sub_node = Node(str(i)+X, current_player=X, action=action, board_result=board_result, result= None, heuristic_value= heuristic_value, selected= None, parent= node)

        min_node = min_player(board_result, best_max_value, best_min_value, sub_node)

        sub_node.result = min_node.result

        if min_node.result > best_max_value.result or (min_node.result == best_max_value.result and min_node.heuristic_value < best_max_value.heuristic_value):
            sub_node.selected = 1
            best_max_value = sub_node
        # elif min_node.result < best_max_value.result:
        #     break
    return best_max_value

def empty_board(board):
    for rows in board:
        for cell in rows:
            if cell != EMPTY:
                return False

    return True

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # print("Initial board: ", board)

    current_player = player(board)

    root = Node(current_player, action=None, board_result= None, result= None, heuristic_value= 0, selected= None, parent= None)

    if terminal(board):
        return None
    else:
        optimal_move = None
        init_best_max = Node("0" + X, current_player=X, action=None, board_result= None, result= -math.inf, heuristic_value= 0, selected= None, parent= None)
        init_best_min = Node("0" + O, current_player=O, action=None, board_result= None, result= math.inf, heuristic_value= 0, selected= None, parent= None)

        if current_player == X:
            optimal_move = max_player(board, init_best_max, init_best_min, root)
        else:
            optimal_move = min_player(board, init_best_max, init_best_min, root)
        return optimal_move.action
