"""
    CS5001
    Fall 2018
    Jake Mittleman
    HW 7
"""

import turtle
import time

def ai_take_turn(board):

    if board._ai_player and board.check_turn() == "white":
        time.sleep(1)
        turtle.onscreenclick(None)
        ai_turn(board)
        turtle.onscreenclick(board.clicked)

def ai_turn(board):
    """
        name: ai_turn
        parameters: board -- a board object
        returns: nothing
        does: picks the move that will flip the most tiles
            out of all legal moves
    """

    move = ai_find_best_move(board._legalmoves)
    if len(move) > 0:
        row = move[0]
        col = move[1]

        turtle.onscreenclick(board.take_turn(row, col))

    else:
        board._turn_counter += 1
        board._legalmoves = board.get_legal_moves()
        return

def ai_find_best_move(legal_moves):
    """
        name: ai_find_best_move
        parameters: legal_moves -- a dictionary (the list of legal
                                    moves from the board class)
        returns: a tuple -- the best move from legal_moves
                            (if no legal moves, returns an empty tuple)
        does: chooses the move that will flip the most tiles. Iterates
            through the dictionary values to find the longest list
            and returns the key of that value
    """

    # if there is at least 1 legal move
    if len(legal_moves) > 0:

        # get a list of keys and values
        boxes = list(legal_moves.keys())
        flippable_tiles = list(legal_moves.values())

        # initialize the max to the first option
        best_move = flippable_tiles[0]

        # find the max
        for option in flippable_tiles[1:]:
            if len(option) > len(best_move):
                best_move = option

        # assign chosen_move
        move_index = flippable_tiles.index(best_move)
        chosen_move = boxes[move_index]

        return chosen_move

    # if no legal moves, return an empty tuple
    else:
        return ()
