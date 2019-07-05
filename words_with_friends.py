import copy
import os
import sys
import time

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

def text_to_board(text):
    #Takes a string and makes it into a column major board
    rows = text.split("\n")
    column_counts = set([len(row) for row in rows])
    if len(column_counts) != 1:
        raise Exception(f"Can't handle board with different length rows, found these: {column_counts}")
    row_length = column_counts.pop()
    column_length = len(rows)
    if column_length != row_length:
        raise Exception(f"Can't handle board with row length {row_length} != column length {column_length}")

    size = column_length
    columns = []
    for column_index in range(size):
        column = []
        for row_index in range(size):
            column.append(rows[row_index][column_index])
        columns.append(column)
    return columns

def board_to_text(board):
    #Takes a column major board and makes it into text
    rows = list(zip(*board))
    return "\n".join(["".join(row) for row in rows])

# W = Triple Word
# L = Triple Letter
# w = Double Word
# l = Double Letter
words_with_friends_full_board = text_to_board("""\
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
""")

def board_size(board):
    column_lengths = {len(column) for column in board}
    if len(column_lengths) != 1:
        raise Exception(f"Can't handle board with different length columns, found these: {column_lengths}")
    width = len(board)
    height = column_lengths.pop()
    return (width, height)


wordlist_path = "../vanreece.github.io/scrabble.txt"
characters = "ohtoail"
with open(wordlist_path, "r") as wordlist_fd:
    wordlist = [word[:-1].upper() for word in wordlist_fd]
wordset = set(wordlist)

def neighbor_tiles(x, y, width, height):
    neighbors = []
    if x > 0:
        neighbors.append((x-1, y))
    if x < width - 1:
        neighbors.append((x+1, y))
    if y > 0:
        neighbors.append((x, y-1))
    if y < height - 1:
        neighbors.append((x, y+1))
    return neighbors


def validate_move(current_board, proposed_move, board_multiples):
    # print(f"validate_move called with current_board:\n{board_to_text(current_board)}\nproposed_move: \n{board_to_text(proposed_move)}\nboard_multiples:\n{board_to_text(board_multiples)}")
    if board_size(current_board) != board_size(proposed_move):
        raise Exception(f"Can't apply different sized move to current board: {board_size(proposed_move)} != {board_size(current_board)}")
    width, height = board_size(current_board)

    # Needs:
    # 1) Tiles must occupy empty squares
    # 2) Tiles must be in a straight line
    # 3) Tiles must be contiguous with each other (and existing tiles)
    # 4) Tiles must spell valid words with all neighbors

    # 1) Tiles must occupy empty squares
    new_tiles = []
    new_rows = set()
    new_cols = set()
    new_board = copy.deepcopy(current_board)
    for x, column in enumerate(proposed_move):
        for y, element in enumerate(column):
            if element == ' ':
                continue
            if current_board[x][y] != ' ':
                # Can't add tile {element} to {(x, y)}, occupied with {current_board[x][y]}
                return (False, "Tiles not occupying empty squares")
            new_tiles.append((x, y, element))
            new_board[x][y] = element
            new_rows.add(y)
            new_cols.add(x)

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
        for neighbor_x, neighbor_y in neighbor_tiles(x, y, width, height):
            if (current_board[neighbor_x][neighbor_y] != ' '):
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
            if (current_board[test_x][test_y] == ' ' and
                    proposed_move[test_x][test_y] == ' '):
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
            if (current_board[test_x][test_y] == ' ' and
                    proposed_move[test_x][test_y] == ' '):
                return (False, "Tiles not contiguous")

    # Need to test *all* the words and make sure they're on the wordlist
    for column in new_board:
        # Find all the words, which are 1+ letters separated by spaces
        words = [word for word in "".join(column).split(" ") if word]
        for word in words:
            if word not in wordset:
                return (False, f"{word} not found in wordlist")


    return (True, "")
