"""Volume 3, Chapter 1 - What Is a Tree?: companion code for the Thinking Problems (Section 1.16).

Run:  python3 ch01_solutions.py
"""

from __future__ import annotations

ACTIVE, DONE = 1, 2


def is_tree(parent: dict, extra_nodes=()) -> bool:
    """Thinking Problem 2: is the map child -> parent a tree? Exactly one node may have no parent (the root), and
    every walk upwards must reach it. Each node is marked ACTIVE once and DONE once: O(n) time.
    extra_nodes lists nodes that appear in no pair (a one-node tree has no edges)."""
    nodes = set(parent) | set(parent.values()) | set(extra_nodes)
    roots = [v for v in nodes if v not in parent]
    if len(roots) != 1:
        return False
    state = {roots[0]: DONE}
    for v in nodes:
        path = []
        while v not in state:              # climb until a node already judged
            state[v] = ACTIVE
            path.append(v)
            v = parent[v]
        if state[v] == ACTIVE:             # met our own walk again: a loop
            return False
        for u in path:
            state[u] = DONE
    return True


def leaves_and_inner(children: dict, root) -> tuple[int, int]:
    """Thinking Problem 1: (number of leaves, number of inner nodes) of a tree given as a children map."""
    kids = children.get(root, [])
    if not kids:
        return 1, 0
    counts = [leaves_and_inner(children, k) for k in kids]
    return sum(c[0] for c in counts), 1 + sum(c[1] for c in counts)


if __name__ == "__main__":
    from ch01_examples import SECTIONS, parents
    print(is_tree(parents(SECTIONS)), is_tree({"B": "A", "C": "D", "D": "C"}), leaves_and_inner(SECTIONS, "Library"))
