"""Volume 4, Chapter 13 - Thinking Problems (Section 13.15): model solutions that can be run.

1. radix_sort_first_pass_unstable / radix_sort_only_last_stable: which passes of LSD radix sort must be stable.
2. sort_cubic_range: sort n whole numbers from 0 to n**3 - 1 in O(n) time (radix sort in base n).
3. The negative-index bug is shown with counting_sort itself: counting_sort([3, -1, 2], 3) == [2, 3, -1].

Run:  python3 ch13_solutions.py
"""

from __future__ import annotations

from ch13_examples import counting_sort, counting_sort_unstable, radix_sort


def radix_sort_first_pass_unstable(a: list, digits: int, base: int = 10) -> list:
    """LSD radix sort whose ones pass is the unstable variant; every later pass is stable (Thinking Problem 1)."""
    for d in range(digits):
        div = base ** d
        sort = counting_sort_unstable if d == 0 else counting_sort
        a = sort(a, base - 1, key=lambda x: (x // div) % base)
    return a


def radix_sort_only_last_stable(a: list, digits: int, base: int = 10) -> list:
    """LSD radix sort in which only the last pass is stable: the claim that this suffices is false."""
    for d in range(digits):
        div = base ** d
        sort = counting_sort if d == digits - 1 else counting_sort_unstable
        a = sort(a, base - 1, key=lambda x: (x // div) % base)
    return a


def sort_cubic_range(a: list) -> list:
    """Sort n whole numbers from 0 to n**3 - 1 in O(n) time: radix sort in base n, three passes of counting sort
    with n trays each (Thinking Problem 2)."""
    n = len(a)
    if n <= 1:
        return list(a)
    if any(not 0 <= x < n ** 3 for x in a):
        raise ValueError("every key must be a whole number from 0 to n**3 - 1")
    return radix_sort(a, 3, base=n)


def cubic_range_steps(n: int) -> dict:
    """Basic steps (2n + 2b per pass, as in Section 13.6) for keys below n**3: base n against base 10."""
    decimal_digits = len(str(n ** 3 - 1))
    return {"base n, 3 passes": 3 * (2 * n + 2 * n), "base 10": decimal_digits * (2 * n + 20),
            "decimal passes": decimal_digits, "counting sort counters": n ** 3}


if __name__ == "__main__":
    print(radix_sort_first_pass_unstable([43, 37, 41, 33, 47], 2), radix_sort_only_last_stable([102, 101], 3))
    print(sort_cubic_range([7, 0, 5, 3]), cubic_range_steps(1_000_000))
    print(counting_sort([3, -1, 2], 3))
