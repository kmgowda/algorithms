"""Volume 15, Chapter 1 - Solutions to the exercises."""

from __future__ import annotations

import random


def randomized_quicksort(values: list[int], rng: random.Random) -> list[int]:
    """Exercise 1: Las Vegas sorting - a random pivot makes the O(n^2) worst case vanishingly unlikely."""
    if len(values) <= 1:
        return list(values)
    pivot = rng.choice(values)
    return (randomized_quicksort([x for x in values if x < pivot], rng) + [x for x in values if x == pivot]
            + randomized_quicksort([x for x in values if x > pivot], rng))


def polynomial_identity(p, q, degree: int, rounds: int, rng: random.Random) -> bool:
    """Exercise 2: are two polynomial functions equal? Evaluate at random points: two different polynomials of
    degree <= d agree on at most d points, so a random point from a range of 100d exposes a difference with
    probability >= 99%."""
    for _ in range(rounds):
        x = rng.randint(1, 100 * max(1, degree))
        if p(x) != q(x):
            return False
    return True


def las_vegas_find(values: list[int], target: int, rng: random.Random) -> tuple[int, int]:
    """Exercise 3: if half the array equals target, random probing finds one in 2 tries on average."""
    tries = 0
    while True:
        tries += 1
        i = rng.randrange(len(values))
        if values[i] == target:
            return i, tries


if __name__ == "__main__":
    rng = random.Random(0)
    print(randomized_quicksort([5, 3, 8, 1, 9, 2], rng),
          polynomial_identity(lambda x: (x + 1) ** 2, lambda x: x * x + 2 * x + 1, 2, 10, rng),
          las_vegas_find([7, 0] * 50, 7, rng))
