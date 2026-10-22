"""Volume 7, Chapter 1 - Thinking Problems (Section 1.14): model solutions.

Run:  python3 ch01_solutions.py
"""

from __future__ import annotations

from ch01_examples import gcd, lcm_many


def gcd_without_each(values: list) -> list:
    """Thinking Problem 2: for every i, the gcd of all the numbers except values[i], in O(n) gcd calls.

    prefix[i] is the gcd of values[0..i-1] and suffix[i] the gcd of values[i..n-1]; leaving out i
    combines prefix[i] and suffix[i + 1]. The gcd of nothing is 0, so a one-item list gives [0].
    """
    n = len(values)
    prefix, suffix = [0] * (n + 1), [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = gcd(prefix[i], values[i])
    for i in range(n - 1, -1, -1):
        suffix[i] = gcd(suffix[i + 1], values[i])
    return [gcd(prefix[i], suffix[i + 1]) for i in range(n)]


def lcm_by_product(values: list) -> int:
    """Thinking Problem 3: the WRONG rule 'lcm = product / gcd of all', right for two numbers only."""
    product, g = 1, 0
    for v in values:
        product *= v
        g = gcd(g, v)
    return product // g


def mersenne_gcd(m: int, n: int) -> int:
    """Thinking Problem 1: gcd(2^m - 1, 2^n - 1), which equals 2^gcd(m, n) - 1."""
    return gcd(2 ** m - 1, 2 ** n - 1)


if __name__ == "__main__":
    print(gcd_without_each([84, 36, 60, 90]), gcd_without_each([7]), gcd_without_each([]))
    print(lcm_by_product([12, 18]), lcm_many([12, 18]), lcm_by_product([2, 4, 8]), lcm_many([2, 4, 8]))
    print(mersenne_gcd(12, 18), 2 ** 6 - 1)
