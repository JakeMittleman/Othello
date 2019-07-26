import turtle
from tile import Tile
from board import Board
import graphics

SQUARE = 50
MIN_BOARD = 4
DEFAULT_BOARD = 8

def turtle_setup():
    """
        name: turtle_setup
        parameters: none
        returns: nothing
        does: sets the turtle up
    """
    turtle.speed(0)
    turtle.hideturtle()
    turtle.colormode(255)
    turtle.title("Othello")

def get_n():
    """
        name: get_n
        parameters: none
        returns: an int (size of the board)
        does: prompts the user for size of the board.
            Only accepts even numbers.
    """

    # bring up the turtle prompt box asking for board size
    n = turtle.textinput("Board Size", "What size board?")

    try:
        n = int(n)

    except ValueError:
        n = DEFAULT_BOARD

    except TypeError:
        n = DEFAULT_BOARD

    # if n is odd or less than MIN_BOARD (4), prompt again
    while n % 2 != 0 or n < MIN_BOARD:
        n = int(turtle.textinput("Board Size", "Sorry," + \
                                    " I need an even number."))

    return n

def main():

    # get user input
    n = get_n()
    turtle_setup()

    # draw the board
    graphics.draw_board(n, SQUARE)

    # make a board object
    board_obj = Board(n, SQUARE)

    # call clicked in onscreenclick to
    # make events happen when board is clicked
    turtle.onscreenclick(board_obj.clicked)

    turtle.done()

main()
