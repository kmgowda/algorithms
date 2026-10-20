"""Volume 1, Chapter 13 - Recursion.

Run:  python3 ch13_examples.py
"""

from __future__ import annotations


def factorial(n: int) -> int:
    """n! for n >= 1, recursively: base case 1! = 1, recursive case n! = n * (n - 1)! (Figure 13.3)."""
    if n == 1:
        return 1
    return n * factorial(n - 1)


def recursive_sum(items: list[int]) -> int:
    """Sum of a list: first item plus the sum of the rest; the empty list sums to 0 (Figure 13.2)."""
    if not items:
        return 0
    return items[0] + recursive_sum(items[1:])


def largest(items: list[int]) -> int:
    """Exercise 5: the larger of the first item and the largest of the rest (non-empty list)."""
    if len(items) == 1:
        return items[0]
    rest = largest(items[1:])
    return items[0] if items[0] > rest else rest


def count_dolls(doll: list) -> int:
    """A doll is a list holding the doll inside it (or nothing): 1 + the dolls inside (Figure 13.1)."""
    if not doll:
        return 1
    return 1 + count_dolls(doll[0])


def countdown_without_base(n: int) -> int:
    """The broken countdown of Figure 13.4: it never stops (raises RecursionError)."""
    return countdown_without_base(n - 1)


if __name__ == "__main__":
    print(factorial(4), factorial(6), recursive_sum([12, 25, 31]), largest([12, 91, 47]))
    print(count_dolls([[[[[]]]]]))
    try:
        countdown_without_base(3)
    except RecursionError:
        print("RecursionError, as expected")
