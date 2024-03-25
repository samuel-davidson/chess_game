# Author: Samuel Davidson
# GitHub Username: samuel-davidson




class ChessVar:
    """Description"""
    def __init__(self):
        """Initializes the board, game state, current turn.  """
        self._board = [['' for _ in range(8)] for _ in range(8)]                      # actual board layout using list comp for 8x8 square
        self._state_of_game = "UNFINISHED"                                            # is game over?
        self._current_turn = "White"                                                 # who's turn it is
        self._white_pieces_captured = []                                              # empty list to hold white pieces no longer on board
        self._black_pieces_captured = []                                              # empty list to hold black pieces no longer on board


        # init the starting board and piece placements

        self._board[0] = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']                     # white back row
        self._board[1] = ['P' for _ in range(8)]                                      # white front row
        self._board[6] = ['p' for _ in range(8)]                                      # black front row
        self._board[7] = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']                     # black black row

    def get_game_state(self):
        """Returns whether game is done or not"""
        return self._state_of_game

    def set_state_of_game(self, winner):
        """Sets game state to 'UNFINISHED', 'WHITE WON' or 'BLACK WON' """
        if winner == "White":
            self._state_of_game = "WHITE_WON"
        else:
            self._state_of_game = "BLACK_WON"

    def get_current_turn(self):
        """Returns player with current turn"""
        return self._current_turn

    def set_current_turn(self, new_turn_player):
        """Sets game to next turn"""
        if new_turn_player == "White":
            self._current_turn = "White"
        else:
            self._current_turn = "Black"

    def get_white_pieces_captured(self):
        """Returns current white pieces captured"""
        return self._white_pieces_captured

    def set_white_pieces_captured(self, captured_piece):
        """Moves the piece passed as an argument to the list of pieces captured

        - interacts with: __init__"""
        captured_piece = captured_piece.lower()
        self._white_pieces_captured.append(captured_piece)
        if captured_piece == 'k':
            self.set_state_of_game('Black')
            # black wins
            # set game status, end game

    def get_black_pieces_captured(self):
        """Returns current black pieces captured

        - interacts with: __init__"""
        return self._black_pieces_captured

    def set_black_pieces_captured(self, captured_piece):
        """Moves the piece passed as an argument to the list of pieces captured

        - interacts with: __init__"""
        captured_piece = captured_piece.lower()
        self._black_pieces_captured.append(captured_piece)
        if captured_piece == 'k':
            self.set_state_of_game('White')
            # white wins
            # set game status, end game

    def is_valid_square(self, square):
        """Takes as an argument a square in chess notation and returns True if the square is on the board/
        and False if otherwise"""
        return len(square) == 2 and square[0] in 'abcdefgh' and square[1] in '12345678'

    def is_square_empty(self, square):
        """Takes as a parameter a square as a string, and
        returns True if the square is unoccupied and False if it is filled,"""
        row, column = self.chess_to_index(square)
        if self._board[row][column] == '':
            return True
        else:
            return False

    def is_square_occ_by_friendly(self, piece, square):
        """Returns True if the square passed as an argument is on the same team as the piece passed
        as an argument, False if otherwise"""
        row, column = self.chess_to_index(square)                                       # fetch index notation for piece
        piece_occupying = self._board[row][column]                                      # init variable for piece
        if piece.isupper() and piece_occupying.isupper():                               # if both white
            return True
        elif piece.islower() and piece_occupying.islower():                             # if both black
            return True
        return False                                                                    # opposite team

    def chess_to_index(self, square):
        """Receives as an argument a square in chess notation (ex:'e4') and returns the corresponding index notation"""
        file_legend = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}  # dictionary to translate
        file_ = square[0]                                                               # file in alg notation
        rank = int(square[1])-1                                                       # rank in alg notation (0 indexed)
        column = file_legend[file_]                                                     # column index
        row = rank                                                                  # row index
        return row, column                                                             # return row and column index

    def index_to_chess(self, row, column):
        """Receives as arguments the column and row of an index position and returns the corresponding chess notation """
        file_legend = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}          # dictionary to translate
        file_ = file_legend[column]                                                     # file as string
        rank = row + 1 # rank in alg
        return file_ + str(rank)                                                        # return string of chess notation

    # def piece_on_square(self, square):
       #  """Takes as a parameter a square as a string. Returns None if square is empty, and returns the piece occupying the square if applicable

        # - interacts with: __init__, is_square_empty"""
        # if not self.is_square_empty(square):
       #      return None
        # find the piece
       #  return # piece

    def make_move(self, square_1, square_2):
        """takes two parameters - strings that represent the square moved from and the square moved to.
        For example, make_move('b2', 'b4'). If the square being moved from does not contain a piece belonging
        to the player whose turn it is, or if the indicated move is not legal, or if the game has already been won,
        then it should just return False. Otherwise it should make the indicated move, remove any captured piece,
        update the game state if necessary, update whose turn it is, and return True

        - interacts with: __init__, is_move_valid"""
        if self.get_game_state() != "UNFINISHED":   # if game is over, no moves allowed
            return False

        if not self.is_valid_square(square_1) or not self.is_valid_square(square_2):    # if either square is invalid
            return False                                                                # no moves allowed


        row_1, column_1 = self.chess_to_index(square_1) # fetch index notation for squares
        row_2, column_2 = self.chess_to_index(square_2)


        moving_piece = self._board[row_1][column_1] # make variable for piece to be moved   # if it is not a players' turn, they cannot move
        if (self._current_turn == "White" and not moving_piece.isupper()) or \
                (self._current_turn == "Black" and not moving_piece.islower()):
            return False

        if not self.is_move_valid(moving_piece, square_1, square_2):                    # check if move is valid
            return False

        captured_piece = self._board[row_2][column_2]                                   # make variable for piece being captured
        if not self.is_square_empty(square_2):                                          # if destination square is occupied, remove the piece on it
            if captured_piece.isupper() is True:                                        # if that piece is white, move to white captured pieces list
                self.set_white_pieces_captured(captured_piece)
            else:
                self.set_black_pieces_captured(captured_piece)                          # if that piece is black, move to black captured pieces list

        self._board[row_2][column_2] = moving_piece                                     # moving piece is placed on new square
        self._board[row_1][column_1] = ""                                               # 'source' square is cleared

        if captured_piece == 'K':                                                       # if white king captured
            self.set_state_of_game("Black")                                                # then black wins
        if captured_piece == 'k':                                                       # if black king captured
            self.set_state_of_game("White")                                                 # then white wins

        self._current_turn = "White" if self._current_turn == "Black" else "Black"      # update turn
        return True



    def is_move_valid(self, piece, current_square, target_square):
        """Returns whether or not the piece passed as an argument is able to move to the square passed as an argument as True or False

        - interacts with: __init__, move_piece, is_square_empty, all of the is_path_clear/ is_move methods

        - includes the rules/ regulations for piece movement here
            - thinking of having the pawn 2-squares for the first rule be an if statement, dependent on the row since they can
                    only move forwards...
                    so if they are in their original row, can move one or two. otherwise can move one
        - first checks the piece type and finds available moves
            - checks if requested move is within range
        - second, checks that path is open for said piece type"""
        # validated by this point: game state, player turn, both squares on board

        row_1, column_1 = self.chess_to_index(current_square)  # fetch index notation for squares
        row_2, column_2 = self.chess_to_index(target_square)

        if not self.is_square_empty(target_square) and self.is_square_occ_by_friendly(piece, target_square):
            return False                                                    # only disallows same team movement/ capturing

        # validated by this point: game state, player turn, both squares on board, target square
            # is either empty or occupied by opposing team
        # convert all pieces to lower and run based off of piece type
        # these next lines just call a methods per piece type
        if piece.lower() == 'p':
            return self.is_valid_pawn_move(current_square, target_square)
        if piece.lower() == 'r':
            return self.is_valid_rook_move(current_square, target_square)
        if piece.lower() == 'n':
            return self.is_valid_knight_move(current_square, target_square)
        if piece.lower() == 'b':
            return self.is_valid_bishop_move(current_square, target_square)
        if piece.lower() == 'q':
            return self.is_valid_queen_move(current_square, target_square)
        if piece.lower() == 'k':
            return self.is_valid_king_move(current_square, target_square)
        if piece.lower() == 'f':
            return self.is_valid_falcon_move(current_square, target_square)
        if piece.lower() == 'h':
            return self.is_valid_hunter_move(current_square, target_square)
        else:
            return False



    def is_valid_pawn_move(self, current_square, target_square):
        """Returns True if the move is a valid move for a Pawn, False if otherwise"""
        starting_row, column_1 = self.chess_to_index(current_square)  # fetch index notation for squares           # 1,0
        target_row, column_2 = self.chess_to_index(target_square)                                                # 3,0
        diff_row = target_row - starting_row                                # quantify vertical movement                # 2
        diff_column = column_2 - column_1                      # quantify horizontal movement               # 0
        direction = 0
        # logic for double/ first move
        # determine direction due to piece color
        if self.get_current_turn() == "White":
            direction = 1
            if starting_row == 1:                   # are we on the first row for pawns?
                if diff_row == 2:
                    next_avail_square = self.index_to_chess(starting_row + direction, column_1)
                    if self.is_square_empty(next_avail_square) and self.is_square_empty(target_square):
                        # if both squares in front are open, and it's the pawns' first move
                        return True
        else:
            direction = -1
            if starting_row == 6:
                if diff_row == 2 * direction:
                    next_avail_square = self.index_to_chess(starting_row + direction, column_1)
                    if self.is_square_empty(next_avail_square) and self.is_square_empty(target_square):
                        # if both squares in front are open, and it's the pawns' first move
                        return True

        # logic for every subsequent move
        if diff_column == 0:                                     # if moving straight
            if diff_row == 1 * direction and self.is_square_empty(target_square):                                   # if making a single square movement
                return True

        elif abs(diff_column) == 1 and diff_row == direction:                           # if capturing diagonally
            if not self.is_square_empty(target_square) and not \
                    self.is_square_occ_by_friendly(self._board[starting_row][column_1], target_square):        # ensuring the square is occupied by enemy
                return True
        return False


    def is_valid_rook_move(self, current_square, target_square):
        """Returns True if the move is a valid move for a Rook, False if otherwise"""
        column_1, row_1 = self.chess_to_index(current_square)  # fetch index notation for squares
        column_2, row_2 = self.chess_to_index(target_square)
        diff_row = row_2 - row_1                    # quantify vertical movement
        diff_column = column_2 - column_1           # quantify horizontal movement

        if diff_row != 0 and diff_column != 0:                          # either vert or horiz must be straight
            return False                                                # rooks only move straight

        if diff_row == 0:                                               # horizontal move
            direction = 1 if diff_column > 0 else -1                     # set direction based off white or black
            for col in range(column_1 + direction, column_2, direction): # parse through the path (start, stop, step)
                if not self.is_square_empty(self.index_to_chess(col, row_1)):   # if path is blocked by some piece
                    return False
        else:                                                            # vertical move
            direction = 1 if diff_row > 0 else -1                     # set direction based off white or black
            for row in range(row_1 + direction, row_2, direction):       # parse through the path (start, stop, step)
                if not self.is_square_empty(self.index_to_chess(column_1, row)):  # if path is blocked by some piece
                    return False
        if self.is_square_empty(target_square) or not \
                self.is_square_occ_by_friendly(self._board[column_1][row_1], target_square):
            return True
        else:
            return False


    def is_valid_knight_move(self, current_square, target_square):
        """Returns True if the move is a valid move for a Knight, False if otherwise"""
        column_1, row_1 = self.chess_to_index(current_square)  # fetch index notation for squares
        column_2, row_2 = self.chess_to_index(target_square)
        diff_row = abs(row_2 - row_1)                           # quantify vertical movement
        diff_column = abs(column_2 - column_1)                  # quantify horizontal movement

        if diff_row == 2 and diff_column == 1:                  # Valid L shape with 2 vertical straight path
            if self.is_square_empty(target_square) or \
                    self.is_square_occ_by_friendly(self._board[column_1][row_1], target_square):
                return True
        if diff_row == 1 and diff_column == 2:                  # Valid L shape with 2 horizontal straight path
            if self.is_square_empty(target_square) or \
                    not self.is_square_occ_by_friendly(self._board[column_1][row_1], target_square):
                return True
        return False


    def is_valid_bishop_move(self, current_square, target_square):
        """Returns True if the move is a valid move for a Bishop, False if otherwise"""
        column_1, row_1 = self.chess_to_index(current_square)  # fetch index notation for squares
        column_2, row_2 = self.chess_to_index(target_square)
        diff_row = abs(row_2 - row_1)                           # quantify vertical movement
        diff_column = abs(column_2 - column_1)                  # quantify horizontal movement

        if diff_row == diff_column:                                 # if the move is diagonal
            row_direction = 1 if row_2 > row_1 else -1              # set direction of path based on move
            column_direction = 1 if column_2 > column_1 else -1
            for i in range(1, diff_row):                            # parse through the path of diagonal squares
                row = row_1 + i * row_direction
                column = column_1 + i * column_direction
                if not self.is_square_empty(self.index_to_chess(column, row)):      # check the path is clear
                    return False
            if self.is_square_empty(target_square) or \
                    not self.is_square_occ_by_friendly(self._board[column_1][row_1], target_square):
                # check that the square is empty/ available for capture
                return True
        else:
            return False

    def is_valid_queen_move(self, current_square, target_square):
        """Returns True if the move is a valid move for a Queen, False if otherwise"""
        column_1, row_1 = self.chess_to_index(current_square)  # fetch index notation for squares
        column_2, row_2 = self.chess_to_index(target_square)
        diff_row = abs(row_2 - row_1)  # quantify vertical movement
        diff_column = abs(column_2 - column_1)  # quantify horizontal movement

        if diff_row == diff_column or diff_row == 0 or diff_column == 0:             # check if move is diagonal or straight
            if diff_row == diff_column:                                              # if its diagonal, check the diagonal path
                row_direction = 1 if row_2 > row_1 else -1                           # set direction of path based on move
                column_direction = 1 if column_2 > column_1 else -1
                for i in range(1, diff_row):                                         # parse through the path of diagonal squares
                    row = row_1 + i * row_direction
                    column = column_1 + i * column_direction
                    if not self.is_square_empty(self.index_to_chess(row, column)):   # check the path is clear
                        return False
            elif diff_row == 0:                                               # horizontal move
                direction = 1 if diff_column > 0 else -1                     # set direction based off white or black
                for col in range(column_1 + direction, column_2, direction): # parse through the path (start, stop, step)
                    if not self.is_square_empty(self.index_to_chess(row_1, col)):   # if path is blocked by some piece
                        return False
            else:                                                            # vertical move
                direction = 1 if diff_row > 0 else -1                     # set direction based off white or black
                for row in range(row_1 + direction, row_2, direction):       # parse through the path (start, stop, step)
                    if not self.is_square_empty(self.index_to_chess(row, column_1)):  # if path is blocked by some piece
                        return False
            if self.is_square_empty(target_square) or not \
                    self.is_square_occ_by_friendly(self._board[row_1][column_1], target_square):
                return True
        else:
            return False

    def is_valid_king_move(self, current_square, target_square):
        """Returns True if the move is a valid move for a King, False if otherwise"""
        column_1, row_1 = self.chess_to_index(current_square)   # fetch index notation for squares
        column_2, row_2 = self.chess_to_index(target_square)
        diff_row = abs(row_2 - row_1)                           # quantify vertical movement
        diff_column = abs(column_2 - column_1)                  # quantify horizontal movement

        if diff_row <=1 and diff_column <= 1:                   # check to see within range for king
            if self.is_square_empty(target_square) or \
                    self.is_square_occ_by_friendly(self._board[column_1][row_1], target_square):
                # check that the square is empty/ available for capture
                return True
        return False

    def is_valid_falcon_move(self, current_square, target_square):
        """Returns True if the move is a valid move for a Falcon, False if otherwise
        FALCON RULES: MOVES FORWARD LIKE A BISHOP(Diagonals), MOVES BACKWARDS LIKE A ROOK(straight line)"""
        column_1, row_1 = self.chess_to_index(current_square)  # fetch index notation for squares
        column_2, row_2 = self.chess_to_index(target_square)
        diff_row = abs(row_2 - row_1)  # quantify vertical movement
        diff_column = abs(column_2 - column_1)  # quantify horizontal movement
        current_turn = self.get_current_turn()
        if current_turn == "White":
            forward_direction = 1
            backward_direction = -1
        else:
            forward_direction = -1
            backward_direction = 1
        if diff_row == diff_column and diff_row * forward_direction > 0:
            return self.is_valid_bishop_move(current_square, target_square)
        elif diff_row == 0 and diff_row * backward_direction > 0:
            return self.is_valid_rook_move(current_square, target_square)
        elif diff_column == 0 and diff_row * backward_direction > 0:
            return self.is_valid_rook_move(current_square, target_square)
        else:
            return False

    def is_valid_hunter_move(self, current_square, target_square):
        """Returns True if the move is a valid move for a Falcon, False if otherwise
        HUNTER RULES: MOVES FORWARD LIKE A ROOK(straight line), MOVES BACKWARDS LIKE A BISHOP(diagonals)"""
        column_1, row_1 = self.chess_to_index(current_square)  # fetch index notation for squares
        column_2, row_2 = self.chess_to_index(target_square)
        diff_row = abs(row_2 - row_1)  # quantify vertical movement
        diff_column = abs(column_2 - column_1)  # quantify horizontal movement
        current_turn = self.get_current_turn()
        if current_turn == "White":
            forward_direction = 1
            backward_direction = -1
        else:
            forward_direction = -1
            backward_direction = 1
        if diff_row == 0 and diff_column * forward_direction > 0:
            return self.is_valid_rook_move(current_square, target_square)
        elif diff_row == diff_column and diff_row * backward_direction > 0:
            return self.is_valid_bishop_move(current_square, target_square)
        elif diff_column == 0 and diff_row * backward_direction > 0:
            return self.is_valid_bishop_move(current_square, target_square)
        else:
            return False
    def enter_fairy_piece(self, piece, target_square):
        """takes two parameters - strings that represent the type of the piece
        (white falcon 'F', white hunter 'H', black falcon 'f', black hunter 'h') and the square
        it will enter. For example, enter_fairy_piece ('H', 'c1'). If the fairy piece is not
        allowed to enter this position at this turn for any reason, it should just return False.
        Otherwise it should enter the board at that position, update whose turn it is, and return True.


        ***THIS METHOD JUST VALIDATES THE ENTERING OF THE FAIRY PIECE ONTO THE BOARD, IT DOES NOT CAST A MOVE***

        ***THESE PIECES CAN ONLY ENTER THE GAME AFTER THE PLAYER HAS LOST A SECOND PIECE (ROOK, KNIGHT, BISHOP, QUEEN)
        AND ARE ONLY ALLOWED TO BE PLACED ON THE HOME SQUARES OF THE PLAYER WHO IS PLAYING SAID FAIRY PIECE***

        - interacts with: move_piece
        - validate game state
        - validate turn
        - validate move
        - make move
        - return True"""

        if self.get_game_state() != "UNFINISHED":               # validate game state
            return False

        current_turn = self.get_current_turn()                  # validate turn
        if piece.isupper() and current_turn != "White":
            return False
        if piece.islower() and current_turn != "Black":
            return False

        if not self.is_valid_square(target_square):             # validate move
            return False

        # validate eligibility

        target_column, target_row = self.chess_to_index(target_square)  # fetch index

        if current_turn == "White" and target_row not in [0, 1]:        # ensure being placed on home square
            return False

        if current_turn == "Black" and target_row not in [6, 7]:        # ensure being placed on home square
            return False

        if current_turn == "White":        # get pieces captured
            lost_pieces_list = self.get_white_pieces_captured()
        else:
            lost_pieces_list = self.get_black_pieces_captured()

        # check if player has lost (a correct) piece

        req_lost_pieces = ['q', 'r', 'n', 'b']  # queen rook knight bishop
        for lost_piece in req_lost_pieces:
            if lost_piece not in lost_pieces_list:
                return False

        self._board[target_column][target_row] = piece # place piece on board
        if current_turn == "White":
            self.set_current_turn("Black")
        if current_turn == "Black":
            self.set_current_turn("White")              # update turns

        return True

#