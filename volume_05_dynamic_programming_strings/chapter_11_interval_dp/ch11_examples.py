"""Volume 5, Chapter 11 - Interval DP: merge neighbouring stacks of books at the least total cost.

Run:  python3 ch11_examples.py
"""

from __future__ import annotations

STACKS = [4, 1, 3, 6, 2]                              # books in each stack along the shelf


def merge_cost(stacks: list) -> tuple[int, list, str]:
    """C[i][j] = least cost to merge stacks i..j into one; merging two stacks costs their total books (Figure 11.2).
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


# Four tables to multiply in a chain (rows x columns): A is 10 x 30, B 30 x 5, C 5 x 60, D 60 x 10.
CHAIN = [10, 30, 5, 60, 10]


def matrix_chain(dims: list) -> tuple[int, list, list, str]:
    """Matrix-chain order (Section 11.7): tables M1..Mn, where Mi is dims[i-1] x dims[i]. cost[i][j] = fewest scalar
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


if __name__ == "__main__":
    cost, table, plan = merge_cost(STACKS)
    print(cost, plan)
    for row in table:
        print(row)
    print(greedy_smallest_pair(STACKS), brute(STACKS))
