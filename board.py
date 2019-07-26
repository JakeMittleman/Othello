import turtle
from tile import Tile
import graphics
import ai

STARTER_COLORS = ["white", "black", "black", "white"]

class Board:

    def __init__(self, n, square, test = False):
        """
            -- Constructor (Board class) --
        - Set _n and _square based on parameters
        - Calculate positive and negative bound based on N and SQUARE
        - Calculate TILE RADIUS based on N and SQUARE
        - _num_white and _num_black default to 2
        - _turn_counter default to 0
        - _board is created from method create_board
        """

        self._n = n
        self._SQUARE = square
        self._POS_BOUND = self._n * (self._SQUARE // 2)
        self._NEG_BOUND = -self._n * (self._SQUARE // 2)
        self._TILE_RADIUS = (-self._SQUARE // 2) + 3
        self._num_white = 2
        self._num_black = 2
        self._turn_counter = 0

        # create the dictionary to hold the game information
        self._board = self.create_board(test)
        if not test:
            self._ai_player = self.ask_game_mode()

        else:
            self._ai_player = False
        self._legalmoves = self.get_legal_moves()

    def create_board(self, test = False):
        """
            name: create_board
            parameters: none
            returns: a dictionary where the keys are the squares in
                    (row, column) form, and the value is a Tile object.
            does: Generates a dictionary of tile objects tied to their
                    square location as their key. Also calls draw_starters
                    and place_starters to draw the starting tiles on the
                    board and mark them as played.
        """

        board_map = {}

        # creating row/column pairs that stand for the boxes on the game
        # board. (0, 0), (0, 1), (0, 2),...,(3, 1), (3, 2), (3, 3).
        for row in range(self._n):
            for col in range(self._n):

                # instantiate a Tile object and set it as the value
                # to the key (row, col). Ex: (2, 0) : Tile Object
                # This allows me to check properties of the piece
                # at that given box on the game-board.
                tile = Tile((row, col), "forest green")
                board_map[(row, col)] = tile

        # draw the starting tiles and mark them as played
        if not test:
            self.draw_starters()
        self.place_starters(board_map)

        # after drawing the pieces, return the dictionary
        # to the caller, assigning it to the instance variable.
        return board_map

    def draw_starters(self):
        """
            name: draw_starters
            parameters: none
            returns: nothing
            does: Draws the starting tiles in the middle of
                    the board.
        """

        # the colors in order that the method will draw the pieces
        index = 0

        # x will always be either -square/2 or +square/2
        # y will always be 0 or square. (the -3 is so
        # turtle draws a circle without touching the box lines)
        for x in (-self._SQUARE // 2, self._SQUARE // 2):
            for y in (self._SQUARE - 3, 0 - 3):

                # draw a circle (the tile)
                color = STARTER_COLORS[index]
                turtle.speed(0)
                turtle.pencolor(color)
                turtle.fillcolor(color)
                turtle.penup()
                turtle.goto(x, y)
                turtle.pendown()
                turtle.begin_fill()
                turtle.circle(self._TILE_RADIUS, 360)
                turtle.end_fill()

                # move to the next color
                index += 1


    def place_starters(self, board_map):
        """
            name: place_starters
            parameters: board -- the _board attribute that is a
                                dictionary
            returns: nothing
            does: Marks the starting tiles as played (True) in the
                tile object attribute tile._played.
        """

        # starter pieces will always go
        # halfway inward to the board +/- 1
        middle_box = (self._n // 2)

        index = 0

        # the starter pieces are all
        # (x, y), (x - 1, y), (x, y - 1), or (x - 1, y - 1)
        for row in (middle_box - 1, middle_box):
            for col in (middle_box - 1, middle_box):

                # mark these pieces as being played
                # this prevents users from placing a piece
                # where one already exists.
                board_map[(row, col)].mark_played()
                board_map[(row, col)].set_color(STARTER_COLORS[index])

                index += 1


    def clicked(self, x, y):
        """
            name: clicked
            parameters: x and y (the coordinates of the mouse click)
            returns: False -- if you click outside the game board
                    (the outer boundaries)
                    If not, it calls get_square
            does: checks if the user clicks outside the game board.
                    If so, tells the user and returns False.
                    If not, calls get_box to determine which box
                    the user has clicked in.
        """

        # if user has clicked outside the box,
        # return False
        if x > self._POS_BOUND or x < self._NEG_BOUND:
            return False

        elif y > self._POS_BOUND or y < self._NEG_BOUND:
            return False

        # if not, call get_square and check which box
        # the user clicked in
        else:
            box = self.get_square(self._n, x, y)


    def get_square(self, n, x, y, test = False):
        """
            name: get_square
            parameters: the x and y coordinates of the mouse click
                        n -- (an int) one of the dimensions of the board
            returns: the box in (row, column) form. Ex. (0, 0)
                    calls draw_new_tile with box info Ex. (0, 0)
            does: Identifies which box the user has clicked in by
                iterating through the board squares and checking if the
                x and y coordinate is in the bounds of the box. It uses
                the board class's attribute _NEG_BOUND, _SQUARE, and
                _POS_BOUND to calculate the width of the current square.
        """

        # check each box
        for i in range(n):
            for j in range(n):

                # Ex. if Square is 50:
                # if -100 + (50 * 0) <= x < -100 + (50 * (0 + 1))
                #               -100 <= x < -50
                # this checks if the x coordinate is in the box clicked on
                # from the left bound to the right bound
                if x <= self._NEG_BOUND + (self._SQUARE * (i + 1)) and \
                   x >= self._NEG_BOUND + (self._SQUARE * i):

                    new_y = i

                # y acts the same as x, just with Positive bound instead
                # of negative bound
                if y >= self._POS_BOUND - (self._SQUARE * (j + 1)) and \
                   y <= self._POS_BOUND - (self._SQUARE * j):

                    new_x = j

        if not test:
            self.take_turn(new_x, new_y)

        ###############
        # for testing #
        ###############
        return (new_x, new_y)

    def take_turn(self, row, col):
        """
            name: take_turn
            parameters: row -- an integer (the row of the tile)
                        col -- an integer (the column of the tile)
            returns: nothing
            does: checks if there are legal moves. If so, checks if
                the clicked box is a legal move. Then if it is, it
                draws a new tile there calls the function to flip
                tiles.
        """

        # check if the box clicked is a legal move
        if len(self._legalmoves) > 0:
            if (row, col) in self._legalmoves:

                # if so, draw a tile in the box.
                graphics.draw_new_tile(self, row, col)

                # get list of flippable tiles
                tile_list = self._legalmoves[(row, col)]

                # flip the tile
                graphics.flip_tile(self, tile_list)

                # set the clicked tile's color,
                # increment the turn counter
                # and re-check legal moves
                self._board[(row, col)].set_color(self.check_turn())
                self._turn_counter += 1
                self._legalmoves = self.get_legal_moves()

                ai.ai_take_turn(self)

        # if there are no legal moves, skip turn
        else:
            self._turn_counter += 1
            self._legalmoves = self.get_legal_moves()
            ai.ai_take_turn(self)


        self.check_endgame()

    def check_turn(self):
        """
            name: check_turn
            input: none
            returns: "black" or "white" (strings)
            does: checks if the turn counter is even
                or odd. If even, black's turn. If
                odd, white's turn. Also increments
                the number of pieces respectively.
        """

        # will be black's turn on even turns
        # white on odd turns
        if self._turn_counter % 2 == 0:
            return "black"

        else:
            return "white"

    def gen_tile_list(self, lst_choice = "black"):
        """
            name: gen_tile_list
            parameters: lst_choice -- a color string ("white", "black",
                                                or "Forest Green")
            returns: either a list (if flow is False and
                    denoted by the parameter color)
                    or nothing
            does: generates lists of boxes where the white tiles
                and black tiles are. If flow is set to True, will
                call functions that then check for move legality.
                If flow is set to False, will return a list of
                white tiles, black tiles, or green (free) tiles.
        """
        # these will be the list of white
        # black, and empty tiles
        white_lst = []
        black_lst = []
        green_lst = []

        # iterate through the entire board.
        for row in range(self._n):
            for col in range(self._n):

                # check the color of that tile
                # and append to the appropriate list
                color = self._board[(row, col)]._color

                if color == "white":
                    white_lst.append((row, col))

                elif color == "black":
                    black_lst.append((row, col))

                else:
                    green_lst.append((row, col))

        # use parameter lst_choice to return
        # the appropriate list of tiles
        if lst_choice == "black":
            return black_lst

        elif lst_choice == "white":
            return white_lst

        else:
            return green_lst

    def get_legal_moves(self, flow = True, tile_list = []):
        """
            name: get_legal_moves
            parameters: tile_list -- a list of tuples where each tuple
                                    is a (row, col) pair on the board

                        flow -- True or False. Defaults to True for the game
                                to run. This is used in testing so the
                                method can be run by itself

            returns: a dictionary that contains the legal moves available
                    for a specific tile.
        """

        # flow used for testing purposes.
        # flow is True in game loop. This code bloack
        # will check whose turn it is and get a list
        # of tiles of that turn's color.
        if flow:
            turn = self.check_turn()
            if turn == "white":
                tile_list = self.gen_tile_list("white")

            elif turn == "black":
                tile_list = self.gen_tile_list("black")

        # initiate a dictionary to hold all viable moves.
        # the keys are the boxes where a move is viable
        # and the value is a list of tile objects that
        # will be flipped if the box (its key) is clicked
        viable_moves = {}

        # iterate through each tile on the board
        # based on whose turn it is. From here on assume
        # it's White's turn
        for item in tile_list:

            # the white tile in question
            center_tile = self._board[item]
            center_color = self._board[item]._color

            if center_color == "white":
                opposite_color = "black"

            elif center_color == "black":
                opposite_color = "white"

            # call a helper function to check spaces
            # around the tile in question
            viable_moves = self.check_outer_tiles(item, center_color,
                                                opposite_color, viable_moves)

        return viable_moves



    def check_outer_tiles(self, box, center_color, opposite_color,
                                                            viable_moves):
        """
            name: check_outer_tiles
            parameters: box -- the box the tile, that you want to check
                                if it has a legal move, resides in
                        center_color -- a string. The color of the tile
                                        in "box"
                        opposite_color -- a string. The opposite color
                                            of center_color
                        viable_moves -- a dictionary that will be built
                                        as a result of this method
            returns: a modified (or unmodified) viable_moves dictionary.
            does: searches the tiles around a single tile to look for
                a tile of the opposite color. If it finds one, it calls
                count_flippable_tiles to help build viable_moves. If not,
                it merely returns nothing (leaving an empty dictionary)
        """

        # search the 8 tiles around the tile
        # you want to check legal moves for.
        for row in range(box[0] - 1, box[0] + 2):
            for col in range(box[1] - 1, box[1] + 2):

                # if you've reached past the board border,
                # check the next box
                if row > self._n - 1 or row < 0:
                    continue

                elif col > self._n - 1 or col < 0:
                    continue

                # get the tile object and its color
                outer_tile = self._board[(row, col)]
                outer_color = self._board[(row, col)]._color

                # If the color is the opposite (flippable)
                # call count_flippable_tiles to check if it can be flipped
                # and how many.
                if outer_color == opposite_color:
                    data = self.count_flippable_tiles(self._board[box],
                                                self._board[(row, col)])

                    # if the result of count_flippable_tiles is an empty
                    # list, there are no viable moves
                    if not data:
                        continue

                    # if there are legal moves,
                    # check if that tile has already been added
                    # to legal moves. If so, merge their lists of
                    # flippable tiles (data[1])
                    elif data[0] in viable_moves:
                        tiles = data[1] + viable_moves[data[0]]
                        viable_moves[data[0]] = tiles

                    else:
                        viable_moves[data[0]] = data[1]

        # once viable moves has been built,
        # return it
        return viable_moves


    def count_flippable_tiles(self, center_tile, outer_tile):
        """
            name: count_flippable_tiles
            parameters: center_tile -- a tile object that represents
                                        the tile from which we expand
                                        to check if there's a legal move
                        outer_tile -- the tile in one of the boxes surrounding
                                        the center tile
            returns: a list -- index 0 is the box of the legal move
                                index 1 is the list of tiles it will flip
            does: starting from the outer tile, counts until it either finds
                a tile of the same color, opposite color, or an empty space.
                If it finds an empty space, returns a list of the box and
                the list of tiles it'll flip. If it finds a tile of the same
                color, it just returns nothing. If it finds a tile of the
                opposite color, it continues down the line.
        """

        # get row and column for the center tile (tile in question)
        # and the tile in the outer ring
        center_row = center_tile.get_pos()[0]
        center_col = center_tile.get_pos()[1]
        outer_row = outer_tile.get_pos()[0]
        outer_col = outer_tile.get_pos()[1]

        # find the row/col increment by subtracting.
        # this allows you to search along the correct line
        row_increment = outer_row - center_row
        col_increment = outer_col - center_col

        # set the current tile and its color
        current_tile = self._board[(outer_row, outer_col)]
        current_color = current_tile.get_color()

        # since this function was called,
        # we know outer_tile is of the opposite color
        flippable_tiles = [outer_tile]

        current_row = current_tile.get_pos()[0]
        current_col = current_tile.get_pos()[1]

        while True:
            # get the next tile in line by incrementing
            # the row and column
            next_pos = (current_row + row_increment,
                        current_col + col_increment)

            # check if reached end of board
            if next_pos not in self._board:
                return []

            # if not, get tile and its color
            next_tile = self._board[next_pos]
            next_color = next_tile.get_color()

            # if its color is the same as the current color
            # append the tile to flippable_tiles and
            # change current_row/col. We want to keep
            # moving down the line until we reach the same
            # color as the center tile, or an empty tile
            if next_color == current_color:
                flippable_tiles.append(next_tile)
                current_row = next_pos[0]
                current_col = next_pos[1]

            # if we've reached the same color as the tile
            # we were checking legal moves for, return
            elif next_color == center_tile.get_color():
                return []

            # if we've reached an empty space, success!
            # we've found a legal move. Return the empty
            # space's position and the tiles it will flip.
            elif next_color == "forest green":
                return [next_pos, flippable_tiles]

            else:
                return []



    def alter_tile_count(self, flip = True):
        """
            name: alter_tile_count
            parameters: flip -- True or False. An optional parameter
                                that will decide whether to subtract
                                the opposite color's tiles too.
                                (This is so the same method can be
                                used for drawing a new tile as well
                                as flipping.)
            returns: nothing
            does: alters the _num_white or _num_black attribute
                based on whether flip is True or False. Flip will
                be True when you want to take into account flipped tiles,
                and False when you don't.
        """

        turn = self.check_turn()

        if turn == "white":
            self._num_white += 1

            if flip:
                self._num_black -= 1

        elif turn == "black":
            self._num_black += 1

            if flip:
                self._num_white -= 1


    def get_winner(self):
        """
            name: get_winner
            input: none
            returns: a string detailing who won
            does: checks if black has more tiles than
                white, vice versa, or if there was a tie
                and returns a string saying as much.
        """

        if self._num_black > self._num_white:
            return "Black Wins!"

        elif self._num_black < self._num_white:
            return "White Wins!"

        else:
            return "Tie game"

    def check_endgame(self, test = False):
        """
            name: check_endgame
            input: none
            returns: nothing
            does: checks if the total number of tiles
                is equal to the number of boxes on the
                board.
        """

        # for an 8x8 board:
        # if white tiles + black tiles = 64
        if self._num_black + self._num_white == self._n ** 2:

            if test:
                return "All tiles placed"

            graphics.draw_winner(self)

        # if there are no legal moves for the next player
        elif len(self._legalmoves) == 0:

            if test:
                return "No legal moves"

            # change turn and check for legal moves
            self._turn_counter += 1
            self._legalmoves = self.get_legal_moves()

            # if still no legal moves, end game
            if len(self._legalmoves) == 0:
                graphics.draw_winner(self)

            # otherwise, check for AI turn
            else:
                ai.ai_take_turn(self)


    def get_winner_score(self):
        """
            name: get_winner_score
            parameters: none
            returns: nothing
            does: prompts the user for their name and records
                their name and score in a scores file.
        """

        user = turtle.textinput("Game Over!", "Enter your name")
        while user == None:
            user = turtle.textinput("Error", "Sorry, please enter a name")
        score = self._num_black

        # if it's a high score, write a high score
        # if not, write a low score
        if self.check_high_score(self._num_black, "scores.txt"):
            if not self.write_high_score(user, score, "scores.txt"):
                print("Sorry, we couldn't record your score at this point")

        else:
            if not self.write_low_score(user, score, "scores.txt"):
                print("Sorry, we couldn't record your score at this point")

    def check_bounds(row, col):
        """
            name: check_bounds
            parameters: row -- an int (the row of the tile)
                        col -- an int (the column of the tile)
            returns: True or False
            does: True if (row, col) in range 0 -> (n - 1)
                    False otherwise
        """

        if row >= 0 and row < self._n:
            if col >= 0 and col < self._n:
                return True

        return False

    def ask_game_mode(self):
        """
            name: ask_game_mode
            parameters: none
            returns: True or False
            does: Prompts the user if they want to play against human
                or AI. If they input human, returns False,
                AI returns True
        """

        # prompts the user for their choice
        choice = turtle.textinput("Game Mode",
                                    "Play against a Human or AI?")

        # tries to make it lowercase
        # if it can't (because they've clicked cancel)
        # default to ai
        try:
            choice = choice.lower()

        except AttributeError:
            choice = "ai"

        # prompt again if not a valid input
        while choice not in ("human", "ai"):
            error_text = "Sorry, not a valid option. Please input Human or AI"
            choice = turtle.textinput("Game Mode", error_text)
            choice = choice.lower()

        if choice == "human":
            return False

        elif choice == "ai":
            return True

    def read_scores(self, filename):
        '''
            name: read_scores
            parameters: filename -- a string
            returns: a list
            does: reads the file and generates a list of the following structure:
                [['Name'], [Score].....['Name'], [Score]]. Name is a string
                and Score is an int. If the file can't be found, returns
                an empty list.
        '''

        try:
            # open the file and process the file
            infile = open(filename, 'r')
            all_lines = infile.read()
            lines = all_lines.splitlines()

            # create the list to store the data
            scores = []

            # for each item in lines (a line is like 'Name Score'
            # or 'Firstname Lastname Score')...
            # split from the right-most space
            for item in lines:
                if lines != '':
                    temp_list = item.rsplit(' ', 1)

                    # create a temporary list with the structure ['Name', 'Score']
                    # or ['First Name', 'Score']
                    scores.append(temp_list[0])
                    scores.append(temp_list[1])
            infile.close()
            return scores

        except OSError:
            return []

    def check_high_score(self, score, filename):
        '''
            name: check_high_score
            parameters: score -- an int
                        filename -- a string
            returns: True or False
            does: checks if the player's score is a high score.
                If read_scores comes back with an empty list, it is considered
                a high score and the function returns True. Otherwise if
                the score is higher than the current high score, returns True.
                Otherwise, return False
        '''

        scores = self.read_scores(filename)

        if not scores:
            return True

        elif score >= int(scores[1]):
            return True

        return False

    def write_high_score(self, user, score, filename):
        '''
            name: write_high_score
            parameters: user -- a string (the player's name)
                        score -- an int (the player's number of wins)
                        filename -- a string (the scores filename)
            returns: nothing
            does: Writes a high score to the filename. If read_scores returns
                an empty list, it merely writes the high score and closes the
                file. If scores has a length > 0, it writes the rest of the
                scores to the file.
        '''

        scores = self.read_scores(filename)
        index = 0

        try:
            outfile = open(filename, 'w')
            outfile.write(user + ' ' + str(score) + '\n')
            if len(scores) > 0:

                # we iterate through scores by 2 (name and score)
                # and write the name + score to the file.
                while index < len(scores):
                    outfile.write(scores[index] + ' ' + scores[index + 1] + '\n')
                    index += 2

            outfile.close()
            return True

        except OSError:
            return False

    def write_low_score(self, user, score, filename):
        '''
            name: write_low_score
            parameters: user -- a string (the player's name)
                        score -- an int (the number of wins)
                        filename -- a string (the scores file)
            returns: nothing
            does: writes the user and their score to the file
        '''

        try:
            outfile = open(filename, 'a')
            outfile.write(user + ' ' + str(score) + '\n')
            outfile.close()
            return True

        except OSError:
            return False


    def __eq__(self, other):
        """
            name: __eq__
            input: an object of type board
            returns: True or False
            does: checks if the board's size and box size are
                    the same
        """

        return self._n == other._n and self._SQUARE == other._SQUARE

    def __str__(self):
        """
            name: __str__
            input: none
            returns: a string
            does: reports the board size, square size,
                positive bound, negative bound, number of
                black and white tiles, and how many turns
                have passed
        """


        printable_1 = "Board Size: " + str(self._n) + " x " + \
                        str(self._n) + "\n"

        printable_2 = "Square Size: " + str(self._SQUARE) + "\n"

        printable_3 = "Positive Bound: " + str(self._POS_BOUND) + "\n"

        printable_4 = "Negative Bound: " + str(self._NEG_BOUND) + "\n"

        printable_5 = "Number of black tiles: " + str(self._num_black) + "\n"

        printable_6 = "Number of white tiles: " + str(self._num_white) + "\n"

        printable_7 = "Number of turns: " + str(self._turn_counter) + "\n"

        printable = printable_1 + printable_2 + printable_3 + printable_4 + \
                    printable_5 + printable_6 + printable_7

        return printable
