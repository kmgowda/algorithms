"""Volume 7, Chapter 6 - Thinking Problems (Section 6.17): model solutions.

Run:  python3 ch06_solutions.py
"""

from __future__ import annotations

import math

from ch06_examples import is_strong_liar, squaring_chain


def split_by_square_root(n: int, bases: list) -> int | None:
    """Thinking Problem 2: a factor d with 1 < d < n found by Miller-Rabin's own chains, or None.

    A base sharing a factor with n gives it away at once. Otherwise, if a chain reaches 1 from some x other
    than 1 and n - 1, then n divides (x - 1)(x + 1) but neither factor, so gcd(x - 1, n) splits n.
    """
    if n < 4:
        return None
    if n % 2 == 0:
        return 2
    for a in bases:
        g = math.gcd(a, n)
        if 1 < g < n:
            return g
        chain = squaring_chain(n, a)
        for x, y in zip(chain, chain[1:]):
            if y == 1 and x not in (1, n - 1):
                return math.gcd(x - 1, n)
    return None


def last_step_only(n: int, a: int) -> bool:
    """Thinking Problem 3: the WRONG shortcut that checks only the last square: a^(n-1) = 1, and the value
    before it is 1 or n - 1."""
    chain = squaring_chain(n, a)
    return chain[-1] == 1 and chain[-2] in (1, n - 1)


def strong_liars(n: int) -> list:
    """Thinking Problem 1: the bases 1..n-1 that let the odd composite n pass one round."""
    return [a for a in range(1, n) if is_strong_liar(n, a)]


if __name__ == "__main__":
    print(strong_liars(65), 8 * 18 % 65, squaring_chain(65, 14))
    print(split_by_square_root(561, [2]), split_by_square_root(8911, [2, 3]), split_by_square_root(97, [2, 3, 5]))
    print(last_step_only(561, 2), is_strong_liar(561, 2))
