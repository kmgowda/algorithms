"""Volume 6, Chapter 20 - Thinking Problems: model solutions (a rerooting design, a leaf-first greedy, a buggy reroot).

Run:  python3 ch20_solutions.py
"""

from __future__ import annotations


def total_distances(reports: dict, root) -> dict:
    """Thinking Problem 2: for every person, the sum of steps along the tree to all other people, in O(n).
    Pass 1 (post-order): size[p] and below[p] = sum of distances from p to its own subtree.
    Pass 2 (pre-order): moving the viewpoint from p to report r brings size[r] people one step closer and
    the other n - size[r] one step farther: total[r] = total[p] + n - 2 * size[r]."""
    size, below = {}, {}

    def up(p):
        size[p], below[p] = 1, 0
        for r in reports[p]:
            up(r)
            size[p] += size[r]
            below[p] += below[r] + size[r]

    up(root)
    n, total = size[root], {root: below[root]}

    def down(p):
        for r in reports[p]:
            total[r] = total[p] + n - 2 * size[r]
            down(r)

    down(root)
    return total


def leaf_first(reports: dict, root) -> set:
    """Thinking Problem 1: with equal fun, invite every leaf, remove the leaves and their managers, repeat."""
    boss = {r: p for p, rs in reports.items() for r in rs}
    alive = set(reports)
    kids = {p: set(rs) for p, rs in reports.items()}
    chosen = set()
    while alive:
        leaves = {p for p in alive if not (kids[p] & alive)}
        chosen |= leaves
        gone = leaves | {boss[p] for p in leaves if p in boss}
        alive -= gone
    return chosen


def farthest_wrong(reports: dict, root) -> dict:
    """Thinking Problem 3: rerooting that forgets to leave out the report's own branch. Wrong on a chain."""
    down, up = {}, {root: 0}

    def go_down(p):
        down[p] = max((1 + go_down(r) for r in reports[p]), default=0)
        return down[p]

    go_down(root)

    def go_up(p):
        for r in reports[p]:
            up[r] = 1 + max([up[p]] + [1 + down[s] for s in reports[p]])
            go_up(r)

    go_up(root)
    return {p: max(down[p], up[p]) for p in down}


if __name__ == "__main__":
    from ch20_examples import REPORTS
    print(total_distances(REPORTS, "Director"))
    print(leaf_first(REPORTS, "Director"))
    print(farthest_wrong({"A": ["B"], "B": ["C"], "C": []}, "A"))
