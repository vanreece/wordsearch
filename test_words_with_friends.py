from words_with_friends import *
import unittest

def blank_board(size):
    return [[' ' for x in range(size)] for x in range(size)]

class TestWordsWithFriends(unittest.TestCase):

    def test_board_text_translators(self):
        current_board = blank_board(3)
        current_board[1] = ['M', 'A', 'N']
        text = board_to_text(current_board)
        reboard = text_to_board(text)
        self.assertEqual(current_board, reboard)


    def test_valid_move(self):
        current_board = blank_board(3)
        current_board[1] = ['M', 'A', 'N']
        valid_move = blank_board(3)
        valid_move[0][1] = 'Z'
        valid_move[2][1] = 'P'
        self.assertEqual((True, ""),
                validate_move(current_board, valid_move, blank_board(3)))


    def test_overlapping_letter(self):
        current_board = blank_board(3)
        current_board[1] = ['M', 'A', 'N']
        overlapping_letter = blank_board(3)
        overlapping_letter[1][1] = 'E'
        self.assertEqual((False, "Tiles not occupying empty squares"),
                validate_move(current_board, overlapping_letter, blank_board(3)))


    def test_not_straight_line(self):
        current_board = blank_board(3)
        current_board[1] = ['M', 'A', 'N']
        not_straight_line = blank_board(3)
        not_straight_line[0][2] = 'O'
        not_straight_line[2][1] = 'M'
        self.assertEqual((False, "Tiles not in a straight line"),
                validate_move(current_board, not_straight_line, blank_board(3)))


    def test_not_contiguous(self):
        current_board = blank_board(3)
        current_board[0] = ['M', 'A', 'N']
        not_contiguous_single = blank_board(3)
        not_contiguous_single[2][0] = 'A'
        self.assertEqual((False, "Tiles not contiguous"),
                validate_move(current_board, not_contiguous_single, blank_board(3)))

        current_board = blank_board(3)
        current_board[0] = ['M', 'A', 'N']
        not_contiguous_double_in_column = blank_board(3)
        not_contiguous_double_in_column[1][0] = 'A'
        not_contiguous_double_in_column[1][2] = 'O'
        self.assertEqual((False, "Tiles not contiguous"),
                validate_move(current_board, not_contiguous_double_in_column, blank_board(3)))

        current_board = blank_board(3)
        current_board[0][2] = 'M'
        current_board[1][2] = 'A'
        current_board[2][2] = 'N'
        not_contiguous_double_in_row = blank_board(3)
        not_contiguous_double_in_row[0][1] = 'A'
        not_contiguous_double_in_row[2][1] = 'O'
        self.assertEqual((False, "Tiles not contiguous"),
                validate_move(current_board, not_contiguous_double_in_row, blank_board(3)))


    def test_not_real_words(self):
        current_board = blank_board(3)
        current_board[1] = ['A', 'M', ' ']
        bad_row = blank_board(3)
        bad_row[1][0] = 'C'
        self.assertEqual((False, "AC not found in wordlist"),
                validate_move(current_board, bad_row, blank_board(3)))
        bad_column = blank_board(3)
        bad_column[0][2] = 'Z'
        self.assertEqual((False, "AMZ not found in wordlist"),
                validate_move(current_board, bad_column, blank_board(3)))


    def test_errors(self):
        with self.assertRaises(Exception):
            validate_move([[' ']], [[' ', ' '],[' ', ' ']], [[' ', ' '],[' ', ' ']])


if __name__ == '__main__':
    unittest.main()
