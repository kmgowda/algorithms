"""Volume 5, Chapter 11 - Thinking Problems: the assignment whose longest trip is as short as possible (Thinking
Problem 2), and the "matched desks" cover that is not a cover (Thinking Problem 3).

Run:  python3 ch11_solutions.py
"""

from __future__ import annotations

import ch11_examples as ex


def bottleneck_assignment(cost: list) -> tuple[float, list]:
    """Give each row a different column so that the LARGEST chosen cost is as small as possible (Thinking Problem 2).
    Binary search over the distinct costs: threshold T works exactly when the cells of cost <= T hold a perfect
    matching, found by the chapter's augmenting-path method. Returns (T, column chosen for each row)."""
    n = len(cost)
    if n == 0:
        return 0, []
    values = sorted({c for row in cost for c in row})

    def match(limit):
        allowed = {i: [j for j in range(n) if cost[i][j] <= limit] for i in range(n)}
        owner = ex.max_matching(allowed)                 # column -> row
        return owner if len(owner) == n else None

    lo, hi = 0, len(values) - 1                         # the largest value always works
    while lo < hi:
        mid = (lo + hi) // 2
        if match(values[mid]) is not None:
            hi = mid
        else:
            lo = mid + 1
    pick = [0] * n
    for j, i in match(values[lo]).items():
        pick[i] = j
    return values[lo], pick


def matched_desks(can_do: dict) -> list:
    """The wrong certificate of Thinking Problem 3: the desks used by a maximum matching."""
    return list(ex.max_matching(can_do))


def uncovered(can_do: dict, cover: list) -> list:
    """The trained pairings that touch nothing in `cover`."""
    return [(p, d) for p, ds in can_do.items() for d in ds if p not in cover and d not in cover]


if __name__ == "__main__":
    print(bottleneck_assignment(ex.MINUTES), bottleneck_assignment(ex.SHELVING), bottleneck_assignment([[1, 6], [5, 9]]))
    print(uncovered(ex.CAN_DO_SIX, matched_desks(ex.CAN_DO_SIX)))
