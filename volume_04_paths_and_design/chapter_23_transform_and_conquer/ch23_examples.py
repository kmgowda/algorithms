"""Volume 4, Chapter 23 - Transform and Conquer: change the problem into an easier one first.

Run:  python3 ch23_examples.py
"""

from __future__ import annotations

import heapq
from collections import Counter

# Call numbers of books returned today; is any book returned twice?
RETURNS = [47, 12, 91, 63, 25, 70, 12, 84, 31, 58]


def has_repeat_pairs(values: list, counter: list) -> bool:
    """Compare every pair: n(n - 1)/2 comparisons in the worst case."""
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            counter[0] += 1
            if values[i] == values[j]:
                return True
    return False


def has_repeat_sorted(values: list, counter: list) -> bool:
    """Transform first: sort, then repeats sit next to each other (Figure 23.2)."""
    s = sorted(values)
    for a, b in zip(s, s[1:]):
        counter[0] += 1
        if a == b:
            return True
    return False


def mode(values: list):
    """The most common value: sort, then walk runs of equal values (ties: the smallest)."""
    if not values:
        return None
    s, best, best_len, run = sorted(values), None, 0, 1
    for i in range(1, len(s) + 1):
        if i < len(s) and s[i] == s[i - 1]:
            run += 1
        else:
            if run > best_len:
                best, best_len = s[i - 1], run
            run = 1
    return best


def horner(coeffs: list, x: float, counter: list) -> float:
    """Evaluate c0 x^k + ... + ck by rewriting it as (((c0) x + c1) x + ...) (Figure 23.3): k multiplications."""
    total = 0
    for c in coeffs:
        counter[0] += 1
        total = total * x + c
    return total


def naive_poly(coeffs: list, x: float, counter: list) -> float:
    k, total = len(coeffs) - 1, 0
    for i, c in enumerate(coeffs):
        term = c
        for _ in range(k - i):
            counter[0] += 1
            term *= x
        total += term
    return total


def k_smallest(values: list, k: int) -> list:
    """Transform into a heap (Volume 2), then take k items off the top."""
    h = list(values)
    heapq.heapify(h)
    return [heapq.heappop(h) for _ in range(min(k, len(h)))]


if __name__ == "__main__":
    a, b = [0], [0]
    print(has_repeat_pairs(RETURNS, a), a[0], has_repeat_sorted(RETURNS, b), b[0])
    print(mode([3, 1, 3, 2, 1, 3]), Counter(RETURNS).most_common(1))
    c1, c2 = [0], [0]
    print(horner([2, -6, 2, -1], 3, c1), c1[0], naive_poly([2, -6, 2, -1], 3, c2), c2[0])
    print(k_smallest(RETURNS, 3))
