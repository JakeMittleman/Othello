"""
    CS5001
    Fall 2018
    Jake Mittleman
    HW 6
"""
class Tile:

    def __init__(self, box_pos, color):
        """
            -- Constructor (Tile class) --
        - _box_pos set to input value
        - _played defaults to False
        """

        self._box_pos = box_pos
        self._color = color
        self._played = False

    def set_color(self, color):
        """
            name: set_color
            input: color -- a string
            returns: nothing
            does: sets the tile's color to the input color
        """

        self._color = color

    def mark_played(self):
        """
            name: mark_played
            input: none
            returns: nothing
            does: marks the current tile as played
        """

        self._played = True

    def check_valid_move(self, x, y):
        """
            name: check_valid_move
            input: x -- an int that signifies a row
                    y -- an int that signifies a column
            returns: True or False
            does: checks if the piece at the current
                box location has not been played. If so,
                return True. If not, return False
        """


        if not self._played:
            return True

        else:
            print("Sorry, that's not a valid move")
            return False

    def get_pos(self):

        return self._box_pos

    def get_color(self):

        return self._color

    def __str__(self):
        """
            name: __str__
            input: none
            returns: a string
            does: prints the position of the tile
                and whether it's been played
        """

        printable = "\nTile at: " + str(self._box_pos) + "\nWith color: " + \
                    str(self._color) + "\nBeen played?: " + str(self._played)

        return printable
