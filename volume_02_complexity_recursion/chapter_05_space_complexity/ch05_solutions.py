"""Volume 2, Chapter 5 - Solutions to the exercises."""

from __future__ import annotations

from typing import Iterable, Iterator


def running_max(readings: Iterable[float]) -> Iterator[float]:
    """Exercise 2: a generator that yields the highest temperature seen so far. O(1) extra space."""
    best = None
    for value in readings:
        if best is None or value > best:
            best = value
        yield best


def move_evens_first(values: list[int]) -> None:
    """Exercise 3: put even numbers before odd ones, in place, O(1) extra space (order may change)."""
    left, right = 0, len(values) - 1
    while left < right:
        if values[left] % 2 == 0:
            left += 1
        elif values[right] % 2 == 1:
            right -= 1
        else:
            values[left], values[right] = values[right], values[left]


def answer_range_questions(sales: list[int], questions: list[tuple[int, int]]) -> list[int]:
    """Exercise 4: many range-total questions -> build prefix totals once (O(n) space), O(1) per question."""
    totals = [0]
    for amount in sales:
        totals.append(totals[-1] + amount)
    return [totals[b + 1] - totals[a] for a, b in questions]


def fits_in_memory(count: int, bytes_each: int, memory_gb: float) -> bool:
    """Exercise 5: rough check that data fits, keeping half the memory free for everything else."""
    return count * bytes_each <= memory_gb * 1_000_000_000 / 2


def average_of_stream(numbers: Iterable[float]) -> float:
    """Exercise 6: average of a stream too large to store: keep only a total and a count."""
    total, count = 0.0, 0
    for value in numbers:
        total += value
        count += 1
    if count == 0:
        raise ValueError("empty stream")
    return total / count


if __name__ == "__main__":
    print(list(running_max([21, 19, 25, 24, 30])))
    values = [3, 8, 5, 2, 7, 6]
    move_evens_first(values)
    print(values, answer_range_questions([5, 1, 4, 2], [(0, 1), (1, 3)]))
    print(fits_in_memory(100_000_000, 8, 4), average_of_stream(x for x in range(1, 101)))
