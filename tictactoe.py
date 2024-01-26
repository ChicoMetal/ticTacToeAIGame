"""
Tic Tac Toe Player
"""

import math
import copy

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

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner = None

    if ((board[0][0] == X and board[0][1] == X and board[0][2] == X)
        or (board[1][0] == X and board[1][1] == X and board[1][2] == X)
        or (board[2][0] == X and board[2][1] == X and board[2][2] == X)

        or (board[0][0] == X and board[1][0] == X and board[2][0] == X)
        or (board[0][1] == X and board[1][1] == X and board[2][1] == X)
        or (board[0][2] == X and board[1][2] == X and board[2][2] == X)

        or board[0][0] == X and board[1][1] == X and board[2][2] == X):
        winner = X
    elif ((board[0][0] == O and board[0][1] == O and board[0][2] == O)
        or (board[1][0] == O and board[1][1] == O and board[1][2] == O)
        or (board[2][0] == O and board[2][1] == O and board[2][2] == O)

        or (board[0][0] == O and board[1][0] == O and board[2][0] == O)
        or (board[0][1] == O and board[1][1] == O and board[2][1] == O)
        or (board[0][2] == O and board[1][2] == O and board[2][2] == O)

        or board[0][0] == O and board[1][1] == O and board[2][2] == O):
        winner = O

    return winner

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

def min_player(board):
    if terminal(board):
        return None, utility(board)

    value = math.inf
    optimal_action = None
    for action in actions(board):
        result_action = result(board, action)
        max_value = max_player(result_action)

        if max_value[1] <= value:
            value = max_value[1]
            optimal_action = action

    return [optimal_action, value]

def max_player(board):
    if terminal(board):
        return None, utility(board)

    value = -math.inf
    optimal_action = None
    for action in actions(board):
        result_action = result(board, action)
        min_value = min_player(result_action)

        if min_value[1] >= value:
            value = min_value[1]
            optimal_action = action

    return [optimal_action, value]

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

    if terminal(board):
        return None
    elif empty_board(board):
        return (1, 1)
    else:
        optimal_move = None
        if current_player == X:
            optimal_move = max_player(board)
        else:
            optimal_move = min_player(board)

        return optimal_move[0]
