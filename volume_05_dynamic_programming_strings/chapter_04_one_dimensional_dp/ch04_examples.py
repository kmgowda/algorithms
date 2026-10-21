"""Volume 5, Chapter 4 - One-Dimensional DP: fewest coins for any coin set, and the best evenings without two in a row.

Run:  python3 ch04_examples.py
"""

from __future__ import annotations

ODD = [4, 3, 1]                                       # Volume 4's coin set where greedy failed
TALKS = [6, 2, 9, 7, 3, 8, 4]                         # members expected at the talk on each evening


def fewest_coins(amount: int, coins: list) -> tuple[int | None, list, list]:
    """best[a] = fewest coins making a (Figure 4.1). Returns (count or None, coins used, the table)."""
    inf = float("inf")
    best, last = [0] + [inf] * amount, [0] * (amount + 1)
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a], last[a] = best[a - c] + 1, c
    if best[amount] == inf:
        return None, [], best
    used, a = [], amount
    while a:
        used.append(last[a])
        a -= last[a]
    return best[amount], used, best


def best_evenings(talks: list) -> tuple[int, list, list]:
    """Most members in total, never attending two evenings in a row (Figure 4.3).
    best[i] = max(best[i-1], best[i-2] + talks[i]). Returns (total, evenings chosen, table)."""
    n = len(talks)
    best = [0] * (n + 1)                              # best[i]: using only the first i evenings
    for i in range(1, n + 1):
        best[i] = max(best[i - 1], (best[i - 2] if i >= 2 else 0) + talks[i - 1])
    chosen, i = [], n
    while i > 0:
        if best[i] == best[i - 1]:
            i -= 1
        else:
            chosen.append(i)
            i -= 2
    return best[n], chosen[::-1], best


if __name__ == "__main__":
    print(fewest_coins(6, ODD))
    print(fewest_coins(87, [200, 100, 50, 20, 10, 5, 2, 1])[:2], fewest_coins(30, [25, 10, 1])[:2])
    print(best_evenings(TALKS))
