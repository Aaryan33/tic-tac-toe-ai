"""
Tic Tac Toe Player
"""

import math
import copy
from queue import Empty

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

    if board == initial_state():
        return X

    else:
        totalmoves_playerX = 0
        totalmoves_playerO = 0

        # To keep track of the number of moves played by X and O
        for row in board:
            
            totalmoves_playerX += row.count(X) 
            totalmoves_playerO += row.count(O)

        if totalmoves_playerX > totalmoves_playerO:
            return O
        else:
            return X 


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    actions = set()

    for i in range(3):              # len(board) - returns the number of rows in the board
        for j in range(3):      # len(board[0]) - returns the number of columns in the board
            
            if board[i][j] == EMPTY:
                actions.add((i,j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if action not in actions(board):
        raise Exception("Invalid action")

    result = copy.deepcopy(board)
    result [action[0]][action[1]] = player(board)
    return result


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    winning_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6)]

    # Check if any player has won
    for condition in winning_conditions:

        # Check if all cells in the condition are the same and equal to X or O

        if all(board[i // 3][i % 3] == X for i in condition):     # Check if X has a winning condition
            return X
        elif all(board[i // 3][i % 3] == O for i in condition):   # Check if O has a winning condition
            return O

    return None     # No winner found


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if (winner(board) == X) or (winner(board) == O):
        return True
    
    total_emptycells = 0
    
    for row in board:
        total_emptycells += row.count(EMPTY)

    if total_emptycells == 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if (winner(board) == X):
        return 1
    
    elif (winner(board) == O):
        return -1

    else:
        return 0



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None
    
    # Create a set of valid_actions for the current board
    valid_actions = actions(board)

    # Determine who the current player is
    next_player = player(board) 
    current_player = ''

    if next_player == O:
        current_player = 'X'
    if next_player == X:
        current_player = 'O'

    # The maximizing player (current player) picks action a in valid_actions that produces the highest value of Min-value(Result(board, a))
    if current_player == O:
        possiblemoveresults = []
        for action in valid_actions:
            possiblemoveresults.append([minValue(result(board, action)), action])
        return sorted(possiblemoveresults, key=lambda x: x[0], reverse=True)[0][1]

    elif current_player == X:
        possiblemoveresults = []
        for action in valid_actions:
            possiblemoveresults.append([maxValue(result(board, action)), action])
        return sorted(possiblemoveresults, key=lambda x: x[0])[0][1]

    for action in valid_actions:
        maxValue(board)

    # The minimizing player (nex_player) picks action a in valid_actions that produces the lowest value of Max-value(Result(board,a))
    def maxValue(board):
        v = float('-inf')
        if terminal(board):
            return utility(board)
        for action in actions(board):
            v = max(v,minValue(result(board, action)))
        return v
    

    def minValue(board):
        v = float('inf')
        if terminal(board):
            return utility(board)
        for action in actions(board):
            v = min(v,maxValue(result(board, action)))
        return v