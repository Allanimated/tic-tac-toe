"""
Tic Tac Toe Player
"""

import math

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
    # count the number of "X" and "O" symbols
    x_count = sum(row.count('X') for row in board)
    o_count = sum(row.count('O') for row in board)  
    if o_count < x_count: # O's turn if x_count is more
        return O
    if x_count == o_count: # X's turn if o_count is level
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # check if the given board is the terminal state
    if terminal(board):
        return None
    
    actions = set() # initialize an empty set of actions
    # loop thru the board and find empty spaces
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                possible_move = tuple([i, j])
                actions.add(possible_move)

    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    from copy import deepcopy
    new_board = deepcopy(board) # create a deep copy of the board
    i,j = action

    # custom exception class
    class GameError(Exception):
        pass

    if not (0 <= i <= 2) or not (0 <= j <= 2): # out of bounds move
        raise GameError("out-of-bounds!!")
    
    if board[i][j] is not EMPTY:
        raise GameError("move has been taken!!")
    
    new_board[i][j] = player(board) # update the board with the players move
    return new_board
    


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check rows 
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not EMPTY:
            return row[0]

    #check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not EMPTY:
            return board[0][col]

    #check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]

    return None # no winner 


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    if winner(board):
        # call the utility fuction and pass the terminal state
        utility(board)
        return True
    # check if the board has zero empty spaces
    for row in board: 
        for cell in row:
            if cell is EMPTY:
                return False
    utility(board)
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) is X:
        return 1
    if winner(board) is O:
        return -1
    if winner(board) is None:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):  # If the board is a terminal board, the minimax function should return None.
        return None

    # maximize the action_score if it is X's turn
    if player(board) is X:
        highest_score = -math.inf # set best action_score to the lowest possible value
        optimal_value = None
        alpha = -math.inf 
        beta = math.inf
        for action in actions(board):
            # get action_score for each action
            action_score = min_value(result(board, action), alpha, beta)
            # Update the best move and best action_score if a higher action_score is obtained
            if action_score > highest_score:
                highest_score = action_score # update best action_score
                optimal_value = action
            alpha = max(alpha, highest_score)
            if beta <= alpha:
                break  # Beta prune
        return optimal_value

    # minimize action_score when it is O's turn
    if player(board) is O:
        highest_score = math.inf  # set best action_score to the highest possible value
        optimal_value = None
        alpha = -math.inf
        beta = math.inf
        for action in actions(board):
            # get action_score for each action
            action_score = max_value(result(board, action), alpha, beta)
            # Update the best move and best action_score if a higher action_score is obtained
            if action_score < highest_score:
                highest_score = action_score
                optimal_value = action
            beta = min(beta, highest_score)
            if beta <= alpha:
                break  # Alpha prune
        return optimal_value


def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, v)
        if beta <= alpha:
            break  # Beta prune
    return v


def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))
        beta = min(beta, v)
        if beta <= alpha:
            break  # Alpha prune
    return v





        

    
    
