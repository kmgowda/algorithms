"""Volume 7, Chapter 7 - Fenwick Trees (Binary Indexed Trees): Prefix Sums That Can Change.

Positions are 1-based inside the tree. Box i covers the (i & -i) values ending at position i.

Run:  python3 ch07_examples.py
"""

from __future__ import annotations


def lowbit(i: int) -> int:
    """The lowest set bit of i: 12 = 0b1100 -> 4. In two's complement, -i flips all bits above it."""
    return i & -i


class FenwickTree:
    def __init__(self, n: int) -> None:
        self.n = n
        self.box = [0] * (n + 1)

    @classmethod
    def from_list(cls, values: list[int]) -> "FenwickTree":
        """O(n) build: each box passes its total up to the next box that covers it."""
        t = cls(len(values))
        for i, v in enumerate(values, 1):
            t.box[i] += v
            parent = i + lowbit(i)
            if parent <= t.n:
                t.box[parent] += t.box[i]
        return t

    def add(self, i: int, delta: int) -> None:
        """values[i] += delta (i is 0-based for callers). Climb to every box that covers position i."""
        i += 1
        while i <= self.n:
            self.box[i] += delta
            i += lowbit(i)

    def prefix_sum(self, i: int) -> int:
        """Sum of values[0..i-1]: add boxes while stripping the lowest bit. O(log n)."""
        total = 0
        while i > 0:
            total += self.box[i]
            i -= lowbit(i)
        return total

    def range_sum(self, left: int, right: int) -> int:
        """Sum of values[left..right] inclusive = prefix(right + 1) - prefix(left)."""
        return self.prefix_sum(right + 1) - self.prefix_sum(left)


def count_smaller_after(values: list[int]) -> list[int]:
    """Industry example (LeetCode 315): for each value, how many later values are smaller?
    Walk right to left; a Fenwick tree counts values seen so far by their rank. O(n log n)."""
    rank = {v: r for r, v in enumerate(sorted(set(values)))}
    tree, out = FenwickTree(len(rank)), []
    for v in reversed(values):
        out.append(tree.prefix_sum(rank[v]))       # how many seen values have smaller rank
        tree.add(rank[v], 1)
    return out[::-1]


def leaderboard_rank(scores: list[int], max_score: int) -> list[int]:
    """Practical example: as players finish, report how many earlier players scored strictly more."""
    tree, out = FenwickTree(max_score + 1), []
    for i, s in enumerate(scores):
        out.append(i - tree.prefix_sum(s + 1))     # earlier players minus those with score <= s
        tree.add(s, 1)
    return out


if __name__ == "__main__":
    print([lowbit(i) for i in range(1, 13)])
    deposits = [5, 3, 7, 9, 6, 4, 1, 2]          # daily deposits at a bank branch
    t = FenwickTree.from_list(deposits)
    print("days 2..5:", t.range_sum(2, 5))
    t.add(3, -4)                                  # a deposit on day 3 is reversed
    print("after correction:", t.range_sum(2, 5))
    print(count_smaller_after([5, 2, 6, 1]))
    print(leaderboard_rank([50, 80, 60, 80, 90], 100))
