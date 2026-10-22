"""Volume 3, Chapter 6 - Why Binary Search Trees Go Wrong: companion code for the Thinking Problems (Section 6.15).

Run:  python3 ch06_solutions.py
"""

from __future__ import annotations

from math import comb


def depths_without_building(keys) -> tuple[int, int]:
    """Thinking Problem 2: the (height, total comparisons) a plain BST would reach, as insert_all returns,
    in O(n log n) time even for sorted keys, without building the tree. Keys must be distinct.
    A new key hangs below the later-inserted of its two neighbours (predecessor and successor) among the
    keys already present. Deleting keys from a sorted linked list in reverse arrival order finds them."""
    keys = list(keys)
    n = len(keys)
    if n == 0:
        return -1, 0
    order = sorted(range(n), key=lambda i: keys[i])       # O(n log n): positions in sorted order
    rank = [0] * n
    for r, i in enumerate(order):
        rank[i] = r
    prev, nxt = list(range(-1, n - 1)), list(range(1, n + 1))   # a doubly linked list over the ranks
    below, above = [None] * n, [None] * n
    for i in reversed(range(n)):                          # remove keys, latest arrival first
        r = rank[i]
        p, q = prev[r], nxt[r]
        below[i] = order[p] if p >= 0 else None           # neighbours among the keys that arrived before i
        above[i] = order[q] if q < n else None
        if p >= 0:
            nxt[p] = q
        if q < n:
            prev[q] = p
    depth = [0] * n
    for i in range(1, n):                                 # forwards: 1 + the deeper neighbour
        depth[i] = 1 + max(depth[j] for j in (below[i], above[i]) if j is not None)
    return max(depth), sum(depth)


def perfect_orders(k: int) -> int:
    """Thinking Problem 1: insertion orders of 2^k - 1 keys that build the perfect tree."""
    if k <= 1:
        return 1
    n = 2 ** k - 1
    return comb(n - 1, (n - 1) // 2) * perfect_orders(k - 1) ** 2


def middle_then_sorted(n: int) -> list[int]:
    """Thinking Problem 3: the middle key first, then everything else in increasing order."""
    m = n // 2
    return [m] + [k for k in range(n) if k != m]


if __name__ == "__main__":
    from ch06_examples import insert_all
    print(depths_without_building([47, 12, 25, 31, 58, 63, 70]), insert_all([47, 12, 25, 31, 58, 63, 70]))
    print([perfect_orders(k) for k in range(1, 5)], insert_all(middle_then_sorted(1001))[0])
    print(depths_without_building(range(100_000)))
