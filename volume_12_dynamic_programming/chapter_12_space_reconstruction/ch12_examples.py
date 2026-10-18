"""Volume 12, Chapter 12 - Space Optimization and Reconstructing Answers.

Run:  python3 ch12_examples.py
"""

from __future__ import annotations

import tracemalloc


def edit_distance_full(a: str, b: str) -> int:
    """The full (m + 1) x (n + 1) table from Chapter 5."""
    d = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        d[i][0] = i
    for j in range(len(b) + 1):
        d[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            d[i][j] = d[i - 1][j - 1] if a[i - 1] == b[j - 1] else 1 + min(d[i - 1][j - 1], d[i - 1][j], d[i][j - 1])
    return d[-1][-1]


def edit_distance_two_rows(a: str, b: str) -> int:
    """Row i only reads row i - 1, so keep just two rows: O(n) memory instead of O(m x n)."""
    if len(a) < len(b):
        a, b = b, a                                      # make the row the shorter string
    prev = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        cur = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            cur[j] = prev[j - 1] if a[i - 1] == b[j - 1] else 1 + min(prev[j - 1], prev[j], cur[j - 1])
        prev = cur
    return prev[-1]


def grid_paths_one_row(rows: int, cols: int) -> int:
    """Grid routes with ONE row: paths[c] += paths[c - 1] (left) - the old paths[c] is the value from above."""
    paths = [1] * cols
    for _ in range(1, rows):
        for c in range(1, cols):
            paths[c] += paths[c - 1]
    return paths[-1]


def peak_memory(func, *args) -> tuple[object, int]:
    """Run func and report the peak bytes it allocated (Python's tracemalloc)."""
    tracemalloc.start()
    result = func(*args)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, peak


def edit_script(a: str, b: str) -> list[str]:
    """Reconstruct the actual edits (needs the full table): walk back from the corner choosing a move that
    explains the cell's value."""
    m, n = len(a), len(b)
    d = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        d[i][0] = i
    for j in range(n + 1):
        d[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            d[i][j] = d[i - 1][j - 1] if a[i - 1] == b[j - 1] else 1 + min(d[i - 1][j - 1], d[i - 1][j], d[i][j - 1])
    ops, i, j = [], m, n
    while i or j:
        if i and j and a[i - 1] == b[j - 1] and d[i][j] == d[i - 1][j - 1]:
            ops.append(f"keep {a[i - 1]}")
            i, j = i - 1, j - 1
        elif i and j and d[i][j] == d[i - 1][j - 1] + 1:
            ops.append(f"replace {a[i - 1]} with {b[j - 1]}")
            i, j = i - 1, j - 1
        elif i and d[i][j] == d[i - 1][j] + 1:
            ops.append(f"delete {a[i - 1]}")
            i -= 1
        else:
            ops.append(f"insert {b[j - 1]}")
            j -= 1
    return ops[::-1]


def coin_change_with_coins(coins: list[int], amount: int) -> list[int] | None:
    """Fewest coins AND which coins: store the coin that achieved each amount's best, then follow it back."""
    INF = amount + 1
    fewest = [0] + [INF] * amount
    last = [0] * (amount + 1)
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and fewest[a - c] + 1 < fewest[a]:
                fewest[a], last[a] = fewest[a - c] + 1, c
    if fewest[amount] > amount:
        return None
    out = []
    while amount:
        out.append(last[amount])
        amount -= last[amount]
    return sorted(out)


def knapsack_one_row_with_items(items: list[tuple[str, int, int]], capacity: int) -> tuple[int, list[str]]:
    """Industry example: one value row is enough for the VALUE; for the ITEMS, keep a small boolean 'took' table
    (1 bit of information per item and capacity) instead of a full table of values."""
    best = [0] * (capacity + 1)
    took = [[False] * (capacity + 1) for _ in items]
    for i, (_, w, v) in enumerate(items):
        for c in range(capacity, w - 1, -1):
            if best[c - w] + v > best[c]:
                best[c] = best[c - w] + v
                took[i][c] = True
    chosen, c = [], capacity
    for i in range(len(items) - 1, -1, -1):
        if took[i][c]:
            chosen.append(items[i][0])
            c -= items[i][1]
    return best[capacity], sorted(chosen)


if __name__ == "__main__":
    a, b = "x" * 1500, "y" * 1500
    full = peak_memory(edit_distance_full, a, b)
    rows = peak_memory(edit_distance_two_rows, a, b)
    print(f"edit distance 1500x1500: full table {full[1] / 1e6:.1f} MB, two rows {rows[1] / 1e3:.1f} KB, answers {full[0]} {rows[0]}")
    print("grid 10x10 with one row:", grid_paths_one_row(10, 10))
    print(edit_script("kitten", "sitting"))
    print("coins for 11:", coin_change_with_coins([1, 2, 5], 11))
    print(knapsack_one_row_with_items([("medicine", 2, 300), ("documents", 1, 120), ("phone", 1, 200), ("laptop", 3, 350)], 5))
