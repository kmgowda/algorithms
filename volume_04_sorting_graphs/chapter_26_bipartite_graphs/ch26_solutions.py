"""Volume 4, Chapter 26 - Thinking Problems: model solutions.

Run:  python3 ch26_solutions.py
"""

from __future__ import annotations

from ch26_examples import MEMBERS, QUARRELS, adjacency, two_colour

# Thinking Problem 2: the club grows by two trios; in each, the middle member has argued with the other two
NEW_MEMBERS = ["Hal", "Ivy", "Kim", "Lea", "Max", "Ned"]
NEW_QUARRELS = [("Hal", "Ivy"), ("Ivy", "Kim"), ("Lea", "Max"), ("Max", "Ned")]


def pieces_with_sides(adj: dict, colour: dict) -> list[tuple[list, list]]:
    """Each connected piece as (its colour-0 side, its colour-1 side), in the order the pieces are met."""
    seen, out = set(), []
    for s in adj:
        if s in seen:
            continue
        piece, i = [s], 0
        seen.add(s)
        while i < len(piece):
            for w in adj[piece[i]]:
                if w not in seen:
                    seen.add(w)
                    piece.append(w)
            i += 1
        out.append(([v for v in piece if colour[v] == 0], [v for v in piece if colour[v] == 1]))
    return out


def balanced_teams(adj: dict) -> tuple[list, list] | None:
    """Thinking Problem 2: two teams with every quarrel between them and sizes as equal as possible, or None if
    no two-colouring exists. Each piece may be flipped independently, so this is a subset-sum over the pieces:
    reach[k] maps every blue-team size reachable with the first k pieces to (previous size, flipped?).
    Cost O(V + E) for the colouring plus O(c * V) for c pieces."""
    colour, _ = two_colour(adj)
    if colour is None:
        return None
    pieces = pieces_with_sides(adj, colour)
    reach = [{0: None}]
    for a, b in pieces:
        nxt = {}
        for t in reach[-1]:
            nxt.setdefault(t + len(a), (t, False))
            nxt.setdefault(t + len(b), (t, True))
        reach.append(nxt)
    n = len(adj)
    t = min(reach[-1], key=lambda size: (abs(n - 2 * size), -size))
    blue, amber = [], []
    for k in range(len(pieces) - 1, -1, -1):
        t, flipped = reach[k + 1][t]
        a, b = pieces[k]
        blue += b if flipped else a
        amber += a if flipped else b
    rank = {v: i for i, v in enumerate(adj)}
    return sorted(blue, key=rank.get), sorted(amber, key=rank.get)


def count_two_colourings(adj: dict) -> int:
    """Thinking Problem 1: a graph with c pieces has 2**c two-colourings if it is bipartite, else 0."""
    colour, _ = two_colour(adj)
    return 0 if colour is None else 2 ** len(pieces_with_sides(adj, colour))


def greedy_scan_colour(adj: dict, order: list) -> dict | None:
    """Thinking Problem 3, the FLAWED method: colour places in a fixed order, each with a colour unused by its
    already-coloured neighbours, and give up when both colours are used. It can wrongly answer 'not bipartite'."""
    colour = {}
    for v in order:
        used = {colour[w] for w in adj[v] if w in colour}
        if len(used) == 2:
            return None
        colour[v] = 0 if 0 not in used else 1
    return colour


if __name__ == "__main__":
    club = adjacency(MEMBERS + NEW_MEMBERS, QUARRELS + NEW_QUARRELS)
    print(balanced_teams(club))
    print(count_two_colourings(club), count_two_colourings(adjacency(MEMBERS, QUARRELS)))
    path = adjacency("ABCD", [("A", "B"), ("B", "C"), ("C", "D")])
    print(greedy_scan_colour(path, ["A", "D", "B", "C"]), two_colour(path))
