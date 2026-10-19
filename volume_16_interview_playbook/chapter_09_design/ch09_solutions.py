"""Volume 16, Chapter 9 - Solutions to the exercises."""

from __future__ import annotations

import heapq


class MedianFinder:
    """Exercise 1 (LeetCode 295): a max-heap for the lower half and a min-heap for the upper half (V7-C3)."""

    def __init__(self) -> None:
        self.low: list[int] = []      # negated values: a max-heap
        self.high: list[int] = []

    def add(self, x: int) -> None:
        heapq.heappush(self.low, -x)
        heapq.heappush(self.high, -heapq.heappop(self.low))
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def median(self) -> float:
        if len(self.low) > len(self.high):
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2


class HitCounter:
    """Exercise 2 (LeetCode 362): hits in the past 300 seconds - one bucket per second of a ring buffer."""

    def __init__(self, window: int = 300) -> None:
        self.window = window
        self.times = [0] * window
        self.counts = [0] * window

    def hit(self, t: int) -> None:
        i = t % self.window
        if self.times[i] != t:
            self.times[i], self.counts[i] = t, 0
        self.counts[i] += 1

    def hits(self, t: int) -> int:
        return sum(c for ts, c in zip(self.times, self.counts) if t - ts < self.window)


class Flatten2D:
    """Exercise 3 (LeetCode 251): iterate a list of lists, skipping empty inner lists."""

    def __init__(self, rows: list[list[int]]) -> None:
        self.rows, self.r, self.c = rows, 0, 0

    def has_next(self) -> bool:
        while self.r < len(self.rows) and self.c >= len(self.rows[self.r]):
            self.r, self.c = self.r + 1, 0
        return self.r < len(self.rows)

    def next(self) -> int:
        self.has_next()
        value = self.rows[self.r][self.c]
        self.c += 1
        return value


if __name__ == "__main__":
    m = MedianFinder()
    for x in (5, 2, 8):
        m.add(x)
    f = Flatten2D([[1, 2], [], [3]])
    out = []
    while f.has_next():
        out.append(f.next())
    print(m.median(), out)
