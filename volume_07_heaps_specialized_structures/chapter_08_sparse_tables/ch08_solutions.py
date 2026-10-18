"""Volume 7, Chapter 8 - Solutions to the exercises."""

from __future__ import annotations

from math import gcd

from ch08_examples import SparseTable


def range_max(values: list[int], queries: list[tuple[int, int]]) -> list[int]:
    """Exercise 1: max works too - it is also unaffected by overlap."""
    st = SparseTable(values, max)
    return [int(st.query(a, b)) for a, b in queries]


def range_gcd(values: list[int], queries: list[tuple[int, int]]) -> list[int]:
    """Exercise 2: gcd(x, x) = x, so overlapping blocks are fine."""
    st = SparseTable(values, gcd)
    return [int(st.query(a, b)) for a, b in queries]


def range_sum_disjoint(values: list[int], left: int, right: int) -> int:
    """Exercise 3: SUM is NOT overlap-safe; use disjoint power-of-two blocks instead: O(log n)."""
    st = SparseTable(values, lambda a, b: a + b)
    total, i = 0, left
    for k in range(len(st.table) - 1, -1, -1):
        if i + (1 << k) - 1 <= right:
            total += st.table[k][i]
            i += 1 << k
    return total


def table_cells(n: int) -> int:
    """Exercise 4: memory used - about n log2 n cells."""
    return sum(n - (1 << k) + 1 for k in range(n.bit_length()) if (1 << k) <= n)


if __name__ == "__main__":
    v = [3, 8, 6, 12, 4, 9]
    print(range_max(v, [(0, 2), (1, 5)]), range_gcd([12, 18, 24, 6], [(0, 2), (1, 3)]), range_sum_disjoint(v, 1, 4), table_cells(1000))
