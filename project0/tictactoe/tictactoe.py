"""
Tic Tac Toe Player
"""
import copy
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
    # Count total Xs and Os on board to determine turn
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Return all empty cell coordinates as possible moves
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] is None}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    # New check for out-of-bounds indices
    if not (0 <= i < 3 and 0 <= j < 3):
        raise Exception("Invalid move: cell position is out of bounds.")

    if board[i][j] is not None:
        raise Exception("invalid move: cell is already filled.")

    # Use deepcopy to avoid mutating original board
    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check all rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != None:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != None:
            return board[0][i]

    # Check both diagonals
    if board[0][0] == board[1][1] == board[2][2] != None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != None:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    # If any empty cell remains, game is not over
    for row in board:
        if None in row:
            return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax_score(board):
    """
    Returns the minimax score of a board (used internally).
    """
    # Base case: game over
    if terminal(board):
        return utility(board)

    # Recursively evaluate best/worst outcome
    if player(board) == X:
        return max(minimax_score(result(board, action)) for action in actions(board))
    else:
        return min(minimax_score(result(board, action)) for action in actions(board))


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    best_action = None

    # Maximizing player (X)
    if player(board) == X:
        best_score = float('-inf')
        for action in actions(board):
            score = minimax_score(result(board, action))
            if score > best_score:
                best_score = score
                best_action = action
    # Minimizing player (O)
    else:
        best_score = float('inf')
        for action in actions(board):
            score = minimax_score(result(board, action))
            if score < best_score:
                best_score = score
                best_action = action

    return best_action
