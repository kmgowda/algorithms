"""Volume 5, Chapter 21 - Thinking Problems.

Problem 1: T(n) = 2 T(n/2) + n with T(1) = 0 is exactly n log2 n for powers of two (checked with solve).
Problem 2: predict how the running time grows when n doubles, from a, b, d alone; compare with exact values.
Problem 3: T(n) = 2 T(n/2) + n log n is n log^2 n, not n log n: the doubling ratio keeps creeping above 2.
"""

from __future__ import annotations

import math

from ch21_examples import solve


def predicted_ratio(a: int, b: int, d: float) -> float:
    """T(2n) / T(n) for large n when T(n) = a T(n/b) + n^d: 2^max(d, log_b a) (times a slowly vanishing log factor)."""
    return 2 ** max(d, math.log(a, b))


def doubling_ratio(n: int, a: int, b: int, f) -> float:
    terms = [b] * a
    return solve(2 * n, terms, f, 0.0) / solve(n, terms, f, 0.0)


if __name__ == "__main__":
    print([solve(2 ** k, [2, 2], lambda n: n, 0.0) for k in range(1, 6)])
    for a, b, d in ((1, 2, 0), (2, 2, 1), (4, 2, 1), (3, 2, 1), (2, 2, 2)):
        print(a, b, d, predicted_ratio(a, b, d), round(doubling_ratio(2 ** 16, a, b, lambda n, d=d: n ** d), 3))
    print([round(doubling_ratio(2 ** k, 2, 2, lambda n: n * math.log2(n)), 3) for k in (8, 12, 16, 20)])
