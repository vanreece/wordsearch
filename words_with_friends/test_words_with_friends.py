from words_with_friends import *
import unittest


class TestBoard(unittest.TestCase):
    def test_board_constructors(self):
        with self.assertRaisesRegex(
            Exception, "Can't handle board with different length columns"
        ):
            Board([[" ", " "], [" "]])
        with self.assertRaisesRegex(
            Exception, "Can't handle board with column length 3 != column count 2"
        ):
            Board([[" ", " ", " "], [" ", " ", " "]])
        self.assertEqual(1, Board([["A"]]).size())
        self.assertEqual(2, Board([["A", "B"], ["A", "B"]]).size())
        self.assertEqual(1, Board.fromsize(1).size())
        self.assertEqual(2, Board.fromsize(2).size())
        self.assertEqual(3, Board.fromsize(3).size())

    def test_board_text_translators(self):
        board = Board.fromsize(3)
        board.set(0, 0, "M")
        board.set(0, 1, "A")
        board.set(0, 2, "N")
        text = board.to_text()
        self.assertEqual("M__\nA__\nN__", text)
        reboard = Board.fromstring(text)
        self.assertEqual(board, reboard)
        with self.assertRaisesRegex(
            Exception,
            "Can't handle board with different length rows, found these: {1, 2}",
        ):
            Board.fromstring("__\n_")
        with self.assertRaisesRegex(
            Exception, "Can't handle board with row length 2 != column length 3"
        ):
            Board.fromstring("__\n__\n__")

    def test_set_and_get(self):
        board = Board.fromsize(2)
        board.set(0, 0, "M")
        board.set(0, 1, "A")
        board.set(1, 0, "D")
        board.set(1, 1, "E")
        self.assertEqual("M", board.get(0, 0))
        self.assertEqual("A", board.get(0, 1))
        self.assertEqual("D", board.get(1, 0))
        self.assertEqual("E", board.get(1, 1))
        with self.assertRaisesRegex(Exception, "Error, coordinates exceed board size"):
            board.set(2, 2, "F")
        with self.assertRaisesRegex(Exception, "Error, coordinates exceed board size"):
            board.get(2, 2)

    def test_columns_and_rows(self):
        board = Board.fromsize(2)
        board.set(0, 0, "M")
        board.set(0, 1, "A")
        board.set(1, 0, "D")
        board.set(1, 1, "E")
        self.assertEqual([["M", "D"], ["A", "E"]], board.rows())
        self.assertEqual([["M", "A"], ["D", "E"]], board.columns())

    def test_words(self):
        board = Board.fromstring("MAN\nAN_\nD__")
        self.assertEqual(sorted(["MAN", "AN", "AN", "MAD"]), sorted(board.words()))

    def test_invalid_coordinates(self):
        # return  # For some reason I can't get this to work?
        board = Board.fromsize(3)
        board.set(1, 0, "M")
        board.set(1, 1, "A")
        board.set(1, 2, "N")
        # _M_
        # _A_
        # _N_
        out_of_x_range = [(3, 0, "X")]
        with self.assertRaisesRegex(
            Exception, "Invalid move, X coordinate \(3\) >= size \(3\)"
        ):
            board.validate_move(out_of_x_range)
        out_of_y_range = [(0, 3, "Y")]
        with self.assertRaisesRegex(
            Exception, "Invalid move, Y coordinate \(3\) >= size \(3\)"
        ):
            board.validate_move(out_of_y_range)

    def test_valid_move(self):
        board = Board.fromsize(3)
        board.set(1, 0, "M")
        board.set(1, 1, "A")
        board.set(1, 2, "N")
        # _M_
        # _A_
        # _N_
        valid_move = []
        valid_move.append((0, 1, "Z"))
        valid_move.append((2, 1, "P"))
        # _M_
        # ZAP
        # _N_
        self.assertEqual((True, ""), board.validate_move(valid_move))

    def test_overlapping_letter(self):
        board = Board.fromsize(3)
        board.set(1, 0, "M")
        board.set(1, 1, "A")
        board.set(1, 2, "N")
        # _M_
        # _A_
        # _N_
        overlapping_letter = []
        overlapping_letter.append((1, 1, "E"))
        self.assertEqual(
            (False, "Tiles not occupying empty squares"),
            board.validate_move(overlapping_letter),
        )

    def test_not_straight_line(self):
        board = Board.fromsize(3)
        board.set(1, 0, "M")
        board.set(1, 1, "A")
        board.set(1, 2, "N")
        # _M_
        # _A_
        # _N_
        not_straight_line = []
        not_straight_line.append((0, 2, "O"))
        not_straight_line.append((2, 1, "M"))
        # _M_
        # _AM
        # ON_
        self.assertEqual(
            (False, "Tiles not in a straight line"),
            board.validate_move(not_straight_line),
        )

    def test_not_contiguous(self):
        board = Board.fromsize(3)
        board.set(0, 0, "M")
        board.set(0, 1, "A")
        board.set(0, 2, "N")
        # M__
        # A__
        # N__
        not_contiguous_single = [(2, 0, "A")]
        # M_A
        # A__
        # N__
        self.assertEqual(
            (False, "Tiles not contiguous"), board.validate_move(not_contiguous_single)
        )

        not_contiguous_double_in_column = []
        not_contiguous_double_in_column.append((1, 0, "A"))
        not_contiguous_double_in_column.append((1, 2, "O"))
        # MA_
        # A__
        # NO_
        self.assertEqual(
            (False, "Tiles not contiguous"),
            board.validate_move(not_contiguous_double_in_column),
        )

        board = Board.fromsize(3)
        board.set(0, 2, "M")
        board.set(1, 2, "A")
        board.set(2, 2, "N")
        # ___
        # ___
        # MAN
        not_contiguous_double_in_row = []
        not_contiguous_double_in_row.append((0, 1, "A"))
        not_contiguous_double_in_row.append((2, 1, "O"))
        # ___
        # A_O
        # MAN
        self.assertEqual(
            (False, "Tiles not contiguous"),
            board.validate_move(not_contiguous_double_in_row),
        )

        board = Board.fromsize(3)
        board.set(1, 0, "A")
        board.set(1, 1, "M")
        # _A_
        # _M_
        # ___
        not_contiguous = [(2, 2, 'A')]
        self.assertEqual(
            (False, "Tiles not contiguous"),
            board.validate_move(not_contiguous),
        )


    def test_not_real_words(self):
        board = Board.fromsize(3)
        board.set(1, 0, "A")
        board.set(1, 1, "M")
        # _A_
        # _M_
        # ___
        bad_row = [(2, 0, "C")]
        # _AC
        # _M_
        # ___
        self.assertEqual(
            (False, "AC not found in wordlist"), board.validate_move(bad_row)
        )
        bad_column = [(1, 2, "Z")]
        # _A_
        # _M_
        # _Z_
        self.assertEqual(
            (False, "AMZ not found in wordlist"), board.validate_move(bad_column)
        )

    def test_generate_valid_moves_for_tiles(self):
        board = Board.fromsize(3)
        board.set(1, 0, "A")
        board.set(1, 1, "M")
        valid_moves = board.generate_valid_moves_for_tiles(['A'])
        golden_moves = set()
        golden_moves.add((0, 0, 'A'))
        golden_moves.add((0, 1, 'A'))
        golden_moves.add((1, 2, 'A'))
        golden_moves.add((2, 0, 'A'))
        golden_moves.add((2, 1, 'A'))
        for valid_move in valid_moves:
            new_board = Board(board.columns())
            new_board.set(valid_move[0][0], valid_move[0][1], valid_move[0][2])
            self.assertIn(valid_move[0], golden_moves)

    def test_errors(self):
        with self.assertRaises(Exception):
            validate_move([[" "]], [[" ", " "], [" ", " "]], [[" ", " "], [" ", " "]])


if __name__ == "__main__":
    unittest.main()
