"""Volume 12, Chapter 6 - The Knapsack Family: 0/1, Unbounded, Subset Sum.

Run:  python3 ch06_examples.py
"""

from __future__ import annotations

Item = tuple[str, int, int]          # (name, weight, value)


def knapsack_01_table(items: list[Item], capacity: int) -> int:
    """Each item at most once. best[i][c] = best value from the first i items with capacity c:
    skip item i (best[i-1][c]) or take it (best[i-1][c - w] + v)."""
    n = len(items)
    best = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        _, w, v = items[i - 1]
        for c in range(capacity + 1):
            best[i][c] = best[i - 1][c]
            if w <= c:
                best[i][c] = max(best[i][c], best[i - 1][c - w] + v)
    return best[n][capacity]


def knapsack_01(items: list[Item], capacity: int) -> int:
    """Same, one row: loop capacity DOWNWARD so each item is used at most once (best[c - w] is still 'old')."""
    best = [0] * (capacity + 1)
    for _, w, v in items:
        for c in range(capacity, w - 1, -1):
            best[c] = max(best[c], best[c - w] + v)
    return best[capacity]


def knapsack_unbounded(items: list[Item], capacity: int) -> int:
    """Unlimited copies of each item: loop capacity UPWARD, so best[c - w] may already include this item."""
    best = [0] * (capacity + 1)
    for _, w, v in items:
        for c in range(w, capacity + 1):
            best[c] = max(best[c], best[c - w] + v)
    return best[capacity]


def subset_sum(values: list[int], target: int) -> bool:
    """Is there a subset adding to target? A knapsack with True/False instead of values."""
    reach = [True] + [False] * target
    for v in values:
        for s in range(target, v - 1, -1):
            reach[s] = reach[s] or reach[s - v]
    return reach[target]


def can_split_equally(values: list[int]) -> bool:
    """LeetCode 416: split into two groups with equal sums = subset sum to half the total."""
    total = sum(values)
    return total % 2 == 0 and subset_sum(values, total // 2)


def cargo_plan(items: list[Item], capacity: int) -> tuple[int, list[str]]:
    """Industry example: which parcels a cargo drone should carry for maximum delivery fees (with the item list)."""
    n = len(items)
    best = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        _, w, v = items[i - 1]
        for c in range(capacity + 1):
            best[i][c] = best[i - 1][c]
            if w <= c:
                best[i][c] = max(best[i][c], best[i - 1][c - w] + v)
    chosen, c = [], capacity
    for i in range(n, 0, -1):
        if best[i][c] != best[i - 1][c]:              # the value changed, so item i was taken
            name, w, _ = items[i - 1]
            chosen.append(name)
            c -= w
    return best[n][capacity], sorted(chosen)


if __name__ == "__main__":
    bag = [("camera", 5, 60), ("laptop", 4, 40), ("books", 4, 40), ("snacks", 1, 10)]
    print("0/1:", knapsack_01_table(bag, 8), knapsack_01(bag, 8), "| unbounded:", knapsack_unbounded(bag, 8))
    print("subset sum 11 from 3, 34, 4, 12, 5, 2:", subset_sum([3, 34, 4, 12, 5, 2], 11))
    print("split equally:", can_split_equally([1, 5, 11, 5]), can_split_equally([1, 2, 3, 5]))
    parcels = [("medicine", 2, 300), ("documents", 1, 120), ("phone", 1, 200), ("laptop", 3, 350), ("shoes", 2, 90)]
    print("drone cargo:", cargo_plan(parcels, 5))
