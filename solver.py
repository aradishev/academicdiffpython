import random
from collections import deque

from minesweeper_engine import get_neighbors, generate_board, reveal_cell, is_lost, is_won


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
        mines = set()

        found = True
        while found:
            found = False
            for cells_a, count_a in list(constraints):
                for cells_b, count_b in list(constraints):
                    # A строго внутри B
                    if len(cells_a) < len(cells_b) and cells_a <= cells_b:
                        new_cells = cells_b - cells_a
                        new_count = count_b - count_a
                        if new_count == 0:
                            safe.update(new_cells)
                        elif new_count == len(new_cells):
                            mines.update(new_cells)
                        if (new_cells, new_count) not in constraints:
                            constraints.append((new_cells, new_count))
                            found = True

        return safe, mines

    def make_probabilistic_move(self, board) -> tuple[int, int]:
        constraints = self._generate_constraints(board, set(), set())
        if len(constraints) == 0:
            closed = []
            for row in range(len(board)):
                for col in range(len(board[0])):
                    if not board[row][col].is_revealed and not board[row][col].is_flagged:
                        closed.append((row, col))
            return random.choice(closed)

        best_cell = None
        best_probability = 2
        for group_cells, group_constraints in self._split_into_groups(constraints):
            result = {"total": 0, "mines": {}}
            for cell in group_cells:
                result["mines"][cell] = 0
            self._backtrack(group_cells, group_constraints, 0, {}, result)

            for cell in group_cells:
                probability = result["mines"][cell] / result["total"]
                if probability < best_probability:
                    best_probability = probability
                    best_cell = cell
        return best_cell

    def _split_into_groups(self, constraints):
        cell_to_constraints = {}
        for i in range(len(constraints)):
            for cell in constraints[i][0]:
                if cell not in cell_to_constraints:
                    cell_to_constraints[cell] = []
                cell_to_constraints[cell].append(i)
        visited = set()
        groups = []
        for start in cell_to_constraints:
            if start in visited:
                continue
            visited.add(start)
            group_cells = []
            used = set()
            queue = deque([start])
            while queue:
                cell = queue.popleft()
                group_cells.append(cell)
                for i in cell_to_constraints[cell]:
                    used.add(i)
                    for other in constraints[i][0]:
                        if other not in visited:
                            visited.add(other)
                            queue.append(other)
            group_constraints = []
            for i in sorted(used):
                group_constraints.append(constraints[i])
            groups.append((group_cells, group_constraints))
        return groups

    def _backtrack(self, cells, constraints, index, assignment, result):
        if index == len(cells):
            result["total"] += 1
            for cell in cells:
                if assignment[cell] == 1:
                    result["mines"][cell] += 1
            return
        for value in (0, 1):
            assignment[cells[index]] = value
            if self._is_valid(constraints, assignment):
                self._backtrack(cells, constraints, index + 1, assignment, result)
        del assignment[cells[index]]

    def _is_valid(self, constraints, assignment):
        for cells, count in constraints:
            mines = 0
            unknown = 0
            for cell in cells:
                if cell in assignment:
                    mines += assignment[cell]
                else:
                    unknown += 1
            if mines > count or mines + unknown < count:
                return False
        return True


def play_with_solver(rows=9, cols=9, num_mines=10):
    solver = Solver()
    start = (rows // 2, cols // 2)
    board = generate_board(rows, cols, num_mines, start)
    reveal_cell(board, start[0], start[1])

    while not is_won(board) and not is_lost(board):
        safe, mines = solver.solve_step(board)
        if len(safe) > 0 or len(mines) > 0:
            for r, c in mines:
                board[r][c].is_flagged = True
            for r, c in safe:
                reveal_cell(board, r, c)
        else:
            r, c = solver.make_probabilistic_move(board)
            print("Угадываем клетку", (r, c))
            reveal_cell(board, r, c)

    if is_won(board):
        print("Решатель выиграл")
    else:
        print("Решатель проиграл")