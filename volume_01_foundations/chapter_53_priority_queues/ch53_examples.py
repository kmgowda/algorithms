"""Volume 1, Chapter 53 - Priority Queues.

Run:  python3 ch53_examples.py
"""

from __future__ import annotations

import bisect
import heapq
import itertools
import random
import timeit


class UnsortedPQ:
    """Add in O(1); serve by scanning for the smallest in O(n) (Figure 53.2, top)."""

    def __init__(self):
        self.items = []

    def insert(self, priority, item=None):
        self.items.append((priority, item))

    def extract_min(self):
        i = min(range(len(self.items)), key=lambda j: self.items[j][0])
        self.items[i], self.items[-1] = self.items[-1], self.items[i]
        return self.items.pop()


class SortedPQ:
    """Insert in order in O(n); serve from the front in O(1) (Figure 53.2, bottom). Stored in reverse."""

    def __init__(self):
        self.items = []
        self._count = itertools.count()

    def insert(self, priority, item=None):
        bisect.insort(self.items, (-priority, -next(self._count), item))

    def extract_min(self):
        p, _, item = self.items.pop()
        return -p, item


class FairHeapPQ:
    """A heap-based priority queue whose ties are served in arrival order (Section 53.7)."""

    def __init__(self):
        self.heap = []
        self._ticket = itertools.count()

    def insert(self, priority, item=None):
        heapq.heappush(self.heap, (priority, next(self._ticket), item))

    def extract_min(self):
        p, _, item = heapq.heappop(self.heap)
        return p, item

    def __len__(self):
        return len(self.heap)


def finish_times(jobs: list[int]) -> list[int]:
    out, t = [], 0
    for j in jobs:
        t += j
        out.append(t)
    return out


def shortest_first(jobs: list[int]) -> list[int]:
    """Section 53.8: print the shortest waiting job next (ties by arrival)."""
    pq = FairHeapPQ()
    for j in jobs:
        pq.insert(j, j)
    return [pq.extract_min()[1] for _ in range(len(jobs))]


def time_all(n: int = 20_000, seed: int = 1) -> dict[str, float]:
    pr = [random.Random(seed).randint(1, 10 ** 6) for _ in range(n)]
    out = {}
    for name, cls in (("unsorted list", UnsortedPQ), ("sorted list", SortedPQ), ("binary heap", FairHeapPQ)):
        def run():
            q = cls()
            for p in pr:
                q.insert(p)
            for _ in range(n):
                q.extract_min()
        out[name] = round(min(timeit.repeat(run, number=1, repeat=2)) * 1000, 1)
    return out


if __name__ == "__main__":
    pq = FairHeapPQ()
    for name, pri in (("Ana", 3), ("Ben", 1), ("Cai", 2), ("Dev", 3)):
        pq.insert(pri, name)
    print([pq.extract_min()[1] for _ in range(4)])
    jobs = [300, 1, 12, 2, 45]
    a, s = finish_times(jobs), finish_times(shortest_first(jobs))
    print(a, sum(a) / 5, s, sum(s) / 5)
    print(time_all(5000))
