"""Volume 12, Chapter 9 - Solutions to the exercises."""

from __future__ import annotations

from collections import deque
from typing import Hashable

from ch09_examples import Node


def max_path_sum(root: Node) -> int:
    """Exercise 1 (LeetCode 124 idea): largest sum of a path between any two nodes (values may be negative).
    Each node returns the best downward path; the best path through it joins its two best non-negative branches."""
    best = root.value

    def down(node: Node) -> int:
        nonlocal best
        gains = sorted((max(0, down(c)) for c in node.children), reverse=True) + [0, 0]
        best = max(best, node.value + gains[0] + gains[1])
        return node.value + gains[0]

    down(root)
    return best


def count_paths_dag(adj: dict[Hashable, list[Hashable]], source: Hashable, target: Hashable) -> int:
    """Exercise 2: number of routes in a DAG - ways[v] = sum of ways of its predecessors, in topological order."""
    indeg = {v: 0 for v in adj}
    for v in adj:
        for w in adj[v]:
            indeg[w] += 1
    ways = {v: 0 for v in adj}
    ways[source] = 1
    q = deque(v for v in adj if indeg[v] == 0)
    while q:
        v = q.popleft()
        for w in adj[v]:
            ways[w] += ways[v]
            indeg[w] -= 1
            if indeg[w] == 0:
                q.append(w)
    return ways[target]


def min_cameras(root: Node) -> int:
    """Exercise 3 (LeetCode 968): fewest cameras so every node is watched (a camera watches itself, its parent and
    children). Each node reports a state: 0 = not watched, 1 = watched without camera, 2 = has a camera."""
    cameras = 0

    def state(node: Node) -> int:
        nonlocal cameras
        kids = [state(c) for c in node.children]
        if 0 in kids:
            cameras += 1
            return 2
        return 1 if 2 in kids else 0

    if state(root) == 0:
        cameras += 1
    return cameras


if __name__ == "__main__":
    print(max_path_sum(Node(-10, Node(9), Node(20, Node(15), Node(7)))),
          count_paths_dag({"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}, "a", "d"),
          min_cameras(Node(0, Node(0, Node(0), Node(0)))))
