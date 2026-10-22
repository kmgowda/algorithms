"""Volume 6, Chapter 15 - Thinking Problems.

Problem 1: on an open r x c floor, the routes number C(r + c - 2, r - 1) (checked against count_paths).
Problem 2: routes that must pass the reading lamp at (lr, lc): routes to it times routes from it.
Problem 3: an empty floor used to crash count_paths and cheapest; they now answer 0 and refuse, respectively.
"""

from __future__ import annotations

from ch15_examples import count_paths


def paths_through(floor: list, lr: int, lc: int) -> int:
    if floor[lr][lc]:
        return 0
    to_lamp = count_paths([row[:lc + 1] for row in floor[:lr + 1]])[0]
    from_lamp = count_paths([row[lc:] for row in floor[lr:]])[0]
    return to_lamp * from_lamp


def brute_through(floor: list, lr: int, lc: int) -> int:
    rows, cols = len(floor), len(floor[0])

    def go(r, c, seen):
        if r >= rows or c >= cols or floor[r][c]:
            return 0
        seen = seen or (r, c) == (lr, lc)
        if (r, c) == (rows - 1, cols - 1):
            return 1 if seen else 0
        return go(r + 1, c, seen) + go(r, c + 1, seen)
    return go(0, 0, False)


if __name__ == "__main__":
    from ch15_examples import FLOOR
    print(count_paths([[0] * 5 for _ in range(4)])[0], paths_through(FLOOR, 2, 2), brute_through(FLOOR, 2, 2), count_paths(FLOOR)[0])
