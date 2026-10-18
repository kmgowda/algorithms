"""Volume 10, Chapter 2 - Greedy Algorithms: Take the Best Bite Now.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations


def assign_snacks(appetites: list[int], snacks: list[int]) -> int:
    """LeetCode 455 idea: each child is happy with a snack at least their appetite size.
    Greedy: sort both; give the smallest snack that satisfies the least hungry child. O(n log n)."""
    appetites, snacks = sorted(appetites), sorted(snacks)
    child = 0
    for s in snacks:
        if child < len(appetites) and s >= appetites[child]:
            child += 1
    return child


def can_reach_end(jumps: list[int]) -> bool:
    """LeetCode 55: from stone i you may jump up to jumps[i] stones. Greedy: track the farthest reachable stone."""
    farthest = 0
    for i, j in enumerate(jumps):
        if i > farthest:
            return False
        farthest = max(farthest, i + j)
    return True


def min_refuel_start(fuel: list[int], cost: list[int]) -> int:
    """LeetCode 134 (gas station): a circular road; station i gives fuel[i], driving to the next costs cost[i].
    Greedy: if the tank goes negative, no station so far can be the start - restart after it. O(n)."""
    if sum(fuel) < sum(cost):
        return -1
    tank, start = 0, 0
    for i in range(len(fuel)):
        tank += fuel[i] - cost[i]
        if tank < 0:
            start, tank = i + 1, 0
    return start


def boats_needed(weights: list[int], limit: int) -> int:
    """Industry example (LeetCode 881): rescue boats carry at most two people within a weight limit.
    Greedy: pair the heaviest with the lightest if they fit; otherwise the heaviest goes alone."""
    w = sorted(weights)
    i, j, boats = 0, len(w) - 1, 0
    while i <= j:
        if w[i] + w[j] <= limit:
            i += 1
        j -= 1
        boats += 1
    return boats


def make_change_canonical(amount: int, coins: tuple[int, ...] = (500, 200, 100, 50, 20, 10, 5, 2, 1)) -> dict[int, int]:
    """Industry example: a ticket machine giving change in rupee notes and coins - largest first."""
    out: dict[int, int] = {}
    for c in coins:
        if amount >= c:
            out[c], amount = divmod(amount, c)
    return out


if __name__ == "__main__":
    print("happy children:", assign_snacks([1, 2, 3], [1, 1, 3]))
    print("reach the far bank:", can_reach_end([2, 3, 1, 1, 4]), can_reach_end([3, 2, 1, 0, 4]))
    print("gas station start:", min_refuel_start([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]))
    print("rescue boats:", boats_needed([3, 2, 2, 1], 3))
    print("change for 788:", make_change_canonical(788))
