from __future__ import nested_scopes
import random
import os
import time
import math
# You can use the functions to write your AI for competition

from checkers_game import *


def select_child(children, color, depth_limit):
    """
    Return the child with the most likely 
    heuristic for the checker game

    : param children: List of children from the action
    : param color: The color determines the player
    : param depth_limit: A limit on the depth required to 
    calculate the heuristic
    """
    child_list = []
    children = clear_unsafe_moves(children, color)
    for child in children:
        child_list.append((compute_heuristic(child, color, depth_limit), child))
    copies1 = sorted(child_list, key=lambda x: x[0], reverse=True)
    return copies1[0][1]


def clear_unsafe_moves(children, color):
    """
    Return a list of child moves and clears the
    unsafe moves

    : param children: List of children
    : param color: The player if its the red player or blue player
    """
    copy_children = []
    for child in children:
        copy_children.append(child)
    safe_list = []
    for child in copy_children:
        des_cor_x, des_cor_y = child.move[-1]
        if color == 'r':
            if des_cor_x == 7 or des_cor_x == 0 or des_cor_y == 0 or des_cor_y == 7:
                safe_list.append(child)
                continue
            if child.board[des_cor_x + 1][des_cor_y - 1] == 'r':
                if child.board[des_cor_x + 1][des_cor_y + 1] != 'r' and child.board[des_cor_x - 1][
                    des_cor_y - 1] == 'b':
                    children.remove(child)
            if child.board[des_cor_x + 1][des_cor_y + 1] == 'r':
                if child.board[des_cor_x + 1][des_cor_y - 1] != 'r' and child.board[des_cor_x - 1][
                    des_cor_y + 1] == 'b':
                    children.remove(child)

    if children == [] and safe_list == []:
        king_children = get_king_moves(copy_children, color)
        if len(king_children) == 0:
            return copy_children
        return king_children
    elif children == [] and safe_list != []:
        return safe_list
    elif children != [] and safe_list != []:
        for child in safe_list:
            children.append(child)
        return children
    return children


def get_king_moves(children, color):
    """
    This gets the moves for the king a king is a 
    piece that is capitalized and can move 2 steps in
    the board 

    : param children: The list of child moves
    : color: Red or Blue 
    """
    king_children = []
    for child in children:
        for i in range(8):
            for j in range(8):
                if child.board[i][j] == color.capitalize():
                    king_children.append(child)
    return king_children


def compute_utility(state, color):
    """
    Computes the utlity function of the state which 
    is that it returns the sum of red count in the board
    and blue count and we have the difference of them

    : param state the state of the board
    : color the red or blue player
    """
    b_count = 0
    r_count = 0

    for row in state.board:
        for element in row:
            if element == 'b':
                b_count = b_count + 1
            elif element == 'r':
                r_count = r_count + 1
            elif element == 'B':
                b_count = b_count + 2
            elif element == 'R':
                r_count = r_count + 2
    if color == 'r':
        return r_count - b_count
    else:
        return b_count - r_count


def compute_heuristic(state, color, depth_limit):
    """
    The function works the following way:
    - checks for horizon moves and alots then low priorities
    - if this move it not a horizon move then alots the pawns with forward movement and
    row numbers are used to increase this. This will result in faster movement
       - black = row_number
       - red = length of board - row number
       - for kings its the reverse
    :param depth_limit:
    :param state: This is the state of the problem
    :param color: The current player in the simulation
    :return: a estimate for the board
    """
    r_count = 0
    b_count = 0
    for i in range(0, 3):
        for j in range(len(state.board)):
            if state.board[i][j] == 'r':
                r_count = r_count + 1
    for i in range(6, 8):
        for j in range(len(state.board)):
            if state.board[i][j] == 'b':
                b_count = b_count + 1
    count = max(r_count, b_count)
    if depth_limit == 0:
        return compute_utility(state, color)
    elif count < 2:
        defence_form_p = 0
        defence_form_op = 0
        for i in range(1, len(state.board) - 1):
            for j in range(1, len(state.board) - 1):
                if state.board[i][j] == color:
                    if color == 'r':
                        if state.board[i + 1][j - 1] == 'r' and state.board[i + 1][j + 1] == 'r':
                            defence_form_p = defence_form_p + 1
                    else:
                        if state.board[i - 1][j - 1] == 'b' and state.board[i - 1][j + 1] == 'r':
                            defence_form_op = defence_form_op + 1
        return defence_form_p - defence_form_op
    else:
        r_count_1 = 0
        b_count_1 = 0
        count = 0
        i = 0
        m = 8
        for row in state.board:
            for element in row:

                if element != '.':
                    count = count + 1
                if element == 'b':
                    b_count_1 = b_count_1 + 1
                elif element == 'r':
                    r_count_1 = r_count_1 + 1
                elif element == 'B':
                    b_count_1 = b_count_1 + 2
                elif element == 'R':
                    r_count_1 = r_count_1 + 2
            i = i + 1
        if color == 'r':
            return r_count_1 - b_count_1
        else:
            return b_count_1 - r_count_1


# If you choose to try MCTS, you can make use of the code below
class MCTS_state():
    """
            This sample code gives you a idea of how to store records for each node
            in the tree. However, you are welcome to modify this part or define your own
            class.
    """

    def __init__(self, ID, parent, child, reward, total, state, player):
        self.ID = ID
        self.parent = parent  # a list of states
        self.child = child  # a list of states
        self.reward = reward  # number of win
        self.total = total  # number of simulation for self and (grand*)children
        self.state = state
        self.player = player
        self.visited = 0  # 0 -> not visited yet, 1 -> already visited


def select_move_MCTS(state, color):
    """
               You can add additional help functions as long as this function will return a position tuple
    """
    tree = MCTS_state(0, [], [], 0, 0, state, color)  # root
    time1 = 10
    children = successors(state, color)
    for child in children:
        if len(child.move) > 2:
            return child.move
    while time1 != 0:
        time2 = os.times()[0]
        # print(time1)
        leaf = _select(tree)
        child = _expand(leaf)
        result = _simulate(child, 50)
        _back_propagate(result, child, color)
        difference = os.times()[0] - time2
        # print(time1)
        time1 = time1 - difference

    max1 = 0
    # print(tree.child)
    if tree.child == []:
        return []
    max_child = tree.child[0]

    for child in tree.child:
        q = (child.reward / child.total)  # + \
        # (math.sqrt((2 * math.log(child.parent[0].total)) / child.total))  # experiment both max probab and UCB
        # print(child.state.move, q)
        if q > max1:
            max1 = q
            max_child = child
    # print(max_child.state.move)
    return max_child.state.move


def _select(tree):
    if tree.child == []:
        tree.visited = 1
        return tree
    else:
        max1 = 0
        max_select = tree.child[0]
        for child in tree.child:
            if child.total == 0:
                return child
            else:
                key = (child.reward / child.total) + \
                      (math.sqrt((2 * math.log(child.parent[0].total)) / child.total))
                if max1 < key:
                    max_select = child
        return _select(max_select)


def _expand(leaf):
    if leaf.total == 0 or leaf.visited == 0:
        leaf.visited = 1
        return leaf
    else:
        children = []
        for succ1 in successors(leaf.state, leaf.player):
            if leaf.player == 'r':
                color = 'b'
            else:
                color = 'r'
            child1 = MCTS_state(0, [leaf], [], 0, 0, succ1, color)
            children.append(child1)
        leaf.child = children
        # print(leaf.child)
        leaf.visited = 1
    if not children:
        return leaf
    return children[0]


def _simulate(child, depth):
    state = child.state
    player = child.player
    children = successors(state, player)
    while len(children) != 0:
        if depth == 0:
            if compute_utility(state, player) >= 0:
                return player
            else:
                if player == 'r':
                    player = 'b'
                else:
                    player = 'r'
                return player

        child = select_child(children, player, depth)
        if player == 'r':
            player = 'b'
        else:
            player = 'r'

        children = successors(child, player)
        depth = depth - 1
    if player == 'r':
        player = 'b'
    else:
        player = 'r'
    return player


def _back_propagate(result, child, player):
    while child != []:

        if player == result:
            child.reward = child.reward + 1
        child.total = child.total + 1

        # print(child.reward, child.total)
        if child.parent == []:
            break
        child = child.parent[0]
    return


# ======================== Class GameEngine =======================================
class GameEngine:
    def __init__(self, str_name):
        self.str = str_name

    def __str__(self):
        return self.str

    # The return value should be a move that is denoted by a list
    def nextMove(self, state, alphabeta, limit, caching, ordering):
        global PLAYER
        PLAYER = self.str
        result = select_move_MCTS(Board(state), PLAYER)

        return result
