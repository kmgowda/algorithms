"""Volume 6, Chapter 8 - Choosing a Design Strategy: the same problems under every strategy, and a preview of Part II.

Run:  python3 ch08_examples.py
"""

from __future__ import annotations

import importlib.util
import os
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(folder: str, name: str):
    spec = importlib.util.spec_from_file_location(name + "_v4", os.path.join(HERE, "..", folder, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_v5(slug: str):
    """Load a Volume 5 companion module by its folder slug, whatever its chapter number."""
    base = os.path.join(HERE, "..", "..", "volume_05_paths_greedy_divide")
    folder = next(f for f in sorted(os.listdir(base)) if f.startswith("chapter_") and f.endswith("_" + slug))
    return _load(os.path.join("..", "volume_05_paths_greedy_divide", folder), "ch" + folder.split("_")[1] + "_examples")


four = _load_v5("four_design_ways")
bnb = _load("chapter_06_branch_and_bound", "ch06_examples")
coins = _load_v5("greedy_idea")


def budget_table() -> dict:
    """The club's \u00a320 budget under each strategy (Section 8.1): (votes, work)."""
    b = four.BOOKS
    return {
        "brute force": four.brute_force(b, 20)[::2],
        "greedy (votes per pound)": (four.greedy(b, 20, key=lambda x: -x[2] / x[1])[0], 1),
        "backtracking": four.backtracking(b, 20)[::2],
        "branch and bound": bnb.branch_and_bound(b, 20)[::2],
    }


def ways_naive(n: int, counter: list) -> int:
    """Ways to climb n library steps taking 1 or 2 at a time, by plain recursion: the same sub-problems again and again."""
    counter[0] += 1
    if n <= 1:
        return 1
    return ways_naive(n - 1, counter) + ways_naive(n - 2, counter)


def ways_remembered(n: int) -> tuple[int, int]:
    """The same, remembering each answer once it is known (Part II): returns (ways, sub-problems solved)."""
    solved = [0]

    @lru_cache(maxsize=None)
    def go(k):
        solved[0] += 1
        return 1 if k <= 1 else go(k - 1) + go(k - 2)

    return go(n), solved[0]


def change_plain(amount: int, coins: list) -> tuple[int, int]:
    """Fewest coins by splitting into 'one coin, then the rest' and solving the rest the same way, with no memory:
    divide and conquer in shape, but the rests overlap. Returns (coins, calls)."""
    calls = [0]

    def go(a):
        calls[0] += 1
        if a == 0:
            return 0
        return 1 + min((go(a - c) for c in coins if c <= a), default=float("inf"))

    return go(amount), calls[0]


def change_backtracking(amount: int, coins: list) -> tuple[int, int]:
    """Fewest coins by backtracking with a bound: choose how many of each coin, largest coin first, and cut a branch
    once it already uses as many coins as the best found. Returns (coins, nodes)."""
    coins = sorted(coins, reverse=True)
    best, nodes = [float("inf")], [0]

    def go(i, left, used):
        nodes[0] += 1
        if left == 0:
            best[0] = min(best[0], used)
            return
        if i == len(coins) or used + 1 >= best[0]:
            return                                    # out of coin kinds, or cannot beat the best
        for k in range(left // coins[i], -1, -1):
            go(i + 1, left - k * coins[i], used + k)

    go(0, amount, 0)
    return best[0], nodes[0]


def change_table(amount: int, coins: list) -> tuple[int, int]:
    """Fewest coins by filling a table for every amount from 0 up (Part II). Returns (coins, entries filled)."""
    inf = float("inf")
    best = [0] + [inf] * amount
    for a in range(1, amount + 1):
        best[a] = 1 + min((best[a - c] for c in coins if c <= a), default=inf)
    return best[amount], amount + 1


def change_greedy(amount: int, coins: list) -> tuple[int, int]:
    """Largest coin first (Volume 5, Chapter 14). Returns (coins, coin kinds looked at)."""
    used = 0
    for c in sorted(coins, reverse=True):
        used += amount // c
        amount %= c
    return (used if amount == 0 else float("inf")), len(coins)


def change_comparison(amount: int, coins: list) -> dict:
    """Section 8.5: one question, four strategies, (answer, work)."""
    return {"greedy": change_greedy(amount, coins), "plain recursion": change_plain(amount, coins),
            "backtracking with a bound": change_backtracking(amount, coins), "table": change_table(amount, coins)}


def meet_in_middle(prices: list, target: int) -> tuple[list | None, int]:
    """Is there a choice of prices summing to target? List every sum of each half (2^(n/2) each),
    sort one half, and binary-search it for target minus each sum of the other. Returns (choice, sums listed)."""
    import bisect
    half = len(prices) // 2

    def sums(part, offset):
        out = [(0, [])]
        for k, p in enumerate(part):
            out += [(s + p, c + [offset + k]) for s, c in out]
        return out
    left, right = sums(prices[:half], 0), sorted(sums(prices[half:], half))
    keys = [s for s, _ in right]
    for s, c in left:
        i = bisect.bisect_left(keys, target - s)
        if i < len(keys) and keys[i] == target - s:
            return sorted(c + right[i][1]), len(left) + len(right)
    return None, len(left) + len(right)


if __name__ == "__main__":
    print(budget_table())
    for n in (10, 20, 25):
        c = [0]
        print(n, ways_naive(n, c), c[0], ways_remembered(n))
    print(len(coins.greedy_change(6, coins.ODD)), len(coins.fewest_coins(6, coins.ODD)))
