"""Volume 7, Chapter 24 - model solution to the design Thinking Problem: how far can one loan rate move before
the best plan changes? (sensitivity of the objective, read from the final tableau in O(m + n) after solving)

Run:  python3 ch24_solutions.py
"""

from __future__ import annotations

from ch24_examples import simplex


def cost_range(A: list, b: list, c: list, j: int):
    """The interval (low, high) of values for c[j] that keep the current best plan optimal; None means no limit.
    Returns None if the program has no best plan."""
    res = simplex(A, b, c)
    if res["status"] != "optimal":
        return None
    T, basis = res["tableau"], res["basis"]
    reduced = T[-1][:-1]
    if j not in basis:                       # not made: it pays once its reduced cost turns positive
        return None, c[j] - reduced[j]
    r = basis.index(j)
    low, high = None, None
    for k, ck in enumerate(reduced):
        if k in basis or T[r][k] == 0:
            continue
        bound = ck / T[r][k]                 # reduced cost of k becomes ck - delta * T[r][k]; it must stay <= 0
        if T[r][k] > 0:
            low = bound if low is None else max(low, bound)
        else:
            high = bound if high is None else min(high, bound)
    return (None if low is None else c[j] + low), (None if high is None else c[j] + high)


if __name__ == "__main__":
    from ch24_examples import LIBRARY_A, LIBRARY_B, LIBRARY_C
    print("hardbacks:", cost_range(LIBRARY_A, LIBRARY_B, LIBRARY_C, 0))
    print("paperbacks:", cost_range(LIBRARY_A, LIBRARY_B, LIBRARY_C, 1))
