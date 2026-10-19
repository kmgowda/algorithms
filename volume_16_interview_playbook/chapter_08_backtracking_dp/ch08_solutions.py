"""Volume 16, Chapter 8 - Solutions to the exercises."""

from __future__ import annotations


def generate_parentheses(n: int) -> list[str]:
    """Exercise 1 (LeetCode 22): add '(' while some remain, ')' only if it keeps the string balanced."""
    out: list[str] = []

    def go(s: str, opened: int, closed: int) -> None:
        if len(s) == 2 * n:
            out.append(s)
            return
        if opened < n:
            go(s + "(", opened + 1, closed)
        if closed < opened:
            go(s + ")", opened, closed + 1)

    go("", 0, 0)
    return out


def can_partition(nums: list[int]) -> bool:
    """Exercise 2 (LeetCode 416): subset sum to half the total, with a set of reachable sums."""
    total = sum(nums)
    if total % 2:
        return False
    reach = {0}
    for x in nums:
        reach |= {r + x for r in reach}
    return total // 2 in reach


def unique_paths(rows: int, cols: int) -> int:
    """Exercise 3 (LeetCode 62): paths into a cell = from above + from the left, one row at a time."""
    row = [1] * cols
    for _ in range(1, rows):
        for c in range(1, cols):
            row[c] += row[c - 1]
    return row[-1]


if __name__ == "__main__":
    print(generate_parentheses(3), can_partition([1, 5, 11, 5]), unique_paths(3, 7))
