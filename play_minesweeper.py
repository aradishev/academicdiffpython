from minesweeper_engine import generate_board, reveal_cell, is_lost, is_won

ROWS = 9
COLS = 9
MINES = 10


def print_board(board, show_mines=False):
    print("   " + " ".join(str(c) for c in range(COLS)))
    for r in range(ROWS):
        line = []
        for c in range(COLS):
            if board is None:
                line.append("#")
                continue
            cell = board[r][c]
            if cell.is_revealed:
                line.append(str(cell.adjacent_mines))
            elif show_mines and cell.is_mine:
                line.append("*")
            elif cell.is_flagged:
                line.append("F")
            else:
                line.append("#")
        print(str(r) + "  " + " ".join(line))


def main():
    board = None
    while True:
        print_board(board)
        parts = input("> ").split()
        command = parts[0]

        if command in ("open", "o"):
            row = int(parts[1])
            col = int(parts[2])
            if board is None:
                board = generate_board(ROWS, COLS, MINES, (row, col))
            reveal_cell(board, row, col)

            if is_lost(board):
                print_board(board, show_mines=True)
                print("Вы проиграли!")
                break
            if is_won(board):
                print_board(board)
                print("Вы выиграли!")
                break
        elif command in ("flag", "f"):
            row = int(parts[1])
            col = int(parts[2])
            if board is None:
                print("Сначала откройте клетку")
            elif not board[row][col].is_revealed:
                board[row][col].is_flagged = not board[row][col].is_flagged
        else:
            print("Неизвестная команда")


if __name__ == "__main__":
    main()
