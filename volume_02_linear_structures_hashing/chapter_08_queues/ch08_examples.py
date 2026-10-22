"""Volume 2, Chapter 8 - Queues.

Run:  python3 ch08_examples.py
"""

from __future__ import annotations

import timeit


class Queue:
    """First in, first out with a linked list and head and tail pointers: O(1) operations (Figure 8.4)."""

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
    """Section 8.7: one slot each in queue order; unfinished students rejoin at the back.
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


class CircularList:
    """Section 8.7: a circularly linked list. Only `tail` is stored; tail.next is the front, so the ring
    can rotate (move the turn on) by moving one pointer."""

    class _Node:
        def __init__(self, value):
            self.value, self.next = value, None

    def __init__(self):
        self.tail = None
        self.size = 0

    def add_back(self, value) -> None:
        node = CircularList._Node(value)
        if self.tail is None:
            node.next = node                      # a ring of one node links to itself
        else:
            node.next = self.tail.next            # the new node points at the front
            self.tail.next = node
        self.tail = node
        self.size += 1

    def front(self):
        if self.tail is None:
            raise IndexError("front of an empty ring")
        return self.tail.next.value

    def rotate(self) -> None:
        """The front moves to the back: one pointer change, nothing is unlinked."""
        if self.tail is not None:
            self.tail = self.tail.next

    def remove_front(self):
        if self.tail is None:
            raise IndexError("remove from an empty ring")
        front = self.tail.next
        if front is self.tail:
            self.tail = None                      # the last node leaves: the ring is empty
        else:
            self.tail.next = front.next
        self.size -= 1
        return front.value

    def values(self) -> list:
        out = []
        if self.tail is not None:
            node = self.tail.next
            for _ in range(self.size):
                out.append(node.value)
                node = node.next
        return out


def round_robin_circular(needs: dict[str, int]) -> list[tuple[int, str, bool]]:
    """Round robin on a circular list: an unfinished student is rotated, a finished one is removed."""
    left = dict(needs)
    ring = CircularList()
    for s in needs:
        ring.add_back(s)
    slots, t = [], 0
    while ring.size:
        s = ring.front()
        t += 1
        left[s] -= 1
        slots.append((t, s, left[s] == 0))
        if left[s] == 0:
            ring.remove_front()
        else:
            ring.rotate()
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
    print(round_robin_circular({"Ana": 3, "Ben": 1, "Cai": 2}))
    for n in (50_000, 100_000, 200_000):
        a, b = time_front_removal(n)
        print(n, round(a, 3), round(b, 3))
