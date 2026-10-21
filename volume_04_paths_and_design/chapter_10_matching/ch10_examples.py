"""Volume 4, Chapter 10 - Matching and Assignment: pair people with jobs.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations

import itertools

# Which festival desks each volunteer is trained for.
CAN_DO = {"Ana": ["Tickets", "Cafe"], "Ben": ["Tickets"], "Cai": ["Cafe", "Stage", "Signs"], "Dev": ["Stage"],
          "Eva": ["Signs", "First aid"]}


def max_matching(can_do: dict, log: list | None = None) -> dict:
    """Augmenting paths (Figure 10.2): give each volunteer a desk, moving earlier volunteers along if needed.
    Returns {desk: volunteer}."""
    owner: dict = {}

    def try_assign(person, seen):
        for desk in can_do[person]:
            if desk in seen:
                continue
            seen.add(desk)
            if desk not in owner or try_assign(owner[desk], seen):
                owner[desk] = person                  # take the desk; its old owner (if any) moved elsewhere
                return True
        return False

    for person in can_do:
        ok = try_assign(person, set())
        if log is not None:
            log.append((person, ok, dict(owner)))
    return owner


def greedy_matching(can_do: dict) -> dict:
    """Each volunteer takes their first free desk and never moves: can leave people out."""
    owner = {}
    for person, desks in can_do.items():
        for d in desks:
            if d not in owner:
                owner[d] = person
                break
    return owner


# Minutes each driver needs to reach each branch (an assignment problem).
DRIVERS = ["Ana", "Ben", "Cai", "Dev"]
BRANCHES = ["North", "East", "South", "West"]
MINUTES = [[2, 9, 8, 9], [1, 3, 5, 2], [3, 2, 8, 7], [7, 1, 1, 5]]


def best_assignment(cost: list) -> tuple[int, tuple]:
    """Try every way of giving each driver a different branch (n! ways); keep the cheapest."""
    n = len(cost)
    return min((sum(cost[i][p[i]] for i in range(n)), p) for p in itertools.permutations(range(n)))


def greedy_assignment(cost: list) -> tuple[int, list]:
    """Repeatedly take the cheapest remaining driver-branch pair."""
    n, used_r, used_c, total, pairs = len(cost), set(), set(), 0, []
    cells = sorted((cost[i][j], i, j) for i in range(n) for j in range(n))
    for c, i, j in cells:
        if i not in used_r and j not in used_c:
            used_r.add(i)
            used_c.add(j)
            total += c
            pairs.append((i, j))
    return total, pairs


if __name__ == "__main__":
    log = []
    print(max_matching(CAN_DO, log))
    for row in log:
        print(row)
    print(greedy_matching(CAN_DO))
    print(best_assignment(MINUTES), greedy_assignment(MINUTES))
