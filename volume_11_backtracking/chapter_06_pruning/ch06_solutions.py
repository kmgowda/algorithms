"""Volume 11, Chapter 6 - Solutions to the exercises."""

from __future__ import annotations

from ch06_examples import can_partition_k


def matchsticks_square(sticks: list[int]) -> bool:
    """Exercise 1 (LeetCode 473): can all matchsticks form a square? A 4-way equal partition."""
    return len(sticks) >= 4 and can_partition_k(sticks, 4)[0]


def max_subset_under(values: list[int], limit: int) -> tuple[int, int]:
    """Exercise 2: the largest subset sum not above a limit, with a bound: stop when even taking everything
    left can't beat the best found. Returns (best, nodes)."""
    vals = sorted(values, reverse=True)
    suffix = [0] * (len(vals) + 1)
    for i in range(len(vals) - 1, -1, -1):
        suffix[i] = suffix[i + 1] + vals[i]
    best, nodes = 0, 0

    def go(i: int, total: int) -> None:
        nonlocal best, nodes
        nodes += 1
        best = max(best, total)
        if i == len(vals) or best == limit or total + suffix[i] <= best:
            return
        if total + vals[i] <= limit:
            go(i + 1, total + vals[i])
        go(i + 1, total)

    go(0, 0)
    return best, nodes


def queens_with_symmetry(n: int) -> int:
    """Exercise 3: count N-Queens solutions by only trying the left half of the first row, then doubling
    (a mirror image of every solution starts in the right half). Odd n: the middle column is counted once."""
    def count(first_cols: range) -> int:
        total = 0
        for c0 in first_cols:
            cols = [c0]

            def go() -> int:
                r = len(cols)
                if r == n:
                    return 1
                found = 0
                for c in range(n):
                    if all(c != cc and abs(c - cc) != r - rr for rr, cc in enumerate(cols)):
                        cols.append(c)
                        found += go()
                        cols.pop()
                return found
            total += go()
        return total

    half = count(range(n // 2))
    middle = count(range(n // 2, n // 2 + 1)) if n % 2 else 0
    return 2 * half + middle


if __name__ == "__main__":
    print(matchsticks_square([1, 1, 2, 2, 2]), matchsticks_square([3, 3, 3, 3, 4]))
    print(max_subset_under([27, 41, 19, 33, 8, 15, 22, 37], 100), [queens_with_symmetry(n) for n in range(1, 9)])
