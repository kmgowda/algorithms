"""Volume 6, Chapter 11 - Thinking Problems.

Problem 1: merge sort on n items works on exactly 2n - 1 different ranges, each once: nothing to remember.
Problem 2: C(n, k) with one row of k + 1 numbers, updated from right to left.
Problem 3: choose(n, k) with k > n used to recurse for ever; it now returns 0.
"""

from __future__ import annotations


def choose_one_row(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    row = [1] + [0] * k
    for i in range(1, n + 1):
        for j in range(min(i, k), 0, -1):          # right to left: row[j - 1] is still the previous row's
            row[j] += row[j - 1]
    return row[k]


if __name__ == "__main__":
    from collections import Counter
    from ch11_examples import choose, merge_sort_ranges, summary
    s = Counter(); merge_sort_ranges(0, 8, s); print(summary(s))
    print(choose_one_row(10, 4), choose(10, 4, Counter()), choose(2, 3, Counter()))
