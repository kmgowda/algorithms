"""Volume 10, Chapter 11 - The Big Comparison: Greedy vs. Divide-and-Conquer (preview of Backtracking and DP).

One problem - making change - solved four ways, plus a race and a decision guide.

Run:  python3 ch11_examples.py
"""

from __future__ import annotations

import timeit
from functools import lru_cache


def change_greedy(amount: int, coins: tuple[int, ...]) -> int | None:
    """Greedy: biggest coin first. Fast; correct only for canonical coin systems."""
    count = 0
    for c in sorted(coins, reverse=True):
        count += amount // c
        amount %= c
    return count if amount == 0 else None


def change_plain_recursion(amount: int, coins: tuple[int, ...]) -> int | None:
    """Plain recursion that splits off one coin - subproblems OVERLAP, so it repeats work exponentially."""
    if amount == 0:
        return 0
    options = [change_plain_recursion(amount - c, coins) for c in coins if c <= amount]
    options = [o for o in options if o is not None]
    return min(options) + 1 if options else None


def change_backtracking(amount: int, coins: tuple[int, ...]) -> int | None:
    """Backtracking with pruning (Volume 11): try big coins first, abandon branches that can't beat the best."""
    coins = tuple(sorted(coins, reverse=True))
    best = [None]

    def go(i: int, left: int, used: int) -> None:
        if left == 0:
            if best[0] is None or used < best[0]:
                best[0] = used
            return
        if i == len(coins) or (best[0] is not None and used + -(-left // coins[i]) >= best[0]):
            return                                        # even all-largest-coins can't beat the best: prune
        for k in range(left // coins[i], -1, -1):
            go(i + 1, left - k * coins[i], used + k)

    go(0, amount, 0)
    return best[0]


def change_dynamic(amount: int, coins: tuple[int, ...]) -> int | None:
    """Dynamic programming (Volume 12): the recursion above, but each amount solved once."""
    @lru_cache(maxsize=None)
    def best(a: int) -> float:
        if a == 0:
            return 0
        return min((best(a - c) + 1 for c in coins if c <= a), default=float("inf"))
    r = best(amount)
    return None if r == float("inf") else int(r)


def race(amount: int, coins: tuple[int, ...]) -> dict[str, float]:
    methods = {"greedy": change_greedy, "backtracking": change_backtracking, "dynamic programming": change_dynamic}
    if amount <= 30:
        methods["plain recursion"] = change_plain_recursion
    return {name: min(timeit.repeat(lambda f=f: f(amount, coins), number=1, repeat=3)) for name, f in methods.items()}


def choose_paradigm(features: set[str]) -> str:
    """A decision guide from problem features to the paradigm to try first."""
    if "provably safe local choice" in features:
        return "greedy"
    if "independent subproblems" in features:
        return "divide and conquer"
    if "overlapping subproblems" in features:
        return "dynamic programming"
    if "one smaller instance suffices" in features:
        return "decrease and conquer"
    if "easier after sorting or restructuring" in features:
        return "transform and conquer"
    if "must explore combinations with constraints" in features:
        return "backtracking"
    return "brute force baseline first"


if __name__ == "__main__":
    for coins in [(1, 5, 10, 25), (1, 3, 4)]:
        print(coins, "amount 6:", change_greedy(6, coins), change_plain_recursion(6, coins),
              change_backtracking(6, coins), change_dynamic(6, coins))
    print({k: f"{v * 1e6:.0f} us" for k, v in race(30, (1, 5, 10, 25)).items()})
    print({k: f"{v * 1e6:.0f} us" for k, v in race(30, (1, 3, 4)).items()})
    print(choose_paradigm({"overlapping subproblems"}))
