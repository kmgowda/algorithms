"""Volume 8, Chapter 5 - Solutions to the exercises."""

from __future__ import annotations

from collections import deque
from typing import Hashable

from ch05_examples import Graph, bfs_distances


def open_lock(deadends: list[str], target: str) -> int:
    """Exercise 1 (LeetCode 752): a 4-wheel lock starts at 0000; each move turns one wheel by 1.
    Fewest moves to target, avoiding dead-end codes. The graph (10,000 codes) is generated on the fly."""
    blocked = set(deadends)
    if "0000" in blocked:
        return -1
    queue, seen = deque([("0000", 0)]), {"0000"}
    while queue:
        code, moves = queue.popleft()
        if code == target:
            return moves
        for i in range(4):
            d = int(code[i])
            for nd in ((d + 1) % 10, (d - 1) % 10):
                nxt = code[:i] + str(nd) + code[i + 1:]
                if nxt not in blocked and nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, moves + 1))
    return -1


def knight_moves(size: int, start: tuple[int, int], goal: tuple[int, int]) -> int:
    """Exercise 2: fewest knight moves on a size x size chessboard."""
    jumps = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
    queue, dist = deque([start]), {start: 0}
    while queue:
        r, c = queue.popleft()
        if (r, c) == goal:
            return dist[(r, c)]
        for dr, dc in jumps:
            nxt = (r + dr, c + dc)
            if 0 <= nxt[0] < size and 0 <= nxt[1] < size and nxt not in dist:
                dist[nxt] = dist[(r, c)] + 1
                queue.append(nxt)
    return -1


def within_k(graph: Graph, start: Hashable, k: int) -> list[Hashable]:
    """Exercise 3: everyone within k friendship steps (e.g. 2nd-degree connections)."""
    return sorted((v for v, d in bfs_distances(graph, start).items() if 0 < d <= k), key=str)


def level_widths(graph: Graph, start: Hashable) -> list[int]:
    """Exercise 4: how many vertices at each distance - the 'ripple' sizes."""
    counts: dict[int, int] = {}
    for d in bfs_distances(graph, start).values():
        counts[d] = counts.get(d, 0) + 1
    return [counts[d] for d in sorted(counts)]


if __name__ == "__main__":
    print(open_lock(["0201", "0101", "0102", "1212", "2002"], "0202"), knight_moves(8, (0, 0), (7, 7)))
    g = {"a": ["b"], "b": ["a", "c"], "c": ["b", "d"], "d": ["c"]}
    print(within_k(g, "a", 2), level_widths(g, "b"))
