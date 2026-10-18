"""Volume 5, Chapter 8 - Non-Comparison Sorts: Counting, Radix, Bucket.

Run:  python3 ch08_examples.py
"""

from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")


def counting_sort(values: list[int], max_value: int) -> list[int]:
    """Small whole numbers 0..max_value: count each value, then write them out. O(n + k)."""
    counts = [0] * (max_value + 1)
    for v in values:
        counts[v] += 1
    out: list[int] = []
    for value, times in enumerate(counts):
        out.extend([value] * times)
    return out


def counting_sort_by_key(items: list[T], key: Callable[[T], int], max_key: int) -> list[T]:
    """Stable counting sort of RECORDS by a small integer key, using prefix sums (V4-C8) for positions."""
    counts = [0] * (max_key + 1)
    for item in items:
        counts[key(item)] += 1
    starts = [0] * (max_key + 1)                 # starts[k] = where the first item with key k goes
    for k in range(1, max_key + 1):
        starts[k] = starts[k - 1] + counts[k - 1]
    out: list[T | None] = [None] * len(items)
    for item in items:                           # left to right keeps equal keys in order: stable
        out[starts[key(item)]] = item
        starts[key(item)] += 1
    return out  # type: ignore[return-value]


def radix_sort(values: list[int], base: int = 10) -> list[int]:
    """Non-negative integers: stable-sort by the last digit, then the next, ... (least significant digit first)."""
    if not values:
        return []
    out, place = list(values), 1
    while max(values) // place > 0:
        out = counting_sort_by_key(out, lambda v: (v // place) % base, base - 1)
        place *= base
    return out


def bucket_sort(values: list[float], buckets: int = 10) -> list[float]:
    """Values spread evenly over [0, 1): drop each into one of n buckets, sort each small bucket, concatenate."""
    groups: list[list[float]] = [[] for _ in range(buckets)]
    for v in values:
        groups[min(int(v * buckets), buckets - 1)].append(v)
    out: list[float] = []
    for g in groups:
        out.extend(sorted(g))                    # each bucket is tiny on average
    return out


def sort_by_age(people: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Practical example: ages are 0..120, so counting sort beats any comparison sort - and stays stable."""
    return counting_sort_by_key(people, key=lambda p: p[1], max_key=120)


def sort_postcodes(codes: list[str]) -> list[str]:
    """Industry example: mail sorting machines sort fixed-length postal codes digit by digit (radix sort)."""
    out = list(codes)
    for position in range(len(codes[0]) - 1, -1, -1) if codes else []:
        out = counting_sort_by_key(out, key=lambda c: int(c[position]), max_key=9)
    return out


if __name__ == "__main__":
    print(counting_sort([3, 1, 4, 1, 5, 2, 0, 3], 5))
    print(radix_sort([170, 45, 75, 90, 802, 24, 2, 66]))
    print(bucket_sort([0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]))
    print(sort_by_age([("Ana", 34), ("Ben", 7), ("Cy", 34), ("Dev", 61), ("Eve", 7)]))
    print(sort_postcodes(["560034", "110001", "560001", "400050"]))
