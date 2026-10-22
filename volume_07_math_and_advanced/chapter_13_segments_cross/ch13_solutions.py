"""Volume 7, Chapter 13 - Thinking Problem 2: count the crossings of horizontal and vertical streets in O(n log n).

Run:  python3 ch13_solutions.py
"""

from __future__ import annotations

import bisect


def count_grid_crossings(horizontals, verticals) -> int:
    """horizontals: (y, x1, x2) with x1 <= x2; verticals: (x, y1, y2) with y1 <= y2.
    Counts the pairs (horizontal, vertical) that share a point, touching ends included."""
    ys = sorted({y for y, _, _ in horizontals})
    tree = [0] * (len(ys) + 1)                      # a Fenwick tree over the heights (Volume 3)

    def add(i, delta):
        i += 1
        while i <= len(ys):
            tree[i] += delta
            i += i & -i

    def below(i):                                   # how many open horizontals have height index < i
        total = 0
        while i > 0:
            total += tree[i]
            i -= i & -i
        return total

    events = [(x1, 0, y, 0) for y, x1, _ in horizontals] + [(x2, 2, y, 0) for y, _, x2 in horizontals]
    events += [(x, 1, y1, y2) for x, y1, y2 in verticals]   # at equal x: open, then ask, then close
    events.sort()
    count = 0
    for _, kind, a, b in events:
        if kind == 1:
            count += below(bisect.bisect_right(ys, b)) - below(bisect.bisect_left(ys, a))
        else:
            add(bisect.bisect_left(ys, a), 1 if kind == 0 else -1)
    return count


if __name__ == "__main__":
    streets = [(1, 0, 6), (3, 2, 8), (5, 0, 4)]
    avenues = [(1, 0, 5), (3, 2, 6), (7, 0, 2)]
    print(count_grid_crossings(streets, avenues))
