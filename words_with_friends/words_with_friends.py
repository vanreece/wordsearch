import copy
import os
import sys
import time
import json

words_with_friends_tiles = {
    "A": {"number": 9, "points": 1},
    "B": {"number": 2, "points": 4},
    "C": {"number": 2, "points": 4},
    "D": {"number": 5, "points": 2},
    "E": {"number": 13, "points": 1},
    "F": {"number": 2, "points": 4},
    "G": {"number": 3, "points": 3},
    "H": {"number": 4, "points": 3},
    "I": {"number": 8, "points": 1},
    "J": {"number": 1, "points": 10},
    "K": {"number": 1, "points": 5},
    "L": {"number": 4, "points": 2},
    "M": {"number": 2, "points": 4},
    "N": {"number": 5, "points": 2},
    "O": {"number": 8, "points": 1},
    "P": {"number": 2, "points": 4},
    "Q": {"number": 1, "points": 10},
    "R": {"number": 6, "points": 1},
    "S": {"number": 5, "points": 1},
    "T": {"number": 7, "points": 1},
    "U": {"number": 4, "points": 2},
    "V": {"number": 2, "points": 5},
    "W": {"number": 2, "points": 4},
    "X": {"number": 1, "points": 8},
    "Y": {"number": 2, "points": 3},
    "Z": {"number": 1, "points": 10},
    ".": {"number": 2, "points": 0},
}


class Board(object):
    # Idea here is to have a thing that can represent the board state, n x n,
    # grab rows, columns, or direct access
    def __init__(self, column_major_data):
        column_lengths = set([len(column) for column in column_major_data])
        if len(column_lengths) != 1:
            raise Exception(
                f"Can't handle board with different length columns, found these: {column_lengths}"
            )
        column_length = column_lengths.pop()
        column_count = len(column_major_data)
        if column_length != column_count:
            raise Exception(
                f"Can't handle board with column length {column_length} != column count {column_count}"
            )
        self._column_major_data = copy.deepcopy(column_major_data)
        self._size = column_count

    @classmethod
    def fromsize(cls, size):
        # Create empty size x size board
        return cls([[" " for x in range(size)] for x in range(size)])

    @classmethod
    def fromstring(cls, text):
        # Takes a string and makes it into a column major board
        rows = text.split("\n")
        column_counts = set([len(row) for row in rows])
        if len(column_counts) != 1:
            raise Exception(
                f"Can't handle board with different length rows, found these: {column_counts}"
            )
        row_length = column_counts.pop()
        column_length = len(rows)
        if column_length != row_length:
            raise Exception(
                f"Can't handle board with row length {row_length} != column length {column_length}"
            )

        size = column_length
        columns = []
        for column_index in range(size):
            column = []
            for row_index in range(size):
                column.append(rows[row_index][column_index])
            columns.append(column)
        return cls(columns)

    def to_text(self):
        return "\n".join(["".join(row) for row in self.rows()])

    def set(self, x, y, character):
        if x >= self._size or y >= self._size:
            raise Exception("Error, coordinates exceed board size")
        self._column_major_data[x][y] = character.upper()

    def get(self, x, y):
        if x >= self._size or y >= self._size:
            raise Exception("Error, coordinates exceed board size")
        return self._column_major_data[x][y]

    def size(self):
        return len(self._column_major_data)

    def rows(self):
        rows = []
        for y in range(self.size()):
            row = []
            for x in range(self.size()):
                row.append(self._column_major_data[x][y])
            rows.append(row)
        return rows

    def columns(self):
        return self._column_major_data

    def words(self):
        words = []
        for line in self.rows() + self.columns():
            words.extend([c for c in "".join(line).split(" ") if len(c) > 1])
        return words

    def __eq__(self, other):
        return json.dumps(self.columns()) == json.dumps(other.columns())

    def __ne__(self, other):
        return json.dumps(self.columns()) != json.dumps(other.columns())

    def validate_move(self, new_tiles):
        # Proposed move is just a list of tuples: (X, Y, Letter)

        # Needs:
        # 1) Tiles must occupy empty squares
        # 2) Tiles must be in a straight line
        # 3) Tiles must be contiguous with each other (and existing tiles)
        # 4) Tiles must spell valid words with all neighbors

        # 1) Tiles must occupy empty squares
        new_coordinates = set()
        new_rows = set()
        new_cols = set()
        new_board = Board(self._column_major_data)
        for x, y, letter in new_tiles:
            if x >= self.size():
                raise Exception(
                    f"Invalid move, X coordinate ({x}) >= size ({self.size()})"
                )
            if y >= self.size():
                raise Exception(
                    f"Invalid move, Y coordinate ({y}) >= size ({self.size()})"
                )
            if self._column_major_data[x][y] != " ":
                return (False, "Tiles not occupying empty squares")
            new_rows.add(y)
            new_cols.add(x)
            new_coordinates.add((x, y))
            new_board.set(x, y, letter)

        # 2) Tiles must be in a straight line
        new_row_count = len(new_rows)
        new_col_count = len(new_cols)
        new_count = len(new_tiles)
        if new_row_count > 1 and new_col_count > 1:
            return (False, "Tiles not in a straight line")

        if new_count == 1:
            # Single new character, must be contiguous on at least one side with existing tiles
            x, y, _ = new_tiles[0]
            found_neighbor = False
            for neighbor_x, neighbor_y in neighbor_tiles(
                x, y, self.size(), self.size()
            ):
                if self._column_major_data[neighbor_x][neighbor_y] != " ":
                    found_neighbor = True
            if not found_neighbor:
                return (False, "Tiles not contiguous")
        elif new_row_count > 1:
            # New column of characters, must be contiguous with itself and existing tiles
            # Also connected to existing tiles
            min_row = min(new_rows)
            max_row = max(new_rows)
            new_col = new_cols.pop()
            new_cols.add(new_col)
            for row_index in range(min_row, max_row + 1):
                test_x = new_col
                test_y = row_index
                if (
                    self._column_major_data[test_x][test_y] == " "
                    and (test_x, test_y) not in new_coordinates
                ):
                    return (False, "Tiles not contiguous")
        elif new_col_count > 1:
            # New row of characters, must be contiguous with itself and existing tiles
            # Also connected to existing tiles
            min_col = min(new_cols)
            max_col = max(new_cols)
            new_row = new_rows.pop()
            new_rows.add(new_row)
            for col_index in range(min_col, max_col + 1):
                test_x = col_index
                test_y = new_row
                if (
                    self._column_major_data[test_x][test_y] == " "
                    and (test_x, test_y) not in new_coordinates
                ):
                    return (False, "Tiles not contiguous")

        # Need to test *all* the words and make sure they're on the wordlist
        for word in new_board.words():
            if word not in wordset:
                return (False, f"{word} not found in wordlist")

        return (True, "")


# W = Triple Word
# L = Triple Letter
# w = Double Word
# l = Double Letter
words_with_friends_full_board = Board.fromstring(
    """\
   W  L L  W   
  l  w   w  l  
 l  l     l  l 
W  L   w   L  W
  l   l l   l  
 w   L   L   W 
L   l     l   L
   w       w   
L   l     l   L
 w   L   L   W 
  l   l l   l  
W  L   w   L  W
 l  l     l  l 
  l  w   w  l  
   W  L L  W   \
"""
)


wordlist_path = "scrabble.txt"
with open(wordlist_path, "r") as wordlist_fd:
    wordlist = [word[:-1].upper() for word in wordlist_fd]
wordset = set(wordlist)


def neighbor_tiles(x, y, width, height):
    neighbors = []
    if x > 0:
        neighbors.append((x - 1, y))
    if x < width - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if y < height - 1:
        neighbors.append((x, y + 1))
    return neighbors
