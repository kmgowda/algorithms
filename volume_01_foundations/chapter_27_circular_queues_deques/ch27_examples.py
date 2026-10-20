"""Volume 1, Chapter 27 - Circular Queues and Deques.

Run:  python3 ch27_examples.py
"""

from __future__ import annotations

from collections import deque


class RingBuffer:
    """A queue in a fixed array whose front and back wrap around (Figures 27.1 and 27.2)."""

    def __init__(self, capacity: int):
        self.slots = [None] * capacity
        self.front = self.back = self.count = 0

    def enqueue(self, x) -> None:
        if self.count == len(self.slots):
            raise OverflowError("ring is full")
        self.slots[self.back] = x
        self.back = (self.back + 1) % len(self.slots)
        self.count += 1

    def dequeue(self):
        if self.count == 0:
            raise IndexError("ring is empty")
        x = self.slots[self.front]
        self.slots[self.front] = None
        self.front = (self.front + 1) % len(self.slots)
        self.count -= 1
        return x

    def items(self) -> list:
        return [self.slots[(self.front + k) % len(self.slots)] for k in range(self.count)]


def window_max(values: list[int], k: int) -> list[int]:
    """The maximum of every window of length k, with a deque of decreasing candidates: O(n) (Figure 27.4)."""
    candidates: deque[int] = deque()             # positions, values decreasing front to back
    result = []
    for i, v in enumerate(values):
        while candidates and values[candidates[-1]] <= v:
            candidates.pop()
        candidates.append(i)
        if candidates[0] <= i - k:
            candidates.popleft()
        if i >= k - 1:
            result.append(values[candidates[0]])
    return result


if __name__ == "__main__":
    ring = RingBuffer(8)
    ring.front = ring.back = 2
    for name in ("Ana", "Ben", "Cai", "Dev"):
        ring.enqueue(name)
    ring.dequeue()
    for name in ("Eva", "Fay", "Gus"):
        ring.enqueue(name)
    print(ring.slots, ring.front, ring.back, ring.items())
    print(window_max([3, 1, 4, 1, 5, 9, 2, 6], 3), window_max([5, 3, 8, 1], 2))
