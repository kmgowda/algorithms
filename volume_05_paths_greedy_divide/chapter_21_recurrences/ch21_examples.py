"""Volume 5, Chapter 21 - Recurrences in Practice: predict a divide-and-conquer cost, then count it.

Run:  python3 ch21_examples.py
"""

from __future__ import annotations

import math
import random


def merge_sort(values: list, counter: list) -> list:
    """Merge sort, counting comparisons (Volume 4, Chapter 8)."""
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
    """Work at each level of the tree for T(n) = a T(n/b) + f(n), down to size 1 (Figure 21.2)."""
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


def measured_ratios(sizes, seed: int = 1) -> list:
    """Figure 21.1: (n, comparisons on random data, comparisons / (n log2 n), the estimate n log2 n - 1.2645 n)."""
    rng = random.Random(seed)
    out = []
    for n in sizes:
        c = [0]
        merge_sort([rng.random() for _ in range(n)], c)
        out.append((n, c[0], round(c[0] / (n * math.log2(n)), 3), round(n * math.log2(n) - 1.2645 * n)))
    return out


def worst_order(n: int) -> list:
    """An order of 0..n-1 (n a power of two) on which every merge interleaves its halves: the worst case."""
    if n <= 1:
        return list(range(n))
    left = worst_order(n // 2)
    right = worst_order(n // 2)
    # merge sort sees the evens on the left and the odds on the right, in worst order at every level
    return [2 * v for v in left] + [2 * v + 1 for v in right]


def master_general(a: int, b: int, p: float, k: int = 0) -> str:
    """The general master theorem for T(n) = a T(n/b) + f(n) with f(n) = n^p (log n)^k.
    Compares f with n^(log_b a). Case 3 needs the regularity condition a f(n/b) <= c f(n), c < 1,
    which always holds for such f when p > log_b a. Returns None when f falls in a gap between the cases."""
    e = math.log(a, b)
    if abs(p - e) < 1e-9:
        if k >= 0:
            return f"n^{e:.2f} log^{k + 1} n"
        return None                       # e.g. 2T(n/2) + n / log n: between cases 1 and 2
    if p < e:
        return f"n^{e:.2f}"
    return f"n^{p:.2f} log^{k} n" if k else f"n^{p:.2f}"


def regularity_ratio(a: int, b: int, f, n: int) -> float:
    """a f(n/b) / f(n): case 3 of the master theorem needs this to stay below some c < 1 for large n."""
    return a * f(n / b) / f(n)


def solve(n: int, terms: list, f, base: float = 1.0, memo: dict | None = None) -> float:
    """Exact value of T(n) = sum of T(n // d) over terms (a list of divisors, repeated for a > 1) + f(n), T(n) = base
    for n <= 1. Used to check guesses made by the substitution method."""
    memo = {} if memo is None else memo
    if n <= 1:
        return base
    if n not in memo:
        memo[n] = sum(solve(n // d, terms, f, base, memo) for d in terms) + f(n)
    return memo[n]


def uneven_levels(n: int) -> list:
    """Work at each level of T(n) = T(n/3) + T(2n/3) + n (Figure 21.5), splitting a size s into s // 3 and s - s // 3,
    with sizes below 3 as leaves of constant work."""
    levels, sizes = [], [n]
    while sizes:
        levels.append(sum(sizes))
        nxt = []
        for s in sizes:
            if s >= 3:
                nxt += [s // 3, s - s // 3]
        sizes = nxt
    return levels


def akra_bazzi_p(terms: list) -> float:
    """The exponent p with sum(a * b^p) = 1 for T(n) = sum a T(b n) + f(n), terms = [(a, b)], found by bisection."""
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if sum(a * b ** mid for a, b in terms) > 1:
            lo = mid
        else:
            hi = mid
    return round((lo + hi) / 2, 3)


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
