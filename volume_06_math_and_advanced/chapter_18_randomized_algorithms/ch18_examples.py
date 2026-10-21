"""Volume 6, Chapter 18 - Randomized Algorithms: random choices that make bad cases unlikely (Las Vegas)
or answers almost certainly right (Monte Carlo).

Run:  python3 ch18_examples.py
"""

from __future__ import annotations

import random


def quickselect(values: list, k: int, rng, pivot: str = "random") -> tuple:
    """The k-th smallest (k from 0), counting comparisons. pivot = 'first' or 'random' (Figure 18.2)."""
    if not 0 <= k < len(values):
        raise ValueError("k must be at least 0 and below the number of values")
    a, comparisons = list(values), 0
    while True:
        p = a[0] if pivot == "first" else a[rng.randrange(len(a))]
        less = [x for x in a if x < p]
        equal = [x for x in a if x == p]
        comparisons += len(a)
        if k < len(less):
            a = less
        elif k < len(less) + len(equal):
            return p, comparisons
        else:
            k -= len(less) + len(equal)
            a = [x for x in a if x > p]


def matmul(A, B):
    return [[sum(A[i][t] * B[t][j] for t in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def freivalds(A, B, C, rounds: int, rng) -> bool:
    """Monte Carlo check of A x B = C (Figure 18.3): multiply by a random 0/1 vector instead of multiplying matrices.
    A 'no' is certain; a 'yes' is wrong with probability at most 1/2 per round."""
    n = len(A)
    for _ in range(rounds):
        r = [rng.randrange(2) for _ in range(n)]
        Br = [sum(B[i][j] * r[j] for j in range(n)) for i in range(n)]
        ABr = [sum(A[i][j] * Br[j] for j in range(n)) for i in range(n)]
        Cr = [sum(C[i][j] * r[j] for j in range(n)) for i in range(n)]
        if ABr != Cr:
            return False
    return True


if __name__ == "__main__":
    rng = random.Random(18)
    pile = [58, 25, 91, 12, 70, 47, 84, 31, 63]
    print(quickselect(pile, 4, rng), quickselect(pile, 4, rng, "first"))
    sorted_list = list(range(2000))
    print(quickselect(sorted_list, 1000, rng, "first")[1], quickselect(sorted_list, 1000, rng)[1])
    A = [[1, 2], [3, 4]]; B = [[5, 6], [7, 8]]; C = matmul(A, B); bad = [[19, 22], [43, 51]]
    print(C, freivalds(A, B, C, 10, rng), freivalds(A, B, bad, 10, rng))
    fooled = sum(freivalds(A, B, bad, 1, random.Random(s)) for s in range(1000))
    print(fooled)
