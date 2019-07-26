"""
    CS5001
    Fall 2018
    Jake Mittleman
    HW 6
"""
import turtle

def draw_board(n, SQUARE):
    '''
        Function: draw_board
        Parameters: n, an int for # of squares
        Returns: nothing
        Does: Draws an nxn board with a green background
    '''

    turtle.setup(n * SQUARE + SQUARE, n * SQUARE + SQUARE)
    turtle.screensize(n * SQUARE, n * SQUARE)
    turtle.bgcolor('white')

    # Create the turtle to draw the board
    othello = turtle.Turtle()
    othello.penup()
    othello.speed(0)
    othello.hideturtle()
    # Line color is black, fill color is green
    othello.color("black", "forest green")

    # Move the turtle to the upper left corner
    corner = -n * SQUARE / 2
    othello.setposition(corner, corner)

    # Draw the green background
    othello.begin_fill()
    for i in range(4):
        othello.pendown()
        othello.forward(SQUARE * n)
        othello.left(90)
    othello.end_fill()

    # Draw the horizontal lines
    for i in range(n + 1):
        othello.setposition(corner, SQUARE * i + corner)
        draw_lines(othello, n, SQUARE)

    # Draw the vertical lines
    othello.left(90)
    for i in range(n + 1):
        othello.setposition(SQUARE * i + corner, corner)
        draw_lines(othello, n, SQUARE)


def draw_lines(turt, n, SQUARE):
    """
        name: draw_lines
        parameters: n -- an int
    """
    turt.pendown()
    turt.forward(SQUARE * n)
    turt.penup()

def draw_new_tile(board, x, y):
    """
        name: draw_new_tile
        inputs: x and y -- ints from the range 0 - (n - 1) that
                refer to which box the user has clicked in
        returns: False -- only if user has clicked a box where
                a piece is located.
                Draws a circle otherwise
        does: if check_valid_move returns True, draws a circle
            in the box the user has clicked in denoted by x and y.
            For example: if x is 1 and y is 3, it will draw a box
            in row 1 and column 3
    """

    # calculate the middle of the box on the x axis
    # and the top of the box (- 3) on the y axis
    # Ex with square = 50: (0, 1) = (-25, 97)
    row = (board._NEG_BOUND + board._SQUARE // 2) + (y * board._SQUARE)
    col = board._POS_BOUND - ((x * board._SQUARE) + 3)

    # if there is no piece there.
    if board._board[(x, y)].check_valid_move(x, y):

        # draw the circle
        turtle.penup()
        turtle.goto(row, col)
        turtle.pendown()

        # check which color needs to be drawn.
        color = board.check_turn()
        turtle.pencolor(color)
        turtle.fillcolor(color)
        turtle.begin_fill()
        turtle.circle(board._TILE_RADIUS, 360)
        turtle.end_fill()

        # with turn over, increment turn counter
        # and mark piece as played.
        board._board[(x, y)].mark_played()
        board.alter_tile_count(False)

    # if a piece is already there,
    # return False
    else:
        return False

def flip_tile(board, tile_list):
    """
        name: flip_tile
        inputs: x and y -- ints from the range 0 - (n - 1) that
                refer to which box the user has clicked in
        returns: nothing
        does: draws a new tile of opposite color where a tile has been
            flipped. This is a more basic version of the draw_new_tile
            function as it doesn't increment turns.
    """

    for tile in tile_list:

        box_row = tile.get_pos()[1]
        box_col = tile.get_pos()[0]

        # calculate the middle of the box on the x axis
        # and the top of the box (- 3) on the y axis
        # Ex with square = 50: (0, 1) = (-25, 97)
        row = (board._NEG_BOUND + board._SQUARE // 2) + (box_row * board._SQUARE)
        col = board._POS_BOUND - ((box_col * board._SQUARE) + 3)

        # draw the circle
        turtle.penup()
        turtle.goto(row, col)
        turtle.pendown()

        # check which color needs to be drawn.
        color = board.check_turn()
        turtle.pencolor(color)
        turtle.fillcolor(color)
        turtle.begin_fill()
        turtle.circle(board._TILE_RADIUS, 360)
        turtle.end_fill()

        tile.set_color(color)

        board.alter_tile_count()

def print_winner_box(board):
    """
        name: print_winner_box
        input: an object of type board
        returns: nothing
        does: draws the background box that will
            be behind the winner information
    """

    turtle.penup()
    turtle.speed(0)
    turtle.goto(board._NEG_BOUND + 10, board._POS_BOUND - 10)
    turtle.pendown()
    turtle.pencolor((140, 47, 94))
    turtle.fillcolor((140, 47, 94))
    turtle.begin_fill()
    turtle.setheading(0)
    for _ in range(4):
        turtle.forward(board._POS_BOUND * 2 - 20)
        turtle.right(90)
    turtle.end_fill()

def print_winner(board, winner):
    """
        name: print_winner
        input: board -- an object of type board
                winner -- a string (the game's winner)
        returns: nothing
        does: writes the winner, the game's score,
            and "click to exit" to the turtle window.
    """
    # print the winner
    turtle.penup()
    turtle.goto(0, board._SQUARE // 2)
    turtle.pencolor("White")
    turtle.pendown()
    turtle.write(winner, False, "center",
                    font = ("Arial", board._n * 5))

    # print the score
    turtle.penup()
    turtle.goto(0, -(board._SQUARE // 2))
    turtle.pendown()
    score = "B: " + str(board._num_black) + " -- " + \
                    str(board._num_white) + " :W"
    turtle.write(score, False, "center",
                    font = ("Arial", board._n * 5))

    # print "click to exit"
    turtle.penup()
    turtle.goto(0, -board._SQUARE - board._SQUARE // 2)
    turtle.pendown()
    turtle.write("Click to exit", False, "center",
                    font = ("Arial", board._n * 5))

def draw_winner(board):
    """
        name: draw_winner
        parameters: board -- a board object
        returns: nothing
        does: prints the winner to the turtle screen
            and records the score
    """

    print_winner_box(board)
    print_winner(board, board.get_winner())
    board.get_winner_score()
    turtle.exitonclick()
