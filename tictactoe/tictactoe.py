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
    x_count=0
    o_count=0
    for i in board:
      for j in i:
        if j==X:
          x_count+=1
        elif j==O:
            o_count+=1
    if x_count<=o_count:
      return X 
    else:
      return O
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action=set()
    for i in range(3):
      for j in range(3):
        if board[i][j]==EMPTY:
          action.add((i,j))

    return action
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action[0] not in range(0,3) or action[1] not in range(0,3):
      raise ValueError

    new_board=copy.deepcopy(board)
    if new_board[action[0]][action[1]]==EMPTY:
      new_board[action[0]][action[1]]=player(new_board)
      return new_board
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    tris=[[board[0][0],board[1][1],board[2][2]],
          [board[0][0],board[0][1],board[0][2]],
          [board[1][0],board[1][1],board[1][2]],
          [board[2][0],board[2][1],board[2][2]],
          [board[0][0],board[1][0],board[2][0]],
          [board[0][1],board[1][1],board[2][1]],
          [board[0][2],board[1][2],board[2][2]],
          [board[0][2],board[1][1],board[2][0]]]
    for i in tris:
      if all(j==X for j in i):
        return X 
      elif all(j==O for j in i):
        return O

    return None
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) !=None:
        return True
    for i in board:
      for j in i:
        if j==None:
          return False
     
    return True
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board)==X:
      return 1
    elif winner(board)==O:
      return -1
    else:
      return 0
    raise NotImplementedError


def max_value(board):
  if terminal(board):
    return utility(board)
  v=-math.inf
  for action in actions(board):
    v=max(v,min_value(result(board,action)))
  return v


def min_value(board):
  if terminal(board):
    return utility(board)
  v=math.inf
  for action in actions(board):
    v=min(v,max_value(result(board,action)))
  return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
      return None

    if all(i==None for i in board[0]+board[1]+board[2]):
      return (0,0)

    a=actions(board).pop()

    if player(board)==X:
      for action in actions(board):
        if min_value(result(board,action))>min_value(result(board,a)):
          a=action

    if player(board)==O:
      for action in actions(board):
        if max_value(result(board,action))<max_value(result(board,a)):
          a=action

    return a
    raise NotImplementedError
