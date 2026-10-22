"""Volume 7, Chapter 29 - Thinking Problem 2: two branches' K-minimum-values sketches, merged in O(k), estimate the
readers of both branches together and the readers they share, without seeing either stream again.

Run:  python3 ch29_solutions.py
"""

from __future__ import annotations

import random

from ch29_examples import h01


def kmv_sketch(stream, k: int) -> list:
    """The k smallest distinct hash values of a stream, in increasing order (the sketch of Section 29.6)."""
    return sorted(set(h01(x) for x in stream))[:k]


def kmv_estimate(sketch: list, k: int) -> float:
    """Exact when fewer than k values were kept; otherwise (k - 1) / (the k-th smallest)."""
    return float(len(sketch)) if len(sketch) < k else (k - 1) / sketch[k - 1]


def merge_kmv(a: list, b: list, k: int) -> list:
    """The k smallest values of a and b together, by one merge of the two sorted lists."""
    out, i, j = [], 0, 0
    while len(out) < k and (i < len(a) or j < len(b)):
        if j == len(b) or (i < len(a) and a[i] < b[j]):
            v, i = a[i], i + 1
        elif i == len(a) or b[j] < a[i]:
            v, j = b[j], j + 1
        else:
            v, i, j = a[i], i + 1, j + 1
        out.append(v)
    return out


def union_and_shared(a: list, b: list, k: int) -> tuple[float, float]:
    """Estimate (readers of either branch, readers of both) from two k-sketches built with the same hash."""
    both = merge_kmv(a, b, k)
    if not both:
        return 0.0, 0.0
    union = kmv_estimate(both, k)
    in_a, in_b = set(a), set(b)
    shared = sum(1 for v in both if v in in_a and v in in_b)
    return union, union * shared / len(both)


if __name__ == "__main__":
    r = random.Random(29)
    north = [f"card{r.randrange(20000)}" for _ in range(40000)]
    south = [f"card{r.randrange(10000, 30000)}" for _ in range(40000)]
    exact_union, exact_shared = len(set(north) | set(south)), len(set(north) & set(south))
    est = union_and_shared(kmv_sketch(north, 1024), kmv_sketch(south, 1024), 1024)
    print(exact_union, exact_shared, [round(x) for x in est])
