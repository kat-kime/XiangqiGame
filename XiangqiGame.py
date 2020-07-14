# Name:                             Kat Kime
# Date:                             3/2/2020
# Description:                      Program that facilitates the execution of a Xiangqi (Chinese Chess) game.


class NoPlayerError(Exception):
    pass


class NonexistentPlayerError(Exception):
    pass


class NoPositionError(Exception):
    pass


class XiangqiGame:
    """
    Facilitates the execution of a Xiangqi (Chinese Chess) game.
    """
    def __init__(self):
        """
        Constructor of Xiangqi objects.
        """
        self._board = GameBoard()
        self._game_state = "UNFINISHED"
        self._current_player = "red"

    def make_move(self, start, end):
        """
        Function that moves a chess piece from one position to another.
        :param start: current piece's starting position
        :param end: current piece's intended end position
        :return: true if the move is executed, false if otherwise
        """
        # first, check game state
        if self._game_state == "RED_WON" or self._game_state == "BLACK_WON":
            return False

        # next, pass moves to the game board
        result = self._board.make_move(start, end, self._current_player)

        # check if red won
        # if red won, change state
        if self.red_won():
            self._game_state = "RED_WON"

        # check if black won
        # if black won, change state
        elif self.black_won():
            self._game_state = "BLACK_WON"

        if self._current_player == "red":
            self._current_player == "black"

        else:
            self._current_player == "red"
        # return the result
        return result

    def red_won(self):
        """
        Determines if red player won game.
        :return: True if red player won, False if otherwise
        """
        # red wins if black is in check and black general's legal moves are no good

        # is the black general in check?
        if self.is_in_check("black"):
            # are the black general's moves good?
            if self.has_available_moves("black"):
                return False

            # if no available moves, return True
            else:
                return True

        else:
            return False

    def black_won(self):
        """
        Determines if black player won game.
        :return: True if black player won, False if otherwise
        """
        # black wins if red is in check and red general's legal moves are no good

        # is the red general in check?
        if self.is_in_check("red"):
            # are the red general's moves good?
            if self.has_available_moves("red"):
                return False

            # if no available moves, return True
            else:
                return True

        else:
            return False

    def has_available_moves(self, player):
        """
        Determines if player has available moves.
        :param player: user-defined player
        :return: True if has available moves, False if otherwise
        """
        return self._board.has_available_moves(player)

    def get_game_state(self):
        """
        Returns the game state of the xiangqi game.
        :return: game state of the xiangqi game.
        """
        return self._game_state

    def set_game_state(self, game_state):
        """
        Sets the game state of the xiangqi game.
        :param game_state: user-defined game state
        """
        self._game_state = game_state

    def is_in_check(self, player):
        """
        Determines if the general of the user-defined player is in check.
        :param player: user-defined player
        :return: True if the player's general is in check, False if otherwise
        """
        # grab the board
        board = self._board

        # ask board if general is in check
        result = board.in_check(player.lower())

        # return the results
        return result

    def print_board(self):
        """
        Prints the current board.
        """
        self._board.print_board()


class GameBoard:
    """
    Oversees the xiangi game and facilitates interaction between game pieces.
    """

    def __init__(self):
        """
        Constructor of GameBoard objects.
        """
        self._board = [["R", "H", "E", "A", "G", "A", "E", "H", "R"],
                       ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
                       ["-", "C", "-", "-", "-", "-", "-", "C", "-"],
                       ["S", "-", "S", "-", "S", "-", "S", "-", "S"],
                       ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
                       ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
                       ["S", "-", "S", "-", "S", "-", "S", "-", "S"],
                       ["-", "C", "-", "-", "-", "-", "-", "C", "-"],
                       ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
                       ["R", "H", "E", "A", "G", "A", "E", "H", "R"]]

        self._min_x_coord = 0  # tracking the limits of the game board
        self._max_x_coord = 8
        self._min_y_coord = 0
        self._max_y_coord = 9

        # set the board
        self._pieces = []
        self._black_general = None
        self._red_general = None
        self.set_board()

    def has_available_moves(self, player):
        """
        Determines if player has available moves
        :param player: user-defined player
        :return: True if has available moves, False if otherwise
        """
        bad_moves = 0

        if player == "black":
            # grab dangerous pieces
            danger_pieces = []

            # iterate through all of the opposing team's pieces
            for red_piece in self._pieces:
                if red_piece.get_player() == "red":

                    # if the general is in piece's legal moves, add that piece to danger pieces
                    if self._black_general.get_position() in red_piece.get_legal_moves():
                        danger_pieces.append(red_piece)

                    else:
                        pass

            # examine all legal moves
            legal_positions = self._black_general.get_legal_moves()

            # iterate through legal moves
            for position in legal_positions:
                # if move is occupied or in danger piece's legal moves and danger piece not blocked
                if self.contains_a_piece(position):
                    bad_moves += 1

                else:
                    # now iterate through danger pieces
                    for danger_piece in danger_pieces:
                        # if position is in the danger piece's legal moves
                        if position in danger_piece.get_legal_moves():
                            # and if move is not blocked - increase bad moves
                            if not self.move_blocked(danger_piece, position):
                                bad_moves +=1

        elif player == "red":
            # grab dangerous pieces
            danger_pieces = []

            # iterate through all of the opposing team's pieces
            for black_piece in self._pieces:
                if black_piece.get_player() == "black":

                    # if the general is in piece's legal moves, add that piece to danger pieces
                    if self._red_general.get_position() in black_piece.get_legal_moves():
                        danger_pieces.append(black_piece)

                    else:
                        pass

            # examine all legal moves
            legal_positions = self._red_general.get_legal_moves()

            # iterate through legal moves
            for position in legal_positions:
                # if move is occupied or in danger piece's legal moves and danger piece not blocked
                if self.contains_a_piece(position):
                    bad_moves += 1

                else:
                    # now iterate through danger pieces
                    for danger_piece in danger_pieces:
                        # if position is in the danger piece's legal moves
                        if position in danger_piece.get_legal_moves():
                            # and if move is not blocked - increase bad moves
                            if not self.move_blocked(danger_piece, position):
                                bad_moves += 1

        if bad_moves < len(legal_positions):
            return True

        else:
            return False


    def in_check(self, player):
        """
        Determines if the general of the user-defined player is in check.
        :param player: user-defined player
        :return: True if the player's general is in check, False if otherwise
        """
        # if player is black, see if black general is in check
        if player == "black":
            result = self.is_in_check(self._black_general)

        # if player is red, see if red general is in check
        elif player == "red":
            result = self.is_in_check(self._red_general)

        return result

    def is_in_check(self, general):
        """
        Determines if general is in check. In check means general is in enemy's sights and NOT blocked.
        :param general: user-defined general
        :return: True if in check, False if otherwise
        """
        # if player is black
        if general.get_player() == "black":
            # iterate through all of red's pieces
            for piece in self._pieces:
                if piece.get_player() == "red":

                    # if this general's position is in this piece's legal moves
                    if general.get_position() in piece.get_legal_moves():

                        # and if the piece is NOT blocked, general is in check:
                        if not self.move_blocked(piece, general.get_position()):
                            return True

                        else:
                            return False

                    else:
                        return False

        # or if player is red
        elif general.get_player() == "red":

            # iterate through all of black's pieces
            for piece in self._pieces:
                if piece.get_player() == "black":

                    # if this general's position is in the piece's legal moves
                    if general.get_position() in piece.get_legal_moves():

                        # and if the piece is NOT blocked, general is in check
                        if not self.move_blocked(piece, general.get_position()):
                            return True

                        else:
                            return False

                    else:
                        return False

    def print_board(self):
        """
        Prints the current board.
        """
        for row in self._board:
            print(row)

    def make_move(self, start, end, player_turn):
        """
        Moves one piece from a starting board position to and end board position
        :param start: game piece's starting position
        :param end: game piece's proposed end position
        :param player_turn: which player is in turn
        :return: True if move has been executed, False if otherwise
        """
        # decipher the position code
        start_position = self.unwrap(start)
        end_position = self.unwrap(end)

        # get the piece at start position
        piece = self.get_piece(start_position)

        # if player matches
        if piece.get_player() != player_turn:
            return False

        # if no piece at start position, return false
        if piece is None:
            return False

        # determine if end position is even part of legal moves
        if end_position not in piece.get_legal_moves():
            return False

        # check if move is blocked
        if self.move_blocked(piece, end_position):
            return False

        # check to see if move creates flying generals
        if self.flying_generals(piece):
            return False

        # check to see if move is putting own general in check
        if self.ditching_general(piece, end_position):
            return False

        # if checks pass, make the move
        result = self.move_piece(piece, end_position)

        # return the result
        return result

    def move_piece(self, piece, end_position):
        """
        Moves piece in question to end_position and cleans up game board to reflect new state.
        :param piece: user-defined piece
        :param end_position: piece's end position
        :return: True if move is made, False if otherwise
        """
        # is a capture in play?
        if self.capture_in_play(piece, end_position):
            # can the piece capture?
            if self.can_capture(piece, end_position):
                # HANDLE CAPTURED PIECE #

                # remove captured piece from board's pieces
                captured_piece = self.get_piece(end_position)
                self._pieces.remove(captured_piece)

                # HANDLE NEW PIECE #
                # remove piece from the board
                self.remove_piece(piece)

                # add piece to new piece in board
                self.add_piece(piece, end_position)

                # change piece's position to end position
                piece.set_position(end_position)

            # if piece cannot capture, no move
            else:
                return False

        # if a capture is not in play, business as usual
        else:
            # remove piece from the board
            self.remove_piece(piece)

            # add piece to new piece in board
            self.add_piece(piece, end_position)

            # change piece's position to end position
            piece.set_position(end_position)

        return True

    def capture_in_play(self, piece, end_position):
        """
        Determines if piece's end_position is occupied by a piece
        :param piece: user-defined piece
        :param end_position: piece's proposed end position
        :return: True if end position is occupied, False if otherwise
        """
        # grab end position's coordinates
        end_row = end_position[0]
        end_column = end_position[1]

        # is the board position empty?
        if self._board[end_row][end_column] == "-":
            # if it is, no capture in play
            return False

        # if the board position is occupied, there may be a capture
        else:
            return True

    def can_capture(self, piece, end_position):
        """
        Determines if piece is able to capture an occupied position.
        :param piece: user-defined piece
        :param end_position: piece's proposed end position
        :return: True if can capture, False if otherwise
        """
        # grab piece at end position
        end_piece = self.get_piece(end_position)

        # are the two pieces from the same player?
        if piece.get_player() == end_piece.get_player():
            # if so, cannot capture
            return False

        else:
            # is the piece a cannon?
            if "cannon" in piece.get_type():
                # is it hopping over exactly one piece?
                if self.legal_cannon_capture(piece, end_position):
                    # if so, return true
                    return True

                # otherwise, return False
                else:
                    return False

            # if not, you can capture
            else:
                return True

    def legal_cannon_capture(self, piece, end_position):
        """
        Determines if the cannon can legally capture the piece at the end position.
        :param piece: user-defined cannon
        :param end_position: cannon's proposed end position
        :return: True if can capture, False if otherwise
        """
        count = 0
        # a cannon can capture a piece if there is exactly one piece between them

        # grab coordinates
        cannon_y = piece.get_position()[0]
        cannon_x = piece.get_position()[1]

        capture_y = end_position[0]
        capture_x = end_position[1]

        # are they on the same x-axis?
        if cannon_x == capture_x:

            # if so iterate through all positions between them
            for y in range(cannon_y +1, capture_y):
                position = [y, cannon_x]

                # if position contains a piece, increase count
                if self.contains_a_piece(position):
                    count += 1

            for y in range(capture_y + 1, cannon_y):
                position = [y, cannon_x]

                # if position contains a piece, increase count
                if self.contains_a_piece(position):
                    count += 1

        # are they on the same y-axis?
        elif cannon_y == capture_y:
            # if so iterate through all positions between them
            for x in range(cannon_x + 1, capture_x):
                position = [cannon_y, x]

                # if position contains a piece, increase count
                if self.contains_a_piece(position):
                    count += 1

            for x in range(capture_x + 1, cannon_x):
                position = [cannon_y, x]

                # if position contains a piece, increase count
                if self.contains_a_piece(position):
                    count += 1

        # is there exactly one piece between the two pieces?
        # if so, return true
        if count == 1:
            return True

        # otherwise, cannot capture
        else:
            return False

    def flying_generals(self, piece):
        """
        Checks to see if proposed move makes generals face each other
        :param piece: user-defined piece
        :return: True if the move creates flying general situation, False if otherwise
        """
        # find coordinates of generals
        black_gen_x = self._black_general.get_position()[1]
        black_gen_y = self._black_general.get_position()[0]

        red_gen_x = self._red_general.get_position()[1]
        red_gen_y = self._red_general.get_position()[0]

        # if x_coordinates of generals don't match, return False
        if black_gen_x != red_gen_x:
            return False

        else:
            # temporarily remove piece from board
            self.remove_piece(piece)

            # starting at black general, iterate through all in-between positions
            for y in range(black_gen_y +1, red_gen_y):
                position = [y, black_gen_x]

                # if position contains a piece, add piece back, then return False
                if self.contains_a_piece(position):
                    self.add_piece(piece, piece.get_position())
                    return False

        # if no opportunity to return false, then flying general situation
        # add piece back, then return true
        self.add_piece(piece, piece.get_position())
        return True

    def ditching_general(self, piece, end_position):
        """
        Checks to see if a piece's proposed move is putting or leaving a general in check
        :param piece: user-defined piece
        :param end_position: piece's proposed ending position
        :return: True if move jeopardizes general, false if otherwise
        """
        if piece.get_player() == "black":
            # is the general in check?
            if self.is_in_check(self._black_general):

                # if so, grab all of the dangerous pieces
                danger_pieces = []

                # iterate through all of the opposing team's pieces
                for red_piece in self._pieces:
                    if red_piece.get_player() == "red":

                        # if the general is in piece's legal moves, add that piece to danger pieces
                        if self._black_general.get_position() in red_piece.get_legal_moves():
                            danger_pieces.append(red_piece)

                        else:
                            pass

                # iterate through all of the dangerous pieces
                for danger_piece in danger_pieces:
                    blocked_positions = danger_piece.get_blocked_moves()

                    # if current piece's end position is in a dangerous piece's blocked position
                    # this means it is actively saving the general - return false
                    if end_position in blocked_positions:
                        return False

                    # otherwise, the piece is leaving the general in check, return true
                    else:
                        return True

            # if the general is not in check - check to see if there are dangerous pieces
            else:
                danger_pieces = []

                # iterate through all of the opposing team's pieces
                for game_piece in self._pieces:
                    if game_piece.get_player() == "red":

                        # if the general is in piece's legal moves, add that piece to danger pieces
                        if self._black_general.get_position() in game_piece.get_legal_moves():
                            danger_pieces.append(game_piece)

                        else:
                            pass

                # if no dangerous pieces, return False
                if len(danger_pieces) == 0:
                    return False

                # otherwise, if there are dangerous pieces, is current piece starting in a vital position?
                else:
                    for danger_piece in danger_pieces:
                        blocked_positions = danger_piece.get_blocked_moves()

                        # if piece's current position is in a dangerous piece's blocked moves, it's important
                        if piece.get_position() in blocked_positions:

                            # if end position is not in danger piece's blocked positions, it's ditching the general
                            if end_position not in blocked_positions:
                                return True

                            # otherwise, it's saving general
                            else:
                                return False

                        # otherwise, it's not vital to saving the general - not ditching
                        else:
                            return False

        elif piece.get_player() == "red":
            # is the general in check?
            if self.is_in_check(self._red_general):

                # if so, grab all of the dangerous pieces
                danger_pieces = []

                # grab all of the black pieces
                for black_piece in self._pieces:
                    if black_piece.get_player() == "black":

                        # if general is in piece's legal moves, add to dangerous pieces
                        if self._red_general.get_position() in black_piece.get_legal_moves():
                            danger_pieces.append(black_piece)

                        else:
                            pass

                # iterate through all of the dangerous pieces
                for danger_piece in danger_pieces:
                    blocked_positions = danger_piece.get_blocked_moves()

                    # if current piece's end position is in a dangerous piece's blocked position
                    # this means it is actively saving the general - return false
                    if end_position in blocked_positions:
                        return False

                    # otherwise, the piece is leaving the general in check, return true
                    else:
                        return True

            # if the general is not in check - check to see if there are dangerous pieces
            else:
                danger_pieces = []

                # iterate through all of the opposing team's pieces
                for game_piece in self._pieces:
                    if game_piece.get_player() == "black":

                        # if the general is in piece's legal moves, add that piece to danger pieces
                        if self._red_general.get_position() in game_piece.get_legal_moves():
                            danger_pieces.append(game_piece)

                        else:
                            pass

                # if no dangerous pieces, return False
                if len(danger_pieces) == 0:
                    return False

                # otherwise, if there are dangerous pieces, is current piece starting in a vital position?
                else:
                    for danger_piece in danger_pieces:
                        blocked_positions = danger_piece.get_blocked_moves()

                        # if piece's current position is in a dangerous piece's blocked moves, it's important
                        if piece.get_position() in blocked_positions:

                            # if end position is not in danger piece's blocked positions, it's ditching the general
                            if end_position not in blocked_positions:
                                return True

                            # otherwise, it's saving general
                            else:
                                return False

                        # otherwise, it's not vital to saving the general - not ditching
                        else:
                            return False

    def remove_piece(self, piece):
        """
        Removes a given piece from the board.
        :param piece: user-defined game piece
        """
        # get piece's board coordinates
        row = piece.get_position()[0]
        column = piece.get_position()[1]

        # replace piece's character with a dash
        self._board[row][column] = "-"

    def add_piece(self, piece, position):
        """
        Adds a piece back to the board
        :param piece: user-defined piece
        :param position: position piece should be added to
        """
        # get the board coordinates
        row = position[0]
        column = position[1]

        # find out the type of piece, then add it
        if "advisor" in piece.get_type():
            self._board[row][column] = "A"

        elif "chariot" in piece.get_type():
            self._board[row][column] = "R"

        elif "cannon" in piece.get_type():
            self._board[row][column] = "C"

        elif "elephant" in piece.get_type():
            self._board[row][column] = "E"

        elif "general" in piece.get_type():
            self._board[row][column] = "G"

        elif "horse" in piece.get_type():
            self._board[row][column] = "H"

        elif "soldier" in piece.get_type():
            self._board[row][column] = "S"

    def move_blocked(self, piece, end_position):
        """
        Determines if a proposed move is blocked by another piece.
        :param piece: piece to be moved
        :param end_position: piece's proposed end position
        :return: True if blocked, False if otherwise
        """
        # get blocked moves
        blocked_positions = piece.get_blocked_moves(end_position)

        # if a piece is in any of those blocked moves, return true
        for position in blocked_positions:
            # check to board to see if that position has a piece
            if self.contains_a_piece(position):
                return True

        # if no piece found, return false
        return False

    def set_board(self):
        """
        Sets the board with all game pieces pieces.
        """
        # creating index valuables
        row = 0

        # iterate through each row
        while row < self._max_y_coord + 1:
            column = 0

            # iterate through each item in the row
            while column < self._max_x_coord + 1:
                position = [row, column]

                # if the board position contains a piece, create it
                if self.contains_a_piece(position):
                    piece = self.create_piece(position)

                    if row < self._max_y_coord / 2:
                        piece.set_player("black")               # set the player of the piece
                        piece.set_position(position)
                        self._pieces.append(piece)

                        # keep track of the general
                        if piece.get_type() == "black general":
                            self._black_general = piece

                    elif row > self._max_y_coord / 2:
                        piece.set_player("red")                 # set the player of the piece
                        piece.set_position(position)
                        self._pieces.append(piece)

                        # keep track of the general
                        if piece.get_type() == "red general":
                            self._red_general = piece

                else:
                    pass

                column += 1

            row += 1

    def contains_a_piece(self, position):
        """
        Determines if a given position contains a game piece.
        :param position: coordinates of a position (in list format)
        :return: True if it contains a piece
        """
        # grab coordinates of a position
        row = position[0]
        column = position[1]

        # return true if position has piece
        if self._board[row][column] == "A":
            return True

        elif self._board[row][column] == "R":
            return True

        elif self._board[row][column] == "C":
            return True

        elif self._board[row][column] == "E":
            return True

        elif self._board[row][column] == "G":
            return True

        elif self._board[row][column] == "H":
            return True

        elif self._board[row][column] == "S":
            return True

        # otherwise, return false
        else:
            return False

    def create_piece(self, position):
        """
        Creates and returns a new piece, according to a user-defined position
        :param position: coordinates of a user-defined position
        :return: game piece
        """
        # grab coordinates of a position
        row = position[0]
        column = position[1]

        # return true if position has piece
        if self._board[row][column] == "A":
            temp = Advisor()
            return temp

        elif self._board[row][column] == "R":
            temp = Chariot()
            return temp

        elif self._board[row][column] == "C":
            temp = Cannon()
            return temp

        elif self._board[row][column] == "E":
            temp = Elephant()
            return temp

        elif self._board[row][column] == "G":
            temp = General()
            return temp

        elif self._board[row][column] == "H":
            temp = Horse()
            return temp

        elif self._board[row][column] == "S":
            temp = Soldier()
            return temp

        # otherwise, return false
        else:
            return None

    def unwrap(self, string):
        """
        Converts algebraic string into a board position
        :param string: user-defined string that represents a board position
        :return: list coordinates that represent a board position
        """
        # split string
        temp = list(string.lower())

        # flip characters and assign to coordinates
        if len(temp) == 3:
            row = 9
        else:
            row = int(temp[1]) - 1
        column = temp[0].lower()

        # translate y_coord into a number
        if column == "a":
            column = 0

        elif column == "b":
            column = 1

        elif column == "c":
            column = 2

        elif column == "d":
            column = 3

        elif column == "e":
            column = 4

        elif column == "f":
            column = 5

        elif column == "g":
            column = 6

        elif column == "i":
            column = 7

        # return board position
        return [row, column]

    def list_pieces(self):
        """
        Returns all the pieces that are currently in play
        :return: list of all pieces that are currently in play
        """
        return self._pieces

    def get_piece(self, position):
        """
        Returns piece at a specific location
        :param position: user-defined position
        :return: piece located at the position
        """
        # iterate through board pieces
        for piece in self.list_pieces():
            # if positions match, return that piece
            if piece.get_position() == position:
                return piece


class GamePiece:
    """
    Represents a game piece in a xiangqi game. Game pieces can make moves and determine if a set of moves are
    legal.
    """
    def __init__(self):
        """
        Constructor of GamePiece objects.
        """
        self._position = None
        self._player = None
        self._type = None

        self._min_x_coord = 0                                       # tracking the limits of the game board
        self._max_x_coord = 8
        self._min_y_coord = 0
        self._max_y_coord = 9

    def get_blocked_moves(self, end_position):
        """
        Returns all moves that will block a piece's move.
        :param end_position: piece's proposed end position
        :return: list of blocked positions
        """

    def get_type(self):
        """
        Returns the type and player of the piece
        :return: the type and player of the piece
        """
        return "" + self._player + " " + self._type

    def set_type(self, piece_type):
        """
        Sets the type of the piece
        :param piece_type: the type of the piece
        """
        self._type = piece_type

    def get_position(self):
        """
        Returns the position of a game piece.
        :return: the position of a game piece, in list coordinate format.
        """
        return self._position

    def set_position(self, position):
        """
        Sets the position of a game piece.
        :param position: Position of a game piece, in list coordinate format
        """
        if self._player is not None:
            if self.in_range(position):
                self._position = position

        else:
            raise NoPlayerError

    def get_player(self):
        """
        Returns the owner of the game piece
        :return: the owner of the game piece
        """
        return self._player

    def set_player(self, player):
        """
        Sets the owner of the game piece
        :param player: the owner of the game piece
        """
        if player.lower() == "black" or player.lower() == "red":
            self._player = player.lower()

        else:
            raise NonexistentPlayerError

    def get_legal_moves(self):
        """
        Returns a list of the game piece's legal moves, depending on its current position.
        :return: list of legal moves
        """

    def in_range(self, position):
        """
        Determines if the given coordinates are within the general's range
        :param position: proposed board position
        :return: True if in range, False if otherwise
        """
        # get coordinates
        x_coord = position[1]
        y_coord = position[0]

        # if coordinates are outside of board max, the position is out of range
        if x_coord < self._min_x_coord:
            return False

        elif x_coord > self._max_x_coord:
            return False

        elif y_coord < self._min_y_coord:
            return False

        elif y_coord > self._max_y_coord:
            return False

        else:
            return True


class Chariot(GamePiece):
    """
    Represents a chariot game piece. Subclass of GamePiece.
    """

    def __init__(self):
        """
        Constructor of Chariot objects.
        """
        super().__init__()
        self.set_type("chariot")

    def get_legal_moves(self):
        """
        Implements the GamePiece declaration of the get_legal_moves function.
        :return: list of legal moves
        """
        # INITIALIZE INDEX VARIABLES #
        legal_moves = []

        try:
            current_y = self._position[0]
            current_x = self._position[1]

            # POPULATE LIST #
            # chariot's legal moves are:
            #   all x_coord + current y_coord (except current position)
            #   all y_coord + x_coord (except current position)

            # start with adding x coordinate values
            for x in range(self._min_x_coord, current_x):
                # add all x_coord with current y_coord
                legal_moves.append([current_y, x])

            for x in range(current_x + 1, self._max_x_coord + 1):
                # add all x_coord with current y_coord
                legal_moves.append([current_y, x])

            # now, follow up with y coordinate values
            for y in range(self._min_y_coord, current_y):
                # add all y_coord with current x_coord
                legal_moves.append([y, current_x])

            for y in range(current_y + 1, self._max_y_coord + 1):
                # add all y_coord with current x_coord
                legal_moves.append([y, current_x])

        except TypeError:
            print("This chariot piece does not have a position.")

        # RETURN LIST #
        return legal_moves

    def get_blocked_moves(self, end_position):
        """
        Returns all moves that will block a piece's move.
        :param end_position: piece's proposed end position
        :return: list of blocked positions
        """
        blocked_moves = []

        try:
            # establising index variables
            current_x = self._position[1]
            current_y = self._position[0]

            end_x = end_position[1]
            end_y = end_position[0]

            # find out if the end_position is an x_move or y_move
            # if x coords are different, then it's an x move
            if current_x != end_x:
                for x in range(current_x + 1, end_x):
                    # add all x coord with current_y coord
                    blocked_moves.append([current_y, x])

            # if y_coords are different, then it's a y move
            elif current_y != end_y:
                for y in range(current_y + 1, end_y):
                    # add all y coord with current_x coord
                    blocked_moves.append([y, current_x])

        except TypeError:
            print("This chariot does not have a position.")

        # return a list of all coordinates between current position and end position
        return blocked_moves


class Cannon(Chariot):
    """
    Represents a cannon game piece. Subclass of Cannon.
    """

    def __init__(self):
        """
        Constructor of cannon objects.
        """
        super().__init__()
        self.set_type("cannon")


class General(GamePiece):
    """
    Represents a general game piece. Subclass of GamePiece.
    """
    def __init__(self):
        """
        Constructor of general objects.
        """
        super().__init__()
        self.set_type("general")

        # establishing palace boundaries
        self._palace_left = 3
        self._palace_right = 5
        self._palace_front_black = 2
        self._palace_front_red = 7
        self._palace_back_black = 0
        self._palace_back_red = 9

    def get_legal_moves(self):
        """
        Implements the GamePiece declaration of the get_legal_moves function.
        :return: list of legal moves
        """
        legal_moves = []

        try:
            # INITIALIZE INDEX VARIABLES #
            current_y_coord = self._position[0]
            current_x_coord = self._position[1]

            # creating useful direction variables
            if self._player == "black":
                forward = [current_y_coord + 1, current_x_coord]
                back = [current_y_coord - 1, current_x_coord]

            elif self._player == "red":
                forward = [current_y_coord - 1, current_x_coord]
                back = [current_y_coord + 1, current_x_coord]

            left = [current_y_coord, current_x_coord - 1]
            right = [current_y_coord, current_x_coord + 1]

            # POPULATE LEGAL MOVES #
            legal_moves.append(forward)                     # to start, add all possible moves for the general
            legal_moves.append(back)
            legal_moves.append(left)
            legal_moves.append(right)

            # now, let's sort out the edge cases
            if self.at_back_edge():
                legal_moves.remove(back)

                if self.at_left_edge():                             # back/left edge can only move forward or right
                    legal_moves.remove(right)

                elif self.at_right_edge():                          # back/right edge can only move forward or left
                    legal_moves.remove(left)

            elif self.at_front_edge():
                legal_moves.remove(forward)

                if self.at_left_edge():                             # front/left edge can only move back or right
                    legal_moves.remove(left)

                elif self.at_right_edge():                          # front/right edge can only move back or left
                    legal_moves.remove(right)

            elif self.at_left_edge():                        # middle/left edge can only move forward, back or right
                legal_moves.remove(left)

            elif self.at_right_edge():                       # middle/right edge can only move forward, back or left
                legal_moves.remove(right)

            else:
                pass                                                # middle/middle can use all moves, so no need to fix

        except TypeError:
            print("This general piece does not have a position.")

        # RETURN LEGAL MOVES #
        return legal_moves

    def at_back_edge(self):
        """
        Determines if the general piece is at the back edge of the palace.
        :return: True if at the back edge, False if otherwise
        """
        try:
            # get y_coord
            y_coord = self._position[0]

            # general is at back edge if y_coord is equal to self._palace_back_black or self._palace_back_red
            if y_coord == self._palace_back_black or y_coord == self._palace_back_red:
                return True

            else:
                return False

        except TypeError:
            print("This general (or advisor) piece does not have a position.")

    def at_front_edge(self):
        """
        Determines if the general piece is at the front edge of the palace.
        :return: True if at the front edge, False if otherwise
        """
        try:
            # get y_coord
            y_coord = self._position[0]

            # general is at front edge if y_coord is equal to self._palace_front_black or self._palace_front_red
            if y_coord == self._palace_front_black or y_coord == self._palace_front_red:
                return True

            else:
                return False

        except TypeError:
            print("This general (or advisor) piece does not have a position.")

    def at_left_edge(self):
        """
        Determines if the general piece is at the left edge of the palace.
        :return: True if at the left edge, False if otherwise
        """
        try:
            # get x_coord
            x_coord = self._position[1]

            # general is at left edge if x_coord is equal to self._palace_left
            if x_coord == self._palace_left:
                return True

            else:
                return False

        except TypeError:
            print("This general (or advisor) piece does not have a position.")

    def at_right_edge(self):
        """
        Determines if the general piece is at the right edge of the palace.
        :return: True if at the right edge, False if otherwise
        """
        try:
            # get x_coord
            x_coord = self._position[1]

            # general is at right edge if x_coord is equal to self._palace_right
            if x_coord == self._palace_right:
                return True

            else:
                return False

        except TypeError:
            print("This general (or advisor) piece does not have a position.")

    def in_range(self, position):
        """
        Determines if the given coordinates are within the general's range
        :param position: proposed board position
        :return: True if in range, False if otherwise
        """
        # get coordinates
        x_coord = position[1]
        y_coord = position[0]

        # if coordinates are outside of palace max, out of range
        # the x coordinates are the same for both players
        if x_coord > self._palace_right:
            return False

        elif x_coord < self._palace_left:
            return False

        # the y coordinate boundaries change, depending on the player
        if self._player == "black":
            if y_coord > self._palace_front_black:
                return False

            elif y_coord < self._palace_back_black:
                return False

        elif self._player == "red":
            if y_coord < self._palace_front_red:
                return False

            elif y_coord > self._palace_back_red:
                return False

        # if position passes all checks, return true
        return True

    def get_blocked_moves(self, end_position):
        """
        Returns all moves that will block a piece's move.
        :param end_position: piece's proposed end position
        :return: list of blocked positions
        """
        return []


class Advisor(General):
    """
    Represents an advisor game piece. Subclass of the General class.
    """

    def __init__(self):
        """
        Constructor of advisor game pieces.
        """
        super().__init__()
        self.set_type("advisor")

    def get_legal_moves(self):
        """
        Implements the GamePiece declaration of the get_legal_moves function.
        :return: list of legal moves
        """
        # INITIALIZE INDEX VARIABLES #
        legal_moves = []

        # initialize useful directional variables
        if self._player == "black":
            front_left_diagonal = [self._palace_front_black, self._palace_left]
            front_right_diagonal = [self._palace_front_black, self._palace_right]
            back_left_diagonal = [self._palace_back_black, self._palace_left]
            back_right_diagonal = [self._palace_back_black, self._palace_right]
            middle = [self._palace_back_black + 1, self._palace_left + 1]

        elif self._player == "red":
            front_left_diagonal = [self._palace_front_red, self._palace_left]
            front_right_diagonal = [self._palace_front_red, self._palace_right]
            back_left_diagonal = [self._palace_back_red, self._palace_left]
            back_right_diagonal = [self._palace_back_red, self._palace_right]
            middle = [self._palace_front_red + 1, self._palace_left + 1]

        # POPULATE LEGAL MOVES LIST #
        if self._position == front_left_diagonal:
            return [middle]

        elif self._position == front_right_diagonal:
            return [middle]

        elif self._position == back_left_diagonal:
            return [middle]

        elif self._position == back_right_diagonal:
            return [middle]

        elif self._position == middle:
            legal_moves.append(front_left_diagonal)
            legal_moves.append(front_right_diagonal)
            legal_moves.append(back_left_diagonal)
            legal_moves.append(back_right_diagonal)
            return legal_moves

        return legal_moves

    def get_blocked_moves(self, end_position):
        """
        Returns all moves that will block a piece's move.
        :param end_position: piece's proposed end position
        :return: list of blocked positions
        """
        return []


class Soldier(GamePiece):
    """
    Represents a soldier game piece. Subclass of GamePiece.
    """

    def __init__(self):
        """
        Constructor of soldier objects.
        """
        super().__init__()
        self.set_type("soldier")
        self._river = 4.5                                                   # approx value of river location

    def get_legal_moves(self):
        """
        Implements the GamePiece declaration of the get_legal_moves function.
        :return: list of legal moves
        """
        legal_moves = []

        try:
            # INITIALIZE INDEX VARIABLES #
            current_y_coord = self._position[0]
            current_x_coord = self._position[1]

            # ORGANIZE LEGAL MOVES #
            # soldier's legal moves are:
            #   one move up (or down) vertically, according to player
            #   when soldier passes river, one move up OR one move horizontally
            #   when soldier reaches the end of board, one move horizontally

            if self.approaching_river():
                if self._player == "black":
                    # return one vertical move forward
                    return [[current_y_coord + 1, current_x_coord]]

                elif self._player == "red":
                    # return one vertical move forward
                    return [[current_y_coord - 1, current_x_coord]]

            elif self.passed_river():
                if self._player == "black":
                    # check if soldier is at left edge
                    if current_x_coord == self._min_x_coord:
                        # return one vertical move forward and one move right
                        return [[current_y_coord + 1, current_x_coord], [current_y_coord, current_x_coord + 1]]

                    # check if at right edge
                    elif current_x_coord == self._max_x_coord:
                        # return one vertical move forward and one move left
                        return [[current_y_coord + 1, current_x_coord], [current_y_coord, current_x_coord - 1]]

                    # otherwise, return one vertical move forward, plus horizontal moves
                    else:
                        return [[current_y_coord + 1, current_x_coord], [current_y_coord, current_x_coord + 1],
                                [current_y_coord, current_x_coord - 1]]

                elif self._player == "red":
                    # check if soldier is at left edge
                    if current_x_coord == self._min_x_coord:

                        # return one vertical move forward and one move right
                        return [[current_y_coord - 1, current_x_coord], [current_y_coord, current_x_coord + 1]]

                    # check if at right edge
                    elif current_x_coord == self._max_x_coord:

                        # return one vertical move forward and one move left
                        return [[current_y_coord - 1, current_x_coord], [current_y_coord, current_x_coord - 1]]

                    # otherwise, return one vertical move forward, plus horizontal moves
                    else:
                        return [[current_y_coord - 1, current_x_coord], [current_y_coord, current_x_coord + 1],
                                [current_y_coord, current_x_coord - 1]]

            elif self.at_forward_edge():
                # check if at left edge
                if current_x_coord == self._min_x_coord:
                    # return one move right
                    return [[current_y_coord, current_x_coord + 1]]

                # check if at right edge
                if current_x_coord == self._max_x_coord:
                    # return one move left
                    return [[current_y_coord, current_x_coord - 1]]

                # otherwise return both horizontal moves
                else:
                    return [[current_y_coord, current_x_coord - 1], [current_y_coord, current_x_coord + 1]]

        except TypeError:
            print("This soldier piece does not have a position.")

        return legal_moves

    def approaching_river(self):
        """
        Determines if soldier is approaching the river
        :return: True if approaching the river, False if otherwise
        """
        try:
            # initialize variables #
            y_coord = self._position[0]

            if self._player == "black":
                # if y_coord < 4.5, soldier is approaching river
                if y_coord < self._river:
                    return True

                # otherwise, return false
                else:
                    return False

            elif self._player == "red":
                # if y_coord > 4.5, soldier is approaching river
                if y_coord > self._river:
                    return True

                # otherwise, return false
                else:
                    return False

        except TypeError:
            print("This soldier piece does not have a position.")

    def passed_river(self):
        """
        Determines if soldier has passed the river
        :return: True if passed the river, False if otherwise
        """
        try:
            # initialize variables #
            y_coord = self._position[0]

            if self._player == "black":

                # if y_coord > 4.5 but not yet at edge, soldier has passed river
                if self._river < y_coord < self._max_y_coord:
                    return True

                # otherwise, return false
                else:
                    return False

            elif self._player == "red":
                # if y_coord < 4.5 but not yet at edge, soldier has passed the river
                if self._river > y_coord > self._min_y_coord:
                    return True

                # otherwise, still approaching river
                else:
                    return False

        except TypeError:
            print("This soldier piece does not have a position.")

    def at_forward_edge(self):
        """
        Determines if soldier is at the edge of the board
        :return: True if at the edge, False if otherwise
        """
        try:
            # initialize variables #
            y_coord = self._position[0]

            if self._player == "black":
                # if reached max y coordinate, soldier is at edge
                if y_coord == self._max_y_coord:
                    return True

                else:
                    return False

            elif self._player == "red":
                # if reached min y coordinate, solider is at edge
                if y_coord == self._min_y_coord:
                    return True

                else:
                    return False

        except TypeError:
            print("This soldier piece does not have a position.")

    def get_blocked_moves(self, end_position):
        """
        Returns all moves that will block a piece's move.
        :param end_position: piece's proposed end position
        :return: list of blocked positions
        """
        return []


class Horse(GamePiece):
    """
    Represents a horse game piece. Subclass of GamePiece.
    """
    def __init__(self):
        """
        Constructor of horse objects.
        """
        super().__init__()
        self.set_type("horse")

    def get_legal_moves(self):
        """
        Returns a list of the game piece's legal moves, depending on its current position.
        :return: list of legal moves
        """
        legal_moves = []

        try:
            # INITIALIZE INDEX VARIABLES #
            current_y_coord = self._position[0]
            current_x_coord = self._position[1]

            # ESTABLISH DIRECTIONAL VARIABLES #
            # need to sort out edge cases first
            # bottom boundary
            if self.at_bottom_boundary():
                # and - even further - if at bottom edge
                if self.at_bottom_edge():

                    if self.at_left_boundary():
                        # if at bottom/left edge cannot move down or left at all
                        if self.at_left_edge():
                            up_right = [current_y_coord - 2, current_x_coord + 1]
                            right_up = [current_y_coord - 1, current_x_coord + 2]

                            # add moves
                            legal_moves.append(up_right)
                            legal_moves.append(right_up)

                        # if at bottom edge/left boundary cannot move left first and cannot move down at all
                        else:
                            up_left = [current_y_coord - 2, current_x_coord - 1]
                            up_right = [current_y_coord - 2, current_x_coord + 1]
                            right_up = [current_y_coord - 1, current_x_coord + 2]

                            # add moves
                            legal_moves.append(up_left)
                            legal_moves.append(up_right)
                            legal_moves.append(right_up)

                    elif self.at_right_boundary():
                        # if at bottom edge/right edge, cannot move down or right at all
                        if self.at_right_edge():
                            up_left = [current_y_coord - 2, current_x_coord - 1]
                            left_up = [current_y_coord - 1, current_x_coord - 2]

                            # add moves
                            legal_moves.append(up_left)
                            legal_moves.append(left_up)

                        # if at bottom edge/right boundary, cannot move right first or down at all
                        else:
                            up_left = [current_y_coord - 2, current_x_coord - 1]
                            up_right = [current_y_coord - 2, current_x_coord + 1]
                            left_up = [current_y_coord - 1, current_x_coord - 2]

                            # add moves
                            legal_moves.append(up_left)
                            legal_moves.append(up_right)
                            legal_moves.append(left_up)

                    # if just at bottom edge, cannot move down at all
                    else:
                        up_left = [current_y_coord - 2, current_x_coord - 1]
                        up_right = [current_y_coord - 2, current_x_coord + 1]
                        left_up = [current_y_coord - 1, current_x_coord - 2]
                        right_up = [current_y_coord - 1, current_x_coord + 2]

                        legal_moves.append(up_left)
                        legal_moves.append(up_right)
                        legal_moves.append(left_up)
                        legal_moves.append(right_up)

                elif self.at_left_boundary():
                    # if at bottom boundary/left edge, cannot move down first or left at all
                    if self.at_left_edge():
                        up_right = [current_y_coord - 2, current_x_coord + 1]
                        right_up = [current_y_coord - 1, current_x_coord + 2]
                        right_down = [current_y_coord + 1, current_x_coord + 2]

                        # add moves
                        legal_moves.append(up_right)
                        legal_moves.append(right_up)
                        legal_moves.append(right_down)

                    # if at bottom boundary/left boundary, cannot move down or left first
                    else:
                        up_left = [current_y_coord - 2, current_x_coord - 1]
                        up_right = [current_y_coord - 2, current_x_coord + 1]
                        right_up = [current_y_coord - 1, current_x_coord + 2]
                        right_down = [current_y_coord + 1, current_x_coord + 2]

                        # add moves
                        legal_moves.append(up_left)
                        legal_moves.append(up_right)
                        legal_moves.append(right_up)
                        legal_moves.append(right_down)

                elif self.at_right_boundary():
                    # if at bottom boundary/right edge, cannot move down first or right at all
                    if self.at_right_edge():
                        up_left = [current_y_coord - 2, current_x_coord - 1]
                        left_up = [current_y_coord - 1, current_x_coord - 2]
                        left_down = [current_y_coord + 1, current_x_coord - 2]

                        # add moves
                        legal_moves.append(up_left)
                        legal_moves.append(left_up)
                        legal_moves.append(left_down)

                    # if at bottom boundary/right boundary, cannot move down or right first
                    else:
                        up_left = [current_y_coord - 2, current_x_coord - 1]
                        up_right = [current_y_coord - 2, current_x_coord + 1]
                        left_up = [current_y_coord - 1, current_x_coord - 2]
                        left_down = [current_y_coord + 1, current_x_coord - 2]

                        # add moves
                        legal_moves.append(up_left)
                        legal_moves.append(up_right)
                        legal_moves.append(left_up)
                        legal_moves.append(left_down)

                # if just at bottom boundary, cannot move down first
                else:
                    up_left = [current_y_coord - 2, current_x_coord - 1]
                    up_right = [current_y_coord - 2, current_x_coord + 1]
                    left_up = [current_y_coord - 1, current_x_coord - 2]
                    left_down = [current_y_coord + 1, current_x_coord - 2]
                    right_up = [current_y_coord - 1, current_x_coord + 2]
                    right_down = [current_y_coord + 1, current_x_coord + 2]

                    # add moves
                    legal_moves.append(up_left)
                    legal_moves.append(up_right)
                    legal_moves.append(left_up)
                    legal_moves.append(left_down)
                    legal_moves.append(right_up)
                    legal_moves.append(right_down)

            # if at top boundary
            elif self.at_top_boundary():

                if self.at_top_edge():
                    if self.at_left_boundary():

                        # if at top edge/left edge, cannot move up or left at all
                        if self.at_left_edge():
                            right_down = [current_y_coord + 1, current_x_coord + 2]
                            down_right = [current_y_coord + 2, current_x_coord + 1]

                            # add moves
                            legal_moves.append(right_down)
                            legal_moves.append(down_right)

                        # if at top edge/left boundary cannot move left first or up at all
                        else:
                            right_down = [current_y_coord + 1, current_x_coord + 2]
                            down_left = [current_y_coord + 2, current_x_coord - 1]
                            down_right = [current_y_coord + 2, current_x_coord + 1]

                            # add moves
                            legal_moves.append(right_down)
                            legal_moves.append(down_left)
                            legal_moves.append(down_right)

                    elif self.at_right_boundary():
                        # if at top edge/right edge, cannot move up or right at all
                        if self.at_right_edge():
                            left_down = [current_y_coord + 1, current_x_coord - 2]
                            down_left = [current_y_coord + 2, current_x_coord - 1]

                            # add moves
                            legal_moves.append(left_down)
                            legal_moves.append(down_left)

                        # if at top edge/right boundary cannot move right first or up at all
                        else:
                            left_down = [current_y_coord + 1, current_x_coord - 2]
                            down_left = [current_y_coord + 2, current_x_coord - 1]
                            down_right = [current_y_coord + 2, current_x_coord + 1]

                            # add moves
                            legal_moves.append(left_down)
                            legal_moves.append(down_left)
                            legal_moves.append(down_right)

                    # if just at top edge, just cannot go up at all
                    else:
                        left_down = [current_y_coord + 1, current_x_coord - 2]
                        right_down = [current_y_coord + 1, current_x_coord + 2]
                        down_left = [current_y_coord + 2, current_x_coord - 1]
                        down_right = [current_y_coord + 2, current_x_coord + 1]

                        # add moves
                        legal_moves.append(left_down)
                        legal_moves.append(right_down)
                        legal_moves.append(down_left)
                        legal_moves.append(down_right)

                elif self.at_left_boundary():
                    # if at top boundary/left edge, cannot go up first or left at all
                    if self.at_left_edge():
                        right_up = [current_y_coord - 1, current_x_coord + 2]
                        right_down = [current_y_coord + 1, current_x_coord + 2]
                        down_right = [current_y_coord + 2, current_x_coord + 1]

                        # add moves
                        legal_moves.append(right_up)
                        legal_moves.append(right_down)
                        legal_moves.append(down_right)

                    # if at top boundary/left boundary, cannot go up or left first
                    else:
                        right_up = [current_y_coord - 1, current_x_coord + 2]
                        right_down = [current_y_coord + 1, current_x_coord + 2]
                        down_left = [current_y_coord + 2, current_x_coord - 1]
                        down_right = [current_y_coord + 2, current_x_coord + 1]

                        # add moves
                        legal_moves.append(right_up)
                        legal_moves.append(right_down)
                        legal_moves.append(down_left)
                        legal_moves.append(down_right)

                elif self.at_right_boundary():
                    # if at top boundary/right edge, cannot go up first or right at all
                    if self.at_right_edge():
                        left_up = [current_y_coord - 1, current_x_coord - 2]
                        left_down = [current_y_coord + 1, current_x_coord - 2]
                        down_left = [current_y_coord + 2, current_x_coord - 1]

                        # add moves
                        legal_moves.append(left_up)
                        legal_moves.append(left_down)
                        legal_moves.append(down_left)

                    # if at top boundary/right boundary, cannot go up or right first
                    else:
                        left_up = [current_y_coord - 1, current_x_coord - 2]
                        left_down = [current_y_coord + 1, current_x_coord - 2]
                        down_left = [current_y_coord + 2, current_x_coord - 1]
                        down_right = [current_y_coord + 2, current_x_coord + 1]

                        # add moves
                        legal_moves.append(left_up)
                        legal_moves.append(left_down)
                        legal_moves.append(down_left)
                        legal_moves.append(down_right)

                # if just at top boundary, cannot move up first
                else:
                    left_up = [current_y_coord - 1, current_x_coord - 2]
                    left_down = [current_y_coord + 1, current_x_coord - 2]
                    right_up = [current_y_coord - 1, current_x_coord + 2]
                    right_down = [current_y_coord + 1, current_x_coord + 2]
                    down_left = [current_y_coord + 2, current_x_coord - 1]
                    down_right = [current_y_coord + 2, current_x_coord + 1]

                    # add moves
                    legal_moves.append(left_up)
                    legal_moves.append(left_down)
                    legal_moves.append(right_up)
                    legal_moves.append(right_down)
                    legal_moves.append(down_left)
                    legal_moves.append(down_right)

            elif self.at_left_boundary():
                # if at left edge, cannot go left at all
                if self.at_left_edge():
                    up_right = [current_y_coord - 2, current_x_coord + 1]
                    right_up = [current_y_coord - 1, current_x_coord + 2]
                    right_down = [current_y_coord + 1, current_x_coord + 2]
                    down_right = [current_y_coord + 2, current_x_coord + 1]

                    # add moves
                    legal_moves.append(up_right)
                    legal_moves.append(right_up)
                    legal_moves.append(right_down)
                    legal_moves.append(down_right)

                # if at left boundary, cannot go left first
                else:
                    up_left = [current_y_coord - 2, current_x_coord - 1]
                    up_right = [current_y_coord - 2, current_x_coord + 1]
                    right_up = [current_y_coord - 1, current_x_coord + 2]
                    right_down = [current_y_coord + 1, current_x_coord + 2]
                    down_left = [current_y_coord + 2, current_x_coord - 1]
                    down_right = [current_y_coord + 2, current_x_coord + 1]

                    # add moves
                    legal_moves.append(up_left)
                    legal_moves.append(up_right)
                    legal_moves.append(right_up)
                    legal_moves.append(right_down)
                    legal_moves.append(down_left)
                    legal_moves.append(down_right)

            elif self.at_right_boundary():
                # if at right edge, cannot go right at all
                if self.at_right_edge():
                    up_left = [current_y_coord - 2, current_x_coord - 1]
                    left_up = [current_y_coord - 1, current_x_coord - 2]
                    left_down = [current_y_coord + 1, current_x_coord - 2]
                    down_left = [current_y_coord + 2, current_x_coord - 1]

                    # add moves
                    legal_moves.append(up_left)
                    legal_moves.append(left_up)
                    legal_moves.append(left_down)
                    legal_moves.append(down_left)

                # if just at right boundary, cannot go right first
                else:
                    up_left = [current_y_coord - 2, current_x_coord - 1]
                    up_right = [current_y_coord - 2, current_x_coord + 1]
                    left_up = [current_y_coord - 1, current_x_coord - 2]
                    left_down = [current_y_coord + 1, current_x_coord - 2]
                    down_left = [current_y_coord + 2, current_x_coord - 1]
                    down_right = [current_y_coord + 2, current_x_coord + 1]

                    # add moves
                    legal_moves.append(up_left)
                    legal_moves.append(up_right)
                    legal_moves.append(left_up)
                    legal_moves.append(left_down)
                    legal_moves.append(down_left)
                    legal_moves.append(down_right)

            # if not at edge case, all moves are available
            else:
                up_left = [current_y_coord - 2, current_x_coord - 1]
                up_right = [current_y_coord - 2, current_x_coord + 1]
                left_up = [current_y_coord - 1, current_x_coord - 2]
                left_down = [current_y_coord + 1, current_x_coord - 2]
                right_up = [current_y_coord - 1, current_x_coord + 2]
                right_down = [current_y_coord + 1, current_x_coord + 2]
                down_left = [current_y_coord + 2, current_x_coord - 1]
                down_right = [current_y_coord + 2, current_x_coord + 1]

                legal_moves.append(up_left)
                legal_moves.append(up_right)
                legal_moves.append(left_up)
                legal_moves.append(left_down)
                legal_moves.append(right_up)
                legal_moves.append(right_down)
                legal_moves.append(down_left)
                legal_moves.append(down_right)

        except TypeError:
            print("This horse piece does not have a position.")

        # RETURN LEGAL MOVES #
        return legal_moves

    def at_bottom_boundary(self):
        """
        Determines if the horse piece is at the bottom boundary of the board.
        :return: True if at the back edge, False if otherwise
        """
        try:
            # get y_coord
            y_coord = self._position[0]

            # horse is at back edge if y_coord is 8 or more
            if y_coord >= self._max_y_coord - 1:
                return True

            else:
                return False

        except TypeError:
            print("This horse piece does not have a position.")

    def at_bottom_edge(self):
        """
        Determines if the horse piece is at the bottom edge of the board.
        :return: True if at the back edge, False if otherwise
        """
        try:
            # get y_coord
            y_coord = self._position[0]

            # horse is at back edge if y_coord is equal to the max y coord
            if y_coord == self._max_y_coord:
                return True

            else:
                return False

        except TypeError:
            print("This horse piece does not have a position.")

    def at_top_edge(self):
        """
        Determines if the horse piece is at the top edge of the board.
        :return: True if at the front edge, False if otherwise
        """
        try:
            # get y_coord
            y_coord = self._position[0]

            # general is at front edge if y_coord is equal to the min y coord
            if y_coord == self._min_y_coord:
                return True

            else:
                return False

        except TypeError:
            print("This horse piece does not have a position.")

    def at_top_boundary(self):
        """
        Determines if the horse piece is at the front edge of the palace.
        :return: True if at the front edge, False if otherwise
        """
        try:
            # get y_coord
            y_coord = self._position[0]

            # general is at front edge if y_coord is 1 or less
            if y_coord <= self._min_y_coord + 1:
                return True

            else:
                return False

        except TypeError:
            print("This horse piece does not have a position.")

    def at_left_edge(self):
        """
        Determines if the horse piece is at the left edge of the board.
        :return: True if at the left edge, False if otherwise
        """
        try:
            # get x_coord
            x_coord = self._position[1]

            # general is at left edge if x_coord is equal to min x coord
            if x_coord == self._min_x_coord:
                return True

            else:
                return False

        except TypeError:
            print("This horse piece does not have a position.")

    def at_left_boundary(self):
        """
        Determines if the horse piece is at the left edge of the board.
        :return: True if at the left edge, False if otherwise
        """
        try:
            # get x_coord
            x_coord = self._position[1]

            # general is at left edge if x_coord is 1 or less
            if x_coord <= self._min_x_coord + 1:
                return True

            else:
                return False

        except TypeError:
            print("This horse piece does not have a position.")

    def at_right_edge(self):
        """
        Determines if the general piece is at the right edge of the board.
        :param position: piece's current position (should be in board coordinate format)
        :return: True if at the right edge, False if otherwise
        """
        try:
            # get x_coord
            x_coord = self._position[1]

            # general is at right edge if x_coord is equal to max x coord
            if x_coord == self._max_x_coord:
                return True

            else:
                return False

        except TypeError:
            print("This horse piece does not have a position.")

    def at_right_boundary(self):
        """
        Determines if the general piece is at the right edge of the board.
        :return: True if at the right edge, False if otherwise
        """
        try:
            # get x_coord
            x_coord = self._position[1]

            # general is at right edge if x_coord is 7 or more
            if x_coord >= self._max_x_coord - 1:
                return True

            else:
                return False

        except TypeError:
            print("This horse piece does not have a position.")

    def get_blocked_moves(self, end_position):
        """
        Returns all moves that will block a piece's move.
        :param end_position: piece's proposed end position
        :return: list of blocked positions
        """
        blocked_moves = []

        try:
            # establish index variables
            current_x = self._position[1]
            current_y = self._position[0]

            end_x = end_position[1]
            end_y = end_position[0]

            x_discrepancy = abs(end_x - current_x)
            y_discrepancy = abs(end_y - current_y)

            # find out where the forward movement is
            # if moving forward on x-axis first, add x positions to blocked moves
            if x_discrepancy == 2:
                for x in range(current_x + 1, end_x + 1):
                    blocked_moves.append([current_y, x])

                for x in range(end_x, current_x):
                    blocked_moves.append([current_y, x])

            # if moving forward on the y-axis first, add y positions to blocked moves
            elif y_discrepancy == 2:
                for y in range(current_y + 1, end_y + 1):
                    blocked_moves.append([y, current_x])

                for y in range(end_y, current_y ):
                    blocked_moves.append([y, current_x])

        except TypeError:
            print("This horse piece does not have a position.")

        # return blocked moves
        return blocked_moves


class Elephant(GamePiece):
    """
    Represents an elephant game piece. Subclass of GamePiece.
    """
    def __init__(self):
        """
        Constructor of Elephant objects.
        """
        super().__init__()
        self.set_type("elephant")

    def get_legal_moves(self):
        """
        Returns a list of the game piece's legal moves, depending on its current position.
        :return: list of legal moves
        """
        # INITIALIZE INDEXING VARIABLES #
        legal_moves = []

        # there are only seven possible positions per player
        # establish directional positions
        if self._player == "black":
            top_left = [0, 2]
            top_right = [0, 6]
            bottom_left = [4, 2]
            bottom_right = [4, 6]
            left = [2, 0]
            right = [2, 8]
            middle = [2, 4]

        elif self._player == "red":
            top_left = [5, 2]
            top_right = [5, 6]
            bottom_left = [9, 2]
            bottom_right = [9, 6]
            left = [7, 0]
            right = [7, 8]
            middle = [7, 4]

        # POPULATE LEGAL MOVES #
        if self._position == top_left:
            legal_moves.append(middle)
            legal_moves.append(left)

        elif self._position == top_right:
            legal_moves.append(middle)
            legal_moves.append(right)

        elif self._position == bottom_left:
            legal_moves.append(middle)
            legal_moves.append(left)

        elif self._position == bottom_right:
            legal_moves.append(middle)
            legal_moves.append(right)

        elif self._position == left:
            legal_moves.append(top_left)
            legal_moves.append(bottom_left)

        elif self._position == right:
            legal_moves.append(top_right)
            legal_moves.append(bottom_right)

        elif self._position == middle:
            legal_moves.append(top_left)
            legal_moves.append(bottom_left)
            legal_moves.append(top_right)
            legal_moves.append(bottom_right)

        # RETURN LEGAL MOVES #
        return legal_moves

    def get_blocked_moves(self, end_position):
        """
        Returns all moves that will block a piece's move.
        :param end_position: piece's proposed end position
        :return: list of blocked positions
        """
        # INITIALIZE INDEXING VARIABLES #
        blocked_moves = []

        # there are only seven possible positions per player
        # establish directional positions
        if self._player == "black":
            top_left = [0, 2]
            top_right = [0, 6]
            bottom_left = [4, 2]
            bottom_right = [4, 6]
            left = [2, 0]
            right = [2, 8]
            middle = [2, 4]

            top_left_block = [1, 1]
            top_mid_left_block = [1, 3]
            top_mid_right_block = [1, 5]
            top_right_block = [1, 7]

            bottom_left_block = [3, 1]
            bottom_mid_left_block = [3, 3]
            bottom_mid_right_block = [3, 5]
            bottom_right_block = [3, 7]

        elif self._player == "red":
            top_left = [5, 2]
            top_right = [5, 6]
            bottom_left = [9, 2]
            bottom_right = [9, 6]
            left = [7, 0]
            right = [7, 8]
            middle = [7, 4]

            top_left_block = [6, 1]
            top_mid_left_block = [6, 3]
            top_mid_right_block = [6, 5]
            top_right_block = [6, 7]

            bottom_left_block = [8, 1]
            bottom_mid_left_block = [8, 3]
            bottom_mid_right_block = [8, 5]
            bottom_right_block = [8, 7]

        # POPULATE BLOCKED MOVES #
        if self._position == top_left:
            blocked_moves.append(top_left_block)
            blocked_moves.append(top_mid_left_block)

        elif self._position == top_right:
            blocked_moves.append(top_right_block)
            blocked_moves.append(top_mid_right_block)

        elif self._position == bottom_left:
            blocked_moves.append(bottom_left_block)
            blocked_moves.append(bottom_mid_left_block)

        elif self._position == bottom_right:
            blocked_moves.append(bottom_right_block)
            blocked_moves.append(bottom_mid_right_block)

        elif self._position == left:
            blocked_moves.append(top_left_block)
            blocked_moves.append(bottom_left_block)

        elif self._position == right:
            blocked_moves.append(top_right_block)
            blocked_moves.append(bottom_right_block)

        elif self._position == middle:
            blocked_moves.append(top_mid_left_block)
            blocked_moves.append(top_mid_right_block)
            blocked_moves.append(bottom_mid_left_block)
            blocked_moves.append(bottom_mid_right_block)

        # RETURN LEGAL MOVES #
        return blocked_moves
