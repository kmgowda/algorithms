"""Volume 4, Chapter 17 - When Greedy Fails: a gallery of counterexamples, each checked against an exact answer.

Run:  python3 ch17_examples.py
"""

from __future__ import annotations

import itertools

# The van must visit every branch and return to the Library (a tour); minutes between branches.
BRANCHES = ["Library", "North", "East", "South", "West"]
TRAVEL = {("Library", "North"): 2, ("Library", "East"): 9, ("Library", "South"): 10, ("Library", "West"): 7,
          ("North", "East"): 6, ("North", "South"): 4, ("North", "West"): 3, ("East", "South"): 8,
          ("East", "West"): 5, ("South", "West"): 1}


def minutes(a, b) -> int:
    return TRAVEL.get((a, b), TRAVEL.get((b, a)))


def tour_length(tour: list) -> int:
    return sum(minutes(a, b) for a, b in zip(tour, tour[1:]))


def nearest_neighbour(start="Library") -> tuple[int, list]:
    """Greedy tour: always drive to the closest branch not yet visited (Figure 17.1)."""
    tour, left = [start], set(BRANCHES) - {start}
    while left:
        nxt = min(sorted(left), key=lambda b: minutes(tour[-1], b))
        tour.append(nxt)
        left.remove(nxt)
    tour.append(start)
    return tour_length(tour), tour


def best_tour(start="Library") -> tuple[int, list]:
    """Try every order of the other branches: (n - 1)! tours."""
    others = [b for b in BRANCHES if b != start]
    return min((tour_length([start, *p, start]), [start, *p, start]) for p in itertools.permutations(others))


def greedy_cover(universe: set, sets: dict) -> list:
    """Set cover, greedy: repeatedly pick the set covering the most still-uncovered items."""
    left, chosen = set(universe), []
    while left:
        name = max(sorted(sets), key=lambda s: len(sets[s] & left))
        if not sets[name] & left:
            return chosen + ["(cannot cover everything)"]
        chosen.append(name)
        left -= sets[name]
    return chosen


def smallest_cover(universe: set, sets: dict) -> list:
    for k in range(1, len(sets) + 1):
        for combo in itertools.combinations(sorted(sets), k):
            if set().union(*(sets[c] for c in combo)) >= universe:
                return list(combo)
    return []


# Which genres each supplier stocks; the library wants every genre from as few suppliers as possible.
GENRES = {"poetry", "maps", "science", "history", "crime", "travel"}
SUPPLIERS = {"Big Books": {"poetry", "maps", "science", "history"}, "Mapworks": {"maps", "crime", "travel"},
             "Verse & Co": {"poetry", "science", "history"}}
SUPPLIERS2 = {"Everything Ltd": {"poetry", "maps", "science", "crime"}, "North Shop": {"poetry", "maps", "history"},
              "South Shop": {"science", "crime", "travel"}}


if __name__ == "__main__":
    print(nearest_neighbour(), best_tour())
    print(greedy_cover(GENRES, SUPPLIERS), smallest_cover(GENRES, SUPPLIERS))
    print(greedy_cover(GENRES, SUPPLIERS2), smallest_cover(GENRES, SUPPLIERS2))
