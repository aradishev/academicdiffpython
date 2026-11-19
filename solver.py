from minesweeper_engine import get_neighbors


class Solver:
    def solve_step(self, board) -> tuple[set, set]:
        safe = set()
        mines = set()

        while True:
            found = True
            while found:
                found = False
                for row in range(len(board)):
                    for col in range(len(board[0])):
                        cell = board[row][col]
                        if not cell.is_revealed:
                            continue

                        flags = 0
                        closed = []
                        for r, c in get_neighbors(board, row, col):
                            neighbor = board[r][c]
                            if neighbor.is_flagged or (r, c) in mines:
                                flags += 1
                            elif neighbor.is_revealed or (r, c) in safe:
                                continue
                            else:
                                closed.append((r, c))

                        if len(closed) == 0:
                            continue
                        if cell.adjacent_mines == flags + len(closed):
                            mines.update(closed)
                            found = True
                        elif cell.adjacent_mines == flags:
                            safe.update(closed)
                            found = True

            constraints = self._generate_constraints(board, safe, mines)
            new_safe, new_mines = self._apply_subset_rule(constraints)
            new_safe = new_safe - safe
            new_mines = new_mines - mines
            if len(new_safe) == 0 and len(new_mines) == 0:
                break
            safe.update(new_safe)
            mines.update(new_mines)

        return safe, mines

    def _generate_constraints(self, board, safe, mines):
        constraints = []
        for row in range(len(board)):
            for col in range(len(board[0])):
                cell = board[row][col]
                if not cell.is_revealed:
                    continue

                known_mines = 0
                unknown = set()
                for r, c in get_neighbors(board, row, col):
                    neighbor = board[r][c]
                    if neighbor.is_flagged or (r, c) in mines:
                        known_mines += 1
                    elif neighbor.is_revealed or (r, c) in safe:
                        continue
                    else:
                        unknown.add((r, c))

                if len(unknown) > 0:
                    constraint = (frozenset(unknown), cell.adjacent_mines - known_mines)
                    if constraint not in constraints:
                        constraints.append(constraint)
        return constraints

    def _apply_subset_rule(self, constraints):
        constraints = list(constraints)
        safe = set()
        mines =set()

        found = True
        while found:
            found = False
            for cells_a, count_a in list(constraints):
                for cells_b, count_b in list(constraints):
                    if len(cells_a) < len(cells_b) and cells_a <= cells_b:
                        new_cells = cells_b- cells_a
                        new_count = count_b - count_a
                        if new_count == 0:
                            safe.update(new_cells)
                        elif new_count == len(new_cells):
                            mines.update(new_cells)
                        if (new_cells, new_count) not in constraints:
                            constraints.append((new_cells, new_count))
                            found = True

        return safe, mines