"""Volume 14, Chapter 10 - The Big Comparison: Math Shortcuts vs. Simulation.

Each problem is solved twice: by simulating (or enumerating) and by a formula. The simulation checks the
formula; the formula makes the answer instant.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations

import math
import random
import timeit
from collections import deque


def sum_simulated(n: int) -> int:
    return sum(range(1, n + 1))


def sum_formula(n: int) -> int:
    """Gauss: 1 + 2 + ... + n = n(n + 1) / 2."""
    return n * (n + 1) // 2


def josephus_simulated(n: int, k: int) -> int:
    """LeetCode 1823: n people in a circle, every k-th leaves; who remains (1-based)? Simulate with a queue."""
    circle = deque(range(1, n + 1))
    while len(circle) > 1:
        circle.rotate(-(k - 1))
        circle.popleft()
    return circle[0]


def josephus_formula(n: int, k: int) -> int:
    """Recurrence J(1) = 0, J(m) = (J(m - 1) + k) mod m (0-based) - O(n) with no list at all."""
    j = 0
    for m in range(2, n + 1):
        j = (j + k) % m
    return j + 1


def birthday_simulated(people: int, trials: int, rng: random.Random) -> float:
    hits = 0
    for _ in range(trials):
        days = [rng.randrange(365) for _ in range(people)]
        hits += len(set(days)) < people
    return hits / trials


def birthday_formula(people: int) -> float:
    return 1 - math.prod((365 - i) / 365 for i in range(people))


def grid_paths_enumerated(rows: int, cols: int) -> int:
    """Count every right/down route by trying all move sequences (exponential)."""
    def walk(r: int, c: int) -> int:
        if r == rows - 1 and c == cols - 1:
            return 1
        return (walk(r + 1, c) if r + 1 < rows else 0) + (walk(r, c + 1) if c + 1 < cols else 0)
    return walk(0, 0)


def grid_paths_formula(rows: int, cols: int) -> int:
    return math.comb(rows + cols - 2, rows - 1)


def race() -> dict[str, tuple[float, float]]:
    """(simulation seconds, formula seconds) for each problem."""
    rng = random.Random(0)
    cases = {
        "sum 1..10^6": (lambda: sum_simulated(10 ** 6), lambda: sum_formula(10 ** 6)),
        "Josephus n=10^5, k=3": (lambda: josephus_simulated(10 ** 5, 3), lambda: josephus_formula(10 ** 5, 3)),
        "birthday, 23 people": (lambda: birthday_simulated(23, 20000, rng), lambda: birthday_formula(23)),
        "grid paths 12 x 12": (lambda: grid_paths_enumerated(12, 12), lambda: grid_paths_formula(12, 12)),
    }
    return {name: (min(timeit.repeat(sim, number=1, repeat=3)), min(timeit.repeat(f, number=1, repeat=3)))
            for name, (sim, f) in cases.items()}


def choose_approach(features: set[str]) -> str:
    """Decision guide: when to trust a formula and when to simulate."""
    if "closed form known and proven" in features:
        return "formula"
    if "recurrence with small state" in features:
        return "recurrence or matrix power"
    if "too complex to analyse" in features:
        return "simulation with error estimate"
    return "simulate small cases, then look for a pattern and prove it"


if __name__ == "__main__":
    print(sum_simulated(100), sum_formula(100), josephus_simulated(7, 3), josephus_formula(7, 3))
    print(round(birthday_simulated(23, 20000, random.Random(1)), 3), round(birthday_formula(23), 3))
    print(grid_paths_enumerated(5, 5), grid_paths_formula(5, 5))
    for name, (sim, f) in race().items():
        print(f"{name:<22} simulation {sim * 1000:9.2f} ms   formula {f * 1e6:8.2f} us")
