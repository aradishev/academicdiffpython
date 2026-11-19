import random
from collections import deque
from dataclasses import dataclass


@dataclass
class Cell:
    is_mine: bool = False
    is_revealed: bool = False
    is_flagged: bool = False
    adjacent_mines: int = 0


def get_neighbors(board, row, col):
    neighbors = []
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            r = row + dr
            c = col + dc
            if 0 <= r < len(board) and 0 <= c < len(board[0]):
                neighbors.append((r, c))
    return neighbors


def generate_board(rows, cols, num_mines, first_click_coords):
    board = [[Cell() for _ in range(cols)] for _ in range(rows)]

    coords = []
    for r in range(rows):
        for c in range(cols):
            if (r, c) != first_click_coords:
                coords.append((r, c))

    for r, c in random.sample(coords, num_mines):
        board[r][c].is_mine = True

    for r in range(rows):
        for c in range(cols):
            count = 0
            for nr, nc in get_neighbors(board, r, c):
                if board[nr][nc].is_mine:
                    count += 1
            board[r][c].adjacent_mines = count

    return board


def reveal_cell(board, row, col):
    cell = board[row][col]
    if cell.is_flagged or cell.is_revealed:
        return
    cell.is_revealed = True

    queue = deque([(row, col)])
    while queue:
        r, c = queue.popleft()
        if board[r][c].adjacent_mines == 0 and not board[r][c].is_mine:
            for nr, nc in get_neighbors(board, r, c):
                neighbor = board[nr][nc]
                if not neighbor.is_revealed and not neighbor.is_flagged:
                    neighbor.is_revealed = True
                    queue.append((nr, nc))


def is_lost(board):
    for row in board:
        for cell in row:
            if cell.is_revealed and cell.is_mine:
                return True
    return False


def is_won(board):
    for row in board:
        for cell in row:
            if not cell.is_mine and not cell.is_revealed:
                return False
    return True
