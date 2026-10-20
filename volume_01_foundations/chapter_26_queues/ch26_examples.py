"""Volume 1, Chapter 26 - Queues.

Run:  python3 ch26_examples.py
"""

from __future__ import annotations

import timeit


class Queue:
    """First in, first out with a linked list and head and tail pointers: O(1) operations (Figure 26.4)."""

    class _Node:
        def __init__(self, value):
            self.value, self.next = value, None

    def __init__(self):
        self._head = self._tail = None

    def enqueue(self, value) -> None:
        node = Queue._Node(value)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node

    def dequeue(self):
        if self._head is None:
            raise IndexError("dequeue from an empty queue")
        node = self._head
        self._head = node.next
        if self._head is None:
            self._tail = None
        return node.value

    def is_empty(self) -> bool:
        return self._head is None


def round_robin(needs: dict[str, int]) -> list[tuple[int, str, bool]]:
    """Section 26.7: one slot each in queue order; unfinished students rejoin at the back.
    Returns (slot, student, finished) for every slot."""
    left = dict(needs)
    q = Queue()
    for s in needs:
        q.enqueue(s)
    slots, t = [], 0
    while not q.is_empty():
        s = q.dequeue()
        t += 1
        left[s] -= 1
        slots.append((t, s, left[s] == 0))
        if left[s] > 0:
            q.enqueue(s)
    return slots


def time_front_removal(n: int) -> tuple[float, float]:
    """Seconds to serve n items with list.pop(0) and with the linked Queue."""
    def with_list():
        items = list(range(n))
        while items:
            items.pop(0)

    def with_queue():
        q = Queue()
        for i in range(n):
            q.enqueue(i)
        while not q.is_empty():
            q.dequeue()
    return timeit.timeit(with_list, number=1), timeit.timeit(with_queue, number=1)


if __name__ == "__main__":
    print(round_robin({"Ana": 3, "Ben": 1, "Cai": 2}))
    print(round_robin({"Ana": 2, "Ben": 2, "Cai": 1}))
    for n in (50_000, 100_000, 200_000):
        a, b = time_front_removal(n)
        print(n, round(a, 3), round(b, 3))
