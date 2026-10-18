"""Volume 7, Chapter 1 - Priority Queues: The Hospital Emergency Room.

Run:  python3 ch01_examples.py
"""

from __future__ import annotations

import heapq
import itertools
from typing import Any


class SortedListPQ:
    """Priority queue on a sorted list: pop is O(1), push is O(n) (shifting)."""

    def __init__(self) -> None:
        self._items: list[tuple[int, int, Any]] = []
        self._counter = itertools.count()

    def push(self, item: Any, priority: int) -> None:
        entry = (priority, next(self._counter), item)
        i = len(self._items)
        while i > 0 and self._items[i - 1] > entry:
            i -= 1
        self._items.insert(i, entry)

    def pop(self) -> Any:
        return self._items.pop(0)[2]

    def __len__(self) -> int:
        return len(self._items)


class UnsortedListPQ:
    """Priority queue on an unsorted list: push is O(1), pop is O(n) (search for the minimum)."""

    def __init__(self) -> None:
        self._items: list[tuple[int, int, Any]] = []
        self._counter = itertools.count()

    def push(self, item: Any, priority: int) -> None:
        self._items.append((priority, next(self._counter), item))

    def pop(self) -> Any:
        best = min(range(len(self._items)), key=lambda i: self._items[i])
        return self._items.pop(best)[2]

    def __len__(self) -> int:
        return len(self._items)


class HeapPQ:
    """Priority queue on a binary heap (heapq): push and pop are both O(log n).
    Lower number = higher priority; a counter keeps equal priorities first-come, first-served."""

    def __init__(self) -> None:
        self._heap: list[tuple[int, int, Any]] = []
        self._counter = itertools.count()

    def push(self, item: Any, priority: int) -> None:
        heapq.heappush(self._heap, (priority, next(self._counter), item))

    def pop(self) -> Any:
        if not self._heap:
            raise IndexError("pop from empty priority queue")
        return heapq.heappop(self._heap)[2]

    def peek(self) -> Any:
        return self._heap[0][2]

    def __len__(self) -> int:
        return len(self._heap)


def triage(arrivals: list[tuple[str, int]]) -> list[str]:
    """Beginner example: emergency room order. Level 1 = most urgent; ties go to whoever arrived first."""
    pq = HeapPQ()
    for name, level in arrivals:
        pq.push(name, level)
    return [pq.pop() for _ in range(len(pq))]


def run_jobs(jobs: list[tuple[int, str, int, int]]) -> list[tuple[str, int]]:
    """Industry example: a CPU scheduler. jobs = (arrival, name, priority, duration).
    Whenever the CPU is free, run the most urgent job that has arrived. Returns (name, finish time)."""
    jobs = sorted(jobs)
    pq, clock, i, done = HeapPQ(), 0, 0, []
    while i < len(jobs) or len(pq):
        while i < len(jobs) and jobs[i][0] <= clock:
            arrival, name, priority, duration = jobs[i]
            pq.push((name, duration), priority)
            i += 1
        if not len(pq):
            clock = jobs[i][0]                        # idle until the next arrival
            continue
        name, duration = pq.pop()
        clock += duration
        done.append((name, clock))
    return done


if __name__ == "__main__":
    print(triage([("sprain", 4), ("chest pain", 1), ("cut", 3), ("breathing", 1), ("fever", 3)]))
    print(run_jobs([(0, "backup", 3, 5), (1, "click", 1, 1), (2, "email", 2, 2), (2, "keypress", 1, 1)]))
