"""Volume 2, Chapter 21 - Thinking Problem solutions (Section 21.16)."""

from __future__ import annotations


def count_divisible(values: list[int], k: int) -> int:
    """Thinking Problem 21.2: how many stretches have a total divisible by k (k >= 1), in O(n + k).

    Two prefixes with the same remainder mod k bound such a stretch, so count the pairs per remainder."""
    tally = [0] * k
    tally[0] = 1                        # the empty prefix P[0] = 0
    running = count = 0
    for v in values:
        running = (running + v) % k     # Python's % is never negative
        count += tally[running]          # pair with every earlier prefix of the same remainder
        tally[running] += 1
    return count


def grid_bookings(bookings, rows: int, cols: int, marks: int = 4) -> list[list[int]]:
    """Thinking Problem 21.3: add c to every block (r1, c1, r2, c2, c), then a 2-D running total.

    marks=4 is correct (inclusion-exclusion); marks=2 is the buggy version with only two corner marks."""
    d = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r1, c1, r2, c2, c in bookings:
        d[r1][c1] += c
        d[r2 + 1][c2 + 1] += -c if marks == 2 else c
        if marks == 4:
            d[r1][c2 + 1] -= c
            d[r2 + 1][c1] -= c
    out = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            out[r][c] = d[r][c] + (out[r - 1][c] if r else 0) + (out[r][c - 1] if c else 0) \
                - (out[r - 1][c - 1] if r and c else 0)
    return out
