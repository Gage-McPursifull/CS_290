# Gage McPursifull
# 6/3/2020
# This program creates a class named GessGame which simulates playing the game Gess. The class has a number of
# methods, but a user only need call make_move, get_game_board, get_game_state, get_player_turn, and resign_game.


class GessGame:
    """This class represents the game Gess. There are methods to make a move, get game board, get game state and
    resign the game."""

    def __init__(self):
        """Initializes GessGame with the following starting conditions."""

        # The game board. Abbreviated _b so that each row could fit on a line perfectly.
        # I know that variable names are supposed to be descriptive, but this decision was made for readability.
        self._b = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', 'W', ' ', 'W', ' ', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', ' ', 'W', ' ', 'W', ' ', ' '],
                   [' ', 'W', 'W', 'W', ' ', 'W', ' ', 'W', 'W', 'W', 'W', ' ', 'W', ' ', 'W', ' ', 'W', 'W', 'W', ' '],
                   [' ', ' ', 'W', ' ', 'W', ' ', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', ' ', 'W', ' ', 'W', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', 'W', ' ', ' ', 'W', ' ', ' ', 'W', ' ', ' ', 'W', ' ', ' ', 'W', ' ', ' ', 'W', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', 'B', ' ', ' ', 'B', ' ', ' ', 'B', ' ', ' ', 'B', ' ', ' ', 'B', ' ', ' ', 'B', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', 'B', ' ', 'B', ' ', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', ' ', 'B', ' ', 'B', ' ', ' '],
                   [' ', 'B', 'B', 'B', ' ', 'B', ' ', 'B', 'B', 'B', 'B', ' ', 'B', ' ', 'B', ' ', 'B', 'B', 'B', ' '],
                   [' ', ' ', 'B', ' ', 'B', ' ', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', ' ', 'B', ' ', 'B', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   ]
        self._game_state = "UNFINISHED"
        self._player_turn = "B"             # B for black, W for white. Black starts the game.

    def get_game_board(self):
        """Returns self._b"""
        row = 0

        while row < 20:
            print(self._b[row])
            row += 1

    def get_player_turn(self):
        """Returns player turn. B for Black, W for white."""

        return self._player_turn

    def get_game_state(self):
        """Returns self._game_state."""

        return self._game_state

    def change_player_turn(self):
        """Changes player turn from B to W or from W to B."""

        if self._player_turn == 'B':
            self._player_turn = 'W'
        else:
            self._player_turn = 'B'

    def resign_game(self):
        """The current player resigns the game."""

        if self._player_turn == 'W':
            self._game_state = 'BLACK_WON'
        else:
            self._game_state = "WHITE_WON"

    def save_board(self):
        """Saves the board in its current state.
        Called by make_move in order to reset the move in the case that a player tries to destroy their ring."""

        board = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
        for row in range(0, 20):
            for col in range(0, 20):
                board[row].append(self._b[row][col])

        return board

    def piece_contents(self, row_from, col_from):
        """Creates and returns a list of the contents of the piece to be moved. Element 0 is the north west space, then
        move clockwise until element 7 which is the west space. Element 8 is the center space.
        Called by: update_board, check_rings, check_piece, check_direction."""

        contents = [self._b[row_from - 1][col_from - 1], self._b[row_from - 1][col_from],
                    self._b[row_from - 1][col_from + 1], self._b[row_from][col_from + 1],
                    self._b[row_from + 1][col_from + 1], self._b[row_from + 1][col_from],
                    self._b[row_from + 1][col_from - 1], self._b[row_from][col_from - 1], self._b[row_from][col_from]]

        return contents

    def update_board(self, row_from, col_from, row_to, col_to):
        """After a legal move is made, the contents of the piece referred to by move_to are replaced by the contents
        of the piece referred to by move_from. The contents of the move_from piece are then cleared.
        All border spaces are also cleared.
        Called by: make_move
        Calls: piece_contents"""

        from_contents = self.piece_contents(row_from, col_from)

        # Replace contents of move_from piece
        self._b[row_from - 1][col_from - 1] = ' '
        self._b[row_from - 1][col_from] = ' '
        self._b[row_from - 1][col_from + 1] = ' '
        self._b[row_from][col_from + 1] = ' '
        self._b[row_from + 1][col_from + 1] = ' '
        self._b[row_from + 1][col_from] = ' '
        self._b[row_from + 1][col_from - 1] = ' '
        self._b[row_from][col_from - 1] = ' '
        self._b[row_from][col_from] = ' '

        # Replace contents of move_to piece
        self._b[row_to - 1][col_to - 1] = from_contents[0]
        self._b[row_to - 1][col_to] = from_contents[1]
        self._b[row_to - 1][col_to + 1] = from_contents[2]
        self._b[row_to][col_to + 1] = from_contents[3]
        self._b[row_to + 1][col_to + 1] = from_contents[4]
        self._b[row_to + 1][col_to] = from_contents[5]
        self._b[row_to + 1][col_to - 1] = from_contents[6]
        self._b[row_to][col_to - 1] = from_contents[7]
        self._b[row_to][col_to] = from_contents[8]

        # Clear the border
        for n in range(0, 20):
            self._b[0][n] = ' '
            self._b[19][n] = ' '
            self._b[n][0] = ' '
            self._b[n][19] = ' '

    def check_rings(self):
        """After an otherwise legal move, this method checks to see if the turn player still has rings.
        Called by: make_move
        Calls: get_player_turn, piece_contents"""

        player = self.get_player_turn()
        ring = [player, player, player, player, player, player, player, player, ' ']

        for row in range(1, 19):
            for col in range(1, 19):
                contents = self.piece_contents(row, col)
                if contents == ring:
                    return True

        return False

    def check_piece(self, row_from, col_from):
        """Checks the piece to be moved for color of stones. If it contains stones of opposing player, return False.
        Called by: make_move
        Calls: piece_contents, change_player_turn"""

        # Call piece contents to get a list of the contents of the piece to be moved
        contents = self.piece_contents(row_from, col_from)

        # Change to opposing player's turn. This is just for the duration of this method.
        self.change_player_turn()

        # If opposing player's stones in piece, the move is illegal, so return False and change turn to current player.
        if self._player_turn in contents:
            self.change_player_turn()
            return False

        # If move is legal, change turn to current player.
        self.change_player_turn()

    def check_distance(self, row_from, col_from, row_to, col_to):
        """Checks to see if the attempted move distance is allowed. Up to 3 spaces. If there is a stone in the center of
        the piece it may move any number of spaces. If not allowed, False is returned.
        Called by: make_move"""

        row_distance = abs(row_from - row_to)
        col_distance = abs(col_from - col_to)

        if (row_distance > 3 or col_distance > 3) and self._b[row_from][col_from] == ' ':
            return False

    def check_direction(self, row_from, col_from, row_to, col_to):
        """Checks to see if move is in a legal direction, e.g. diagonal or straight in a direction allowed by the
        piece's configuration. If not diagonal or straight, False is returned.
        Called by: make_move
        Calls: piece_contents"""

        # Checks that the attempted move is diagonal or straight. If not, return False.
        if abs(col_from - col_to) != abs(row_from - row_to) and (col_from - col_to != 0) and (row_from - row_to != 0):
            return False

        contents = self.piece_contents(row_from, col_from)

        # For an attempted diagonal move check to see if there is a stone in the corresponding space of the piece.
        # If not, the move is illegal, so return False.
        # Note: It doesn't matter if the space contains B or W, check piece is called before this method, which
        # will have already sorted out whether the piece contains the appropriate colored stones.
        if abs(col_from - col_to) == abs(row_from - row_to):
            if row_to < row_from and col_to < col_from and contents[0] == ' ':
                return False
            if row_to < row_from and col_to > col_from and contents[2] == ' ':
                return False
            if row_to > row_from and col_to > col_from and contents[4] == ' ':
                return False
            if row_to > row_from and col_to < col_from and contents[6] == ' ':
                return False

        # For an attempted straight move check to see if there is a stone in the corresponding space of the piece.
        # If not, the move is illegal, so return False.
        else:
            if row_to < row_from and contents[1] == ' ':
                return False
            if col_to > col_from and contents[3] == ' ':
                return False
            if row_to > row_from and contents[5] == ' ':
                return False
            if col_to < col_from and contents[7] == ' ':
                return False

    def check_adjacent(self, row, column, changed, direction):
        """After a row or column has been changed in check_move, check_adjacent looks to see if the adjacent row or
        column is empty. Returns True if empty, returns False otherwise. Changed contains 'Row' or 'Column'
        depending on which attributed was just updated. Direction contains +1 if updated in positive direction
        or -1 if updated in negative direction.
        Called by: check_overlap"""

        adjacent_list = []

        # If the Row number was just changed, adjacent list will contain the elements of self._b that are directly
        # adjacent to the new position.
        if changed == "Row":
            adjacent_list.append(self._b[row + direction][column - 1])
            adjacent_list.append(self._b[row + direction][column])
            adjacent_list.append(self._b[row + direction][column + 1])

        # If the Column number was just changed, adjacent list will contain the elements of self._b that are directly
        # adjacent to the new position.
        elif changed == "Column":
            adjacent_list.append(self._b[row - 1][column + direction])
            adjacent_list.append(self._b[row][column + direction])
            adjacent_list.append(self._b[row + 1][column + direction])

        if 'B' in adjacent_list or 'W' in adjacent_list:
            return False
        else:
            return True

    def check_boundary(self, row_to, col_to):
        """Checks to see if the destination is on the outer edge of the board. If so, return False.
        Called by: make_move"""

        if row_to == 0 or row_to == 19 or col_to == 0 or col_to == 19:
            return False

    def check_overlap(self, row_from, col_from, row_to, col_to):
        """Checks the attempted move one space at a time. If the move would have a piece keep moving after its footprint
        overlaps some stones, False is returned.
        Called by: make_move
        Calls: check_adjacent, check_overlap"""

        if (col_from - col_to == 0) and (row_from - row_to == 0):
            return True

        # If we haven't reached our destination, move one step closer to it.
        else:

            if col_from < col_to:
                col_from += 1
                # Call check_adjacent to see what the next column contains.
                # If it isn't empty, check to see if we have moved as far as we want to.
                # If not, it is an illegal move, so return False.
                if self.check_adjacent(row_from, col_from, 'Column', 1) is False:
                    if col_from - col_to != 0:
                        return False

            elif col_from > col_to:
                col_from -= 1
                if self.check_adjacent(row_from, col_from, 'Column', -1) is False:
                    if col_from - col_to != 0:
                        return False

            if row_from < row_to:
                row_from += 1
                if self.check_adjacent(row_from, col_from, 'Row', 1) is False:
                    if row_from - row_to != 0:
                        return False

            elif row_from > row_to:
                row_from -= 1
                if self.check_adjacent(row_from, col_from, 'Row', -1) is False:
                    if row_from - row_to != 0:
                        return False

            # Call check move again with updated row_from and col_from.
            return self.check_overlap(row_from, col_from, row_to, col_to)

    def convert_column_and_row(self, move):
        """Translates the move_from and move_to input strings into row and column numbers that make
        sense for the board.
        Called by: make_move"""

        # Convert the letter in move_from into a column number. a = 0, b = 1, c = 2, ...
        coordinates = []
        col = -1
        letter_from = move[0]
        alphabet = 'abcdefghijklmnopqrst'
        for n in alphabet:
            col += 1
            if letter_from == n:
                break

        # Convert the number of move_from to the appropriate row number. E.g. 20 = 0, 19 = 1, 18 = 2, ...
        row = (-int(move[1:])) % 20

        coordinates.append(row)
        coordinates.append(col)

        return coordinates

    def make_move(self, move_from, move_to):
        """Allows the current player to make a move. If the game is already finished, 'The game is over.' is printed.
        Otherwise this method calls check_direction, check_distance, check_move
        before making a move to see if it is legal."""

        if self.get_game_state() != 'UNFINISHED':
            return False

        else:

            # Call convert_column_and_row to get usable column and row coordinates from move_from and move_to.
            row_from = self.convert_column_and_row(move_from)[0]
            col_from = self.convert_column_and_row(move_from)[1]
            row_to = self.convert_column_and_row(move_to)[0]
            col_to = self.convert_column_and_row(move_to)[1]

            # Check to see if the piece to be moved contains opposing player's stones. If so, return False
            if self.check_piece(row_from, col_from) is False:
                return False

            # Check that the move is allowed by the configuration of the stones. If not, return False.
            if self.check_direction(row_from, col_from, row_to, col_to) is False:
                return False

            # Check that the distance to be moved is allowed based on whether the piece contains a center stone.
            # If not, return False
            if self.check_distance(row_from, col_from, row_to, col_to) is False:
                return False

            # Check if the piece will be moved so that the center is on the border. If so, return False.
            if self.check_boundary(row_to, col_to) is False:
                return False

            # Check to see if the attempted move will move past the allowed number of pieces. Returns False if so.
            if self.check_overlap(row_from, col_from, row_to, col_to) is False:
                return False

            # Save board state, then update it.
            board = self.save_board()
            self.update_board(row_from, col_from, row_to, col_to)

            # If the move has destroyed the player's last ring, it is illegal, so revert the board to its state
            # before the move was made, then return False.
            if self.check_rings() is False:
                self._b = board
                return False

            # At this point the move will have to be legal, so the turn is given to the opposing player.
            self.change_player_turn()

            # Check turn player's rings. If there are none, the game goes to the opposing player (their move caused
            # the turn player to have no more rings).
            if self.check_rings() is False:
                if self._player_turn == 'W':
                    self._game_state = 'BLACK_WON'
                else:
                    self._game_state = "WHITE_WON"

            return True
