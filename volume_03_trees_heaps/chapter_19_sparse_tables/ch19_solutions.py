"""Volume 3, Chapter 19 - Sparse Tables: companion code for the Thinking Problems (Section 19.15).

Run:  python3 ch19_solutions.py
"""

from __future__ import annotations

from ch19_examples import NOISE, SparseTable


def first_at_most(st: SparseTable, a: int, t: int):
    """Thinking Problem 2: the first position >= a whose value is <= t, or None. O(log n) jumps."""
    n = len(st.table[0])
    pos = a
    for k in range(len(st.table) - 1, -1, -1):
        if pos + (1 << k) <= n and st.table[k][pos] > t:   # the whole window is louder than t: jump over it
            pos += 1 << k
    return pos if pos < n else None


def naive_repair(st: SparseTable, i: int, value: int) -> None:
    """Thinking Problem 3, the bug: change value i and recompute only the cells that START at i."""
    st.table[0][i] = value
    for k in range(1, len(st.table)):
        if i < len(st.table[k]):
            st.table[k][i] = min(st.table[k - 1][i], st.table[k - 1][i + (1 << (k - 1))])


def cells_to_repair(n: int, i: int) -> int:
    """Thinking Problem 3, the fix: the number of cells whose window contains position i."""
    total, k = 0, 0
    while (1 << k) <= n:
        total += min(i, n - (1 << k)) - max(0, i - (1 << k) + 1) + 1
        k += 1
    return total


if __name__ == "__main__":
    st = SparseTable(NOISE)
    print(first_at_most(st, 1, 3), first_at_most(st, 6, 4), cells_to_repair(8, 5), cells_to_repair(1024, 512))
