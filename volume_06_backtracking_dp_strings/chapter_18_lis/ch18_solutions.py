"""Volume 6, Chapter 18 - Thinking Problems: model solutions that design an algorithm.

Run:  python3 ch18_solutions.py
"""

from __future__ import annotations

import bisect


def longest_nesting(boxes: list) -> tuple[int, list]:
    """Thinking Problem 2: the longest chain of boxes (width, height), each fitting strictly inside the next.
    Sort by width rising and, for equal widths, height falling; then a strict LIS on the heights. O(n log n).
    Returns (length, one longest chain, smallest box first)."""
    order = sorted(boxes, key=lambda b: (b[0], -b[1]))
    tops, top_index, link = [], [], [-1] * len(order)
    for i, (_, h) in enumerate(order):
        k = bisect.bisect_left(tops, h)
        link[i] = top_index[k - 1] if k else -1
        if k == len(tops):
            tops.append(h); top_index.append(i)
        else:
            tops[k] = h; top_index[k] = i
    chain, i = [], top_index[-1] if top_index else -1
    while i != -1:
        chain.append(order[i])
        i = link[i]
    return len(tops), chain[::-1]


def nesting_table(boxes: list) -> int:
    """The O(n^2) check: longest chain ending at each box, after sorting by width."""
    order = sorted(boxes)
    best = [1] * len(order)
    for i, (w, h) in enumerate(order):
        for j in range(i):
            if order[j][0] < w and order[j][1] < h:
                best[i] = max(best[i], best[j] + 1)
    return max(best, default=0)


if __name__ == "__main__":
    BOXES = [(5, 4), (6, 4), (6, 7), (2, 3), (4, 5), (7, 8), (6, 6)]
    print(longest_nesting(BOXES), nesting_table(BOXES))
