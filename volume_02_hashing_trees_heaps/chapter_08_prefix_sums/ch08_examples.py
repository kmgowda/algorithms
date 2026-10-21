"""Volume 2, Chapter 8 - Prefix Sums and Difference Arrays.

Run:  python3 ch08_examples.py
"""

from __future__ import annotations

import random

VISITS = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]


def prefix_sums(values: list[int]) -> list[int]:
    """P[i] = total of the first i values, with P[0] = 0 (Figure 8.1)."""
    p = [0]
    for v in values:
        p.append(p[-1] + v)
    return p


def range_sum(p: list[int], a: int, b: int) -> int:
    """Total of values[a..b] inclusive, in O(1): P[b + 1] - P[a]."""
    return p[b + 1] - p[a]


def chairs_in_use(bookings: list[tuple[int, int, int]], hours: int) -> list[int]:
    """Two marks per booking (a, b, chairs), then one running total (Figure 8.3)."""
    d = [0] * (hours + 1)
    for a, b, c in bookings:
        d[a] += c
        d[b + 1] -= c
    out, running = [], 0
    for i in range(hours):
        running += d[i]
        out.append(running)
    return out


def count_stretches_with_sum(values: list[int], k: int) -> int:
    """How many stretches sum to exactly k: prefixes plus the complement pattern (Section 8.4)."""
    seen, running, count = {0: 1}, 0, 0
    for v in values:
        running += v
        count += seen.get(running - k, 0)
        seen[running] = seen.get(running, 0) + 1
    return count


def grid_prefix(g: list[list[int]]) -> list[list[int]]:
    """P[r][c] = total of the rectangle above-left of (r, c) (Figure 8.4)."""
    rows, cols = len(g), len(g[0])
    p = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r in range(rows):
        for c in range(cols):
            p[r + 1][c + 1] = g[r][c] + p[r][c + 1] + p[r + 1][c] - p[r][c]
    return p


def block_sum(p, r1, c1, r2, c2) -> int:
    """Total of rows r1..r2 and columns c1..c2, by inclusion-exclusion."""
    return p[r2 + 1][c2 + 1] - p[r1][c2 + 1] - p[r2 + 1][c1] + p[r1][c1]


if __name__ == "__main__":
    p = prefix_sums(VISITS)
    print(p, range_sum(p, 3, 7), range_sum(p, 0, 4), range_sum(p, 6, 9))
    print(chairs_in_use([(1, 4, 2), (3, 6, 1), (0, 2, 3)], 10), count_stretches_with_sum(VISITS, 10))
    g = [[1, 0, 2], [0, 3, 1], [2, 1, 0]]
    gp = grid_prefix(g)
    print(block_sum(gp, 1, 1, 2, 2), block_sum(gp, 0, 0, 1, 1))
    rng = random.Random(1)
    week = [(a, min(97, a + rng.randint(0, 5)), rng.randint(1, 4)) for a in (rng.randrange(98) for _ in range(2000))]
    use = chairs_in_use(week, 98)
    print(max(use), use.index(max(use)))
