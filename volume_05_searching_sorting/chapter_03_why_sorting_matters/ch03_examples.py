"""Volume 5, Chapter 3 - Why Sorting Matters: What Order Makes Easy; Keys and Comparators.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations

from functools import cmp_to_key


def is_sorted(items: list) -> bool:
    """Every neighbour pair in order. O(n)."""
    return all(items[i] <= items[i + 1] for i in range(len(items) - 1))


def leaderboard(players: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Sort by score (highest first), then by name (A-Z) for ties - a tuple key does both at once."""
    return sorted(players, key=lambda p: (-p[1], p[0]))


def smallest_gap(prices: list[int]) -> int:
    """After sorting, the closest pair is always next to each other. O(n log n) instead of O(n^2)."""
    s = sorted(prices)
    return min(b - a for a, b in zip(s, s[1:]))


def merge_meetings(meetings: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """LeetCode 56: merge overlapping time blocks (a calendar's 'busy' view). Sort by start, then sweep."""
    merged: list[tuple[int, int]] = []
    for start, end in sorted(meetings):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged


def median(values: list[float]) -> float:
    """The middle value of the sorted data (average of the two middles for even counts)."""
    s = sorted(values)
    n = len(s)
    if n == 0:
        raise ValueError("median of empty list")
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def largest_number(numbers: list[int]) -> str:
    """LeetCode 179: arrange numbers to form the biggest number. A comparator: a before b if a+b > b+a."""
    def compare(a: str, b: str) -> int:
        return -1 if a + b > b + a else (1 if a + b < b + a else 0)
    joined = "".join(sorted(map(str, numbers), key=cmp_to_key(compare)))
    return "0" if joined.startswith("0") else joined


def sort_versions(versions: list[str]) -> list[str]:
    """Industry example: '1.10.0' comes after '1.9.3' - compare numeric parts, not text."""
    return sorted(versions, key=lambda v: tuple(int(part) for part in v.split(".")))


if __name__ == "__main__":
    print(is_sorted([1, 2, 2, 5]), is_sorted([3, 1]))
    print(leaderboard([("Zoe", 90), ("Ali", 95), ("Ben", 90)]))
    print(smallest_gap([340, 120, 905, 128, 610]), merge_meetings([(9, 10), (13, 15), (9.5, 11), (14, 16)]))
    print(median([7, 1, 5, 3]), largest_number([3, 30, 34, 5, 9]))
    print(sort_versions(["1.10.0", "1.9.3", "1.2.10", "1.2.9"]), sorted(["1.10.0", "1.9.3"]))
