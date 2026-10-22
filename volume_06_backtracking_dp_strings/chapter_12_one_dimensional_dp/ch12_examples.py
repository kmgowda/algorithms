"""Volume 6, Chapter 12 - One-Dimensional DP: fewest coins for any coin set, and the best evenings without two in a row.

Run:  python3 ch12_examples.py
"""

from __future__ import annotations

ODD = [4, 3, 1]                                       # Volume 5's coin set where greedy failed
TALKS = [6, 2, 9, 7, 3, 8, 4]                         # members expected at the talk on each evening


def fewest_coins(amount: int, coins: list) -> tuple[int | None, list, list]:
    """best[a] = fewest coins making a (Figure 12.1). Returns (count or None, coins used, the table)."""
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
    """Most members in total, never attending two evenings in a row (Figure 12.3).
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


# Reading-room bookings: (group, start hour, finish hour, members who would come)
BOOKINGS = [("Story time", 9, 11, 5), ("Chess club", 10, 13, 9), ("Poetry", 11, 12, 3), ("Film club", 12, 15, 8),
            ("Knitting", 13, 14, 4), ("History talk", 14, 17, 7), ("Book swap", 15, 18, 6)]


def weighted_intervals(bookings: list) -> tuple[int, list, list, list]:
    """Weighted interval scheduling (Section 12.6): the most members from bookings that do not overlap.
    Sort by finish; p[j] = how many bookings finish no later than booking j starts (found by binary search);
    opt[j] = max(opt[j - 1], value_j + opt[p[j]]). Returns (best, chosen names in time order, p, opt)."""
    from bisect import bisect_right
    jobs = sorted(bookings, key=lambda b: b[2])
    finishes = [b[2] for b in jobs]
    n = len(jobs)
    p = [bisect_right(finishes, jobs[j][1]) for j in range(n)]    # bookings 1..p[j] are compatible with j + 1
    opt = [0] * (n + 1)
    for j in range(1, n + 1):
        opt[j] = max(opt[j - 1], jobs[j - 1][3] + opt[p[j - 1]])
    chosen, j = [], n
    while j > 0:
        if jobs[j - 1][3] + opt[p[j - 1]] > opt[j - 1]:
            chosen.append(jobs[j - 1][0])
            j = p[j - 1]
        else:
            j -= 1
    return opt[n], chosen[::-1], p, opt


def greedy_intervals(bookings: list, key) -> tuple[int, list]:
    """Take bookings in the order given by key, keeping each one that fits: a greedy rule to compare against."""
    taken = []
    for b in sorted(bookings, key=key):
        if all(b[2] <= t[1] or t[2] <= b[1] for t in taken):
            taken.append(b)
    return sum(t[3] for t in taken), [t[0] for t in sorted(taken, key=lambda t: t[1])]


if __name__ == "__main__":
    print(fewest_coins(6, ODD))
    print(fewest_coins(87, [200, 100, 50, 20, 10, 5, 2, 1])[:2], fewest_coins(30, [25, 10, 1])[:2])
    print(best_evenings(TALKS))
