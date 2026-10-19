"""Volume 16, Chapter 6 - Trees and Graphs: Interview Drill.

Run:  python3 ch06_examples.py
"""

from __future__ import annotations

from collections import deque


class TreeNode:
    def __init__(self, val: int, left: "TreeNode | None" = None, right: "TreeNode | None" = None) -> None:
        self.val, self.left, self.right = val, left, right


def from_level_list(values: list[int | None]) -> TreeNode | None:
    """Build a tree from LeetCode's level-order list (None = missing child)."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    q, i = deque([root]), 1
    while q and i < len(values):
        node = q.popleft()
        for side in ("left", "right"):
            if i < len(values) and values[i] is not None:
                child = TreeNode(values[i])                      # type: ignore[arg-type]
                setattr(node, side, child)
                q.append(child)
            i += 1
    return root


def max_depth(root: TreeNode | None) -> int:
    """LeetCode 104: a tree's depth is 1 + the deeper subtree (the 'trust the recursion' pattern, V6-C4)."""
    return 0 if root is None else 1 + max(max_depth(root.left), max_depth(root.right))


def invert(root: TreeNode | None) -> TreeNode | None:
    """LeetCode 226: swap the children at every node."""
    if root:
        root.left, root.right = invert(root.right), invert(root.left)
    return root


def level_order(root: TreeNode | None) -> list[list[int]]:
    """LeetCode 102: BFS, one queue 'layer' at a time."""
    out, q = [], deque([root] if root else [])
    while q:
        layer = [q.popleft() for _ in range(len(q))]
        out.append([n.val for n in layer])
        q.extend(c for n in layer for c in (n.left, n.right) if c)
    return out


def is_valid_bst(root: TreeNode | None, lo: float = float("-inf"), hi: float = float("inf")) -> bool:
    """LeetCode 98: every node must lie inside the range allowed by ALL its ancestors, not just its parent."""
    if root is None:
        return True
    return lo < root.val < hi and is_valid_bst(root.left, lo, root.val) and is_valid_bst(root.right, root.val, hi)


def lowest_common_ancestor(root: TreeNode | None, p: int, q: int) -> TreeNode | None:
    """LeetCode 236: the first node where p and q are found in different subtrees (or the node is one of them)."""
    if root is None or root.val in (p, q):
        return root
    left, right = lowest_common_ancestor(root.left, p, q), lowest_common_ancestor(root.right, p, q)
    return root if left and right else left or right


def count_islands(grid: list[str]) -> int:
    """LeetCode 200: each unvisited land cell starts a flood fill (V8-C6)."""
    rows, cols = len(grid), len(grid[0]) if grid else 0
    seen: set[tuple[int, int]] = set()
    islands = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in seen:
                islands += 1
                stack = [(r, c)]
                seen.add((r, c))
                while stack:
                    y, x = stack.pop()
                    for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                        if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == "1" and (ny, nx) not in seen:
                            seen.add((ny, nx))
                            stack.append((ny, nx))
    return islands


def can_finish(courses: int, prerequisites: list[tuple[int, int]]) -> bool:
    """LeetCode 207: possible exactly when the prerequisite graph has no cycle - Kahn's topological sort (V8-C7)."""
    after = [[] for _ in range(courses)]
    indeg = [0] * courses
    for course, pre in prerequisites:
        after[pre].append(course)
        indeg[course] += 1
    q = deque(c for c in range(courses) if indeg[c] == 0)
    done = 0
    while q:
        c = q.popleft()
        done += 1
        for nxt in after[c]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                q.append(nxt)
    return done == courses


def org_chart_depth(reports: dict[str, list[str]], ceo: str) -> int:
    """Industry example: how many management levels an org chart has (tree depth over a dictionary)."""
    return 1 + max((org_chart_depth(reports, r) for r in reports.get(ceo, [])), default=0)


if __name__ == "__main__":
    t = from_level_list([3, 9, 20, None, None, 15, 7])
    print(max_depth(t), level_order(t))
    print(level_order(invert(from_level_list([4, 2, 7, 1, 3, 6, 9]))))
    print(is_valid_bst(from_level_list([2, 1, 3])), is_valid_bst(from_level_list([5, 1, 4, None, None, 3, 6])))
    print(lowest_common_ancestor(from_level_list([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]), 5, 4).val)
    print(count_islands(["11000", "11000", "00100", "00011"]), can_finish(2, [(1, 0)]), can_finish(2, [(1, 0), (0, 1)]))
    print(org_chart_depth({"CEO": ["CTO", "CFO"], "CTO": ["Lead"], "Lead": ["Dev"]}, "CEO"))
