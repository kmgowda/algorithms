"""Volume 12, Chapter 3 - The DP Recipe: State, Choice, Transition, Base Case.

Each solver is written in the same four labelled steps.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations

def best_tutoring_income(offers: list[int]) -> int:
    """A tutor gets offers for consecutive days but can't work two days in a row. Maximum income?
    1. STATE      best[i] = most money using only days 0..i-1
    2. CHOICE     on day i-1: work it, or rest
    3. TRANSITION best[i] = max(best[i-1], best[i-2] + offers[i-1])
    4. BASE CASE  best[0] = 0, best[1] = offers[0]"""
    n = len(offers)
    best = [0] * (n + 1)
    if n:
        best[1] = offers[0]
    for i in range(2, n + 1):
        best[i] = max(best[i - 1], best[i - 2] + offers[i - 1])
    return best[n]


def cheapest_tickets(days: list[int], prices: tuple[int, int, int] = (2, 7, 15)) -> int:
    """LeetCode 983: travel days in a year; passes for 1, 7 or 30 days. Cheapest total?
    1. STATE      cost[d] = cheapest way to cover all travel days up to day d
    2. CHOICE     the pass that covers day d: 1-day, 7-day or 30-day (bought on day d - len + 1)
    3. TRANSITION cost[d] = cost[d-1] if no travel on d, else min(cost[d-L] + price) over L in 1, 7, 30
    4. BASE CASE  cost[0] = 0, and cost of negative days = 0"""
    travel = set(days)
    last = max(days, default=0)
    cost = [0] * (last + 1)
    for d in range(1, last + 1):
        if d not in travel:
            cost[d] = cost[d - 1]
            continue
        cost[d] = min(cost[max(0, d - length)] + price for length, price in zip((1, 7, 30), prices))
    return cost[last]


def min_path_cost(grid: list[list[int]]) -> int:
    """LeetCode 64: cheapest walk from top-left to bottom-right moving right or down.
    1. STATE      c[r][col] = cheapest cost to reach cell (r, col)
    2. CHOICE     arrive from above or from the left
    3. TRANSITION c[r][col] = grid[r][col] + min(c[r-1][col], c[r][col-1])
    4. BASE CASE  c[0][0] = grid[0][0]; the first row and column have only one way in"""
    rows, cols = len(grid), len(grid[0])
    c = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for col in range(cols):
            if r == 0 and col == 0:
                c[r][col] = grid[0][0]
            elif r == 0:
                c[r][col] = c[r][col - 1] + grid[r][col]
            elif col == 0:
                c[r][col] = c[r - 1][col] + grid[r][col]
            else:
                c[r][col] = grid[r][col] + min(c[r - 1][col], c[r][col - 1])
    return c[-1][-1]


def brute_tutoring(offers: list[int]) -> int:
    """Reference: try every set of days with no two adjacent."""
    best = 0
    for mask in range(1 << len(offers)):
        if mask & (mask >> 1) == 0:
            best = max(best, sum(o for i, o in enumerate(offers) if mask >> i & 1))
    return best


def brute_tickets(days: list[int], prices: tuple[int, int, int] = (2, 7, 15)) -> int:
    """Reference: try every choice of pass at each uncovered travel day (exponential)."""
    days = sorted(days)

    def go(i: int) -> int:
        if i == len(days):
            return 0
        best = 10 ** 9
        for length, price in zip((1, 7, 30), prices):
            j = i
            while j < len(days) and days[j] < days[i] + length:
                j += 1
            best = min(best, price + go(j))
        return best
    return go(0)


if __name__ == "__main__":
    print("tutor income:", best_tutoring_income([30, 10, 50, 40, 20, 60]))
    print("cheapest passes:", cheapest_tickets([1, 4, 6, 7, 8, 20]), cheapest_tickets(list(range(1, 31))))
    print("cheapest grid walk:", min_path_cost([[1, 3, 1], [1, 5, 1], [4, 2, 1]]))
