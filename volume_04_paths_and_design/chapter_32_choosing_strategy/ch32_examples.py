"""Volume 4, Chapter 32 - Choosing a Design Strategy: the same problems under every strategy, and a preview of Volume 5.

Run:  python3 ch32_examples.py
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


four = _load("chapter_12_four_design_ways", "ch12_examples")
bnb = _load("chapter_30_branch_and_bound", "ch30_examples")
coins = _load("chapter_13_greedy_idea", "ch13_examples")


def budget_table() -> dict:
    """The club's \u00a320 budget under each strategy (Figure 32.1): (votes, work)."""
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
    """The same, remembering each answer once it is known (Volume 5): returns (ways, sub-problems solved)."""
    solved = [0]

    @lru_cache(maxsize=None)
    def go(k):
        solved[0] += 1
        return 1 if k <= 1 else go(k - 1) + go(k - 2)

    return go(n), solved[0]


if __name__ == "__main__":
    print(budget_table())
    for n in (10, 20, 25):
        c = [0]
        print(n, ways_naive(n, c), c[0], ways_remembered(n))
    print(len(coins.greedy_change(6, coins.ODD)), len(coins.fewest_coins(6, coins.ODD)))
