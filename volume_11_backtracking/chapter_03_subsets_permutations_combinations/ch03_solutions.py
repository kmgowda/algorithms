"""Volume 11, Chapter 3 - Solutions to the exercises."""

from __future__ import annotations


def combination_sum_once(candidates: list[int], target: int) -> list[list[int]]:
    """Exercise 1 (LeetCode 40): each number used at most once, no duplicate answers - sort and skip equal siblings."""
    c = sorted(candidates)
    out: list[list[int]] = []
    path: list[int] = []

    def go(start: int, remaining: int) -> None:
        if remaining == 0:
            out.append(list(path))
            return
        for i in range(start, len(c)):
            if i > start and c[i] == c[i - 1]:
                continue
            if c[i] > remaining:
                break
            path.append(c[i])
            go(i + 1, remaining - c[i])
            path.pop()

    go(0, target)
    return out


def k_digits_sum(k: int, n: int) -> list[list[int]]:
    """Exercise 2 (LeetCode 216): k distinct digits 1-9 adding to n."""
    out: list[list[int]] = []
    path: list[int] = []

    def go(start: int, remaining: int) -> None:
        if len(path) == k:
            if remaining == 0:
                out.append(list(path))
            return
        for d in range(start, 10):
            if d > remaining:
                break
            path.append(d)
            go(d + 1, remaining - d)
            path.pop()

    go(1, n)
    return out


def subsets_by_bitmask(items: list[str]) -> list[list[str]]:
    """Exercise 3: subsets without recursion - the bits of 0 .. 2^n - 1 say which items to take."""
    n = len(items)
    return [[items[i] for i in range(n) if mask >> i & 1] for mask in range(1 << n)]


def next_permutation(values: list[int]) -> list[int]:
    """Exercise 4 (LeetCode 31): the next order in dictionary order, in place - no search needed."""
    v = list(values)
    i = len(v) - 2
    while i >= 0 and v[i] >= v[i + 1]:
        i -= 1
    if i >= 0:
        j = len(v) - 1
        while v[j] <= v[i]:
            j -= 1
        v[i], v[j] = v[j], v[i]
    v[i + 1:] = reversed(v[i + 1:])
    return v


if __name__ == "__main__":
    print(combination_sum_once([10, 1, 2, 7, 6, 1, 5], 8), k_digits_sum(3, 9))
    print(subsets_by_bitmask(["x", "y"]), next_permutation([1, 3, 2]))
