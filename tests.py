import unittest
import Hexapawn



class Starting3x3Board(unittest.TestCase):
    input = ["W",
             "ppp",
             "...",
             "PPP"]
    whites_turn = True
    num_rows = 3
    num_cols = 3
    white_pieces = [(2, 0),
                    (2, 1),
                    (2, 2)]

    black_pieces = [(0, 0),
                    (0, 1),
                    (0, 2)]
    check_move = True
    get_move = white_pieces[0], (1, 0), False
    get_all_moves = [(white_pieces[0], (1, 0), False),
                     (white_pieces[1], (1, 1), False),
                     (white_pieces[2], (1, 2), False),
                     ]

    def test_state(self):
        hexapawn = Hexapawn.Hexapawn(self.input)
        assert self.whites_turn == hexapawn.whites_turn
        assert self.num_rows == hexapawn.num_rows
        assert self.num_cols == hexapawn.num_cols
        assert self.white_pieces == hexapawn.white_pieces
        assert self.black_pieces == hexapawn.black_pieces

    def test_move_generation(self):
        hexapawn = Hexapawn.Hexapawn(self.input)
        assert self.check_move == hexapawn.check_move(hexapawn.white_pieces[0], -1, 0, False)
        assert self.get_move == hexapawn.get_move(hexapawn.white_pieces[0], -1, 0, False)
        assert self.get_all_moves == hexapawn.get_all_moves()

    def test_posn(self):
        hexapawn = Hexapawn.Hexapawn(self.input)
        assert self.board_value == hexapawn.position_value()


class Progressed6x6Board(unittest.TestCase):
    input = ["B",
             "....p.",
             "...PP.",
             "..p..p",
             ".P...P",
             "pP.P..",
             "......",
             ]
    whites_turn = False
    num_rows = 6
    num_cols = 6
    white_pieces = [(1, 3),
                    (1, 4),
                    (3, 1),
                    (3, 5),
                    (4, 1),
                    (4, 3)]

    black_pieces = [(0, 4),
                    (2, 2),
                    (2, 5),
                    (4, 0)]
    check_move = True
    get_move = black_pieces[0], (1, 3), True
    get_all_moves = [((0, 4), (1, 3), True),
                     ((2, 2), (3, 1), True),
                     ((2, 2), (3, 2), False),
                     ((4, 0), (5, 0), False)]

    def test_state(self):
        hexapawn = Hexapawn.Hexapawn(self.input)
        assert self.whites_turn == hexapawn.whites_turn
        assert self.num_rows == hexapawn.num_rows
        assert self.num_cols == hexapawn.num_cols
        assert self.white_pieces == hexapawn.white_pieces
        assert self.black_pieces == hexapawn.black_pieces

    def test_move_generation(self):
        hexapawn = Hexapawn.Hexapawn(self.input)
        assert self.check_move == hexapawn.check_move(hexapawn.black_pieces[0], 1, -1, True)
        assert self.get_move == hexapawn.get_move(hexapawn.black_pieces[0], 1, -1, True)
        assert self.get_all_moves == hexapawn.get_all_moves()


class MoveUndo(unittest.TestCase):
    white_start = ["W",
                   "...",
                   "...",
                   "..P"]
    black_start = ["B",
                   ".p.",
                   "PP.",
                   "..."]
    white_result = ["B",
                    "...",
                    "..P",
                    "..."]
    black_result = ["W",
                    "...",
                    "pP.",
                    "..."]

    def test_move_undo1(self):
        hexapawn = Hexapawn.Hexapawn(self.white_start)
        move = hexapawn.get_all_moves()
        hexapawn.apply_move(move[0])
        assert self.white_result == hexapawn.get_char_board()
        hexapawn.undo_move(move[0])
        assert self.white_start == hexapawn.get_char_board()

    def test_move_undo2(self):
        hexapawn = Hexapawn.Hexapawn(self.black_start)
        move = hexapawn.get_all_moves()
        hexapawn.apply_move(move[0])
        assert self.black_result == hexapawn.get_char_board()
        hexapawn.undo_move(move[0])
        assert self.black_start == hexapawn.get_char_board()



if __name__ == "__main__":
    unittest.main()
