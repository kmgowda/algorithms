"""Volume 15, Chapter 2 - Hard Problems: P, NP, NP-Complete Explained With Puzzles.

The heart of NP: CHECKING a proposed answer (a certificate) is fast, even when FINDING one seems to need search.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations

import itertools
import timeit

Clause = tuple[int, ...]          # literals: 3 means x3 is true, -3 means x3 is false


def check_sudoku(grid: list[list[int]]) -> bool:
    """Verify a filled 9 x 9 Sudoku in O(81): every row, column and box holds 1..9 once."""
    want = set(range(1, 10))
    rows = all(set(r) == want for r in grid)
    cols = all({grid[r][c] for r in range(9)} == want for c in range(9))
    boxes = all({grid[r][c] for r in range(br, br + 3) for c in range(bc, bc + 3)} == want
                for br in range(0, 9, 3) for bc in range(0, 9, 3))
    return rows and cols and boxes


def check_subset_sum(values: list[int], target: int, chosen: list[int]) -> bool:
    """Verify a subset-sum certificate (indices of chosen values) in O(n)."""
    return len(set(chosen)) == len(chosen) and all(0 <= i < len(values) for i in chosen) and \
        sum(values[i] for i in chosen) == target


def solve_subset_sum(values: list[int], target: int) -> list[int] | None:
    """Find a certificate by trying all 2^n subsets - the only general method known (for large values)."""
    for r in range(len(values) + 1):
        for combo in itertools.combinations(range(len(values)), r):
            if sum(values[i] for i in combo) == target:
                return list(combo)
    return None


def check_sat(clauses: list[Clause], assignment: dict[int, bool]) -> bool:
    """Verify a SAT certificate: every clause has at least one true literal. O(total clause length)."""
    return all(any(assignment[abs(l)] == (l > 0) for l in clause) for clause in clauses)


def solve_sat(clauses: list[Clause], n_vars: int) -> dict[int, bool] | None:
    """Brute-force SAT: 2^n assignments. (SAT was the first problem proven NP-complete.)"""
    for bits in itertools.product([False, True], repeat=n_vars):
        assignment = {i + 1: b for i, b in enumerate(bits)}
        if check_sat(clauses, assignment):
            return assignment
    return None


def verify_vs_solve(sizes: list[int]) -> list[tuple[int, float, float]]:
    """Measure: checking a subset-sum certificate vs finding one, as n grows (impossible instance = full search)."""
    out = []
    for n in sizes:
        values = [2 * (i + 1) for i in range(n)]                 # all even
        target = 1                                               # odd: no subset works, so the search is complete
        cert = [0]
        check = min(timeit.repeat(lambda: check_subset_sum(values, target, cert), number=1, repeat=3))
        solve = min(timeit.repeat(lambda: solve_subset_sum(values, target), number=1, repeat=1))
        out.append((n, check, solve))
    return out


def exam_schedule_ok(conflicts: list[tuple[str, str]], slot: dict[str, int], slots: int) -> bool:
    """Industry example: checking an exam timetable (graph colouring certificate) is easy; finding one is NP-hard."""
    return all(0 <= s < slots for s in slot.values()) and all(slot[a] != slot[b] for a, b in conflicts)


if __name__ == "__main__":
    print(check_subset_sum([3, 34, 4, 12, 5, 2], 9, [0, 2, 5]), solve_subset_sum([3, 34, 4, 12, 5, 2], 9))
    clauses = [(1, 2), (-1, 3), (-2, -3), (2, 3)]
    sol = solve_sat(clauses, 3)
    print(sol, check_sat(clauses, sol))
    for n, check, solve in verify_vs_solve([10, 14, 18]):
        print(f"n = {n}: check {check * 1e6:.1f} us, solve {solve * 1000:.1f} ms")
    print(exam_schedule_ok([("Maths", "Physics"), ("Physics", "Art")], {"Maths": 0, "Physics": 1, "Art": 0}, 2))
