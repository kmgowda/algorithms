"""Volume 8, Chapter 5 - Breadth-First Search: Ripples in a Pond; Shortest Paths in Unweighted Graphs.

Run:  python3 ch05_examples.py
"""

from __future__ import annotations

from collections import deque
from typing import Hashable, Iterable

Graph = dict[Hashable, list[Hashable]]


def bfs_distances(graph: Graph, start: Hashable) -> dict[Hashable, int]:
    """Visit vertices in rings: distance 0, then 1, then 2 ... A queue keeps the rings in order."""
    dist = {start: 0}
    queue = deque([start])
    while queue:
        v = queue.popleft()
        for w in graph.get(v, []):
            if w not in dist:                    # mark when DISCOVERED, so nothing is queued twice
                dist[w] = dist[v] + 1
                queue.append(w)
    return dist


def shortest_path(graph: Graph, start: Hashable, goal: Hashable) -> list[Hashable] | None:
    """Fewest-edge path: BFS with a parent map. The first time BFS reaches goal is via a shortest route."""
    parent: dict[Hashable, Hashable | None] = {start: None}
    queue = deque([start])
    while queue:
        v = queue.popleft()
        if v == goal:
            path = []
            while v is not None:
                path.append(v)
                v = parent[v]
            return path[::-1]
        for w in graph.get(v, []):
            if w not in parent:
                parent[w] = v
                queue.append(w)
    return None


def multi_source_distances(graph: Graph, sources: Iterable[Hashable]) -> dict[Hashable, int]:
    """Practical example: distance from every town to its NEAREST hospital - start BFS from all hospitals at once."""
    dist = {s: 0 for s in sources}
    queue = deque(dist)
    while queue:
        v = queue.popleft()
        for w in graph.get(v, []):
            if w not in dist:
                dist[w] = dist[v] + 1
                queue.append(w)
    return dist


def degrees_of_separation(friends: Graph, a: Hashable, b: Hashable) -> int:
    """Industry example: how many friendship steps separate two people (-1 if not connected)."""
    return bfs_distances(friends, a).get(b, -1)


def word_ladder(start: str, goal: str, words: list[str]) -> int:
    """Industry example (LeetCode 127): change one letter at a time through dictionary words.
    Words are vertices; one-letter changes are edges built on the fly. Returns the number of words on the ladder."""
    dictionary = set(words)
    if goal not in dictionary:
        return 0
    queue, seen = deque([(start, 1)]), {start}
    while queue:
        word, steps = queue.popleft()
        if word == goal:
            return steps
        for i in range(len(word)):
            for ch in "abcdefghijklmnopqrstuvwxyz":
                nxt = word[:i] + ch + word[i + 1:]
                if nxt in dictionary and nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, steps + 1))
    return 0


if __name__ == "__main__":
    metro = {"Central": ["Park", "Market"], "Park": ["Central", "Zoo"], "Market": ["Central", "Port", "Zoo"],
             "Zoo": ["Park", "Market", "Airport"], "Port": ["Market"], "Airport": ["Zoo"]}
    print(bfs_distances(metro, "Central"))
    print("fewest stops Central->Airport:", shortest_path(metro, "Central", "Airport"))
    print("nearest hospital distance:", multi_source_distances(metro, ["Port", "Airport"]))
    print(word_ladder("cold", "warm", ["cord", "card", "ward", "warm", "word", "worm"]))
