"""Chapter 33, Section 33.11: one hard problem, every method. The fewest wardens who between them watch every
road of the town (vertex cover), found by exhaustive search, by branching (Chapter 28), by a greedy rule, by the
matching 2-approximation (Chapter 26), by LP rounding (Chapter 25), and by local search (Chapter 27)."""
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
for d in ("chapter_25_duality_rounding", "chapter_26_approximation", "chapter_28_exact_hard"):
    sys.path.insert(0, os.path.join(HERE, "..", d))

import ch25_examples as c25   # noqa: E402
import ch26_examples as c26   # noqa: E402
import ch28_examples as c28   # noqa: E402

TOWN, ROADS = c26.TOWN, c26.ROADS


def is_cover(cover, edges) -> bool:
    return all(a in cover or b in cover for a, b in edges)


def greedy_degree(vertices: list, edges: list) -> list:
    """Repeatedly take the place touching the most uncovered roads (ties: first in the list)."""
    left, cover = list(edges), []
    while left:
        v = max(vertices, key=lambda u: sum(u in e for e in left))
        cover.append(v)
        left = [e for e in left if v not in e]
    return cover


def local_search(vertices: list, edges: list, start: list | None = None) -> tuple[list, int]:
    """Start from every place and drop any warden whose roads are all watched by others, until none can go.
    Returns (cover, wardens dropped)."""
    cover, dropped = list(start or vertices), 0
    changed = True
    while changed:
        changed = False
        for v in list(cover):
            rest = [u for u in cover if u != v]
            if is_cover(rest, edges):
                cover, dropped, changed = rest, dropped + 1, True
    return cover, dropped


def local_search_orders(vertices: list = TOWN, edges: list = ROADS) -> dict:
    """Run local search from every order of the places: {cover size: how many orders end there}."""
    from itertools import permutations
    counts = {}
    for order in permutations(vertices):
        k = len(local_search(vertices, edges, list(order))[0])
        counts[k] = counts.get(k, 0) + 1
    return dict(sorted(counts.items()))


def compare(vertices: list = TOWN, edges: list = ROADS) -> dict:
    best = c26.smallest_cover(vertices, edges)
    k = len(best)
    found, tried = c28.cover_brute(vertices, edges, k)
    calls = [0]
    branched = c28.cover_branching(list(edges), k, calls)
    value, x = c25.cover_lp(vertices, edges, {v: 1 for v in vertices})
    rounded = c25.round_cover(x)
    return {"best": best, "brute": (found, tried), "branching": (branched, calls[0]),
            "greedy": greedy_degree(vertices, edges), "matching": c26.cover_by_matching(edges),
            "lp": (value, rounded), "local": local_search(vertices, edges)}


if __name__ == "__main__":
    for key, val in compare().items():
        print(key, val)
