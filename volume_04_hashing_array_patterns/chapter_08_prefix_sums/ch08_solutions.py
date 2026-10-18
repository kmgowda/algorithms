"""Volume 4, Chapter 8 - Solutions to the exercises."""

from __future__ import annotations

from ch08_examples import apply_range_updates


def running_totals(values: list[int]) -> list[int]:
    """Exercise 1 (LeetCode 1480): the running sum."""
    out, total = [], 0
    for v in values:
        total += v
        out.append(total)
    return out


def flight_bookings(bookings: list[tuple[int, int, int]], flights: int) -> list[int]:
    """Exercise 2 (LeetCode 1109): seats booked on each flight 1..n from (first, last, seats) bookings."""
    return apply_range_updates(flights, [(a - 1, b - 1, seats) for a, b, seats in bookings])


def car_pooling(trips: list[tuple[int, int, int]], capacity: int) -> bool:
    """Exercise 3 (LeetCode 1094): (passengers, pick-up km, drop-off km). Is capacity ever exceeded?"""
    if not trips:
        return True
    end = max(drop for _, _, drop in trips)
    load = apply_range_updates(end, [(pick, drop - 1, people) for people, pick, drop in trips if drop > pick])
    return max(load, default=0) <= capacity


def count_in_ranges(values: list[int], queries: list[tuple[int, int]], low: int, high: int) -> list[int]:
    """Exercise 4: how many values in positions i..j fall within [low, high]? Prefix counts of a yes/no flag."""
    prefix = [0]
    for v in values:
        prefix.append(prefix[-1] + (low <= v <= high))
    return [prefix[j + 1] - prefix[i] for i, j in queries]


if __name__ == "__main__":
    print(running_totals([3, 1, 4, 1]), flight_bookings([(1, 2, 10), (2, 3, 20), (2, 5, 25)], 5))
    print(car_pooling([(2, 1, 5), (3, 3, 7)], 4), count_in_ranges([5, 12, 30, 18, 2], [(0, 4), (1, 3)], 10, 20))
