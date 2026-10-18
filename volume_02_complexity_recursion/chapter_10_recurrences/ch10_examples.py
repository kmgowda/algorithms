"""Volume 2, Chapter 10 - Analyzing Recursive Algorithms: Recurrences and the Master Theorem.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations

import math
from functools import lru_cache


# ------------------------------------------------------------------ recurrences evaluated exactly
@lru_cache(maxsize=None)
def t_shrink_by_one(n: int) -> int:
    """T(n) = T(n-1) + 1, T(0) = 0   (factorial, countdown)  -> n."""
    return 0 if n == 0 else t_shrink_by_one(n - 1) + 1


@lru_cache(maxsize=None)
def t_halving(n: int) -> int:
    """T(n) = T(n//2) + 1, T(1) = 0   (binary search, fast power)  -> floor(log2 n)."""
    return 0 if n <= 1 else t_halving(n // 2) + 1


@lru_cache(maxsize=None)
def t_split_and_merge(n: int) -> int:
    """T(n) = 2T(n/2) + n, T(1) = 0   (merge sort)  -> n log2 n when n is a power of 2."""
    return 0 if n <= 1 else t_split_and_merge(n // 2) + t_split_and_merge(n - n // 2) + n


@lru_cache(maxsize=None)
def t_two_halves_constant(n: int) -> int:
    """T(n) = 2T(n/2) + 1, T(1) = 1   (tournament maximum)  -> 2n - 1."""
    return 1 if n <= 1 else t_two_halves_constant(n // 2) + t_two_halves_constant(n - n // 2) + 1


@lru_cache(maxsize=None)
def t_hanoi(n: int) -> int:
    """T(n) = 2T(n-1) + 1, T(0) = 0  -> 2^n - 1."""
    return 0 if n == 0 else 2 * t_hanoi(n - 1) + 1


@lru_cache(maxsize=None)
def t_shrink_by_one_linear_work(n: int) -> int:
    """T(n) = T(n-1) + n, T(0) = 0   (recursion that slices, or selection-style work)  -> n(n+1)/2."""
    return 0 if n == 0 else t_shrink_by_one_linear_work(n - 1) + n


# ------------------------------------------------------------------ unrolling
def unroll_halving(n: int) -> list[str]:
    """Show T(n) = T(n/2) + 1 expanded step by step."""
    lines = []
    k = 0
    while n > 1:
        k += 1
        n //= 2
        lines.append(f"T(n) = T(n/{2 ** k}) + {k}")
    lines.append(f"stops after {k} halvings, so T(n) = {k}")
    return lines


# ------------------------------------------------------------------ recursion trees and the Master Theorem
def level_work(a: int, b: int, d: float, n: int) -> list[float]:
    """Total work on each level of the recursion tree of T(n) = a T(n/b) + n^d.

    Level i has a^i subproblems, each of size n / b^i, each doing (n / b^i)^d work.
    """
    levels = []
    size = float(n)
    count = 1
    while size >= 1:
        levels.append(count * size ** d)
        count *= a
        size /= b
    return levels


def master_theorem(a: int, b: int, d: float) -> str:
    """Solve T(n) = a T(n/b) + Theta(n^d) by comparing d with log_b(a)."""
    if a < 1 or b <= 1 or d < 0:
        raise ValueError("need a >= 1, b > 1, d >= 0")
    def n_to(power: float) -> str:
        return "n" if math.isclose(power, 1) else f"n^{power:.3g}"

    critical = math.log(a, b)
    if math.isclose(d, critical):
        return f"Theta({n_to(d)} log n)" if d != 0 else "Theta(log n)"
    if d > critical:
        return f"Theta({n_to(d)})" if d != 0 else "Theta(1)"
    return f"Theta({n_to(critical)})"


# ------------------------------------------------------------------ divide-and-conquer examples
def tournament_max(values: list[int], low: int = 0, high: int | None = None) -> tuple[int, int]:
    """Largest value by splitting into halves; returns (max, comparisons). T(n) = 2T(n/2) + 1."""
    if high is None:
        high = len(values) - 1
    if low == high:
        return values[low], 0
    middle = (low + high) // 2
    left, c1 = tournament_max(values, low, middle)
    right, c2 = tournament_max(values, middle + 1, high)
    return (left if left >= right else right), c1 + c2 + 1


def merge_sort_counting(values: list[int]) -> tuple[list[int], int]:
    """Preview of Volume 5: sort by splitting, sorting halves, merging. Returns (sorted, items merged)."""
    if len(values) <= 1:
        return list(values), 0
    middle = len(values) // 2
    left, w1 = merge_sort_counting(values[:middle])
    right, w2 = merge_sort_counting(values[middle:])
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, w1 + w2 + len(merged)


def word_count_split(documents: list[str]) -> tuple[dict[str, int], int]:
    """Industry example: split the work in half, count each half, merge the counts (MapReduce style).

    Returns (counts, depth of the split tree).
    """
    if len(documents) <= 1:
        counts: dict[str, int] = {}
        for doc in documents:
            for word in doc.lower().split():
                counts[word] = counts.get(word, 0) + 1
        return counts, 0
    middle = len(documents) // 2
    left, d1 = word_count_split(documents[:middle])
    right, d2 = word_count_split(documents[middle:])
    for word, count in right.items():
        left[word] = left.get(word, 0) + count
    return left, max(d1, d2) + 1


if __name__ == "__main__":
    print("T(n)=T(n-1)+1 at 50:", t_shrink_by_one(50), "| T(n)=T(n/2)+1 at 1024:", t_halving(1024))
    print("T(n)=2T(n/2)+n at 1024:", t_split_and_merge(1024), "= 1024 x 10")
    print("T(n)=2T(n/2)+1 at 1000:", t_two_halves_constant(1000), "| Hanoi T(20):", t_hanoi(20))
    print("\n".join(unroll_halving(16)))
    for a, b, d, name in ((1, 2, 0, "binary search"), (2, 2, 0, "tournament max"), (2, 2, 1, "merge sort"),
                          (3, 2, 1, "Karatsuba"), (4, 2, 1, "naive split multiply"), (1, 2, 1, "halve with linear work")):
        print(f"{name:>22}: a={a} b={b} d={d} -> {master_theorem(a, b, d)} | level work:",
              [round(x) for x in level_work(a, b, d, 16)])
    print("Tournament max:", tournament_max([5, 3, 9, 1, 7, 2, 8, 6]))
    print("Merge sort:", merge_sort_counting([5, 3, 9, 1, 7, 2, 8, 6]))
    print("Word counts:", word_count_split(["the lion", "the zebra", "a lion", "the end"]))
