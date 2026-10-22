"""Volume 4, Chapter 16 - Thinking Problems: model solutions (Section 16.14).

Run:  python3 ch16_solutions.py
"""

from __future__ import annotations


def is_tree(adj: dict) -> bool:
    """Thinking Problem 2: is the undirected graph a tree (connected, no cycle)? O(V) time, even when E is huge.
    adj lists each road at both ends (a self-loop appears twice in its own list, as in ch16_examples.adjacency)."""
    n = len(adj)
    if n == 0:
        return False                      # a tree has at least one place
    total = 0
    for v in adj:                         # add degrees, but stop as soon as there are too many roads
        total += len(adj[v])
        if total > 2 * (n - 1):
            return False
    if total != 2 * (n - 1):
        return False                      # fewer than n - 1 roads: cannot be connected
    start = next(iter(adj))
    seen, frontier = {start}, [start]
    while frontier:                       # the explore loop of Section 16.5 reads only 2(n - 1) entries
        v = frontier.pop()
        for w in adj[v]:
            if w not in seen:
                seen.add(w)
                frontier.append(w)
    return len(seen) == n


def explore_marking_late(adj: dict, start, limit: int = 1000) -> list:
    """Thinking Problem 3: the buggy walk that marks a place only when it leaves the frontier and never
    checks again. It visits some places more than once (at most `limit` visits are recorded)."""
    visited, frontier, order = set(), [start], []
    while frontier and len(order) < limit:
        v = frontier.pop()
        visited.add(v)
        order.append(v)
        for w in adj[v]:
            if w not in visited:
                frontier.append(w)
    return order


if __name__ == "__main__":
    import ch16_examples as ex
    print(is_tree(ex.adjacency()), is_tree({"A": ["B"], "B": ["A"]}))
    print(explore_marking_late(ex.adjacency(), "Library"))
