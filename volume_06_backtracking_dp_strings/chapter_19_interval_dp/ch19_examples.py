"""Volume 6, Chapter 19 - Interval DP: merge neighbouring stacks of books at the least total cost.

Run:  python3 ch19_examples.py
"""

from __future__ import annotations

STACKS = [4, 1, 3, 6, 2]                              # books in each stack along the shelf


def merge_cost(stacks: list) -> tuple[int, list, str]:
    """C[i][j] = least cost to merge stacks i..j into one; merging two stacks costs their total books (Figure 19.2).
    Filled by interval length. Returns (cost, table, merge plan as brackets)."""
    n = len(stacks)
    if n == 0:
        return 0, [], ""
    pre = [0]
    for s in stacks:
        pre.append(pre[-1] + s)
    C = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            C[i][j], split[i][j] = min((C[i][k] + C[k + 1][j], k) for k in range(i, j))
            C[i][j] += pre[j + 1] - pre[i]                # the final merge moves every book in i..j

    def plan(i, j):
        if i == j:
            return str(stacks[i])
        k = split[i][j]
        return f"({plan(i, k)} + {plan(k + 1, j)})"

    return C[0][n - 1], C, plan(0, n - 1)


def knuth_merge_cost(stacks: list) -> int:
    """Knuth's speed-up (Section 19.6): the best split of i..j lies between the best splits of i..j-1 and
    i+1..j (the largest best split is kept), so each stretch tries only that range. O(n^2) in total."""
    n = len(stacks)
    pre = [0]
    for s in stacks:
        pre.append(pre[-1] + s)
    C = [[0] * n for _ in range(n)]
    opt = [[i] * n for i in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            best = None
            for k in range(opt[i][j - 1], min(opt[i + 1][j], j - 1) + 1):
                if best is None or C[i][k] + C[k + 1][j] <= best:
                    best, opt[i][j] = C[i][k] + C[k + 1][j], k
            C[i][j] = best + pre[j + 1] - pre[i]
    return C[0][n - 1] if n else 0


def knuth_trace(stacks: list) -> tuple[list, int, int]:
    """The best-split table of the speed-up (stacks counted from 1) and the number of splits tried,
    with Knuth's ranges and with every split, for Figure 19.4."""
    n = len(stacks)
    pre = [0]
    for s in stacks:
        pre.append(pre[-1] + s)
    C = [[0] * n for _ in range(n)]
    opt = [[i] * n for i in range(n)]
    tried = 0
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            best = None
            for k in range(opt[i][j - 1], min(opt[i + 1][j], j - 1) + 1):
                tried += 1
                if best is None or C[i][k] + C[k + 1][j] <= best:
                    best, opt[i][j] = C[i][k] + C[k + 1][j], k
            C[i][j] = best + pre[j + 1] - pre[i]
    table = [[opt[i][j] + 1 if j > i else None for j in range(n)] for i in range(n)]
    every = sum(length - 1 for length in range(2, n + 1) for _ in range(n - length + 1))
    return table, tried, every


# Four tables to multiply in a chain (rows x columns): A is 10 x 30, B 30 x 5, C 5 x 60, D 60 x 10.
CHAIN = [10, 30, 5, 60, 10]


def matrix_chain(dims: list) -> tuple[int, list, list, str]:
    """Matrix-chain order (Section 19.8): tables M1..Mn, where Mi is dims[i-1] x dims[i]. cost[i][j] = fewest scalar
    multiplications for Mi..Mj = min over k of cost[i][k] + cost[k+1][j] + dims[i-1] * dims[k] * dims[j].
    Returns (cost, cost table, split table, bracketing), with tables indexed from 1."""
    n = len(dims) - 1
    if n <= 0:
        return 0, [], [], ""
    cost = [[0] * (n + 1) for _ in range(n + 1)]
    split = [[0] * (n + 1) for _ in range(n + 1)]
    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            cost[i][j] = None
            for k in range(i, j):
                c = cost[i][k] + cost[k + 1][j] + dims[i - 1] * dims[k] * dims[j]
                if cost[i][j] is None or c < cost[i][j]:
                    cost[i][j], split[i][j] = c, k
    names = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def bracket(i: int, j: int) -> str:
        if i == j:
            return names[i - 1] if n <= 26 else f"M{i}"
        k = split[i][j]
        return "(" + bracket(i, k) + " " + bracket(k + 1, j) + ")"

    return cost[1][n], cost, split, bracket(1, n)


def chain_brute(dims: list) -> int:
    """Try every bracketing (exponentially many) to check matrix_chain."""
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def best(i: int, j: int) -> int:
        if i == j:
            return 0
        return min(best(i, k) + best(k + 1, j) + dims[i - 1] * dims[k] * dims[j] for k in range(i, j))

    return best(1, len(dims) - 1) if len(dims) > 1 else 0


def greedy_smallest_pair(stacks: list) -> int:
    """Always merge the neighbouring pair with the fewest books: tempting, not always best."""
    s, cost = list(stacks), 0
    while len(s) > 1:
        i = min(range(len(s) - 1), key=lambda k: s[k] + s[k + 1])
        cost += s[i] + s[i + 1]
        s[i:i + 2] = [s[i] + s[i + 1]]
    return cost


def brute(stacks: list) -> int:
    if len(stacks) <= 1:
        return 0
    best = None
    for i in range(len(stacks) - 1):
        nxt = stacks[:i] + [stacks[i] + stacks[i + 1]] + stacks[i + 2:]
        c = stacks[i] + stacks[i + 1] + brute(nxt)
        best = c if best is None else min(best, c)
    return best


TOKENS = [3, 9, 1, 2]      # book tokens in a row; players take one from either end (Section 19.7)


def game_margin(row: list) -> tuple[int, list]:
    """Two players take turns removing a token from either end of the row; each wants the most points.
    margin[i][j] = the most the player to move can win by (their points minus the other's) on row[i..j].
    Returns (margin for the first player, table)."""
    n = len(row)
    margin = [[0] * n for _ in range(n)]
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if i == j:
                margin[i][j] = row[i]
            else:
                margin[i][j] = max(row[i] - margin[i + 1][j], row[j] - margin[i][j - 1])
    return (margin[0][n - 1] if n else 0), margin


if __name__ == "__main__":
    cost, table, plan = merge_cost(STACKS)
    print(cost, plan)
    for row in table:
        print(row)
    print(greedy_smallest_pair(STACKS), brute(STACKS))
    print(game_margin(TOKENS)[0])
