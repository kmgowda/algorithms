"""Volume 6, Chapter 23 - Approximation Algorithms: fast answers with a proven bound on how far from best they can be.

Run:  python3 ch23_examples.py
"""

from __future__ import annotations

import itertools
import random

TOWN = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
ROADS = [("Library", "School"), ("Library", "Park"), ("School", "Market"), ("Park", "Market"), ("School", "Station"),
         ("Market", "Station"), ("Market", "Museum"), ("Park", "Hospital"), ("Hospital", "Museum"), ("Station", "Harbour"),
         ("Museum", "Harbour"), ("Station", "Museum")]


def cover_by_matching(edges: list) -> list:
    """2-approximation for vertex cover (Figure 23.2): take both ends of any road not yet covered."""
    cover = []
    for a, b in edges:
        if a not in cover and b not in cover:
            cover += [a, b]
    return cover


def smallest_cover(vertices: list, edges: list) -> list:
    for k in range(len(vertices) + 1):
        for g in itertools.combinations(vertices, k):
            if all(a in g or b in g for a, b in edges):
                return list(g)


def first_fit_decreasing(sizes: list, capacity: int) -> list:
    """Bin packing: largest box first, into the first bin with room (Figure 23.3). Uses at most about 11/9 of the best."""
    bins = []
    for s in sorted(sizes, reverse=True):
        if s > capacity:
            raise ValueError("a box is larger than a bin")
        for b in bins:
            if sum(b) + s <= capacity:
                b.append(s)
                break
        else:
            bins.append([s])
    return bins


def fewest_bins(sizes: list, capacity: int) -> int:
    for k in range(1, len(sizes) + 1):
        for assign in itertools.product(range(k), repeat=len(sizes)):
            load = [0] * k
            for s, b in zip(sizes, assign):
                load[b] += s
            if max(load) <= capacity:
                return k
    return 0


if __name__ == "__main__":
    c = cover_by_matching(ROADS)
    print(c, len(c), smallest_cover(TOWN, ROADS))
    boxes = [7, 6, 5, 4, 4, 3, 2, 2, 2, 1]
    print(first_fit_decreasing(boxes, 10), fewest_bins(boxes, 10))
    r = random.Random(23)
    worst = 0
    for _ in range(200):
        vs = list(range(7))
        es = [e for e in itertools.combinations(vs, 2) if r.random() < 0.35]
        if es:
            worst = max(worst, len(cover_by_matching(es)) / len(smallest_cover(vs, es)))
    print(worst)
