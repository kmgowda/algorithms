"""Volume 2, Chapter 14 - model solution for Thinking Problem 2: place every key without eviction chains.

Run:  python3 ch14_solutions.py
"""

from __future__ import annotations


def place_all(keys, f0, f1, m: int):
    """Give every key one of its two homes, all different, or return None if that is impossible (Section 14.18).

    Slots are dots 0..m-1 (table 1) and m..2m-1 (table 2); each key is a line between its two homes.
    1. Count: a piece of the picture with more lines than dots cannot be placed.
    2. Peel: a dot touching exactly one unplaced line must hold that line's key.
    3. What is left of each piece is a single loop; walk round it, giving each key the dot it leaves from.
    O(n + m) time apart from the near-constant union-find factor.
    """
    ends = [(f0(k), m + f1(k)) for k in keys]
    parent = list(range(2 * m))

    def root(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    dots, lines = [1] * (2 * m), [0] * (2 * m)
    for a, b in ends:
        ra, rb = root(a), root(b)
        if ra != rb:
            parent[rb] = ra
            dots[ra] += dots[rb]
            lines[ra] += lines[rb]
        lines[ra] += 1
    if any(lines[v] > dots[v] for v in range(2 * m) if root(v) == v):
        return None
    touching = [[] for _ in range(2 * m)]
    for e, (a, b) in enumerate(ends):
        touching[a].append(e)
        touching[b].append(e)
    degree = [len(t) for t in touching]
    home = [None] * len(keys)
    leaves = [v for v in range(2 * m) if degree[v] == 1]
    while leaves:
        v = leaves.pop()
        if degree[v] != 1:
            continue
        e = next(e for e in touching[v] if home[e] is None)
        home[e] = v
        for w in ends[e]:
            degree[w] -= 1
            if degree[w] == 1:
                leaves.append(w)
    for e in range(len(keys)):
        v = ends[e][0]
        while home[e] is None:             # walk round the loop that e lies on
            home[e] = v
            v = ends[e][1] if ends[e][0] == v else ends[e][0]
            nxt = [x for x in touching[v] if home[x] is None]
            if not nxt:
                break
            e = nxt[0]
    T = [[None] * m, [None] * m]
    for e, v in enumerate(home):
        T[v // m][v % m] = keys[e]
    return T


if __name__ == "__main__":
    from ch14_examples import SHELF, h1, h2
    print(place_all(SHELF + [108], lambda k: h1(k, 11), lambda k: h2(k, 11), 11))
    print(place_all([25, 146, 267], lambda k: h1(k, 11), lambda k: h2(k, 11), 11))
