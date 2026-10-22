"""Volume 2, Chapter 9 - Thinking Problems.

Problem 1: front and back alone cannot tell c + 1 queue lengths apart (checked by counting states).
Problem 2: the longest stretch of hours whose busiest and quietest differ by at most `limit`, in O(n) with two deques.
Problem 3: the wrong overwriting logger that forgets to move the front, kept here so the tests can show it.
"""

from __future__ import annotations

from collections import deque


def longest_steady_stretch(values: list[int], limit: int) -> int:
    if limit < 0:
        return 0                                # not even one hour differs from itself by less than 0
    high: deque[int] = deque()                  # positions, values decreasing: front is the window's maximum
    low: deque[int] = deque()                   # positions, values increasing: front is the window's minimum
    best, start = 0, 0
    for i, v in enumerate(values):
        while high and values[high[-1]] <= v:
            high.pop()
        high.append(i)
        while low and values[low[-1]] >= v:
            low.pop()
        low.append(i)
        while values[high[0]] - values[low[0]] > limit:
            start += 1                          # shrink from the left until the window is steady again
            if high[0] < start:
                high.popleft()
            if low[0] < start:
                low.popleft()
        best = max(best, i - start + 1)
    return best


class OverwriteRingBuggy:
    """WRONG: when full, it overwrites the oldest entry but forgets to move the front past it."""

    def __init__(self, capacity: int):
        self.slots = [None] * capacity
        self.front = self.back = self.count = 0

    def log(self, x) -> None:
        self.slots[self.back] = x
        self.back = (self.back + 1) % len(self.slots)
        self.count = min(self.count + 1, len(self.slots))   # the fix: if it was full, also move front on

    def oldest(self):
        return self.slots[self.front]


if __name__ == "__main__":
    print(longest_steady_stretch([3, 1, 4, 1, 5, 9, 2, 6], 3))
    r = OverwriteRingBuggy(3)
    for x in "ABCD":
        r.log(x)
    print(r.slots, r.front, r.oldest())
