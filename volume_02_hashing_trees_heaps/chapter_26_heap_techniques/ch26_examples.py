"""Volume 2, Chapter 26 - Heap Techniques.

Run:  python3 ch26_examples.py
"""

from __future__ import annotations

import heapq
import random


def heapify(a: list) -> int:
    """Bottom-up heap construction in place: sift down every parent, last first (Figure 26.1).
    Returns the number of swaps."""
    swaps = 0
    n = len(a)
    for start in range(n // 2 - 1, -1, -1):
        i = start
        while True:
            small, l, r = i, 2 * i + 1, 2 * i + 2
            if l < n and a[l] < a[small]:
                small = l
            if r < n and a[r] < a[small]:
                small = r
            if small == i:
                break
            a[i], a[small] = a[small], a[i]
            swaps += 1
            i = small
    return swaps


def top_k(stream, k: int) -> list:
    """The k largest items with a min-heap of size k: the smallest of the best k sits on top (Figure 26.3)."""
    best: list = []
    for x in stream:
        if len(best) < k:
            heapq.heappush(best, x)
        elif best and x > best[0]:
            heapq.heapreplace(best, x)        # the weakest of the k leaves
    return sorted(best, reverse=True)


def merge_k(lists: list[list]) -> list:
    """Merge k sorted lists with a heap holding one front item from each list (Figure 26.4)."""
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapq.heapify(heap)
    out = []
    while heap:
        v, i, j = heapq.heappop(heap)
        out.append(v)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return out


class RunningMedian:
    """Two heaps: a max-heap of the smaller half and a min-heap of the larger half (Figure 26.6)."""

    def __init__(self):
        self.low: list = []      # max-heap via negated values
        self.high: list = []     # min-heap

    def add(self, x) -> None:
        if not self.low or x <= -self.low[0]:
            heapq.heappush(self.low, -x)
        else:
            heapq.heappush(self.high, x)
        if len(self.low) > len(self.high) + 1:
            heapq.heappush(self.high, -heapq.heappop(self.low))
        elif len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def median(self):
        if len(self.low) > len(self.high):
            return -self.low[0]
        return (-self.low[0] + self.high[0]) / 2


def height_sum(n: int) -> int:
    """The most swaps heapify can make on n items: the sum of every node's height (Section 26.4, Why it works).
    It always equals n minus the number of 1-bits in n, so it is below n."""
    total = 0
    for i in range(n):
        h, j = 0, i
        while 2 * j + 1 < n:            # in a complete tree the leftmost path is the longest
            j, h = 2 * j + 1, h + 1
        total += h
    return total


def k_smallest(stream, k: int) -> list:
    """The mirror rule: the k smallest items with a MAX-heap of size k (negated values in heapq)."""
    best: list = []
    for x in stream:
        if len(best) < k:
            heapq.heappush(best, -x)
        elif best and x < -best[0]:
            heapq.heapreplace(best, -x)       # the largest of the k leaves
    return sorted(-v for v in best)


def join_cost(lengths) -> tuple[int, list]:
    """Pop, change, push: repeatedly join the two shortest pieces; each join costs their combined length.
    Returns (total cost, list of joins) (Figure 26.5). The same greedy loop builds Huffman codes (Volume 4, Chapter 16)."""
    heap = list(lengths)
    heapq.heapify(heap)
    total, joins = 0, []
    while len(heap) > 1:
        a, b = heapq.heappop(heap), heapq.heappop(heap)
        total += a + b
        joins.append((a, b, a + b))
        heapq.heappush(heap, a + b)
    return total, joins


if __name__ == "__main__":
    a = [70, 63, 58, 47, 31, 25, 12]
    print(heapify(a), a)
    rng = random.Random(1)
    big = [rng.random() for _ in range(1_000_000)]
    print("swaps for 1,000,000:", heapify(big))
    scores = [72, 95, 41, 88, 60, 99, 77, 83]
    print(top_k(scores, 3))
    print(merge_k([[12, 47, 84], [25, 31, 91], [58, 63, 70]]))
    rm = RunningMedian()
    meds = []
    for x in [5, 15, 1, 3, 8, 7, 9]:
        rm.add(x)
        meds.append(rm.median())
    print(meds)
    print("height sums", [height_sum(n) for n in (7, 15, 31)], height_sum(1_000_000))
    print(k_smallest([7, 2, 9, 4, 1, 8], 3))
    print(join_cost([4, 3, 2, 6]), join_cost([1, 2, 3, 4]))
