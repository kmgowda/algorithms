"""Volume 5, Chapter 17 - When Greedy Fails: a gallery of counterexamples, each checked against an exact answer.

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


def two_opt(tour: list) -> tuple[int, list]:
    """Challenge 1: reverse a stretch of the round whenever that shortens it, until no reversal helps."""
    tour, better = list(tour), True
    while better:
        better = False
        for i in range(1, len(tour) - 2):
            for j in range(i + 1, len(tour) - 1):
                new = tour[:i] + tour[i:j + 1][::-1] + tour[j + 1:]
                if tour_length(new) < tour_length(tour):
                    tour, better = new, True
    return tour_length(tour), tour


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


# Section 17.6: the desk's reserve shelf holds 3 books; readers ask for books in this order (a day's requests).
REQUESTS = ["A", "B", "C", "D", "A", "B", "E", "A", "B", "C", "D", "E"]
SHELF = 3


def farthest_in_future(requests: list, k: int, log: list | None = None) -> int:
    """Belady's rule (Figure 17.4): on a miss with a full shelf, remove the book whose next request is farthest away
    (or never comes). Returns the number of misses; log gets (request, hit or miss, book removed or None)."""
    shelf, misses = [], 0
    for i, book in enumerate(requests):
        if book in shelf:
            if log is not None:
                log.append((book, "hit", None))
            continue
        misses += 1
        out = None
        if 0 < k == len(shelf):
            def next_use(b):
                rest = requests[i + 1:]
                return rest.index(b) if b in rest else len(rest)
            out = max(shelf, key=next_use)            # ties: the book listed first on the shelf
            shelf.remove(out)
        if k > 0:
            shelf.append(book)
        if log is not None:
            log.append((book, "miss", out))
    return misses


def least_recently_used(requests: list, k: int) -> int:
    """Remove the book whose last request is longest ago: the usual rule when the future is unknown."""
    shelf, misses = [], 0                             # most recently used at the end
    for book in requests:
        if book in shelf:
            shelf.remove(book)
        else:
            misses += 1
            if len(shelf) == k and k > 0:
                shelf.pop(0)
        if k > 0:
            shelf.append(book)
    return misses


def first_in_first_out(requests: list, k: int) -> int:
    """Remove the book that has been on the shelf longest."""
    shelf, misses = [], 0
    for book in requests:
        if book not in shelf:
            misses += 1
            if len(shelf) == k and k > 0:
                shelf.pop(0)
            if k > 0:
                shelf.append(book)
    return misses


def fewest_misses(requests: list, k: int) -> int:
    """Brute force over every possible choice of book to remove at every miss (remembering states already seen)."""
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def go(i, shelf):
        if i == len(requests):
            return 0
        book = requests[i]
        if book in shelf:
            return go(i + 1, shelf)
        if k == 0:
            return 1 + go(i + 1, shelf)
        if len(shelf) < k:
            return 1 + go(i + 1, shelf | {book})
        return 1 + min(go(i + 1, (shelf - {b}) | {book}) for b in shelf)

    return go(0, frozenset())


if __name__ == "__main__":
    log = []
    print(farthest_in_future(REQUESTS, SHELF, log), least_recently_used(REQUESTS, SHELF),
          first_in_first_out(REQUESTS, SHELF), fewest_misses(REQUESTS, SHELF))
    print(log)
    print(nearest_neighbour(), best_tour())
    print(greedy_cover(GENRES, SUPPLIERS), smallest_cover(GENRES, SUPPLIERS))
    print(greedy_cover(GENRES, SUPPLIERS2), smallest_cover(GENRES, SUPPLIERS2))
