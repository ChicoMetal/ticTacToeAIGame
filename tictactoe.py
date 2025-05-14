"""
Tic Tac Toe Player
"""

import math
import copy

result_key = "result"
X = "X"
O = "O"
EMPTY = None

class Node:
    """Node custome class"""
    def __init__(self, name, parent=None, **kwargs):
        self.name = name
        self.parent = parent
        self.children = []
        if parent is not None:
            self.heuristic_value_prop = parent.heuristic_value + 1
        else:
            self.heuristic_value_prop = 0
        self.__dict__.update(kwargs)

        if parent is not None:
            parent.add_child(self)

    def add_child(self, node):
        self.children.append(node)
        node.parent = self

    @property
    def depth(self):
        d = 0
        node = self.parent
        while node is not None:
            d += 1
            node = node.parent
        return d

    @property
    def path(self):
        node = self
        parts = []
        while node:
            parts.append(node.name)
            node = node.parent
        return "/".join(reversed(parts))

    @property
    def result(self):
        """set current_best_value"""
        return self.__dict__["result"]


    def set_result(self, result):
        """get current_best_value"""
        self.__dict__["result"] = result

    @property
    def heuristic_value(self):
        """set current_best_value"""
        return self.heuristic_value_prop

    def get_custom_properties(self):
        """Get custom properties"""
        # Exclude internal attributes
        built_ins = {'name', 'parent', 'children'}
        return {
            k: v for k, v in self.__dict__.items()
            if k not in built_ins and not k.startswith('_')
        }

    def get_parent(self):
        """Return the parent node if it exists, otherwise None."""
        return self.parent

    def get_children(self):
        """Return the children nodes"""
        return self.children

    def get_custom_property(self, custom_property):
        """Get the value of a specific custom property"""
        return self.get_custom_properties()[custom_property]

    def set_custom_property(self, key: str, value):
        """Replace the value of a custom property"""
        if key in {"name", "parent", "children"}:
            raise KeyError(f"Cannot overwrite internal attribute '{key}'")
        self.__dict__[key] = value

    def __repr__(self):
        return f"Node({self.name!r}, depth={self.depth})"

    def __str__(self):
        return self._display()

    def _display(self, level=0):
        indent = "  " * level
        result = f"{indent}- {self.name} (depth: {self.depth})\n"
        for child in self.children:
            result += child._display(level + 1)
        return result

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

def min_player(board, node, alpha, beta):
    """Look the best move to score the minimum possible value with alpha-beta pruning"""

    if terminal(board):
        node.set_result(utility(board))
        return node

    current_best_min_value = node

    for i, action in enumerate(actions(board)):
        board_result = result(board, action)

        sub_node = Node(str(i)+O, current_player=O, action=action, board_result=board_result, result=None, selected=None, parent=node)

        max_node = max_player(board_result, sub_node, alpha, beta)

        sub_node.set_result(max_node.result)

        if (current_best_min_value.result is None or max_node.result < current_best_min_value.result
            # or (max_node.result == current_best_min_value.result and max_node.heuristic_value < current_best_min_value.heuristic_value)
        ):
            sub_node.set_custom_property("selected", 1)
            current_best_min_value = sub_node

            beta = min(beta, current_best_min_value.result)
            if beta <= alpha:
                break  # Alpha-beta pruning

    return current_best_min_value

def max_player(board, node, alpha, beta):
    """Look the best move to score the maximum possible value with alpha-beta pruning"""

    if terminal(board):
        node.set_result(utility(board))
        return node

    current_best_max_value = node

    for i, action in enumerate(actions(board)):
        board_result = result(board, action)

        sub_node = Node(str(i)+X, current_player=X, action=action, board_result=board_result, result=None, selected=None, parent=node)

        min_node = min_player(board_result, sub_node, alpha, beta)

        sub_node.set_result(min_node.result)

        if (current_best_max_value.result is None or min_node.result > current_best_max_value.result
            # or (min_node.result == current_best_max_value.result and min_node.heuristic_value < current_best_max_value.heuristic_value)
        ):
            sub_node.set_custom_property("selected", 1)
            current_best_max_value = sub_node

            alpha = max(alpha, current_best_max_value.result)
            if beta <= alpha:
                break  # Alpha-beta pruning

    return current_best_max_value

def empty_board(board):
    """Verify if the board is completely empty"""
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
    else:
        optimal_move = None
        if current_player == X:
            root = Node(current_player, current_player=X, action=None, board_result=None, result=-math.inf, selected=None, parent=None)
            optimal_move = max_player(board, root, -math.inf, math.inf)
        else:
            root = Node(current_player, current_player=O, action=None, board_result=None, result=math.inf, selected=None, parent=None)
            optimal_move = min_player(board, root, -math.inf, math.inf)
        return optimal_move.get_custom_property("action")
