import numpy as np
import sys


class Hexapawn:
    """
    This is a solver for the game Hexapawn. 
    """

    def __init__(self, game_state: list):
        """
        When given a character representation of the game state, 
        it will initalize variables with the values from that state.
        :param game_state: An example game state:
        W
        ppp
        ...
        PPP
        """
        players_turn = game_state[0][0]
        self.init_char_board = game_state[1:]
        self.init_char_board = [list(x) for x in self.init_char_board]
        self.whites_turn = players_turn == "W"
        self.num_rows = len(self.init_char_board)
        self.num_cols = len(self.init_char_board[0])
        self.white_pieces = self.get_pieces('P')
        self.black_pieces = self.get_pieces('p')
        self.numpy_board = self.get_numpy_board()

    def get_pieces(self, piece: str):
        """
        Checks each position of char_board to see if the piece in question is there.
        When one is found, a (row, column) tuple is added to the piece list
        :param piece: the type of piece being looked for
        :return: a list of (row, column) tuples representing the position of the pieces
        """
        piece_list = []
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if self.init_char_board[r][c] == piece:
                    piece_list.append((r, c))
        return piece_list

    def get_numpy_board(self):
        """
        Gets a numpy array representation of the board from the piece lists
        1 is for white, -1 is for black, and 0 is an empty space
        :return: a numpy array representation of the board
        """
        board = np.zeros((self.num_rows, self.num_cols))
        for r, c in self.white_pieces:
            board[r][c] = 1
        for r, c in self.black_pieces:
            board[r][c] = -1
        return board

    def get_char_board(self):
        """
        Gets a list of strings representation of the board from the numpy array.
        This is just for visualization.
        :return: a list of strings representation of the board.
        """
        board = []
        if self.whites_turn:
            board.append('W')
        else:
            board.append('B')
        for row in self.numpy_board:
            result_row = ''
            for col in row:
                if col == -1:
                    result_row += 'p'
                if col == 0:
                    result_row += '.'
                if col == 1:
                    result_row += 'P'
            board.append(result_row)
        return board

    def print_char_board(self):
        """
        Will print out the board to stderr
        :return: None
        """
        board = self.get_char_board()
        for row in board:
            sys.stderr.write(row + '\n')

    def position_value(self, depth=0, logging=False):
        """
        This is where the adversary search happens. All of the moves are generated,
        then applied one at a time. When the value of the resulting board is 1, that 
        move is a winning move and no more moves need to be checked.
        When the value of the resulting board is -1, that move was a losing move,
        it's undone and the next move is checked.
        Before leaving this function all moves applied need to be undone to return
        the board into its previous state.
        :param depth: This is for debugging to see how deep the recursion goes
        :param logging: This is for debugging to see how the state changes between moves
        :return: 
        """
        moves = self.get_all_moves()
        if not moves:
            return -1
        max_val = -1
        for move in moves:
            if logging:
                self.print_char_board()
                sys.stderr.write("black: " + str(self.black_pieces) + '\n')
                sys.stderr.write("white: " + str(self.white_pieces) + '\n')
                sys.stderr.write(str(depth) + " move: " + str(move) + '\n')
            result = self.apply_move(move)
            if logging:
                self.print_char_board()
                sys.stderr.write("black: " + str(self.black_pieces) + '\n')
                sys.stderr.write("white: " + str(self.white_pieces) + '\n')
                sys.stderr.write('\n')
            if result == 1:
                # If a winning move is found, return a win
                self.undo_move(move)
                return 1
            else:
                val = - self.position_value(depth=depth + 1, logging=logging)
            max_val = max(max_val, val)
            if max_val == 1:
                # If a winning move has been found, return a win
                self.undo_move(move)
                return 1
            if logging:
                sys.stderr.write("UNDO: " + str(move) + '\n')
            self.undo_move(move)
        return max_val

    def get_all_moves(self):
        """
        :return: A list of all the moves that the current player can make
        """
        moves = []
        if self.whites_turn:
            for piece in self.white_pieces:
                moves += self.get_moves(piece)
        else:
            for piece in self.black_pieces:
                moves += self.get_moves(piece)
        return moves

    def get_moves(self, piece: tuple):
        """
        Gets the moves a piece could make.
        :param piece: The piece that is making the moves
        :return: A list of moves that the piece could make
        """
        moves = []
        if self.whites_turn:
            forward = -1
        else:
            forward = 1
        moves.append(self.get_move(piece, forward, -1, True))
        moves.append(self.get_move(piece, forward, 0, False))
        moves.append(self.get_move(piece, forward, 1, True))
        # remove the falses from the list
        moves = list(filter(lambda m: m, moves))
        return moves

    def get_move(self, piece, row, col, capture):
        """
        Checks if a move is possible, then returns that move
        :param piece: A tuple describing where the piece is right now
        :param row: How many rows to travel
        :param col: How many columns to travel
        :param capture: If the piece is going to capture or not
        :return: 
        """
        new_position = self.get_new_position(piece, row, col)
        if not self.on_board(new_position):
            return False
        occupied_by = self.numpy_board[new_position]
        if capture:
            if self.whites_turn:
                enemy = -1
            else:
                enemy = 1
            if occupied_by == enemy:
                return piece, new_position, capture
        else:
            if occupied_by == 0:
                return piece, new_position, capture
        return False

    def on_board(self, position: tuple):
        """
        Checks if a position is within bounds of the board
        :param position: The position to check
        :return: True if the position is within bounds or false otherwise
        """
        if position[0] > self.num_rows - 1 or position[0] < 0:
            return False
        if position[1] > self.num_cols - 1 or position[1] < 0:
            return False
        return True

    @staticmethod
    def get_new_position(piece, row, col):
        """
        Turns a starting position and move directions into a new position
        :param piece: The starting position for the piece
        :param row: How many rows to travel
        :param col: How many columns to travel
        :return: The new position
        """
        return piece[0] + row, piece[1] + col

    def apply_move(self, move: tuple):
        """
        Changes the state of the numpy board to reflect this move
        and report if a pawn reaches the last rank
        :param move: The move to be taken
        :return: Will return 1
        """
        start_pos = move[0]
        end_pos = move[1]
        capture = move[2]
        win = 0

        if capture:
            self.remove_piece(end_pos, not self.whites_turn)
        self.remove_piece(start_pos, self.whites_turn)
        self.place_piece(end_pos, self.whites_turn)
        if self.whites_turn:
            if end_pos[0] == 0:
                win = 1
        else:
            if end_pos[0] == self.num_rows - 1:
                win = 1
        self.whites_turn = not self.whites_turn
        return win

    def remove_piece(self, piece, white: bool):
        """
        Takes a piece off the board and out of the piece list
        :param piece: The piece to remove
        :param white: If it is a white piece
        :return: None
        """
        if white:
            self.white_pieces.remove(piece)
        else:
            self.black_pieces.remove(piece)

    def undo_move(self, move: tuple):
        """
        Returns state to before the move was made
        :param move: the move to undo
        :return: None
        """
        start_pos = move[0]
        end_pos = move[1]
        capture = move[2]

        # change the turn
        self.whites_turn = not self.whites_turn
        self.remove_piece(end_pos, self.whites_turn)
        self.place_piece(start_pos, self.whites_turn)
        if capture:
            self.place_piece(end_pos, not self.whites_turn)

    def place_piece(self, piece, white: bool):
        """
        Puts a piece onto the board and into a piece list
        :param piece: The piece to place
        :param white: If the piece is white
        :return: 
        """
        if white:
            self.white_pieces.append(piece)
            self.numpy_board[piece] = 1
        else:
            self.black_pieces.append(piece)
            self.numpy_board[piece] = -1

if __name__ == "__main__":
    """
    This function will take a file as an argument or from the stdin
    """
    if len(sys.argv) == 2:
        char_state_rep = open(sys.argv[1]).read().splitlines()
    else:
        char_state_rep = sys.stdin.read().splitlines()
    hexapawn = Hexapawn(char_state_rep)
    value = hexapawn.position_value(logging=False)
    print(str(value))
