"""Volume 12, Chapter 9 - DP on Trees and Graphs: Multistage Graphs, Tree DP.

Run:  python3 ch09_examples.py
"""

from __future__ import annotations

import math
from typing import Hashable


def multistage_shortest(stages: list[list[str]], cost: dict[tuple[str, str], float]) -> tuple[float, list[str]]:
    """A journey through stages (e.g. cities on each day). Edges only go from one stage to the next, so the graph is
    a DAG and best[v] = min over the next stage of cost(v, w) + best[w], computed from the LAST stage backward."""
    best: dict[str, float] = {v: 0.0 for v in stages[-1]}
    nxt: dict[str, str | None] = {v: None for v in stages[-1]}
    for s in range(len(stages) - 2, -1, -1):
        for v in stages[s]:
            options = [(cost[(v, w)] + best[w], w) for w in stages[s + 1] if (v, w) in cost]
            best[v], nxt[v] = min(options) if options else (math.inf, None)
    start = min(stages[0], key=lambda v: best[v])
    path, v = [start], start
    while nxt[v] is not None:
        v = nxt[v]                                       # type: ignore[assignment]
        path.append(v)
    return best[start], path


class Node:
    def __init__(self, value: int, *children: "Node") -> None:
        self.value = value
        self.children = list(children)


def tree_robber(root: Node | None) -> int:
    """LeetCode 337 (house robber III, on any tree): houses form a tree; never take a node and its child.
    For each node return (best if taken, best if skipped) - computed from the children up (post-order)."""
    def solve(node: Node) -> tuple[int, int]:
        take, skip = node.value, 0
        for child in node.children:
            c_take, c_skip = solve(child)
            take += c_skip                                   # child must be skipped
            skip += max(c_take, c_skip)                      # child free to choose
        return take, skip
    return max(solve(root)) if root else 0


def tree_diameter(adj: dict[Hashable, list[Hashable]], root: Hashable) -> int:
    """LeetCode 543 idea: longest path (in edges) between any two nodes. Each node reports its deepest branch;
    the best path THROUGH a node uses its two deepest branches. Iterative post-order, no recursion limit."""
    parent = {root: None}
    order, stack = [], [root]
    while stack:
        v = stack.pop()
        order.append(v)
        for w in adj[v]:
            if w != parent[v]:
                parent[w] = v
                stack.append(w)
    depth = {v: 0 for v in adj}
    best = 0
    for v in reversed(order):                              # children before parents
        top1 = top2 = 0
        for w in adj[v]:
            if w != parent[v]:
                d = depth[w] + 1
                if d > top1:
                    top1, top2 = d, top1
                elif d > top2:
                    top2 = d
        depth[v] = top1
        best = max(best, top1 + top2)
    return best


def subtree_sizes(adj: dict[Hashable, list[Hashable]], root: Hashable) -> dict[Hashable, int]:
    """Industry example: size of each manager's team (everyone below them in the org chart, including themselves)."""
    parent = {root: None}
    order, stack = [], [root]
    while stack:
        v = stack.pop()
        order.append(v)
        for w in adj[v]:
            if w != parent[v]:
                parent[w] = v
                stack.append(w)
    size = {v: 1 for v in adj}
    for v in reversed(order):
        if parent[v] is not None:
            size[parent[v]] += size[v]                      # type: ignore[index]
    return size


def party_guests(org: dict[str, list[str]], fun: dict[str, int], boss: str) -> int:
    """Industry example: invite employees to a party for maximum fun, but nobody comes with their direct manager."""
    def build(name: str) -> Node:
        return Node(fun[name], *(build(r) for r in org.get(name, [])))
    return tree_robber(build(boss))


if __name__ == "__main__":
    stages = [["Home"], ["A1", "A2"], ["B1", "B2", "B3"], ["Goa"]]
    cost = {("Home", "A1"): 4, ("Home", "A2"): 2, ("A1", "B1"): 3, ("A1", "B2"): 1, ("A2", "B2"): 6, ("A2", "B3"): 2,
            ("B1", "Goa"): 2, ("B2", "Goa"): 3, ("B3", "Goa"): 7}
    print("multistage:", multistage_shortest(stages, cost))
    tree = Node(3, Node(4, Node(1), Node(3)), Node(5, Node(1)))
    print("tree robber:", tree_robber(tree))
    adj = {1: [2, 3], 2: [1, 4, 5], 3: [1], 4: [2], 5: [2, 6], 6: [5]}
    print("diameter:", tree_diameter(adj, 1), "| team sizes:", subtree_sizes(adj, 1))
    org = {"CEO": ["CTO", "CFO"], "CTO": ["Dev1", "Dev2"], "CFO": ["Acc"]}
    print("party fun:", party_guests(org, {"CEO": 5, "CTO": 3, "CFO": 2, "Dev1": 4, "Dev2": 4, "Acc": 6}, "CEO"))
