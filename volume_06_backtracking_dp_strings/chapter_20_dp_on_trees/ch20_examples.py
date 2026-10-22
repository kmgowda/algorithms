"""Volume 6, Chapter 20 - DP on Trees: answers flow up from the leaves.

Run:  python3 ch20_examples.py
"""

from __future__ import annotations

import itertools

# The library's staff tree: each person and their direct reports, with how much each enjoys parties.
REPORTS = {"Director": ["Maya", "Omar"], "Maya": ["Ben", "Cai", "Dev"], "Omar": ["Eva", "Fay"], "Ben": [], "Cai": ["Gus"],
           "Dev": [], "Eva": [], "Fay": ["Hal", "Ivy"], "Gus": [], "Hal": [], "Ivy": []}
FUN = {"Director": 3, "Maya": 8, "Omar": 4, "Ben": 2, "Cai": 5, "Dev": 3, "Eva": 6, "Fay": 7, "Gus": 4, "Hal": 2, "Ivy": 3}


def party(reports: dict, fun: dict, root) -> tuple[int, list, dict]:
    """No one attends with their direct manager. For each person: (best if they come, best if they stay away),
    computed after their reports (Figure 20.2). Returns (best fun, guests, the pair for each person)."""
    pair = {}

    def solve(p):
        come, away = fun[p], 0
        for r in reports[p]:
            rc, ra = solve(r)
            come += ra                                 # if p comes, each report must stay away
            away += max(rc, ra)                        # if p stays away, each report does whatever is better
        pair[p] = (come, away)
        return come, away

    solve(root)
    guests = []

    def pick(p, may_come):
        come = may_come and pair[p][0] >= pair[p][1]
        if come:
            guests.append(p)
        for r in reports[p]:
            pick(r, not come)

    pick(root, True)
    return max(pair[root]), sorted(guests), pair


def party_pair(reports: dict, fun: dict, p) -> tuple[int, int]:
    """Party(p) of Section 20.4: (most fun in p's subtree if p comes, most if p stays away)."""
    come, away = fun[p], 0
    for r in reports[p]:
        rc, ra = party_pair(reports, fun, r)
        come += ra                                     # p comes: r must stay away
        away += max(rc, ra)                            # p stays away: r chooses freely
    return come, away


def subtree_sizes(reports: dict, root) -> dict:
    """People in each person's part of the tree, including themselves: another answer that flows up."""
    size = {}

    def go(p):
        size[p] = 1 + sum(go(r) for r in reports[p])
        return size[p]

    go(root)
    return size


def farthest_colleague(reports: dict, root) -> dict:
    """Rerooting (Section 20.7): for every person, the most steps along the tree to any other person.
    Pass 1 (up): down[p] = longest chain down from p. Pass 2 (down): up[r] = longest chain from r that starts by
    going to r's manager p: 1 + the best of up[p] and down through p's other reports. Answer = max(down, up)."""
    down, up = {}, {root: 0}

    def go_down(p):
        down[p] = max((1 + go_down(r) for r in reports[p]), default=0)
        return down[p]

    go_down(root)

    def go_up(p):
        kids = reports[p]
        branch = [1 + down[r] for r in kids]          # chain from p through each report
        for i, r in enumerate(kids):
            others = max((b for k, b in enumerate(branch) if k != i), default=0)
            up[r] = 1 + max(up[p], others)
            go_up(r)

    go_up(root)
    return {p: max(down[p], up[p]) for p in down}


def brute(reports: dict, fun: dict) -> int:
    people = list(fun)
    boss = {r: p for p, rs in reports.items() for r in rs}
    best = 0
    for k in range(len(people) + 1):
        for group in itertools.combinations(people, k):
            g = set(group)
            if all(boss.get(x) not in g for x in g):
                best = max(best, sum(fun[x] for x in g))
    return best


if __name__ == "__main__":
    total, guests, pair = party(REPORTS, FUN, "Director")
    print(total, guests, pair)
    print(brute(REPORTS, FUN), subtree_sizes(REPORTS, "Director"))
