"""Volume 10, Chapter 10 - Solutions to the exercises."""

from __future__ import annotations

from ch10_examples import gcd


def integer_sqrt(n: int) -> int:
    """Exercise 1 (LeetCode 69): floor of the square root by halving the search range (decrease by half)."""
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid * mid <= n:
            lo = mid
        else:
            hi = mid - 1
    return lo


def subsets_decrease(items: list[str]) -> list[list[str]]:
    """Exercise 2: all subsets - those without the last item, plus those with it (decrease by one)."""
    if not items:
        return [[]]
    rest = subsets_decrease(items[:-1])
    return rest + [s + [items[-1]] for s in rest]


def two_sum_presort(values: list[int], target: int) -> bool:
    """Exercise 3: transform by sorting, then two pointers (V4-C5)."""
    s = sorted(values)
    i, j = 0, len(s) - 1
    while i < j:
        total = s[i] + s[j]
        if total == target:
            return True
        if total < target:
            i += 1
        else:
            j -= 1
    return False


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Exercise 4: gcd plus x, y with a*x + b*y = gcd - the decrease step run backwards (used in cryptography)."""
    if b == 0:
        return a, 1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y


if __name__ == "__main__":
    print(integer_sqrt(50), len(subsets_decrease(["a", "b", "c"])), two_sum_presort([8, 3, 5, 1], 9),
          extended_gcd(240, 46), gcd(240, 46))
