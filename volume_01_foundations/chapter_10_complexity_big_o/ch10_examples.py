"""Chapter 10 - How Fast Is My Algorithm? A Gentle Introduction to Complexity and Big O.

Every function here returns the answer AND the number of basic steps it took,
so you can see growth rates with your own eyes.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations

import math
import time
from typing import Callable


# ------------------------------------------------------------------ O(1): constant
def first_in_line(queue: list[str]) -> tuple[str, int]:
    """O(1): looking at the first person takes one step, however long the queue."""
    return queue[0], 1


def gauss_sum(n: int) -> tuple[int, int]:
    """O(1): the formula n(n+1)/2 takes the same few steps for any n."""
    return n * (n + 1) // 2, 3


# ------------------------------------------------------------------ O(n): linear
def loop_sum(n: int) -> tuple[int, int]:
    """O(n): one addition per number."""
    total, steps = 0, 0
    for value in range(1, n + 1):
        total += value
        steps += 1
    return total, steps


# ------------------------------------------------------------------ O(n^2): quadratic
def handshakes(people: list[str]) -> tuple[int, int]:
    """O(n^2): everyone shakes hands with everyone else once - pairs of pairs."""
    count, steps = 0, 0
    for i in range(len(people)):
        for _ in range(i + 1, len(people)):
            count += 1
            steps += 1
    return count, steps


def has_duplicate_slow(items: list[str]) -> tuple[bool, int]:
    """O(n^2): compare every pair."""
    steps = 0
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            steps += 1
            if items[i] == items[j]:
                return True, steps
    return False, steps


def has_duplicate_fast(items: list[str]) -> tuple[bool, int]:
    """O(n) time, O(n) extra space: remember what we have seen in a set."""
    seen: set[str] = set()
    steps = 0
    for item in items:
        steps += 1
        if item in seen:
            return True, steps
        seen.add(item)
    return False, steps


# ------------------------------------------------------------------ O(log n): logarithmic
def halvings(n: int) -> int:
    """O(log n): how many times can we halve n before reaching 1?"""
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps


def guess_the_number(secret: int, low: int = 1, high: int = 100) -> int:
    """O(log n) preview of Chapter 11: always guess the middle; count the guesses."""
    guesses = 0
    while low <= high:
        guesses += 1
        middle = (low + high) // 2
        if middle == secret:
            return guesses
        if middle < secret:
            low = middle + 1
        else:
            high = middle - 1
    raise ValueError("secret was outside the range")


# ------------------------------------------------------------------ O(2^n): exponential
def all_outfits(clothes: list[str]) -> int:
    """O(2^n): every item can be worn or not worn - the number of choices doubles each time."""
    return 2 ** len(clothes)


# ------------------------------------------------------------------ space complexity
def reverse_copy(items: list[int]) -> list[int]:
    """O(n) extra space: builds a whole new list."""
    return items[::-1]


def reverse_in_place(items: list[int]) -> None:
    """O(1) extra space: only two position variables, whatever the size."""
    left, right = 0, len(items) - 1
    while left < right:
        items[left], items[right] = items[right], items[left]
        left, right = left + 1, right - 1


# ------------------------------------------------------------------ measuring
def growth_table(sizes: list[int]) -> list[dict[str, int]]:
    """How many steps different growth rates need for each input size."""
    rows = []
    for n in sizes:
        rows.append({
            "n": n,
            "O(1)": 1,
            "O(log n)": max(1, math.ceil(math.log2(n))) if n > 1 else 1,
            "O(n)": n,
            "O(n log n)": n * max(1, math.ceil(math.log2(n))) if n > 1 else 1,
            "O(n^2)": n * n,
        })
    return rows


def time_it(function: Callable[[int], object], n: int, repeats: int = 3) -> float:
    """Wall-clock seconds for function(n), best of a few runs (less noise)."""
    best = float("inf")
    for _ in range(repeats):
        start = time.perf_counter()
        function(n)
        best = min(best, time.perf_counter() - start)
    return best


if __name__ == "__main__":
    for row in growth_table([10, 100, 1000, 1_000_000]):
        print(row)
    print("Handshakes among 10 people:", handshakes([str(i) for i in range(10)]))
    animals = [f"animal{i}" for i in range(2000)]      # worst case: no duplicates at all
    print("Duplicate check, slow:", has_duplicate_slow(animals)[1], "steps")
    print("Duplicate check, fast:", has_duplicate_fast(animals)[1], "steps")
    print("Halvings of 1,000,000:", halvings(1_000_000))
    print("Guesses to find 73 in 1..100:", guess_the_number(73))
    for n in (100_000, 200_000, 400_000):
        print(f"loop_sum({n}) took {time_it(loop_sum, n):.4f} s; gauss_sum took {time_it(gauss_sum, n):.7f} s")
