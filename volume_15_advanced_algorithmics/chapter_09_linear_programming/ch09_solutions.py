"""Volume 15, Chapter 9 - Solutions to the exercises."""

from __future__ import annotations

from fractions import Fraction

from ch09_examples import simplex, solve_2d


def diet_problem() -> tuple[Fraction, tuple[Fraction, Fraction]] | None:
    """Exercise 1: MINIMISE cost 2*rice + 3*dal (per 100 g) with at least 8 units of protein (rice 1, dal 4) and
    at least 12 units of energy (rice 4, dal 2). Minimising cost = maximising -cost; 'at least' becomes '<='
    by negating both sides."""
    best = solve_2d((-2, -3), [(-1, -4, -8), (-4, -2, -12), (-1, 0, 0), (0, -1, 0), (1, 0, 100), (0, 1, 100)])
    if best is None:
        return None
    value, point = best
    return -value, point


def is_feasible(point: tuple[float, ...], a: list[list[float]], b: list[float]) -> bool:
    """Exercise 2: check a proposed plan against every constraint (and x >= 0) - the LP certificate check."""
    return all(x >= -1e-9 for x in point) and all(sum(r * x for r, x in zip(row, point)) <= bi + 1e-9 for row, bi in zip(a, b))


def best_mix(profits: list[float], usage: list[list[float]], capacity: list[float]) -> tuple[float, list[float]]:
    """Exercise 3: a production mix with any number of products - just call simplex."""
    return simplex(profits, usage, capacity)


if __name__ == "__main__":
    print(diet_problem(), is_feasible((30, 20), [[1, 3], [2, 1]], [90, 80]), best_mix([5, 4], [[6, 4], [1, 2]], [24, 6]))
