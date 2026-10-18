"""Volume 7, Chapter 2 - Binary Heaps: Sift Up, Sift Down, Heapify, and Changing Priorities.

A min-heap in a list: parent of i is (i-1)//2, children are 2i+1 and 2i+2; every parent <= its children.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations

from typing import Any, Hashable


class MinHeap:
    """A min-heap of (priority, item) pairs that ALSO supports changing an item's priority.
    A dictionary remembers where each item sits in the list (an 'index map')."""

    def __init__(self) -> None:
        self._data: list[tuple[float, Hashable]] = []
        self._where: dict[Hashable, int] = {}

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, item: Hashable) -> bool:
        return item in self._where

    def _swap(self, i: int, j: int) -> None:
        self._data[i], self._data[j] = self._data[j], self._data[i]
        self._where[self._data[i][1]] = i
        self._where[self._data[j][1]] = j

    def _sift_up(self, i: int) -> None:
        """A new or improved item climbs while it's smaller than its parent. O(log n)."""
        while i > 0:
            parent = (i - 1) // 2
            if self._data[i][0] >= self._data[parent][0]:
                return
            self._swap(i, parent)
            i = parent

    def _sift_down(self, i: int) -> None:
        """An item that got bigger sinks below its smaller child. O(log n)."""
        n = len(self._data)
        while True:
            smallest, left, right = i, 2 * i + 1, 2 * i + 2
            if left < n and self._data[left][0] < self._data[smallest][0]:
                smallest = left
            if right < n and self._data[right][0] < self._data[smallest][0]:
                smallest = right
            if smallest == i:
                return
            self._swap(i, smallest)
            i = smallest

    def push(self, item: Hashable, priority: float) -> None:
        if item in self._where:
            raise KeyError(f"{item!r} already in heap; use change_priority")
        self._data.append((priority, item))
        self._where[item] = len(self._data) - 1
        self._sift_up(len(self._data) - 1)

    def peek(self) -> tuple[Hashable, float]:
        priority, item = self._data[0]
        return item, priority

    def pop(self) -> tuple[Hashable, float]:
        """Remove the smallest: move the last item to the root, then sift it down."""
        if not self._data:
            raise IndexError("pop from empty heap")
        self._swap(0, len(self._data) - 1)
        priority, item = self._data.pop()
        del self._where[item]
        if self._data:
            self._sift_down(0)
        return item, priority

    def change_priority(self, item: Hashable, priority: float) -> None:
        """Decrease-key or increase-key in O(log n): find the item via the index map, then sift."""
        i = self._where[item]
        old = self._data[i][0]
        self._data[i] = (priority, item)
        if priority < old:
            self._sift_up(i)
        else:
            self._sift_down(i)

    def remove(self, item: Hashable) -> None:
        """Delete any item: swap it with the last, shrink, then fix the moved item up or down."""
        i = self._where[item]
        last = len(self._data) - 1
        self._swap(i, last)
        self._data.pop()
        del self._where[item]
        if i < len(self._data):
            self._sift_up(i)
            self._sift_down(i)

    def is_valid(self) -> bool:
        ok_order = all(self._data[(i - 1) // 2][0] <= self._data[i][0] for i in range(1, len(self._data)))
        ok_index = all(self._where[item] == i for i, (_, item) in enumerate(self._data))
        return ok_order and ok_index and len(self._where) == len(self._data)


def heapify(values: list[Any]) -> list[Any]:
    """Bottom-up heap construction in O(n): sift down every parent, last parent first (V5-C7)."""
    a = list(values)
    n = len(a)
    for start in range(n // 2 - 1, -1, -1):
        i = start
        while True:
            smallest, left, right = i, 2 * i + 1, 2 * i + 2
            if left < n and a[left] < a[smallest]:
                smallest = left
            if right < n and a[right] < a[smallest]:
                smallest = right
            if smallest == i:
                break
            a[i], a[smallest] = a[smallest], a[i]
            i = smallest
    return a


def ride_hailing(requests: list[tuple[str, float]], updates: list[tuple[str, float]]) -> list[str]:
    """Industry example: drivers waiting by distance to a rider; distances change as cars move (change_priority)."""
    heap = MinHeap()
    for driver, km in requests:
        heap.push(driver, km)
    for driver, km in updates:
        heap.change_priority(driver, km)
    return [heap.pop()[0] for _ in range(len(heap))]


if __name__ == "__main__":
    h = MinHeap()
    for name, p in [("cut", 3), ("sprain", 4), ("chest pain", 1), ("fever", 3)]:
        h.push(name, p)
    h.change_priority("sprain", 0)           # the sprain turns out to be a broken bone
    print([h.pop() for _ in range(len(h))])
    print(heapify([9, 4, 7, 1, 8, 2, 6]))
    print(ride_hailing([("Ana", 2.5), ("Ben", 1.2), ("Cy", 4.0)], [("Cy", 0.8), ("Ben", 3.0)]))
