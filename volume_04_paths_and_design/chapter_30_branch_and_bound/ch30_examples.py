"""Volume 4, Chapter 30 - Branch and Bound: prune any branch whose best possible result cannot beat the best found.

Run:  python3 ch30_examples.py
"""

from __future__ import annotations

import heapq
import random

# Chapter 12's books: (name, price, votes); budget 20 pounds, whole books only.
BOOKS = [("Atlas", 9, 6), ("Novel", 6, 4), ("Poems", 5, 6), ("Comic", 5, 2), ("Cookbook", 10, 7)]


def fractional_bound(items: list, i: int, room: float) -> float:
    """The most votes still possible if the remaining items could be bought in part (Chapter 14)."""
    best = 0.0
    for _, price, votes in items[i:]:
        if price <= room:
            room -= price
            best += votes
        else:
            return best + votes * room / price
    return best


def branch_and_bound(books: list, budget: int, use_bound: bool = True, log: list | None = None) -> tuple[int, list, int]:
    """Take-or-leave search in order of votes per pound, cutting branches whose bound cannot beat the best so far.
    Returns (votes, names, nodes visited)."""
    items = sorted(books, key=lambda b: b[2] / b[1], reverse=True)
    best = [0, []]
    nodes = [0]

    def go(i, room, votes, chosen):
        nodes[0] += 1
        if votes > best[0]:
            best[0], best[1] = votes, list(chosen)
        if i == len(items):
            return
        bound = votes + fractional_bound(items, i, room)
        if use_bound and bound <= best[0]:
            if log is not None:
                log.append((i, votes, round(bound, 2), best[0]))
            return                                    # even the optimistic bound cannot beat the best: prune
        name, price, v = items[i]
        if price <= room:
            chosen.append(name)
            go(i + 1, room - price, votes + v, chosen)
            chosen.pop()
        go(i + 1, room, votes, chosen)

    go(0, budget, 0, [])
    return best[0], best[1], nodes[0]


def best_first(books: list, budget: int) -> tuple[int, list, int]:
    """Branch and bound that always expands the waiting node with the highest bound (Section 30.6).
    Nodes wait in a heap; the search stops when the best bound left cannot beat the incumbent.
    Returns (votes, names, nodes expanded)."""
    items = sorted(books, key=lambda b: b[2] / b[1], reverse=True)
    best, best_names, expanded = 0, [], 0
    heap = [(-fractional_bound(items, 0, budget), 0, budget, 0, ())]
    while heap:
        neg_bound, i, room, votes, chosen = heapq.heappop(heap)
        if -neg_bound <= best:
            break                                     # no waiting node can do better: the incumbent is optimal
        expanded += 1
        if i == len(items):
            continue
        name, price, v = items[i]
        children = []
        if price <= room:
            children.append((room - price, votes + v, chosen + (name,)))
        children.append((room, votes, chosen))
        for r, vv, ch in children:
            if vv > best:
                best, best_names = vv, list(ch)
            bound = vv + fractional_bound(items, i + 1, r)
            if bound > best:
                heapq.heappush(heap, (-bound, i + 1, r, vv, ch))
    return best, best_names, expanded


# Section 30.7: Chapter 17's van round (minutes between the Library and four branches), solved exactly.
BRANCHES = ["Library", "North", "East", "South", "West"]
TRAVEL = {("Library", "North"): 2, ("Library", "East"): 9, ("Library", "South"): 10, ("Library", "West"): 7,
          ("North", "East"): 6, ("North", "South"): 4, ("North", "West"): 3, ("East", "South"): 8,
          ("East", "West"): 5, ("South", "West"): 1}


def town_minutes(a, b) -> int:
    return TRAVEL.get((a, b), TRAVEL.get((b, a)))


def tree_weight(places: list, dist) -> int:
    """Prim's minimum spanning tree weight over places (Chapter 8)."""
    if not places:
        return 0
    inside, total = {places[0]}, 0
    while len(inside) < len(places):
        w, p = min((dist(a, b), b) for a in inside for b in places if b not in inside)
        inside.add(p)
        total += w
    return total


def tour_bound(path: list, left: list, dist, kind: str) -> float:
    """A lower bound on any round that starts with path and still visits left, then returns to path[0].
    'none': just the cost so far. 'cheapest': plus, for each place still to leave (the current end and every
    unvisited place), its cheapest road to somewhere it could still go. 'tree': plus a spanning tree of the
    unvisited places and the two cheapest roads joining it to the current end and to home."""
    so_far = sum(dist(a, b) for a, b in zip(path, path[1:]))
    if kind == "none" or not left:
        return so_far
    end, home = path[-1], path[0]
    if kind == "cheapest":
        extra = min(dist(end, q) for q in left)
        for p in left:
            extra += min(dist(p, q) for q in left + [home] if q != p)
        return so_far + extra
    return (so_far + tree_weight(left, dist) + min(dist(end, q) for q in left)
            + min(dist(home, q) for q in left))


def tour_branch_and_bound(places: list, dist, kind: str) -> tuple[int, list, int]:
    """The shortest round from places[0] through every place, by depth-first branch and bound.
    Returns (minutes, round, nodes visited)."""
    best, best_tour, nodes = [float("inf")], [None], [0]

    def go(path, left):
        nodes[0] += 1
        if not left:
            total = sum(dist(a, b) for a, b in zip(path, path[1:])) + dist(path[-1], path[0])
            if total < best[0]:
                best[0], best_tour[0] = total, path + [path[0]]
            return
        if tour_bound(path, left, dist, kind) >= best[0]:
            return                                    # even the optimistic round is no better: cut
        for q in sorted(left, key=lambda q: dist(path[-1], q)):
            go(path + [q], [x for x in left if x != q])

    go([places[0]], list(places[1:]))
    return best[0], best_tour[0], nodes[0]


def random_map(n: int, seed: int):
    """n places at random points of a 100 x 100 square; minutes are rounded straight-line distances."""
    r = random.Random(seed)
    pts = {i: (r.uniform(0, 100), r.uniform(0, 100)) for i in range(n)}
    return list(pts), lambda a, b: round(((pts[a][0] - pts[b][0]) ** 2 + (pts[a][1] - pts[b][1]) ** 2) ** 0.5)


def random_shop(n: int, seed: int) -> list:
    r = random.Random(seed)
    return [(f"b{i}", r.randint(2, 20), r.randint(1, 15)) for i in range(n)]


if __name__ == "__main__":
    log = []
    print(branch_and_bound(BOOKS, 20, True, log), log)
    print(branch_and_bound(BOOKS, 20, False))
    for n in (10, 20, 30):
        shop = random_shop(n, n)
        cap = sum(p for _, p, _ in shop) // 3
        a, b = branch_and_bound(shop, cap, True), branch_and_bound(shop, cap, False) if n <= 20 else (None, None, None)
        print(n, a[0], a[2], b[0], b[2])
