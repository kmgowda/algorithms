"""Volume 6, Chapter 19 - Thinking Problems: model solutions that design an algorithm, and a tempting wrong one.

Run:  python3 ch19_solutions.py
"""

from __future__ import annotations

from functools import lru_cache

from ch19_examples import knuth_merge_cost


def cut_beam(length: int, marks: list) -> int:
    """Thinking Problem 2: the least total cost to saw a beam at every mark, where each cut costs the length of
    the piece being sawn. Run backwards, the cuts are merges of neighbouring pieces, so the piece lengths are the
    stacks of Section 19.4, and Knuth's speed-up gives O(m^2) for m marks."""
    points = [0] + sorted(marks) + [length]
    pieces = [b - a for a, b in zip(points, points[1:])]
    return knuth_merge_cost(pieces)


def cut_beam_brute(length: int, marks: list) -> int:
    """Try every cut order directly: the cheapest way to finish the piece from points[i] to points[j]."""
    points = [0] + sorted(marks) + [length]

    @lru_cache(maxsize=None)
    def best(i: int, j: int) -> int:
        if j - i < 2:
            return 0
        return points[j] - points[i] + min(best(i, k) + best(k, j) for k in range(i + 1, j))

    return best(0, len(points) - 1)


def matrix_chain_knuth(dims: list) -> int:
    """Thinking Problem 3: Knuth's narrowed split range applied to matrix-chain order. Plausible, and WRONG:
    the last step's cost depends on the split, so the best splits need not move monotonically."""
    n = len(dims) - 1
    if n <= 1:
        return 0
    cost = [[0] * (n + 1) for _ in range(n + 1)]
    opt = [[i] * (n + 1) for i in range(n + 1)]
    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            cost[i][j] = None
            for k in range(opt[i][j - 1], min(opt[i + 1][j], j - 1) + 1):
                c = cost[i][k] + cost[k + 1][j] + dims[i - 1] * dims[k] * dims[j]
                if cost[i][j] is None or c <= cost[i][j]:
                    cost[i][j], opt[i][j] = c, k
    return cost[1][n]


if __name__ == "__main__":
    print(cut_beam(10, [2, 4, 7]), cut_beam_brute(10, [2, 4, 7]))
    from ch19_examples import matrix_chain
    print(matrix_chain([1, 3, 2, 4, 5])[0], matrix_chain_knuth([1, 3, 2, 4, 5]), matrix_chain([1, 3, 2, 4, 5])[3])
