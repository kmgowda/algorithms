"""Volume 5, Chapter 3 - Solutions to the exercises."""

from __future__ import annotations


def relative_order(items: list[int], order: list[int]) -> list[int]:
    """Exercise 1 (LeetCode 1122): items in the order given by `order`; the rest ascending at the end."""
    rank = {v: i for i, v in enumerate(order)}
    return sorted(items, key=lambda v: (rank.get(v, len(order)), v))


def can_attend_all(meetings: list[tuple[int, int]]) -> bool:
    """Exercise 2 (LeetCode 252): after sorting by start, any overlap is between neighbours."""
    s = sorted(meetings)
    return all(s[i][1] <= s[i + 1][0] for i in range(len(s) - 1))


def sort_by_last_name(names: list[str]) -> list[str]:
    """Exercise 3: 'Maya Rao', 'Leo Adams' -> by last name, then first name, ignoring case."""
    return sorted(names, key=lambda n: (n.split()[-1].lower(), n.split()[0].lower()))


def h_index(citations: list[int]) -> int:
    """Exercise 4 (LeetCode 274): largest h with at least h papers cited at least h times. Sort descending."""
    s = sorted(citations, reverse=True)
    h = 0
    while h < len(s) and s[h] >= h + 1:
        h += 1
    return h


if __name__ == "__main__":
    print(relative_order([2, 3, 1, 3, 2, 4, 6, 7, 9, 2, 19], [2, 1, 4, 3, 9, 6]))
    print(can_attend_all([(9, 10), (10, 11)]), sort_by_last_name(["Maya Rao", "Leo Adams", "ali rao"]), h_index([3, 0, 6, 1, 5]))
