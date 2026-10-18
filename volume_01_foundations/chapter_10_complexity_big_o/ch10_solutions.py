"""Chapter 10 - Solutions to the exercises.

Each function's docstring states its Big O, which is the real answer to the exercise.
"""

from __future__ import annotations


def last_item(items: list[int]) -> int:
    """Exercise 2a: O(1) - one index operation."""
    return items[-1]


def count_evens(items: list[int]) -> int:
    """Exercise 2b: O(n) - one check per item."""
    return sum(1 for value in items if value % 2 == 0)


def multiplication_grid(n: int) -> list[list[int]]:
    """Exercise 2c: O(n^2) time and space - n rows of n numbers."""
    return [[row * col for col in range(1, n + 1)] for row in range(1, n + 1)]


def digits_in(n: int) -> int:
    """Exercise 2d: O(log n) - each step removes one digit (divides by 10)."""
    n = abs(n)
    count = 1
    while n >= 10:
        n //= 10
        count += 1
    return count


def common_students(class_a: list[str], class_b: list[str]) -> set[str]:
    """Exercise 5: O(a + b) using a set, instead of O(a x b) with nested loops."""
    in_a = set(class_a)
    return {student for student in class_b if student in in_a}


def pair_with_sum(prices: list[int], budget: int) -> tuple[int, int] | None:
    """Exercise 6 (Two Sum): two different items whose prices add up exactly to budget. O(n)."""
    seen: dict[int, int] = {}          # price -> index where we saw it
    for index, price in enumerate(prices):
        needed = budget - price
        if needed in seen:
            return seen[needed], index
        seen[price] = index
    return None


def simplify(terms: dict[str, int]) -> str:
    """Exercise 3 helper: keep the fastest-growing term, drop its constant.

    `terms` maps a growth name to its coefficient, e.g. {"n^2": 3, "n": 5, "1": 100}.
    """
    order = ["1", "log n", "n", "n log n", "n^2", "n^3", "2^n"]
    present = [term for term in order if terms.get(term, 0) != 0]
    if not present:
        raise ValueError("no terms")
    return f"O({present[-1]})"


if __name__ == "__main__":
    print(last_item([1, 2, 3]), count_evens([1, 2, 4]), multiplication_grid(3), digits_in(12345))
    print(common_students(["Ana", "Ben"], ["Ben", "Cy"]), pair_with_sum([300, 150, 700, 450], 750))
    print(simplify({"n^2": 3, "n": 5, "1": 100}))
