"""Volume 7, Chapter 1 - Solutions to the exercises."""

from __future__ import annotations

import heapq


def max_priority_order(items: list[tuple[str, int]]) -> list[str]:
    """Exercise 1: highest number first (e.g. biggest donors), using a min-heap with negated priorities."""
    heap = [(-p, i, name) for i, (name, p) in enumerate(items)]
    heapq.heapify(heap)
    return [heapq.heappop(heap)[2] for _ in range(len(heap))]


def boarding_order(passengers: list[tuple[str, str]]) -> list[str]:
    """Exercise 2: airline boarding groups - 'first' before 'business' before 'economy', then by arrival."""
    rank = {"first": 0, "business": 1, "economy": 2}
    heap = [(rank[cls], i, name) for i, (name, cls) in enumerate(passengers)]
    heapq.heapify(heap)
    return [heapq.heappop(heap)[2] for _ in range(len(heap))]


def merge_deadlines(*task_lists: list[tuple[int, str]]) -> list[str]:
    """Exercise 3: several teams each keep tasks sorted by deadline; produce one list by earliest deadline."""
    return [name for _, name in heapq.merge(*task_lists)]


if __name__ == "__main__":
    print(max_priority_order([("Ana", 50), ("Ben", 200), ("Cy", 120)]))
    print(boarding_order([("Ana", "economy"), ("Ben", "first"), ("Cy", "business"), ("Dev", "first")]))
    print(merge_deadlines([(1, "a1"), (5, "a2")], [(2, "b1"), (3, "b2")]))
