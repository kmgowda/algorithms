"""Volume 5, Chapter 16 - Recognising a DP Problem: one new problem taken through the checklist, three ways.

Run:  python3 ch16_examples.py
"""

from __future__ import annotations

# A printer sells banner pieces by length (metres -> pounds). The club has a 8-metre banner to cut and sell.
PRICE = {1: 1, 2: 5, 3: 8, 4: 9, 5: 10, 6: 17, 7: 17, 8: 20}


def best_plain(n: int, price: dict, calls: list) -> int:
    """Try every length for the first piece, then cut the rest the best way: plain recursion."""
    calls[0] += 1
    if n == 0:
        return 0
    return max(price[k] + best_plain(n - k, price, calls) for k in range(1, n + 1) if k in price)


def best_memo(n: int, price: dict, memo: dict) -> int:
    if n == 0:
        return 0
    if n not in memo:
        memo[n] = max(price[k] + best_memo(n - k, price, memo) for k in range(1, n + 1) if k in price)
    return memo[n]


def best_table(n: int, price: dict) -> tuple[int, list, list]:
    """best[m] = most money from m metres (Figure 16.2). Returns (money or None if impossible, pieces, table)."""
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


if __name__ == "__main__":
    c = [0]
    print(best_plain(8, PRICE, c), c[0], best_memo(8, PRICE, {}), best_table(8, PRICE), greedy_best_rate(8, PRICE))
    for n in (10, 15, 20):
        p = {k: PRICE.get(k, 0) or 2 * k for k in range(1, n + 1)}
        c = [0]
        best_plain(n, p, c)
        print(n, c[0], n)
