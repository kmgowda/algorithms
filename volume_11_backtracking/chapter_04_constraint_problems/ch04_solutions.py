"""Volume 11, Chapter 4 - Solutions to the exercises."""

from __future__ import annotations


def count_queens_bits(n: int) -> int:
    """Exercise 1 (LeetCode 52): count N-Queens solutions using bitmasks for the attacked columns and diagonals."""
    full = (1 << n) - 1

    def go(cols: int, diag: int, anti: int) -> int:
        if cols == full:
            return 1
        total, free = 0, full & ~(cols | diag | anti)
        while free:
            bit = free & -free                    # lowest free column
            free -= bit
            total += go(cols | bit, (diag | bit) << 1 & full, (anti | bit) >> 1)
        return total

    return go(0, 0, 0)


def find_all_words(grid: list[str], words: list[str]) -> list[str]:
    """Exercise 2 (LeetCode 212 idea): which words appear? Build a trie (V6-C11) so one search checks all words."""
    trie: dict = {}
    for w in words:
        node = trie
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = w
    rows, cols = len(grid), len(grid[0])
    found: set[str] = set()

    def go(r: int, c: int, node: dict, used: set) -> None:
        if not (0 <= r < rows and 0 <= c < cols) or (r, c) in used or grid[r][c] not in node:
            return
        nxt = node[grid[r][c]]
        if "$" in nxt:
            found.add(nxt["$"])
        used.add((r, c))
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            go(r + dr, c + dc, nxt, used)
        used.remove((r, c))

    for r in range(rows):
        for c in range(cols):
            go(r, c, trie, set())
    return sorted(found)


def queens_are_safe(cols: list[int]) -> bool:
    """Exercise 3: check a full placement (one queen per row)."""
    n = len(cols)
    return all(cols[i] != cols[j] and abs(cols[i] - cols[j]) != j - i for i in range(n) for j in range(i + 1, n))


if __name__ == "__main__":
    print([count_queens_bits(n) for n in range(1, 11)])
    print(find_all_words(["oaan", "etae", "ihkr", "iflv"], ["oath", "pea", "eat", "rain"]), queens_are_safe([1, 3, 0, 2]))
