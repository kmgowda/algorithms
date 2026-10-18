"""Volume 10, Chapter 7 - Divide and Conquer: Split, Solve, Combine.

Run:  python3 ch07_examples.py
"""

from __future__ import annotations

import math


def merge_sort(values: list[int]) -> list[int]:
    """The model divide-and-conquer algorithm. Split in half, sort each half, merge. T(n) = 2T(n/2) + n = O(n log n)."""
    if len(values) <= 1:                                  # base case: already solved
        return list(values)
    mid = len(values) // 2
    left, right = merge_sort(values[:mid]), merge_sort(values[mid:])   # divide + conquer
    out, i, j = [], 0, 0                                  # combine
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    return out + left[i:] + right[j:]


def total_votes(booths: list[int]) -> int:
    """Beginner example: add up votes the way an election office does - each region adds its halves."""
    if len(booths) == 1:
        return booths[0]
    mid = len(booths) // 2
    return total_votes(booths[:mid]) + total_votes(booths[mid:])


def recursion_tree_work(n: int, a: int, b: int, f) -> list[float]:
    """Work done at each level of the recursion tree for T(n) = a T(n/b) + f(n).
    Level k has a^k subproblems of size n / b^k, each costing f(n / b^k)."""
    levels, k = [], 0
    while n / b ** k >= 1:
        levels.append(a ** k * f(n / b ** k))
        k += 1
    return levels


def power_of_n(e: float) -> str:
    """Readable n^e: '' for e = 0, 'n' for e = 1, otherwise 'n^e' (3 significant digits)."""
    if abs(e) < 1e-9:
        return ""
    if abs(e - 1) < 1e-9:
        return "n"
    return f"n^{e:.3g}"


def master_theorem(a: int, b: int, d: float) -> str:
    """T(n) = a T(n/b) + n^d. Compare d with log_b(a): which part of the tree dominates? (V2-C10)"""
    critical = math.log(a, b)
    if abs(d - critical) < 1e-9:
        return f"Theta({(power_of_n(d) + ' log n').strip()})"
    return f"Theta({power_of_n(max(d, critical)) or '1'})"


def count_calls(n: int, a: int, b: int) -> int:
    """How many subproblems a divide-and-conquer recursion creates (sizes rounded down)."""
    if n <= 1:
        return 1
    return 1 + a * count_calls(n // b, a, b)


def parallel_sum(values: list[int], workers: int) -> tuple[int, list[int]]:
    """Industry example: split a big job across workers (like MapReduce), each sums its chunk, then combine."""
    size = math.ceil(len(values) / workers)
    partial = [sum(values[i:i + size]) for i in range(0, len(values), size)]
    return sum(partial), partial


if __name__ == "__main__":
    print(merge_sort([38, 27, 43, 3, 9, 82, 10]))
    print("votes:", total_votes([120, 340, 95, 410, 230, 180, 75, 300]))
    print("merge sort levels (n=16):", recursion_tree_work(16, 2, 2, lambda m: m))
    for a, b, d in [(2, 2, 1), (1, 2, 0), (4, 2, 1), (3, 2, 1), (8, 2, 2), (7, 2, 2), (2, 2, 2)]:
        print(f"T(n) = {a}T(n/{b}) + n^{d}: {master_theorem(a, b, d)}")
    print("parallel:", parallel_sum(list(range(1, 101)), 4))
