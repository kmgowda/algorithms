"""Volume 11, Chapter 4 - Constraint Problems: N-Queens, Sudoku, Word Search.

Run:  python3 ch04_examples.py
"""

from __future__ import annotations


def n_queens(n: int) -> list[list[int]]:
    """LeetCode 51: place n queens so none attack each other. One queen per row; for each row try every column
    not attacked. Sets of used columns and diagonals make each check O(1). Returns cols[row] for each solution."""
    solutions: list[list[int]] = []
    cols: list[int] = []
    used_cols, used_diag, used_anti = set(), set(), set()

    def place(row: int) -> None:
        if row == n:
            solutions.append(list(cols))
            return
        for c in range(n):
            if c in used_cols or row - c in used_diag or row + c in used_anti:
                continue                                    # attacked: prune this branch
            cols.append(c)
            used_cols.add(c); used_diag.add(row - c); used_anti.add(row + c)
            place(row + 1)
            cols.pop()
            used_cols.remove(c); used_diag.remove(row - c); used_anti.remove(row + c)

    place(0)
    return solutions


def board_picture(cols: list[int]) -> list[str]:
    return ["".join("Q" if c == q else "." for c in range(len(cols))) for q in cols]


def solve_sudoku(board: list[list[int]]) -> bool:
    """LeetCode 37: fill zeros so every row, column and 3x3 box has 1-9 once. Fills in place; True if solved.
    Picks the empty cell with the FEWEST legal digits first (most constrained first) - a huge saving."""
    rows = [set(r) - {0} for r in board]
    cols = [{board[r][c] for r in range(9)} - {0} for c in range(9)]
    boxes = [{board[r][c] for r in range(b // 3 * 3, b // 3 * 3 + 3) for c in range(b % 3 * 3, b % 3 * 3 + 3)} - {0}
             for b in range(9)]
    empty = [(r, c) for r in range(9) for c in range(9) if board[r][c] == 0]

    def candidates(r: int, c: int) -> set[int]:
        return set(range(1, 10)) - rows[r] - cols[c] - boxes[r // 3 * 3 + c // 3]

    def go() -> bool:
        if not empty:
            return True
        cell = min(empty, key=lambda rc: len(candidates(*rc)))
        r, c = cell
        empty.remove(cell)
        for d in candidates(r, c):
            board[r][c] = d
            rows[r].add(d); cols[c].add(d); boxes[r // 3 * 3 + c // 3].add(d)
            if go():
                return True
            rows[r].remove(d); cols[c].remove(d); boxes[r // 3 * 3 + c // 3].remove(d)
        board[r][c] = 0
        empty.append(cell)
        return False

    return go()


def is_valid_sudoku(board: list[list[int]]) -> bool:
    groups = [board[r] for r in range(9)] + [[board[r][c] for r in range(9)] for c in range(9)] + \
             [[board[r][c] for r in range(b // 3 * 3, b // 3 * 3 + 3) for c in range(b % 3 * 3, b % 3 * 3 + 3)] for b in range(9)]
    return all(sorted(g) == list(range(1, 10)) for g in groups)


def word_search(grid: list[str], word: str) -> bool:
    """LeetCode 79: can the word be traced through neighbouring cells, each used at most once?"""
    rows, cols = len(grid), len(grid[0])
    used: set[tuple[int, int]] = set()

    def trace(r: int, c: int, i: int) -> bool:
        if i == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols) or (r, c) in used or grid[r][c] != word[i]:
            return False
        used.add((r, c))
        found = any(trace(r + dr, c + dc, i + 1) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        used.remove((r, c))
        return found

    return any(trace(r, c, 0) for r in range(rows) for c in range(cols))


def exam_seating(students: list[str], same_class: set[frozenset[str]], seats: int) -> list[str] | None:
    """Industry example: seat students in a row so that classmates never sit together (first valid plan)."""
    plan: list[str] = []

    def go() -> bool:
        if len(plan) == seats:
            return True
        for s in students:
            if s in plan or (plan and frozenset({plan[-1], s}) in same_class):
                continue
            plan.append(s)
            if go():
                return True
            plan.pop()
        return False

    return list(plan) if go() else None


PUZZLE = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0], [6, 0, 0, 1, 9, 5, 0, 0, 0], [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3], [4, 0, 0, 8, 0, 3, 0, 0, 1], [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0], [0, 0, 0, 4, 1, 9, 0, 0, 5], [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


if __name__ == "__main__":
    sols = n_queens(8)
    print(len(sols), "solutions for 8 queens; first:")
    print("\n".join(board_picture(sols[0])))
    board = [row[:] for row in PUZZLE]
    print("sudoku solved:", solve_sudoku(board), is_valid_sudoku(board), board[0])
    print(word_search(["ABCE", "SFCS", "ADEE"], "ABCCED"), word_search(["ABCE", "SFCS", "ADEE"], "ABCB"))
    print(exam_seating(["A1", "A2", "B1", "B2"], {frozenset({"A1", "A2"}), frozenset({"B1", "B2"})}, 4))
