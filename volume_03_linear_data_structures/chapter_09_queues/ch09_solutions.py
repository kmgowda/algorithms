"""Volume 3, Chapter 9 - Solutions to the exercises."""

from __future__ import annotations

from collections import deque
from typing import Any


class QueueStack:
    """Exercise 1 (LeetCode 225): a stack from one queue. push is O(n): rotate the new item to the front."""

    def __init__(self) -> None:
        self._q: deque[Any] = deque()

    def push(self, item: Any) -> None:
        self._q.append(item)
        for _ in range(len(self._q) - 1):
            self._q.append(self._q.popleft())

    def pop(self) -> Any:
        return self._q.popleft()

    def top(self) -> Any:
        return self._q[0]

    def empty(self) -> bool:
        return not self._q


def hot_potato(children: list[str], passes: int) -> str:
    """Exercise 2: pass the potato `passes` times; whoever holds it leaves. Last one wins."""
    circle: deque[str] = deque(children)
    while len(circle) > 1:
        for _ in range(passes):
            circle.append(circle.popleft())
        circle.popleft()
    return circle[0]


def recent_counter(pings: list[int], window: int = 3000) -> list[int]:
    """Exercise 3 (LeetCode 933): for each ping time, how many pings in [t - window, t]?"""
    recent: deque[int] = deque()
    counts = []
    for t in pings:
        recent.append(t)
        while recent[0] < t - window:
            recent.popleft()
        counts.append(len(recent))
    return counts


def first_unique_stream(letters: str) -> list[str]:
    """Exercise 4: after each new letter, the first letter seen exactly once so far ('#' if none)."""
    counts: dict[str, int] = {}
    candidates: deque[str] = deque()
    out = []
    for ch in letters:
        counts[ch] = counts.get(ch, 0) + 1
        candidates.append(ch)
        while candidates and counts[candidates[0]] > 1:
            candidates.popleft()
        out.append(candidates[0] if candidates else "#")
    return out


def average_wait(arrivals: list[int], service_time: int) -> float:
    """Exercise 5: one cashier; each customer takes `service_time`. Average minutes spent waiting."""
    free_at, total = 0, 0
    for arrival in sorted(arrivals):
        start = max(arrival, free_at)
        total += start - arrival
        free_at = start + service_time
    return total / len(arrivals) if arrivals else 0.0


if __name__ == "__main__":
    s = QueueStack()
    for x in (1, 2, 3):
        s.push(x)
    print(s.pop(), s.top(), hot_potato(["Ana", "Ben", "Cy", "Dev", "Eve"], 3))
    print(recent_counter([1, 100, 3001, 3002]), first_unique_stream("aabcbd"), average_wait([0, 1, 2, 10], 3))
