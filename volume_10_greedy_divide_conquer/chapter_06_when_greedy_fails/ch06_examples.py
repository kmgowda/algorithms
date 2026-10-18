"""Volume 10, Chapter 6 - When Greedy Fails.

Run:  python3 ch06_examples.py
"""

from __future__ import annotations

import itertools
import math


def knapsack_greedy(items: list[tuple[str, int, int]], capacity: int) -> int:
    """0/1 knapsack (whole items only), greedy by value per kg. Fast, but can miss the best choice."""
    total = 0
    for _, w, v in sorted(items, key=lambda it: it[2] / it[1], reverse=True):
        if w <= capacity:
            capacity -= w
            total += v
    return total


def knapsack_best(items: list[tuple[str, int, int]], capacity: int) -> int:
    """The truth, by dynamic programming over capacities (Volume 12). O(n x capacity)."""
    best = [0] * (capacity + 1)
    for _, w, v in items:
        for c in range(capacity, w - 1, -1):
            best[c] = max(best[c], best[c - w] + v)
    return best[capacity]


def nearest_neighbour_tour(points: list[tuple[float, float]]) -> float:
    """Travelling salesperson, greedy: always go to the closest unvisited city. Often decent, never guaranteed."""
    unvisited, route = set(range(1, len(points))), [0]
    while unvisited:
        here = points[route[-1]]
        nxt = min(unvisited, key=lambda i: (math.dist(here, points[i]), i))
        route.append(nxt)
        unvisited.remove(nxt)
    route.append(0)
    return sum(math.dist(points[a], points[b]) for a, b in zip(route, route[1:]))


def best_tour(points: list[tuple[float, float]]) -> float:
    """The truth for small n: try every order."""
    best = math.inf
    for perm in itertools.permutations(range(1, len(points))):
        route = (0, *perm, 0)
        best = min(best, sum(math.dist(points[a], points[b]) for a, b in zip(route, route[1:])))
    return best if len(points) > 1 else 0.0


def greedy_set_cover(universe: set[str], sets: dict[str, set[str]]) -> list[str]:
    """Pick the set covering the most still-uncovered items, repeatedly. Not always optimal, but never worse than
    about ln(n) times optimal - and nothing efficient does better (Volume 15)."""
    uncovered, chosen = set(universe), []
    while uncovered:
        name = max(sets, key=lambda s: (len(sets[s] & uncovered), s))
        if not sets[name] & uncovered:
            raise ValueError("cannot cover everything")
        chosen.append(name)
        uncovered -= sets[name]
    return chosen


def smallest_cover(universe: set[str], sets: dict[str, set[str]]) -> int:
    for k in range(1, len(sets) + 1):
        for combo in itertools.combinations(sets, k):
            if set().union(*(sets[c] for c in combo)) >= universe:
                return k
    return 0


def wrong_activity_rules() -> dict[str, int]:
    """Three plausible greedy rules for booking a hall, on inputs that break the wrong ones. Optimal is earliest END."""
    def run(intervals, key):
        chosen, taken = 0, []
        for s, e in sorted(intervals, key=key):
            if all(e <= a or s >= b for a, b in taken):
                taken.append((s, e))
                chosen += 1
        return chosen
    long_first = [(0, 10), (1, 2), (3, 4), (5, 6)]              # earliest start grabs the long event
    short_bridge = [(0, 5), (4, 6), (5, 10)]                     # shortest event blocks two others
    return {"earliest start": run(long_first, lambda iv: iv[0]),
            "earliest end (correct)": run(long_first, lambda iv: iv[1]),
            "shortest first": run(short_bridge, lambda iv: iv[1] - iv[0]),
            "earliest end on the same input": run(short_bridge, lambda iv: iv[1])}


if __name__ == "__main__":
    bag = [("camera", 5, 60), ("laptop", 4, 40), ("books", 4, 40)]
    print("knapsack greedy vs best:", knapsack_greedy(bag, 8), knapsack_best(bag, 8))
    towns = [(0, 0), (1, 0), (-2, 0), (4, 0), (-8, 0)]   # zigzag along a road
    print("tour greedy vs best:", round(nearest_neighbour_tour(towns), 2), round(best_tour(towns), 2))
    cover = {"A": {"1", "2", "3", "4"}, "B": {"1", "2", "5"}, "C": {"3", "4", "6"}}
    print("set cover greedy:", greedy_set_cover({"1", "2", "3", "4", "5", "6"}, cover),
          "| smallest:", smallest_cover({"1", "2", "3", "4", "5", "6"}, cover))
    print(wrong_activity_rules())
