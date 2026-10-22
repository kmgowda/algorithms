"""Volume 5, Chapter 27 - Thinking Problems.

Problem 1: max_dc makes exactly n - 1 comparisons, like the greedy scan, for every n >= 1 (checked).
Problem 2: the best stretch together with where it starts and ends, in one greedy pass.
Problem 3: max_dc on an empty list used to recurse for ever; it now refuses the input.
"""

from __future__ import annotations


def best_stretch_where(values: list) -> tuple[int, int, int]:
    """(best total, first index, last index) of the best non-empty stretch."""
    if not values:
        raise ValueError("no stretch in an empty list")
    run, start = values[0], 0
    best = (values[0], 0, 0)
    for i in range(1, len(values)):
        if run < 0:
            run, start = values[i], i
        else:
            run += values[i]
        if run > best[0]:
            best = (run, start, i)
    return best


if __name__ == "__main__":
    print(best_stretch_where([-2, 5, -1, 4, -7, 3]), best_stretch_where([-4, -1, -3]))
