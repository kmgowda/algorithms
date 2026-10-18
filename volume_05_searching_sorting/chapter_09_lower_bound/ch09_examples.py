"""Volume 5, Chapter 9 - The Lower Bound for Comparison Sorting: Why n log n Is a Wall.

Run:  python3 ch09_examples.py
"""

from __future__ import annotations

import itertools
import math
from functools import total_ordering


@total_ordering
class Counted:
    """A value that counts every comparison made on it - so we can measure ANY sort's comparisons."""

    comparisons = 0

    def __init__(self, value: int) -> None:
        self.value = value

    def __lt__(self, other: "Counted") -> bool:
        Counted.comparisons += 1
        return self.value < other.value

    def __eq__(self, other: object) -> bool:
        Counted.comparisons += 1
        return isinstance(other, Counted) and self.value == other.value


def comparisons_used(sort_function, values: list[int]) -> int:
    """How many comparisons a sort function makes on this input."""
    Counted.comparisons = 0
    sort_function([Counted(v) for v in values])
    return Counted.comparisons


def lower_bound_comparisons(n: int) -> int:
    """Any comparison sort needs at least ceil(log2(n!)) comparisons in the worst case.
    n! possible orders = leaves of the decision tree; a binary tree of height h has at most 2^h leaves."""
    return math.ceil(math.log2(math.factorial(n))) if n > 1 else 0


def stirling_estimate(n: int) -> float:
    """log2(n!) is about n*log2(n) - n*log2(e): the 'n log n' in the wall."""
    return n * math.log2(n) - n * math.log2(math.e) if n > 1 else 0.0


def worst_case_comparisons(sort_function, n: int) -> int:
    """Try every ordering of n items and report the most comparisons the sort ever needed."""
    return max(comparisons_used(sort_function, list(p)) for p in itertools.permutations(range(n)))


def guessing_game_questions(choices: int) -> int:
    """'Higher or lower?' questions needed to find one secret among `choices`: ceil(log2(choices))."""
    return math.ceil(math.log2(choices)) if choices > 1 else 0


def sort_three(a, b, c) -> tuple:
    """An optimal decision tree for 3 items: never more than 3 comparisons (and 3! = 6 orders need at least 3)."""
    if not b < a:                                # a <= b, using exactly one comparison
        if not c < b:
            return a, b, c
        return (a, c, b) if not c < a else (c, a, b)
    if not c < a:
        return b, a, c
    return (b, c, a) if not c < b else (c, b, a)


if __name__ == "__main__":
    for n in (3, 5, 10, 100, 1000):
        print(f"n={n:>4}: at least {lower_bound_comparisons(n):>5} comparisons | n log2 n = {n * math.log2(n):>8.0f}")
    print("Python's sorted, worst case over all orders of 6 items:", worst_case_comparisons(sorted, 6),
          "| lower bound:", lower_bound_comparisons(6))
    print("Guess a number 1..1,000,000 in", guessing_game_questions(1_000_000), "questions")
    print(sort_three(3, 1, 2), sort_three("zebra", "ant", "lion"))
