"""Volume 5, Chapter 18 - Divide and Conquer: split, solve the halves, combine.

Run:  python3 ch18_examples.py
"""

from __future__ import annotations

# Visitors counted at the festival gate, hour by hour.
VISITORS = [12, 7, 21, 15, 3, 18, 9, 26]


def total(values: list, depth: int = 0, log: list | None = None) -> int:
    """Sum by splitting in half (Figure 18.1): each half could be counted by a different volunteer."""
    if log is not None:
        log.append((depth, list(values)))
    if len(values) == 0:
        return 0
    if len(values) == 1:
        return values[0]
    mid = len(values) // 2
    return total(values[:mid], depth + 1, log) + total(values[mid:], depth + 1, log)


def min_max(values: list, counter: list) -> tuple:
    """Smallest and largest together (Figure 18.2): about 3n/2 comparisons instead of 2n - 2."""
    if len(values) == 1:
        return values[0], values[0]
    if len(values) == 2:
        counter[0] += 1
        return (values[0], values[1]) if values[0] < values[1] else (values[1], values[0])
    mid = len(values) // 2
    a_lo, a_hi = min_max(values[:mid], counter)
    b_lo, b_hi = min_max(values[mid:], counter)
    counter[0] += 2
    return min(a_lo, b_lo), max(a_hi, b_hi)


def min_max_simple(values: list, counter: list) -> tuple:
    lo = hi = values[0]
    for v in values[1:]:
        counter[0] += 2
        lo, hi = min(lo, v), max(hi, v)
    return lo, hi


def best_stretch(values: list) -> tuple[int, int, int]:
    """The busiest run of consecutive hours by total (Figures 18.3 and 18.4; values may be negative): best left, best right, or across the middle.
    Returns (total, start, end)."""
    if len(values) == 1:
        return values[0], 0, 0
    mid = len(values) // 2
    left = best_stretch(values[:mid])
    r = best_stretch(values[mid:])
    right = (r[0], r[1] + mid, r[2] + mid)
    best_l, s, run = float("-inf"), mid, 0
    for i in range(mid - 1, -1, -1):
        run += values[i]
        if run > best_l:
            best_l, s = run, i
    best_r, e, run = float("-inf"), mid, 0
    for j in range(mid, len(values)):
        run += values[j]
        if run > best_r:
            best_r, e = run, j
    across = (best_l + best_r, s, e)
    return max(left, right, across, key=lambda t: t[0])


def crossing(values: list, lo: int, mid: int, hi: int) -> int:
    """Section 18.5's Crossing: the best run containing positions mid - 1 and mid."""
    run, best_left = 0, float("-inf")
    for i in range(mid - 1, lo - 1, -1):
        run += values[i]
        best_left = max(best_left, run)
    run, best_right = 0, float("-inf")
    for j in range(mid, hi):
        run += values[j]
        best_right = max(best_right, run)
    return best_left + best_right


def stretch_summary(values: list, lo: int = 0, hi: int | None = None) -> tuple[int, int, int, int]:
    """Challenge 3: (total, best, best touching the left end, best touching the right end) with a constant-time
    combine, so the whole method is O(n)."""
    hi = len(values) if hi is None else hi
    if hi - lo == 1:
        v = values[lo]
        return v, v, v, v
    mid = (lo + hi) // 2
    lt, lb, ll, lr = stretch_summary(values, lo, mid)
    rt, rb, rl, rr = stretch_summary(values, mid, hi)
    return lt + rt, max(lb, rb, lr + rl), max(ll, lt + rl), max(rr, rt + lr)


if __name__ == "__main__":
    log = []
    print(total(VISITORS, 0, log), len(log))
    c1, c2 = [0], [0]
    print(min_max(VISITORS, c1), c1[0], min_max_simple(VISITORS, c2), c2[0])
    changes = [5, -9, 6, -2, 3, -1, 4, -8]
    print(best_stretch(changes))
