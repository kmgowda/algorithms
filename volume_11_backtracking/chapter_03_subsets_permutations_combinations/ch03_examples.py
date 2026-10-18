"""Volume 11, Chapter 3 - Subsets, Permutations, Combinations.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations


def subsets(items: list[str]) -> list[list[str]]:
    """LeetCode 78: every subset. Each item: include or exclude. 2^n subsets."""
    out: list[list[str]] = []
    path: list[str] = []

    def go(i: int) -> None:
        if i == len(items):
            out.append(list(path))
            return
        path.append(items[i])          # include items[i]
        go(i + 1)
        path.pop()                     # exclude items[i]
        go(i + 1)

    go(0)
    return out


def subsets_with_duplicates(items: list[int]) -> list[list[int]]:
    """LeetCode 90: subsets when items repeat - sort, then never start a branch with a value just used at this level."""
    items = sorted(items)
    out: list[list[int]] = []
    path: list[int] = []

    def go(start: int) -> None:
        out.append(list(path))
        for i in range(start, len(items)):
            if i > start and items[i] == items[i - 1]:
                continue                                  # same value at the same level: duplicate branch
            path.append(items[i])
            go(i + 1)
            path.pop()

    go(0)
    return out


def permutations(items: list[str]) -> list[list[str]]:
    """LeetCode 46: every order. Swap each remaining item into the next position. n! orders."""
    items = list(items)
    out: list[list[str]] = []

    def go(k: int) -> None:
        if k == len(items):
            out.append(list(items))
            return
        for i in range(k, len(items)):
            items[k], items[i] = items[i], items[k]      # choose items[i] for position k
            go(k + 1)
            items[k], items[i] = items[i], items[k]      # un-choose

    go(0)
    return out


def unique_permutations(items: list[int]) -> list[list[int]]:
    """LeetCode 47: orders of a multiset - count how many of each value remain, choose a VALUE not a position."""
    counts: dict[int, int] = {}
    for x in items:
        counts[x] = counts.get(x, 0) + 1
    out: list[list[int]] = []
    path: list[int] = []

    def go() -> None:
        if len(path) == len(items):
            out.append(list(path))
            return
        for value in sorted(counts):
            if counts[value]:
                counts[value] -= 1
                path.append(value)
                go()
                path.pop()
                counts[value] += 1

    go()
    return out


def combinations(n: int, k: int) -> list[list[int]]:
    """LeetCode 77: choose k of 1..n. Only pick numbers above the last; stop when too few remain. C(n, k) results."""
    out: list[list[int]] = []
    path: list[int] = []

    def go(start: int) -> None:
        if len(path) == k:
            out.append(list(path))
            return
        for x in range(start, n - (k - len(path)) + 2):   # leave room for the numbers still needed
            path.append(x)
            go(x + 1)
            path.pop()

    go(1)
    return out


def combination_sum(prices: list[int], target: int) -> list[list[int]]:
    """LeetCode 39 (industry: making an exact bill): numbers may repeat; stop when the running total exceeds the target."""
    prices = sorted(prices)
    out: list[list[int]] = []
    path: list[int] = []

    def go(start: int, remaining: int) -> None:
        if remaining == 0:
            out.append(list(path))
            return
        for i in range(start, len(prices)):
            if prices[i] > remaining:
                break                                     # sorted: every later price is too big as well
            path.append(prices[i])
            go(i, remaining - prices[i])                  # i, not i + 1: the same price may be used again
            path.pop()

    go(0, target)
    return out


def team_lineups(players: list[str], size: int, captain_pool: set[str]) -> list[tuple[str, list[str]]]:
    """Industry example: every team of `size` players plus a choice of captain from eligible players in the team."""
    return [(captain, [players[i - 1] for i in combo])
            for combo in combinations(len(players), size)
            for captain in sorted(players[i - 1] for i in combo) if captain in captain_pool]


if __name__ == "__main__":
    print(subsets(["a", "b", "c"]))
    print(subsets_with_duplicates([1, 2, 2]))
    print(len(permutations(["a", "b", "c", "d"])), unique_permutations([1, 1, 2]))
    print(combinations(4, 2))
    print("exact bill of 8 from prices 2, 3, 5:", combination_sum([2, 3, 5], 8))
    print(len(team_lineups(["Asha", "Ben", "Cy", "Dev", "Eli"], 3, {"Asha", "Dev"})), "lineups")
