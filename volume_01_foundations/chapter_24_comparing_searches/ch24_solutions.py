"""Volume 1, Chapter 24, Thinking Problem 2: the k-th smallest call number of two sorted branch shelves.

If the answer uses i books from shelf a and k - i from shelf b, then "i is too small" (the next book of a is
smaller than the last book taken from b) is a yes/no question whose answers go yes, ..., yes, no, ..., no.
Binary search on the answer (Chapter 20) finds the first "no" in O(log k) looks at each shelf.
"""
from __future__ import annotations


def kth_of_two(a: list[int], b: list[int], k: int) -> int:
    """The k-th smallest (k = 1 is the smallest) of the two sorted lists taken together."""
    if not 1 <= k <= len(a) + len(b):
        raise ValueError("k must be between 1 and the total number of books")
    lo, hi = max(0, k - len(b)), min(k, len(a))       # books taken from a
    while lo < hi:
        i = (lo + hi) // 2
        if a[i] < b[k - i - 1]:                        # too few from a
            lo = i + 1
        else:
            hi = i
    i = lo
    last_a = a[i - 1] if i > 0 else None
    last_b = b[k - i - 1] if k - i > 0 else None
    return max(x for x in (last_a, last_b) if x is not None)


if __name__ == "__main__":
    print(kth_of_two([12, 31, 58, 70, 91], [25, 47, 63, 84], 5))
