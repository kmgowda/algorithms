"""Volume 5, Chapter 26 - Transform and Conquer: change the problem into an easier one first.

Run:  python3 ch26_examples.py
"""

from __future__ import annotations

import heapq
from collections import Counter

# Call numbers of books returned today; is any book returned twice?
RETURNS = [47, 12, 91, 63, 25, 70, 12, 84, 31, 58]


def has_repeat_pairs(values: list, counter: list) -> bool:
    """Compare every pair: n(n - 1)/2 comparisons in the worst case."""
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            counter[0] += 1
            if values[i] == values[j]:
                return True
    return False


def has_repeat_sorted(values: list, counter: list) -> bool:
    """Transform first: sort, then repeats sit next to each other (Figure 26.2)."""
    s = sorted(values)
    for a, b in zip(s, s[1:]):
        counter[0] += 1
        if a == b:
            return True
    return False


def mode(values: list):
    """The most common value: sort, then walk runs of equal values (ties: the smallest)."""
    if not values:
        return None
    s, best, best_len, run = sorted(values), None, 0, 1
    for i in range(1, len(s) + 1):
        if i < len(s) and s[i] == s[i - 1]:
            run += 1
        else:
            if run > best_len:
                best, best_len = s[i - 1], run
            run = 1
    return best


def horner(coeffs: list, x: float, counter: list) -> float:
    """Evaluate c0 x^k + ... + ck by rewriting it as (((c0) x + c1) x + ...) (Figure 26.3): k multiplications."""
    total = 0
    for c in coeffs:
        counter[0] += 1
        total = total * x + c
    return total


def naive_poly(coeffs: list, x: float, counter: list) -> float:
    k, total = len(coeffs) - 1, 0
    for i, c in enumerate(coeffs):
        term = c
        for _ in range(k - i):
            counter[0] += 1
            term *= x
        total += term
    return total


def k_smallest(values: list, k: int) -> list:
    """Transform into a heap (Volume 3), then take k items off the top."""
    h = list(values)
    heapq.heapify(h)
    return [heapq.heappop(h) for _ in range(min(k, len(h)))]


def break_even(n: int) -> int:
    """Section 26.4: the fewest membership questions for which sorting once (about n log2 n comparisons) plus a
    binary search per question beats a fresh linear scan per question (about n / 2 comparisons on average)."""
    import math
    sort_cost = n * math.log2(n)
    q = 1
    while sort_cost + q * math.log2(n) >= q * n / 2:
        q += 1
    return q


# Section 26.5: three orders of novels (x), atlases (y), and comics (z), with their totals in pounds.
ORDERS = [[1, 1, 1], [2, 1, 3], [1, 3, 2]]
TOTALS = [20, 36, 43]


def gaussian(A: list, b: list, log: list | None = None, counter: list | None = None) -> list:
    """Solve A x = b exactly: transform to a triangular system by subtracting multiples of rows, then back-substitute
    (Figure 26.4). A zero pivot is replaced by swapping in a lower row; raises ValueError when there is no single
    solution. counter[0] counts multiplications."""
    from fractions import Fraction
    n = len(A)
    M = [[Fraction(v) for v in row] + [Fraction(t)] for row, t in zip(A, b)]
    counter = counter if counter is not None else [0]
    for col in range(n):
        pivot = next((r for r in range(col, n) if M[r][col] != 0), None)
        if pivot is None:
            raise ValueError("no single solution: the equations depend on each other")
        if pivot != col:
            M[col], M[pivot] = M[pivot], M[col]
            if log is not None:
                log.append(("swap", col, pivot))
        for r in range(col + 1, n):
            factor = M[r][col] / M[col][col]
            if factor:
                for c in range(col, n + 1):
                    counter[0] += 1
                    M[r][c] -= factor * M[col][c]
                if log is not None:
                    log.append(("subtract", r, factor, col, [list(row) for row in M]))
    x = [Fraction(0)] * n
    for r in range(n - 1, -1, -1):
        rest = sum(M[r][c] * x[c] for c in range(r + 1, n))
        counter[0] += n - r - 1
        x[r] = (M[r][n] - rest) / M[r][r]
    return [int(v) if v.denominator == 1 else v for v in x]


def elimination_cost(n: int, seed: int = 1) -> int:
    """Multiplications Gaussian elimination makes on a random n x n system (Section 26.5: about n^3 / 3)."""
    import random
    rng = random.Random(seed)
    A = [[rng.randint(1, 9) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        A[i][i] += 10 * n                      # a strong diagonal: never singular
    c = [0]
    gaussian(A, [rng.randint(-9, 9) for _ in range(n)], None, c)
    return c[0]


def mat_mult(P: list, Q: list) -> list:
    return [[sum(P[i][t] * Q[t][j] for t in range(len(Q))) for j in range(len(Q[0]))] for i in range(len(P))]


def mat_power(M: list, k: int) -> list:
    """M to the k by Chapter 25's squaring: about 2 log2 k matrix multiplications."""
    n = len(M)
    result = [[int(i == j) for j in range(n)] for i in range(n)]
    base = [row[:] for row in M]
    while k:
        if k % 2:
            result = mat_mult(result, base)
        base = mat_mult(base, base)
        k //= 2
    return result


TOWN = ["Library", "School", "Park", "Market", "Station", "Museum", "Hospital", "Harbour"]
TOWN_ROADS = [("Library", "School"), ("Library", "Park"), ("School", "Market"), ("Park", "Market"), ("School", "Station"),
              ("Market", "Station"), ("Market", "Museum"), ("Park", "Hospital"), ("Hospital", "Museum"),
              ("Station", "Harbour"), ("Museum", "Harbour"), ("Station", "Museum")]


def count_walks(places: list, roads: list, start: str, goal: str, k: int) -> int:
    """Walks of exactly k roads from start to goal (places may repeat): entry (start, goal) of A^k."""
    idx = {p: i for i, p in enumerate(places)}
    A = [[0] * len(places) for _ in places]
    for a, b in roads:
        A[idx[a]][idx[b]] = A[idx[b]][idx[a]] = 1
    return mat_power(A, k)[idx[start]][idx[goal]]


def count_walks_brute(places: list, roads: list, start: str, goal: str, k: int) -> int:
    adj = {p: set() for p in places}
    for a, b in roads:
        adj[a].add(b)
        adj[b].add(a)
    if k == 0:
        return int(start == goal)
    return sum(count_walks_brute(places, roads, w, goal, k - 1) for w in adj[start])


def lcm(a: int, b: int) -> int:
    """Lowest common multiple, reduced to Chapter 25's Euclid: a b / gcd(a, b)."""
    import math
    if a == 0 or b == 0:
        return 0
    return a * b // math.gcd(a, b)


if __name__ == "__main__":
    a, b = [0], [0]
    print(has_repeat_pairs(RETURNS, a), a[0], has_repeat_sorted(RETURNS, b), b[0])
    print(mode([3, 1, 3, 2, 1, 3]), Counter(RETURNS).most_common(1))
    c1, c2 = [0], [0]
    print(horner([2, -6, 2, -1], 3, c1), c1[0], naive_poly([2, -6, 2, -1], 3, c2), c2[0])
    print(k_smallest(RETURNS, 3))
