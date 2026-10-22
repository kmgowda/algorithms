"""Volume 4, Chapter 12 - How Fast Can Sorting Be? The decision-tree lower bound.

Run:  python3 ch12_examples.py
"""

from __future__ import annotations

import itertools
import math


def sort3(a, b, c, path: list | None = None) -> tuple:
    """Sort three items with the decision tree of Figure 12.2: at most 3 comparisons."""
    def less(x, y, nx, ny):
        if path is not None:
            path.append(f"{nx}<{ny}")
        return x < y
    if less(a, b, "a", "b"):
        if less(b, c, "b", "c"):
            return (a, b, c)
        if less(a, c, "a", "c"):
            return (a, c, b)
        return (c, a, b)
    if less(a, c, "a", "c"):
        return (b, a, c)
    if less(b, c, "b", "c"):
        return (b, c, a)
    return (c, b, a)


def every_order_of_three() -> list[tuple]:
    """Each of the 3! = 6 orders of three distinct books: (order, comparisons made, path)."""
    out = []
    for perm in itertools.permutations((12, 25, 31)):
        path = []
        result = sort3(*perm, path)
        assert result == (12, 25, 31)
        out.append((perm, len(path), path))
    return out


def lower_bound(n: int) -> int:
    """Fewest comparisons any comparison sort needs in the worst case: ceil(log2(n!))."""
    return math.ceil(math.lgamma(n + 1) / math.log(2) - 1e-9) if n > 1 else 0


def merge_sort_worst(n: int) -> int:
    """Worst-case comparisons of merge sort: n*ceil(log2 n) - 2**ceil(log2 n) + 1."""
    if n <= 1:
        return 0
    k = math.ceil(math.log2(n))
    return n * k - 2 ** k + 1


def merge_comparisons(a: list) -> int:
    count = 0

    def ms(x):
        nonlocal count
        if len(x) <= 1:
            return x
        m = len(x) // 2
        l, r = ms(x[:m]), ms(x[m:])
        out, i, j = [], 0, 0
        while i < len(l) and j < len(r):
            count += 1
            if l[i] <= r[j]:
                out.append(l[i]); i += 1
            else:
                out.append(r[j]); j += 1
        return out + l[i:] + r[j:]
    ms(list(a))
    return count


def average_depth_sort3() -> float:
    """Average number of comparisons of the Sort3 tree over the six orders: 16 / 6 = 8/3 (Section 12.6)."""
    runs = every_order_of_three()
    return sum(c for _, c, _ in runs) / len(runs)


def min_total_leaf_depth(leaves: int) -> int:
    """Smallest possible sum of leaf depths of a binary tree with this many leaves (Figure 12.4).
    The best tree is as balanced as possible: all leaves on the last two levels."""
    if leaves <= 1:
        return 0
    h = math.ceil(math.log2(leaves))
    return h * leaves + leaves - 2 ** h


def average_lower_bound(n: int) -> float:
    """Fewest comparisons any comparison sort can average over the n! orders of n distinct items."""
    leaves = math.factorial(n)
    return min_total_leaf_depth(leaves) / leaves


def all_distinct_by_sorting(a: list) -> tuple[bool, int]:
    """Element distinctness, upper bound: merge sort, then compare each neighbour pair once.
    Returns (all distinct?, comparisons made)."""
    b = sorted(a)
    comparisons = merge_comparisons(a) + max(0, len(b) - 1)
    return all(b[i] != b[i + 1] for i in range(len(b) - 1)), comparisons


if __name__ == "__main__":
    for row in every_order_of_three():
        print(row)
    for n in (2, 3, 4, 5, 9, 16, 1000, 1_000_000):
        print(n, math.factorial(n) if n < 20 else "-", lower_bound(n), merge_sort_worst(n), round(n * math.log2(n)))
    print(max(merge_comparisons(p) for p in itertools.permutations(range(5))), lower_bound(5))
    print(max(merge_comparisons(p) for p in itertools.permutations(range(4))), lower_bound(4))
    print(average_depth_sort3(), [round(average_lower_bound(n), 3) for n in range(1, 7)])
    print(all_distinct_by_sorting([58, 25, 91, 12, 70, 47, 84, 31, 63]), all_distinct_by_sorting([58, 25, 58]))
