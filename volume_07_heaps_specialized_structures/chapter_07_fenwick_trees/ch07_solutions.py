"""Volume 7, Chapter 7 - Solutions to the exercises."""

from __future__ import annotations

from ch07_examples import FenwickTree


def count_inversions(values: list[int]) -> int:
    """Exercise 1: pairs i < j with values[i] > values[j] (V5-C5 used merge sort)."""
    rank = {v: r for r, v in enumerate(sorted(set(values)))}
    tree, inversions = FenwickTree(len(rank)), 0
    for seen, v in enumerate(values):
        inversions += seen - tree.prefix_sum(rank[v] + 1)     # earlier values that are larger
        tree.add(rank[v], 1)
    return inversions


class RangeAddPointQuery:
    """Exercise 2: add delta to a whole range, read one value - store DIFFERENCES (V4-C8) in a Fenwick tree."""

    def __init__(self, n: int) -> None:
        self.diff = FenwickTree(n + 1)

    def add_range(self, left: int, right: int, delta: int) -> None:
        self.diff.add(left, delta)
        self.diff.add(right + 1, -delta)

    def value(self, i: int) -> int:
        return self.diff.prefix_sum(i + 1)


def find_kth(tree: FenwickTree, k: int) -> int:
    """Exercise 3: smallest 0-based index whose prefix sum reaches k (counts stored as 0/1).
    Walks down powers of two: O(log n)."""
    pos, step = 0, 1 << tree.n.bit_length()
    while step:
        if pos + step <= tree.n and tree.box[pos + step] < k:
            pos += step
            k -= tree.box[pos]
        step >>= 1
    return pos                                                  # 1-based pos+1 -> 0-based pos


if __name__ == "__main__":
    print(count_inversions([2, 4, 1, 3, 5]))
    r = RangeAddPointQuery(6)
    r.add_range(1, 3, 5)
    r.add_range(2, 5, 1)
    print([r.value(i) for i in range(6)])
    present = FenwickTree.from_list([0, 1, 0, 1, 1, 0, 1])     # seats taken at 1, 3, 4, 6
    print(find_kth(present, 3))
