"""Volume 3, Chapter 10 - Solutions to the exercises."""

from __future__ import annotations

from collections import deque

from ch10_examples import RingBuffer


def moving_average(values: list[float], k: int) -> list[float]:
    """Exercise 1 (LeetCode 346 idea): average of the last k values after each new value, O(1) each."""
    buffer = RingBuffer(k)
    total = 0.0
    out = []
    for v in values:
        if buffer.is_full():
            total -= buffer.dequeue()
        buffer.enqueue(v)
        total += v
        out.append(round(total / len(buffer), 2))
    return out


def sliding_window_min(values: list[int], k: int) -> list[int]:
    """Exercise 2: the same monotonic deque, with the comparison flipped (increasing values)."""
    window: deque[int] = deque()
    result = []
    for i, value in enumerate(values):
        while window and window[0] <= i - k:
            window.popleft()
        while window and values[window[-1]] >= value:
            window.pop()
        window.append(i)
        if i >= k - 1:
            result.append(values[window[0]])
    return result


def longest_calm_stretch(readings: list[int], limit: int) -> int:
    """Exercise 3 (LeetCode 1438): longest run where max - min <= limit. Two monotonic deques."""
    highs: deque[int] = deque()
    lows: deque[int] = deque()
    left = best = 0
    for right, value in enumerate(readings):
        while highs and readings[highs[-1]] <= value:
            highs.pop()
        while lows and readings[lows[-1]] >= value:
            lows.pop()
        highs.append(right)
        lows.append(right)
        while readings[highs[0]] - readings[lows[0]] > limit:
            left += 1
            if highs[0] < left:
                highs.popleft()
            if lows[0] < left:
                lows.popleft()
        best = max(best, right - left + 1)
    return best


def rotate(values: list[int], steps: int) -> list[int]:
    """Exercise 4: rotate right by `steps` with deque.rotate (O(steps))."""
    d = deque(values)
    d.rotate(steps)
    return list(d)


if __name__ == "__main__":
    print(moving_average([10, 20, 30, 40], 3), sliding_window_min([4, 2, 12, 3, 8, 1], 3))
    print(longest_calm_stretch([8, 2, 4, 7], 4), rotate([1, 2, 3, 4, 5], 2))
