"""Volume 10, Chapter 1 - What Is an Algorithm Design Paradigm?

One problem, several ways of thinking. Run:  python3 ch01_examples.py
"""

from __future__ import annotations

from functools import lru_cache


# ---------------------------------------------------------------- problem 1: best stretch of daily profits
def best_stretch_brute(profits: list[int]) -> int:
    """Brute force: try every start and end. O(n^2). (At least one day must be chosen.)"""
    best = profits[0]
    for i in range(len(profits)):
        total = 0
        for j in range(i, len(profits)):
            total += profits[j]
            best = max(best, total)
    return best


def best_stretch_divide(profits: list[int]) -> int:
    """Divide and conquer: the best stretch is in the left half, the right half, or crosses the middle. O(n log n)."""
    def solve(lo: int, hi: int) -> int:
        if lo == hi:
            return profits[lo]
        mid = (lo + hi) // 2
        left_best, right_best = solve(lo, mid), solve(mid + 1, hi)
        run, cross_left = 0, profits[mid]
        for i in range(mid, lo - 1, -1):
            run += profits[i]
            cross_left = max(cross_left, run)
        run, cross_right = 0, profits[mid + 1]
        for j in range(mid + 1, hi + 1):
            run += profits[j]
            cross_right = max(cross_right, run)
        return max(left_best, right_best, cross_left + cross_right)
    return solve(0, len(profits) - 1)


def best_stretch_dynamic(profits: list[int]) -> int:
    """Dynamic programming (Kadane): best stretch ENDING today = today, or today + best ending yesterday. O(n)."""
    best = ending_here = profits[0]
    for p in profits[1:]:
        ending_here = max(p, ending_here + p)
        best = max(best, ending_here)
    return best


# ---------------------------------------------------------------- problem 2: paying with the fewest coins
def coins_greedy(amount: int, coins: list[int]) -> int | None:
    """Greedy: always use the biggest coin that fits. Fast - but only right for some coin systems (Chapter 6)."""
    count = 0
    for c in sorted(coins, reverse=True):
        count += amount // c
        amount %= c
    return count if amount == 0 else None


def coins_exhaustive(amount: int, coins: list[int]) -> int | None:
    """Exhaustive search (backtracking, Volume 11): try every coin at every step. Exponential."""
    if amount == 0:
        return 0
    best = None
    for c in coins:
        if c <= amount:
            sub = coins_exhaustive(amount - c, coins)
            if sub is not None and (best is None or sub + 1 < best):
                best = sub + 1
    return best


def coins_dynamic(amount: int, coins: list[int]) -> int | None:
    """Dynamic programming (Volume 12): the exhaustive search, but remember each amount's answer. O(amount x coins)."""
    @lru_cache(maxsize=None)
    def best(a: int) -> float:
        if a == 0:
            return 0
        return min((best(a - c) + 1 for c in coins if c <= a), default=float("inf"))
    result = best(amount)
    return None if result == float("inf") else int(result)


PARADIGMS = {
    "brute force": "try every candidate",
    "greedy": "make the best-looking choice now, never undo it",
    "divide and conquer": "split into independent smaller copies, solve, combine",
    "decrease and conquer": "shrink the problem by a constant or factor, solve the rest",
    "transform and conquer": "change the problem into an easier form first",
    "backtracking": "build a solution step by step, undo dead ends",
    "dynamic programming": "solve overlapping subproblems once and reuse their answers",
}


if __name__ == "__main__":
    week = [3, -5, 4, -1, 2, 1, -6, 5]                 # a fruit stall's daily profit
    print("best stretch:", best_stretch_brute(week), best_stretch_divide(week), best_stretch_dynamic(week))
    print("coins for 63 (1, 5, 10, 25):", coins_greedy(63, [1, 5, 10, 25]), coins_dynamic(63, [1, 5, 10, 25]))
    print("coins for 6 (1, 3, 4):", coins_greedy(6, [1, 3, 4]), "greedy vs best", coins_exhaustive(6, [1, 3, 4]))
    for name, idea in PARADIGMS.items():
        print(f"{name:>22}: {idea}")
