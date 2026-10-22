"""Volume 6, Chapter 17 - Thinking Problems: model solutions that design an algorithm.

Run:  python3 ch17_solutions.py
"""

from __future__ import annotations


def within_distance(a: str, b: str, k: int):
    """Thinking Problem 2: the edit distance of a and b if it is at most k, else None.
    Fills only the band of cells with |i - j| <= k (every cell outside holds at least |i - j| > k),
    so the cost is O((k + 1) * len(a)) time instead of the whole table."""
    n, m = len(a), len(b)
    if k < 0 or abs(n - m) > k:
        return None
    big = k + 1                                       # stands for "more than k"
    prev = {j: j for j in range(min(m, k) + 1)}       # row 0 inside the band
    for i in range(1, n + 1):
        cur = {}
        for j in range(max(0, i - k), min(m, i + k) + 1):
            if j == 0:
                cur[0] = i
                continue
            pair = prev.get(j - 1, big) + (a[i - 1] != b[j - 1])
            cur[j] = min(pair, prev.get(j, big) + 1, cur.get(j - 1, big) + 1, big)
        prev = cur
    d = prev[m]
    return d if d <= k else None


def cells_filled(n: int, m: int, k: int) -> int:
    """How many cells within_distance fills for lengths n, m and threshold k (row 0 included)."""
    return sum(min(m, i + k) - max(0, i - k) + 1 for i in range(n + 1)) if abs(n - m) <= k else 0


if __name__ == "__main__":
    print(within_distance("PEOMS", "POEMS", 2), within_distance("PEOMS", "POEMS", 1))
    print(within_distance("KITTEN", "SITTING", 3), cells_filled(6, 7, 3), 7 * 8)
