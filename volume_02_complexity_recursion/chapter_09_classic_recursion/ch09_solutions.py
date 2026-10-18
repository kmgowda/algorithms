"""Volume 2, Chapter 9 - Solutions to the exercises."""

from __future__ import annotations

from typing import Any

from ch09_examples import gcd


def lcm(a: int, b: int) -> int:
    """Exercise 1: least common multiple = a x b / gcd(a, b). When do two buses leave together again?"""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def climb_stairs(steps: int, memo: dict[int, int] | None = None) -> int:
    """Exercise 2 (LeetCode 70): ways to climb `steps` stairs taking 1 or 2 at a time."""
    if memo is None:
        memo = {}
    if steps <= 1:
        return 1
    if steps not in memo:
        memo[steps] = climb_stairs(steps - 1, memo) + climb_stairs(steps - 2, memo)
    return memo[steps]


def hanoi_moves_needed(disks: int) -> int:
    """Exercise 3: moves(n) = 2 moves(n-1) + 1 with moves(0) = 0 -> 2^n - 1."""
    return 2 ** disks - 1


def nested_sum(items: list[Any]) -> int:
    """Exercise 4: add every number in a nested list."""
    total = 0
    for item in items:
        total += nested_sum(item) if isinstance(item, list) else item
    return total


def count_paths_in_grid(rows: int, cols: int, memo: dict[tuple[int, int], int] | None = None) -> int:
    """Exercise 5: a delivery robot moves only right or down. Paths from the top-left to the bottom-right."""
    if memo is None:
        memo = {}
    if rows == 1 or cols == 1:
        return 1
    key = (rows, cols)
    if key not in memo:
        memo[key] = count_paths_in_grid(rows - 1, cols, memo) + count_paths_in_grid(rows, cols - 1, memo)
    return memo[key]


def binary_digits(n: int) -> str:
    """Exercise 6: write n in binary recursively: binary(n) = binary(n // 2) + last bit."""
    if n < 2:
        return str(n)
    return binary_digits(n // 2) + str(n % 2)


if __name__ == "__main__":
    print(lcm(12, 18), climb_stairs(10), hanoi_moves_needed(64), nested_sum([1, [2, [3]], 4]))
    print(count_paths_in_grid(3, 7), binary_digits(37))
