"""Volume 3, Chapter 2 - Binary Trees: companion code for the Thinking Problems (Section 2.16).

Run:  python3 ch02_solutions.py
"""

from __future__ import annotations

from collections import deque

from ch02_examples import TreeNode


def leaves(node) -> int:
    """Thinking Problem 1: nodes with no children."""
    if node is None:
        return 0
    if node.left is None and node.right is None:
        return 1
    return leaves(node.left) + leaves(node.right)


def array_cells(node) -> int:
    """Thinking Problem 3: array length the index rules need for this tree (largest index + 1; 0 if empty)."""
    best, q = -1, deque([(node, 0)] if node else [])
    while q:
        n, i = q.popleft()
        best = max(best, i)
        for c, j in ((n.left, 2 * i + 1), (n.right, 2 * i + 2)):
            if c:
                q.append((c, j))
    return best + 1


def is_complete(root) -> bool:
    """Thinking Problem 2: can the tree be stored in an array with no gaps? O(n) time.
    The n nodes get n different indexes; they fill 0..n-1 exactly when none of them is n or more."""
    n, stack = 0, [root] if root else []
    while stack:                          # count the nodes without recursion (chains can be deep)
        node = stack.pop()
        n += 1
        stack += [c for c in (node.left, node.right) if c]
    q = deque([(root, 0)] if root else [])
    while q:
        node, i = q.popleft()
        if i >= n:                        # a gap before this node: stop before indexes grow huge
            return False
        for c, j in ((node.left, 2 * i + 1), (node.right, 2 * i + 2)):
            if c:
                q.append((c, j))
    return True


if __name__ == "__main__":
    from ch02_examples import from_array
    chain = TreeNode(1, None, TreeNode(2, None, TreeNode(3, None, TreeNode(4))))
    print(is_complete(from_array([58, 25, 84, 12, 47, 70, 91, 9])), is_complete(chain), array_cells(chain))
