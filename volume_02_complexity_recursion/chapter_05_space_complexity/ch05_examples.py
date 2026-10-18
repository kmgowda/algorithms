"""Volume 2, Chapter 5 - Space Complexity and Memory Trade-offs.

Run:  python3 ch05_examples.py
"""

from __future__ import annotations

import sys
from typing import Iterable, Iterator


# ------------------------------------------------------------------ auxiliary space: copy vs in place
def unique_sorted_with_set(ids: list[int]) -> list[int]:
    """O(n) extra space: build a set and a new list."""
    seen: set[int] = set()
    result = []
    for value in ids:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def unique_sorted_in_place(ids: list[int]) -> int:
    """O(1) extra space: for a SORTED list, keep one copy of each value at the front.

    Returns how many unique values there are; ids[:count] holds them.
    """
    if not ids:
        return 0
    write = 1
    for read in range(1, len(ids)):
        if ids[read] != ids[write - 1]:
            ids[write] = ids[read]
            write += 1
    return write


# ------------------------------------------------------------------ measuring memory
def list_memory_bytes(n: int) -> int:
    """Bytes used by a list object holding n small integers (the list itself, not the integers)."""
    return sys.getsizeof(list(range(n)))


def bytes_needed(count: int, bytes_each: int) -> int:
    """Back-of-the-envelope memory estimate."""
    return count * bytes_each


# ------------------------------------------------------------------ generators: produce values on demand
def squares_list(n: int) -> list[int]:
    """Builds all n values in memory at once: O(n) space."""
    return [x * x for x in range(n)]


def squares_generator(n: int) -> Iterator[int]:
    """Produces one value at a time: O(1) space, however large n is."""
    for x in range(n):
        yield x * x


def count_errors(log_lines: Iterable[str]) -> int:
    """Industry example: scan a huge log one line at a time (works on files, lists, or generators)."""
    errors = 0
    for line in log_lines:
        if " ERROR " in line:
            errors += 1
    return errors


def fake_log(lines: int) -> Iterator[str]:
    """A generator standing in for a giant log file."""
    for i in range(lines):
        level = "ERROR" if i % 50 == 0 else "INFO"
        yield f"2026-10-18T10:{i % 60:02d} {level} request {i}"


# ------------------------------------------------------------------ spending space to save time
def prefix_totals(daily_visitors: list[int]) -> list[int]:
    """totals[k] = visitors on days 0..k-1. One O(n) pass, O(n) extra space."""
    totals = [0]
    for count in daily_visitors:
        totals.append(totals[-1] + count)
    return totals


def visitors_between(totals: list[int], first_day: int, last_day: int) -> int:
    """Visitors from first_day to last_day inclusive, in O(1) using the prefix totals."""
    return totals[last_day + 1] - totals[first_day]


def visitors_between_slow(daily_visitors: list[int], first_day: int, last_day: int) -> int:
    """No extra space, but O(length of range) per question."""
    return sum(daily_visitors[first_day:last_day + 1])


BITS_IN_BYTE = [bin(value).count("1") for value in range(256)]   # a 256-entry lookup table


def count_set_bits(number: int) -> int:
    """Count 1-bits using the precomputed table, one byte (8 bits) at a time."""
    if number < 0:
        raise ValueError("non-negative numbers only")
    total = 0
    while number:
        total += BITS_IN_BYTE[number & 0xFF]   # the lowest 8 bits
        number >>= 8                            # drop those 8 bits
    return total


if __name__ == "__main__":
    ids = [101, 101, 102, 105, 105, 105, 110]
    print("With a set:", unique_sorted_with_set(ids))
    count = unique_sorted_in_place(ids)
    print("In place:", ids[:count])
    for n in (0, 10, 1000, 1_000_000):
        print(f"list of {n:>9,} ints uses {list_memory_bytes(n):>11,} bytes (list only)")
    print("Generator object size:", sys.getsizeof(squares_generator(1_000_000)), "bytes")
    print("Sum via generator:", sum(squares_generator(1_000_000)))
    print("Errors in a 100,000-line log:", count_errors(fake_log(100_000)))
    visitors = [120, 340, 90, 410, 500, 220, 610]
    totals = prefix_totals(visitors)
    print("Visitors days 2..5:", visitors_between(totals, 2, 5), visitors_between_slow(visitors, 2, 5))
    print("Set bits in 2026:", count_set_bits(2026))
    print("Memory for 10 million 8-byte prices:", bytes_needed(10_000_000, 8), "bytes")
