"""Volume 7, Chapter 20 - Thinking Problems.

Problem 1: p (1 - p) <= 1/4, so a fraction's standard error is at most 1 / (2 sqrt N), whatever p is.
Problem 2: trials for a 95% half-width h with no idea of p: ceil(1 / h^2) (two standard errors, worst case p = 1/2).
Problem 3: reusing one seed for every repeat makes the repeats identical, so their spread looks like zero.
"""

from __future__ import annotations

import math
import random
import statistics

from ch20_examples import estimate_pi


def worst_standard_error(trials: int) -> float:
    return 1 / (2 * math.sqrt(trials))


def trials_for_any_p(half_width: float) -> int:
    """2 standard errors <= half_width for every p: 2 / (2 sqrt N) <= h, so N >= 1 / h^2."""
    return math.ceil(1 / half_width ** 2)


def spread_of_estimates(repeats: int, trials: int, same_seed: bool) -> float:
    out = []
    for r in range(repeats):
        rng = random.Random(20 if same_seed else 1000 + r)
        out.append(estimate_pi(trials, rng))
    return statistics.pstdev(out)


if __name__ == "__main__":
    print(trials_for_any_p(0.01), worst_standard_error(10000))
    print(spread_of_estimates(20, 1000, True), round(spread_of_estimates(20, 1000, False), 4))
