"""Volume 3, Chapter 10 - Circular Queues, Deques, and Monotonic Queues.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations

from collections import deque
from typing import Any, Iterator


class RingBuffer:
    """A fixed-capacity circular queue. The front index wraps around with % capacity.

    Invariants: 0 <= size <= capacity; items live at (front + i) % capacity for i in range(size).
    """

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self._slots: list[Any] = [None] * capacity
        self._front = 0
        self._size = 0

    @property
    def capacity(self) -> int:
        return len(self._slots)

    def __len__(self) -> int:
        return self._size

    def is_full(self) -> bool:
        return self._size == self.capacity

    def enqueue(self, item: Any) -> None:
        if self.is_full():
            raise OverflowError("ring buffer is full")
        back = (self._front + self._size) % self.capacity
        self._slots[back] = item
        self._size += 1

    def dequeue(self) -> Any:
        if self._size == 0:
            raise IndexError("dequeue from empty ring buffer")
        item = self._slots[self._front]
        self._slots[self._front] = None
        self._front = (self._front + 1) % self.capacity
        self._size -= 1
        return item

    def push_overwrite(self, item: Any) -> None:
        """When full, drop the oldest item to make room (like a dashcam keeping the last N minutes)."""
        if self.is_full():
            self.dequeue()
        self.enqueue(item)

    def __iter__(self) -> Iterator[Any]:
        for i in range(self._size):
            yield self._slots[(self._front + i) % self.capacity]


class Deque:
    """A double-ended queue on a growable ring buffer: O(1) amortized at BOTH ends."""

    def __init__(self) -> None:
        self._slots: list[Any] = [None] * 4
        self._front = 0
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def _grow(self) -> None:
        old = [self._slots[(self._front + i) % len(self._slots)] for i in range(self._size)]
        self._slots = old + [None] * len(old)
        self._front = 0

    def push_back(self, item: Any) -> None:
        if self._size == len(self._slots):
            self._grow()
        self._slots[(self._front + self._size) % len(self._slots)] = item
        self._size += 1

    def push_front(self, item: Any) -> None:
        if self._size == len(self._slots):
            self._grow()
        self._front = (self._front - 1) % len(self._slots)
        self._slots[self._front] = item
        self._size += 1

    def pop_front(self) -> Any:
        if not self._size:
            raise IndexError("pop from empty deque")
        item = self._slots[self._front]
        self._slots[self._front] = None
        self._front = (self._front + 1) % len(self._slots)
        self._size -= 1
        return item

    def pop_back(self) -> Any:
        if not self._size:
            raise IndexError("pop from empty deque")
        back = (self._front + self._size - 1) % len(self._slots)
        item = self._slots[back]
        self._slots[back] = None
        self._size -= 1
        return item

    def __iter__(self) -> Iterator[Any]:
        for i in range(self._size):
            yield self._slots[(self._front + i) % len(self._slots)]


# ------------------------------------------------------------------ applications
def recent_readings(readings: list[float], keep: int) -> list[float]:
    """Industry example: a heart monitor shows only the last `keep` readings."""
    buffer = RingBuffer(keep)
    for r in readings:
        buffer.push_overwrite(r)
    return list(buffer)


def is_palindrome_deque(text: str) -> bool:
    """Beginner example: compare letters taken from both ends."""
    d = Deque()
    for ch in text.lower():
        if ch.isalnum():
            d.push_back(ch)
    while len(d) > 1:
        if d.pop_front() != d.pop_back():
            return False
    return True


def sliding_window_max(values: list[int], k: int) -> list[int]:
    """LeetCode 239: the maximum of every window of k items in O(n) with a monotonic deque.

    The deque holds INDEXES whose values are decreasing; the front is the current window's maximum.
    """
    if k < 1:
        raise ValueError("window must be at least 1")
    window: deque[int] = deque()
    result = []
    for i, value in enumerate(values):
        while window and window[0] <= i - k:
            window.popleft()                      # the front fell out of the window
        while window and values[window[-1]] <= value:
            window.pop()                          # smaller items can never be the max again
        window.append(i)
        if i >= k - 1:
            result.append(values[window[0]])
    return result


def peak_traffic_per_hour(cars_per_minute: list[int], window: int = 60) -> list[int]:
    """Industry example: a city traffic dashboard shows the busiest minute of the last hour, every minute."""
    return sliding_window_max(cars_per_minute, window)


def work_stealing(tasks: list[str]) -> tuple[list[str], list[str]]:
    """Industry example: a worker takes its own newest task from the back; a thief steals the oldest from the front."""
    d = Deque()
    for task in tasks:
        d.push_back(task)
    own, stolen = [], []
    while len(d):
        own.append(d.pop_back())
        if len(d):
            stolen.append(d.pop_front())
    return own, stolen


if __name__ == "__main__":
    print("Last 3 heart readings:", recent_readings([72, 75, 80, 78, 90, 85], keep=3))
    print("Deque palindrome:", is_palindrome_deque("Never odd or even"))
    print("Window max (k=3):", sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3))
    print("Peak cars over 3-minute windows:", peak_traffic_per_hour([12, 30, 18, 25, 40, 22, 15], window=3))
    print("Work stealing:", work_stealing(["t1", "t2", "t3", "t4", "t5"]))
