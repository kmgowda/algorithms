"""Volume 3, Chapter 14 - Binary Heaps: companion code for the Thinking Problems (Section 14.16).

Run:  python3 ch14_solutions.py
"""

from __future__ import annotations

import heapq


def push_build_worst(n: int) -> int:
    """Thinking Problem 1: swaps made by pushing n, n-1, ..., 1 into an empty heap, the most any order can cost:
    the sum of floor(log2 i) for i = 1..n, which is (n + 1) L - 2^(L+1) + 2 with L = floor(log2 n)."""
    if n < 1:
        return 0
    L = n.bit_length() - 1
    return (n + 1) * L - 2 ** (L + 1) + 2


def kth_smallest(heap: list, k: int):
    """Thinking Problem 2: the k-th smallest item of a min-heap array, without changing it, in O(k log k).
    A second heap holds the frontier: (value, index) of nodes whose parents have already been taken."""
    if not 1 <= k <= len(heap):
        raise IndexError("k must be between 1 and the heap size")
    frontier = [(heap[0], 0)]
    for _ in range(k - 1):
        _, i = heapq.heappop(frontier)
        for c in (2 * i + 1, 2 * i + 2):
            if c < len(heap):
                heapq.heappush(frontier, (heap[c], c))
    return frontier[0][0]


def pop_first_smaller_child(a: list):
    """Thinking Problem 3: a buggy extract-min that swaps with the LEFT child whenever it is smaller,
    without checking whether the right child is smaller still."""
    top = a[0]
    last = a.pop()
    if a:
        a[0] = last
        i = 0
        while True:
            l, r = 2 * i + 1, 2 * i + 2
            if l < len(a) and a[l] < a[i]:
                c = l
            elif r < len(a) and a[r] < a[i]:
                c = r
            else:
                break
            a[i], a[c] = a[c], a[i]
            i = c
    return top


if __name__ == "__main__":
    print([push_build_worst(n) for n in (1, 5, 7, 100)])
    print(kth_smallest([12, 25, 47, 31, 70, 91, 84, 58, 63], 4))
    a = [1, 5, 3, 9]
    print(pop_first_smaller_child(a), a)
