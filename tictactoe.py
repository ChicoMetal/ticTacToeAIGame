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

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if action == None or not isinstance(action, tuple) or len(action) != 2:
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

    winner_board = False
    if not terminal_board:
        winner_board = winner(board)

    return terminal_board or winner_board

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

def min_player(board, best_max_value, best_min_value, root):
    if terminal(board):
        return [None, utility(board)]

    index = 0
    for action in actions(board):
        result_action = result(board, action)
        index = index + 1
        sub_node = Node(str(index) + O, board_state=result_action, result = 0, parent=root)
        max_value = max_player(result_action, best_max_value, best_min_value, sub_node)

        if max_value[1] < best_min_value[1]:
            sub_node.result =max_value[1]
            best_min_value = [action, max_value[1]]
        elif max_value[1] > best_min_value[1]:
            return best_min_value
    return best_min_value

def max_player(board, best_max_value, best_min_value, root):
    if terminal(board):
        return [None, utility(board)]

    index = 0
    for action in actions(board):
        result_action = result(board, action)
        index = index + 1
        sub_node = Node(str(index) + X, board_state=result_action, result = 0, parent=root)
        min_value = min_player(result_action, best_max_value, best_min_value, sub_node)

        if min_value[1] > best_max_value[1]:
            sub_node.result = min_value[1]
            best_max_value = [action, min_value[1]]
        elif min_value[1] < best_max_value[1]:
            return best_max_value
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

    current_player = player(board)

    root = Node(current_player, board_state=board, result=0)

    if terminal(board):
        return None
    elif empty_board(board):
        return (1, 1)
    else:
        optimal_move = None
        if current_player == X:
            optimal_move = max_player(board, [None, -math.inf], [None, math.inf], root)
        else:
            optimal_move = min_player(board, [None, -math.inf], [None, math.inf], root)
        root.result = optimal_move[1]
        # root.show(attr_list=["result"])

        return optimal_move[0]
