"""Volume 16, Chapter 6 - Solutions to the exercises."""

from __future__ import annotations

from collections import deque

from ch06_examples import TreeNode


def diameter(root: TreeNode | None) -> int:
    """Exercise 1 (LeetCode 543): longest path in edges - each node joins its two deepest branches."""
    best = 0

    def depth(node: TreeNode | None) -> int:
        nonlocal best
        if node is None:
            return 0
        left, right = depth(node.left), depth(node.right)
        best = max(best, left + right)
        return 1 + max(left, right)

    depth(root)
    return best


def rotting_oranges(grid: list[list[int]]) -> int:
    """Exercise 2 (LeetCode 994): multi-source BFS from every rotten orange; minutes = BFS layers. -1 if some stay fresh."""
    rows, cols = len(grid), len(grid[0])
    q = deque((r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 2)
    fresh = sum(row.count(1) for row in grid)
    grid = [row[:] for row in grid]
    minutes = 0
    while q and fresh:
        for _ in range(len(q)):
            r, c = q.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    q.append((nr, nc))
        minutes += 1
    return -1 if fresh else minutes


def right_side_view(root: TreeNode | None) -> list[int]:
    """Exercise 3 (LeetCode 199): the last node of each BFS layer."""
    out, q = [], deque([root] if root else [])
    while q:
        layer = [q.popleft() for _ in range(len(q))]
        out.append(layer[-1].val)
        q.extend(c for n in layer for c in (n.left, n.right) if c)
    return out


if __name__ == "__main__":
    from ch06_examples import from_level_list
    print(diameter(from_level_list([1, 2, 3, 4, 5])), rotting_oranges([[2, 1, 1], [1, 1, 0], [0, 1, 1]]),
          right_side_view(from_level_list([1, 2, 3, None, 5, None, 4])))
