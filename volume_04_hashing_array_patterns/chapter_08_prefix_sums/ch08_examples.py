"""Volume 4, Chapter 8 - Prefix Sums and Difference Arrays.

Run:  python3 ch08_examples.py
"""

from __future__ import annotations


class RangeTotals:
    """Answer 'total from day i to day j' in O(1) after O(n) setup (LeetCode 303).

    prefix[k] = sum of the first k values, so sum(i..j) = prefix[j + 1] - prefix[i].
    """

    def __init__(self, values: list[int]) -> None:
        self.prefix = [0]
        for v in values:
            self.prefix.append(self.prefix[-1] + v)

    def total(self, i: int, j: int) -> int:
        if not 0 <= i <= j < len(self.prefix) - 1:
            raise IndexError("range out of bounds")
        return self.prefix[j + 1] - self.prefix[i]


def balance_point(weights: list[int]) -> int:
    """LeetCode 724: an index where everything to the left weighs the same as everything to the right. -1 if none."""
    total, left = sum(weights), 0
    for i, w in enumerate(weights):
        if left == total - left - w:
            return i
        left += w
    return -1


def product_of_others(values: list[int]) -> list[int]:
    """LeetCode 238: each position gets the product of all OTHER values, without division.

    Prefix products from the left times suffix products from the right.
    """
    n = len(values)
    out = [1] * n
    running = 1
    for i in range(n):
        out[i] = running
        running *= values[i]
    running = 1
    for i in range(n - 1, -1, -1):
        out[i] *= running
        running *= values[i]
    return out


def apply_range_updates(length: int, updates: list[tuple[int, int, int]]) -> list[int]:
    """Difference array: add `amount` to every position from start to end (inclusive), for many updates.

    Each update touches only TWO cells; one prefix-sum pass at the end rebuilds the values. O(n + updates).
    """
    diff = [0] * (length + 1)
    for start, end, amount in updates:
        diff[start] += amount
        diff[end + 1] -= amount
    values, running = [], 0
    for i in range(length):
        running += diff[i]
        values.append(running)
    return values


def hotel_occupancy(bookings: list[tuple[int, int]], nights: int) -> list[int]:
    """Industry example: guests check in on night a and leave the morning after night b. Rooms used per night."""
    return apply_range_updates(nights, [(a, b, 1) for a, b in bookings])


def busiest_hour(entries: list[tuple[int, int]]) -> tuple[int, int]:
    """Practical example: people inside a museum per hour (arrive hour, leave hour exclusive). (hour, count)."""
    hours = max(leave for _, leave in entries)
    counts = apply_range_updates(hours, [(arrive, leave - 1, 1) for arrive, leave in entries if leave > arrive])
    best = max(range(hours), key=lambda h: counts[h])
    return best, counts[best]


if __name__ == "__main__":
    steps = RangeTotals([4000, 6500, 3000, 8000, 7200, 1000, 9100])
    print("Steps Tue-Thu:", steps.total(1, 3))
    print("Balance point:", balance_point([1, 7, 3, 6, 5, 6]))
    print("Product of others:", product_of_others([1, 2, 3, 4]))
    print("Range updates:", apply_range_updates(5, [(1, 3, 2), (2, 4, 3), (0, 2, -2)]))
    print("Hotel rooms per night:", hotel_occupancy([(0, 2), (1, 3), (2, 2), (4, 5)], nights=6))
    print("Busiest museum hour:", busiest_hour([(9, 12), (10, 11), (10, 13), (14, 16)]))
