"""Volume 6, Chapter 24 - Recognising a DP Problem: one new problem taken through the checklist, three ways.

Run:  python3 ch24_examples.py
"""

from __future__ import annotations

# A printer sells banner pieces by length (metres -> pounds). The club has a 8-metre banner to cut and sell.
PRICE = {1: 1, 2: 5, 3: 8, 4: 9, 5: 10, 6: 17, 7: 17, 8: 20}


def best_plain(n: int, price: dict, calls: list) -> int:
    """Try every length for the first piece, then cut the rest the best way: plain recursion."""
    calls[0] += 1
    if n == 0:
        return 0
    return max((price[k] + best_plain(n - k, price, calls) for k in range(1, n + 1) if k in price), default=float("-inf"))


def best_memo(n: int, price: dict, memo: dict) -> int:
    if n == 0:
        return 0
    if n not in memo:
        memo[n] = max((price[k] + best_memo(n - k, price, memo) for k in range(1, n + 1) if k in price),
                      default=float("-inf"))      # -inf: this length cannot be cut exactly
    return memo[n]


def best_table(n: int, price: dict) -> tuple[int, list, list]:
    """best[m] = most money from m metres (Figure 24.2). Returns (money or None if impossible, pieces, table)."""
    ninf = float("-inf")                              # a length that cannot be cut exactly into priced pieces
    best, first = [0] + [ninf] * n, [0] * (n + 1)
    for m in range(1, n + 1):
        options = [(price[k] + best[m - k], k) for k in range(1, m + 1) if k in price and best[m - k] > ninf]
        if options:
            best[m], first[m] = max(options)
    if best[n] == ninf:
        return None, [], best
    pieces, m = [], n
    while m:
        pieces.append(first[m])
        m -= first[m]
    return best[n], sorted(pieces), best


def greedy_best_rate(n: int, price: dict) -> int:
    """Always cut the piece with the best price per metre that fits: tempting, not always best."""
    money = 0
    while n:
        k = max((k for k in price if k <= n), key=lambda k: (price[k] / k, k))
        money += price[k]
        n -= k
    return money


# The stall's price list for one collectible edition, day by day (pounds); at most one copy is held at a time.
PRICES = [4, 9, 3, 7, 2, 8, 6, 10]


def trade_cooldown(prices: list) -> tuple[int, list, list]:
    """State-machine DP (Section 24.6): three states at the end of each day.
    hold = best money while holding a copy; cool = best just after selling today (tomorrow is a rest day);
    free = best with no copy and free to buy tomorrow.
      hold[d] = max(hold[d-1], free[d-1] - p)    keep the copy, or buy today
      cool[d] = hold[d-1] + p                    sell today
      free[d] = max(free[d-1], cool[d-1])        rest
    Returns (best money, the plan as a list of (day, action), table rows (hold, cool, free) per day)."""
    if not prices:
        return 0, [], []
    ninf = float("-inf")
    hold, cool, free = [-prices[0]], [ninf], [0]
    for d in range(1, len(prices)):
        p = prices[d]
        hold.append(max(hold[-1], free[-1] - p))
        cool.append(hold[d - 1] + p)
        free.append(max(free[-1], cool[-2]))
    rows = list(zip(hold, cool, free))
    # rebuild: walk back from the better of cool and free on the last day
    d = len(prices) - 1
    state = "cool" if cool[d] >= free[d] else "free"
    plan = []
    while d >= 0:
        if state == "hold":
            if d == 0 or free[d - 1] - prices[d] > hold[d - 1]:
                plan.append((d + 1, "buy"))
                state = "free"
            d -= 1
        elif state == "cool":
            plan.append((d + 1, "sell"))
            state = "hold"
            d -= 1
        else:
            if d == 0:
                break
            state = "cool" if cool[d - 1] > free[d - 1] else "free"
            d -= 1
    return max(cool[-1], free[-1], 0), plan[::-1], rows


def trade_k(prices: list, k: int) -> tuple[int, list]:
    """At most k sales (Section 24.7): state (day, sales done, holding?).
      free[j] = max(free[j], hold[j - 1] + p)    sell today: the j-th sale
      hold[j] = max(hold[j], free[j] - p)        buy today, after j sales
    Returns (best money, best money for each k' = 0..k)."""
    ninf = float("-inf")
    free = [0] + [ninf] * k                           # free[j]: no copy, j sales completed
    hold = [ninf] * (k + 1)                           # hold[j]: holding, j sales completed before this buy
    for p in prices:
        for j in range(k, -1, -1):
            if j > 0 and hold[j - 1] > ninf:
                free[j] = max(free[j], hold[j - 1] + p)
            if free[j] > ninf:
                hold[j] = max(hold[j], free[j] - p)
    best_by_k = []
    run = 0
    for j in range(k + 1):
        run = max(run, free[j])
        best_by_k.append(run)
    return best_by_k[-1], best_by_k


def trade_brute(prices: list, k=None, cooldown: bool = False) -> int:
    """Try every day-by-day choice of buy / sell / wait, to check the tables."""
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def go(d: int, holding: bool, sales: int, resting: bool) -> int:
        if d == len(prices):
            return 0
        best = go(d + 1, holding, sales, False)                       # wait
        if holding and (k is None or sales < k):
            best = max(best, prices[d] + go(d + 1, False, sales + 1, cooldown))
        if not holding and not resting:
            best = max(best, -prices[d] + go(d + 1, True, sales, False))
        return best

    return go(0, False, 0, False)


if __name__ == "__main__":
    c = [0]
    print(best_plain(8, PRICE, c), c[0], best_memo(8, PRICE, {}), best_table(8, PRICE), greedy_best_rate(8, PRICE))
    for n in (10, 15, 20):
        p = {k: PRICE.get(k, 0) or 2 * k for k in range(1, n + 1)}
        c = [0]
        best_plain(n, p, c)
        print(n, c[0], n)
