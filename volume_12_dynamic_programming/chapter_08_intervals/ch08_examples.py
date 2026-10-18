"""Volume 12, Chapter 8 - DP on Intervals: Matrix Chain, Burst Balloons, Optimal BST.

Run:  python3 ch08_examples.py
"""

from __future__ import annotations


def matrix_chain(dims: list[int]) -> tuple[int, str]:
    """Multiply matrices A1..An where Ai is dims[i-1] x dims[i]. Fewest scalar multiplications, and the bracketing.
    cost[i][j] = min over split k of cost[i][k] + cost[k+1][j] + dims[i-1] * dims[k] * dims[j]."""
    n = len(dims) - 1
    cost = [[0] * (n + 1) for _ in range(n + 1)]
    split = [[0] * (n + 1) for _ in range(n + 1)]
    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            cost[i][j] = min(cost[i][k] + cost[k + 1][j] + dims[i - 1] * dims[k] * dims[j] for k in range(i, j))
            split[i][j] = min(range(i, j), key=lambda k: cost[i][k] + cost[k + 1][j] + dims[i - 1] * dims[k] * dims[j])

    def brackets(i: int, j: int) -> str:
        if i == j:
            return f"A{i}"
        k = split[i][j]
        return f"({brackets(i, k)} {brackets(k + 1, j)})"

    return cost[1][n], brackets(1, n)


def burst_balloons(nums: list[int]) -> int:
    """LeetCode 312: bursting balloon k earns left * k * right (its current neighbours). Maximum total?
    Trick: think of the LAST balloon burst inside an open interval (i, j) - its neighbours are then i and j."""
    vals = [1] + nums + [1]
    n = len(vals)
    best = [[0] * n for _ in range(n)]
    for length in range(2, n):
        for i in range(n - length):
            j = i + length
            best[i][j] = max(best[i][k] + vals[i] * vals[k] * vals[j] + best[k][j] for k in range(i + 1, j))
    return best[0][n - 1]


def optimal_bst_cost(freq: list[int]) -> int:
    """Keys in sorted order with search frequencies: build the BST minimising sum(freq x depth), depth from 1.
    cost[i][j] = min over root r of cost[i][r-1] + cost[r+1][j] + sum(freq[i..j])."""
    n = len(freq)
    prefix = [0]
    for f in freq:
        prefix.append(prefix[-1] + f)
    cost = [[0] * (n + 1) for _ in range(n + 2)]
    for length in range(1, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            weight = prefix[j] - prefix[i - 1]
            cost[i][j] = weight + min((cost[i][r - 1] if r > i else 0) + (cost[r + 1][j] if r < j else 0)
                                      for r in range(i, j + 1))
    return cost[1][n] if n else 0


def cut_stick(length: int, cuts: list[int]) -> int:
    """Industry example (LeetCode 1547): cutting a rod costs its current length; choose the order of cuts to minimise
    the total. Same pattern: the FIRST cut inside a piece splits it into two independent pieces."""
    points = [0] + sorted(cuts) + [length]
    n = len(points)
    best = [[0] * n for _ in range(n)]
    for gap in range(2, n):
        for i in range(n - gap):
            j = i + gap
            best[i][j] = points[j] - points[i] + min(best[i][k] + best[k][j] for k in range(i + 1, j))
    return best[0][n - 1]


if __name__ == "__main__":
    print("matrix chain 10x30, 30x5, 5x60:", matrix_chain([10, 30, 5, 60]))
    print("matrix chain 40x20x30x10x30:", matrix_chain([40, 20, 30, 10, 30]))
    print("balloons 3,1,5,8:", burst_balloons([3, 1, 5, 8]))
    print("optimal BST for frequencies 34, 8, 50:", optimal_bst_cost([34, 8, 50]))
    print("cutting a 7 m beam at 1, 3, 4, 5:", cut_stick(7, [1, 3, 4, 5]))
