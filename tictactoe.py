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
    # Collapse the board using list comprehension
    collapsed_board = [cell for row in board for cell in row]

    # It is player O's turn only if there are more X's than O's on the board
    return O if collapsed_board.count(X) > collapsed_board.count(O) else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_set = set()
    for row in range(len(board)):
        for cell in range(len(board[row])):
            item = board[row][cell]
            if item == EMPTY:
                actions_set.add((row, cell))
    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    class InvalidPlayException(Exception):
        pass

    x, y = action
    
    # Raise exception if a cell is not empty
    if board[x][y] != EMPTY:
        raise InvalidPlayException
    
    # Raise exception for Out-of-bounds move
    if action not in actions(initial_state()):
        raise IndexError
    
    whose_move = player(board)
    
    # Make a copy of the board before applying changes
    resulting_board = copy.deepcopy(board)
    resulting_board[x][y] = whose_move
    return resulting_board

    
def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Iterate through a list using a generator expression
    def list_equality(row):
        return all(x == row[0] for x in row)

    # Check for horizontal equality
    for row in range(len(board)):
        if list_equality(board[row]) and board[row][0] is not None:
            return(board[row][0])
    
    #Check for vertical equality
    vertical_list = []
    i = 0
    while i < len(board[0]): # len(board[0]) gives the number of columns. Alternative to hardcoding 3
        for row in range(len(board)):
            vertical_list.append(board[row][i])
        if list_equality(vertical_list) and vertical_list[0] is not None:
            return vertical_list[0]
        vertical_list = []
        i += 1

    # Chack for diagonal equality
    left_diagonal_list = [] # From left to right
    right_diagonal_list = [] # From right to left
    i = j = 0

    # Left check
    while i < len(board) and j < len(board[0]):
        left_diagonal_list.append(board[i][j])
        i += 1
        j += 1
    if list_equality(left_diagonal_list) and left_diagonal_list[0] is not None:
        return left_diagonal_list[0]

    # Right check
    i = 0
    j = len(board[0]) - 1
    while i < len(board) and j >= 0:
        right_diagonal_list.append(board[i][j])
        i += 1
        j -= 1
    if list_equality(right_diagonal_list) and right_diagonal_list[0] is not None:
        return right_diagonal_list[0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Collapse the board using list comprehension
    collapsed_board = [cell for row in board for cell in row]

    # Check that all cells on the board are filled
    def no_element_is_None(collapsed_board):
        return all(element is not None for element in collapsed_board)
    
    if winner(board) or no_element_is_None(collapsed_board):
        return True

    return False 


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    return 1 if winner(board) == X else (-1 if winner(board) == O else 0)


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Define function for X player
    if terminal(board):
        return None
    else:
        if player(board) == X:
            _, optimal_move = max_value(board)      
        else:
            _, optimal_move = min_value(board)
            
    return optimal_move


def max_value(board):
    if terminal(board):
        return utility(board), None

    v = float('-inf')
    optimal_move = None
    for action in actions(board):
        score, _ = min_value(result(board, action))
        if score > v:
            v = score
            optimal_move = action
            if v == 1:
                return v, optimal_move
            
    return v, optimal_move


def min_value(board):
    if terminal(board):
        return utility(board), None

    v = float('inf')
    optimal_move = None
    for action in actions(board):
        score, _ = max_value(result(board, action))
        if score < v:
            v = score
            optimal_move = action
            if v == -1:
                return v, optimal_move

    return v, optimal_move
