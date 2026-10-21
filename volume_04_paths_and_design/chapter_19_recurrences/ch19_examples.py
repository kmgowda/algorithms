"""Volume 4, Chapter 19 - Recurrences in Practice: predict a divide-and-conquer cost, then count it.

Run:  python3 ch19_examples.py
"""

from __future__ import annotations

import math


def merge_sort(values: list, counter: list) -> list:
    """Merge sort, counting comparisons (Volume 3, Chapter 11)."""
    if len(values) <= 1:
        return list(values)
    mid = len(values) // 2
    a, b = merge_sort(values[:mid], counter), merge_sort(values[mid:], counter)
    out, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        counter[0] += 1
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    return out + a[i:] + b[j:]


def recursion_tree(n: int, a: int, b: int, f) -> list:
    """Work at each level of the tree for T(n) = a T(n/b) + f(n), down to size 1 (Figure 19.2)."""
    levels, size, count = [], n, 1
    while size >= 1:
        levels.append((count, size, count * f(size)))
        if size == 1:
            break
        size, count = size // b, count * a
    return levels


def master(a: int, b: int, d: int) -> str:
    """The master theorem's verdict for T(n) = a T(n/b) + n^d (Volume 1, Chapter 16)."""
    if a < b ** d:
        return f"n^{d}"
    if a == b ** d:
        return f"n^{d} log n"
    return f"n^{math.log(a, b):.2f}"


def count_calls(n: int, a: int, b: int) -> int:
    """Number of calls when each call on size > 1 makes a calls on size n // b."""
    return 1 if n <= 1 else 1 + a * count_calls(n // b, a, b)


if __name__ == "__main__":
    import random
    for n in (1024, 4096, 16384):
        c = [0]
        merge_sort([random.random() for _ in range(n)], c)
        print(n, c[0], round(n * math.log2(n)))
    print(recursion_tree(16, 2, 2, lambda s: s))
    print(recursion_tree(16, 4, 2, lambda s: s))
    print(recursion_tree(16, 1, 2, lambda s: s))
    print([master(*t) for t in ((2, 2, 1), (4, 2, 1), (1, 2, 1), (3, 2, 1), (1, 2, 0))])
    print(count_calls(16, 2, 2), count_calls(16, 4, 2), count_calls(16, 3, 2), count_calls(16, 1, 2))
