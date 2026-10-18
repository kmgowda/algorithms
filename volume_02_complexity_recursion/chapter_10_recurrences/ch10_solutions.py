"""Volume 2, Chapter 10 - Solutions to the exercises."""

from __future__ import annotations

from functools import lru_cache

from ch10_examples import master_theorem


def exercise1_answers() -> dict[str, str]:
    """Exercise 1: match each recurrence to its solution."""
    return {
        "T(n) = T(n-1) + 1": "Theta(n)",
        "T(n) = T(n/2) + 1": "Theta(log n)",
        "T(n) = 2T(n/2) + n": "Theta(n log n)",
        "T(n) = 2T(n-1) + 1": "Theta(2^n)",
        "T(n) = T(n-1) + n": "Theta(n^2)",
    }


def exercise2_master() -> dict[str, str]:
    """Exercise 2: apply the Master Theorem."""
    return {
        "T(n) = 4T(n/2) + n^2": master_theorem(4, 2, 2),
        "T(n) = 8T(n/2) + n^2": master_theorem(8, 2, 2),
        "T(n) = 2T(n/2) + n^2": master_theorem(2, 2, 2),
        "T(n) = 9T(n/3) + n": master_theorem(9, 3, 1),
    }


@lru_cache(maxsize=None)
def t_power_two_calls(e: int) -> int:
    """Exercise 3: the BUGGY power that calls power(b, e//2) twice: T(e) = 2T(e/2) + 1 -> Theta(e)."""
    return 0 if e == 0 else 2 * t_power_two_calls(e // 2) + 1


@lru_cache(maxsize=None)
def t_ternary_search(n: int) -> int:
    """Exercise 4: split into thirds, recurse into ONE third: T(n) = T(n/3) + 2 -> Theta(log n)."""
    return 0 if n <= 1 else t_ternary_search(n // 3) + 2


def fibonacci_calls_ratio(n: int) -> float:
    """Exercise 5: calls(n) / calls(n-1) approaches the golden ratio 1.618..."""
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, 1 + a + b
    return b / a


if __name__ == "__main__":
    print(exercise1_answers())
    print(exercise2_master())
    print(t_power_two_calls(1024), t_ternary_search(3 ** 10), round(fibonacci_calls_ratio(30), 6))
