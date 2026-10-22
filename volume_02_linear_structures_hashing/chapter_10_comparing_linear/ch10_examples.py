"""Volume 2, Chapter 10 - Comparing Linear Structures.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations

import collections
import timeit


class _Node:
    __slots__ = ("value", "next")

    def __init__(self, value, next=None):
        self.value, self.next = value, next


def time_operations(n: int = 50_000) -> dict[str, float]:
    """Milliseconds for n operations of each kind (Figure 10.3), best of 3."""
    data = list(range(n))
    dq = collections.deque(data)

    def list_front():
        a = []
        for i in range(n):
            a.insert(0, i)

    def deque_front():
        a = collections.deque()
        for i in range(n):
            a.appendleft(i)

    def linked_front():
        head = None
        for i in range(n):
            head = _Node(i, head)

    def list_back():
        a = []
        for i in range(n):
            a.append(i)

    def deque_back():
        a = collections.deque()
        for i in range(n):
            a.append(i)

    def list_read():
        for i in range(0, n, 10):
            data[i]

    def deque_read():
        for i in range(0, n, 10):
            dq[i]

    tests = {"insert at front: Python list": list_front, "insert at front: deque": deque_front,
             "insert at front: linked list": linked_front, "append at back: Python list": list_back,
             "append at back: deque": deque_back, "read every 10th item: Python list": list_read,
             "read every 10th item: deque": deque_read}
    return {k: round(min(timeit.repeat(f, number=1, repeat=3)) * 1000, 2) for k, f in tests.items()}


def front_insert_moves(n: int) -> int:
    """Items shifted by n inserts at the front of an array: 0 + 1 + ... + (n - 1)."""
    return n * (n - 1) // 2


def returns_desk(arrivals: list[int], newest_first: bool) -> list[int]:
    """Shelve all returns with a deque, newest first (stack use) or oldest first (queue use)."""
    d = collections.deque()
    for b in arrivals:
        d.append(b)
    out = []
    while d:
        out.append(d.pop() if newest_first else d.popleft())
    return out


if __name__ == "__main__":
    for k, v in time_operations().items():
        print(f"{k:38s} {v:8.2f} ms")
    print(front_insert_moves(50_000), returns_desk([47, 12, 63], True), returns_desk([47, 12, 63], False))
