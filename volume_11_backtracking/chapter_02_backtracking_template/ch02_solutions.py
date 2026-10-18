"""Volume 11, Chapter 2 - Solutions to the exercises."""

from __future__ import annotations

from ch02_examples import backtrack


def words_from_tiles(tiles: str, length: int) -> list[str]:
    """Exercise 1: every word of a given length from letter tiles, each tile used at most once (positions matter)."""
    out: list[list[int]] = []
    backtrack([], lambda s: len(s) == length, lambda s: [i for i in range(len(tiles)) if i not in s], lambda s: True, out)
    return sorted({"".join(tiles[i] for i in s) for s in out})


def increasing_sequences(n: int, k: int) -> list[list[int]]:
    """Exercise 2: strictly increasing sequences of k numbers from 1..n - options are numbers above the last one."""
    out: list[list[int]] = []
    backtrack([], lambda s: len(s) == k, lambda s: range((s[-1] + 1) if s else 1, n + 1), lambda s: True, out)
    return out


def count_with_visit_counter(n: int) -> tuple[int, int]:
    """Exercise 3: how many bit strings of length n without '11' - and how many nodes the search visited."""
    visited = 0

    def go(last: str, length: int) -> int:
        nonlocal visited
        visited += 1
        if length == n:
            return 1
        total = go("0", length + 1)
        if last != "1":
            total += go("1", length + 1)
        return total

    return go("", 0), visited


if __name__ == "__main__":
    print(words_from_tiles("aab", 2), increasing_sequences(4, 2), count_with_visit_counter(10))
