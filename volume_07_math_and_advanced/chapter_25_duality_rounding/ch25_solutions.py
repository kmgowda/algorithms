"""Volume 7, Chapter 25 - model solution to the design Thinking Problem: weighted set cover when every title is
offered by at most f suppliers, within f times the best, by rounding the linear program at 1/f.

Run:  python3 ch25_solutions.py
"""

from __future__ import annotations

from fractions import Fraction

from ch25_examples import simplex


def round_set_cover(universe: set, sets: dict, cost: dict) -> list:
    """Relax 'choose suppliers covering every title' to 0 <= x_S, sum of x_S over S holding e >= 1; keep x_S >= 1/f."""
    names = sorted(sets)
    titles = sorted(universe)
    if not titles:
        return []
    if any(not any(e in sets[s] for s in names) for e in titles):
        raise ValueError("some title is offered by no supplier")
    A = [[-1 if e in sets[s] else 0 for s in names] for e in titles]
    res = simplex(A, [-1] * len(titles), [-cost[s] for s in names])
    f = max(sum(e in sets[s] for s in names) for e in titles)
    return [s for s, x in zip(names, res["x"]) if x >= Fraction(1, f)]


if __name__ == "__main__":
    sets = {"A": {1, 2, 3}, "B": {3, 4}, "C": {4, 5, 1}, "D": {2, 5}}
    print(round_set_cover({1, 2, 3, 4, 5}, sets, {"A": 3, "B": 1, "C": 3, "D": 2}))
