"""Volume 7, Chapter 18 - Thinking Problem 2: do two lists hold the same values, with the same counts?
A Monte Carlo fingerprint in O(n) per round, wrong with chance at most (n/p) per round, like Freivalds' check.

Run:  python3 ch18_solutions.py
"""

from __future__ import annotations

import random

P = 2 ** 61 - 1                                     # a prime larger than every value compared


def same_multiset(a: list, b: list, rounds: int, rng) -> bool:
    """Compare the polynomials (z - a1)(z - a2)... and (z - b1)(z - b2)... mod P at random points z.
    Values must be whole numbers in 0..P-1. A 'no' is certain; a 'yes' is wrong with chance at most (n/P)^rounds."""
    if len(a) != len(b):
        return False
    for _ in range(rounds):
        z = rng.randrange(P)
        fa = fb = 1
        for x in a:
            fa = fa * (z - x) % P
        for y in b:
            fb = fb * (z - y) % P
        if fa != fb:
            return False
    return True


if __name__ == "__main__":
    pile = [58, 25, 91, 12, 70, 47, 84, 31, 63]
    rng = random.Random(18)
    print(same_multiset(pile, sorted(pile), 3, rng), same_multiset(pile, sorted(pile)[:-1] + [92], 3, rng))
