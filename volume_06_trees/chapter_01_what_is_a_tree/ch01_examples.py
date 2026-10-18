"""Volume 6, Chapter 1 - What Is a Tree? Family Trees, Folders, and Organization Charts.

Run:  python3 ch01_examples.py
"""

from __future__ import annotations

from collections import deque
from typing import Iterator


class TreeNode:
    """A general tree node: a name, an optional size, and any number of children."""

    def __init__(self, name: str, size: int = 0, children: list["TreeNode"] | None = None) -> None:
        self.name = name
        self.size = size
        self.children: list[TreeNode] = children or []

    def add(self, child: "TreeNode") -> "TreeNode":
        self.children.append(child)
        return child


def count_nodes(node: TreeNode) -> int:
    """Every node is 1 plus all the nodes below it - recursion follows the tree's shape."""
    return 1 + sum(count_nodes(c) for c in node.children)


def leaves(node: TreeNode) -> list[str]:
    """Nodes with no children (files in a folder tree, employees with no reports)."""
    if not node.children:
        return [node.name]
    return [name for c in node.children for name in leaves(c)]


def height(node: TreeNode) -> int:
    """Edges on the longest path from this node down to a leaf. A single node has height 0."""
    return 0 if not node.children else 1 + max(height(c) for c in node.children)


def total_size(node: TreeNode) -> int:
    """Practical example: a folder's disk usage = its own files + everything inside it."""
    return node.size + sum(total_size(c) for c in node.children)


def show(node: TreeNode, depth: int = 0) -> Iterator[str]:
    """Draw the tree with indentation, like a file explorer."""
    yield "    " * depth + node.name
    for c in node.children:
        yield from show(c, depth + 1)


def path_to(node: TreeNode, target: str) -> list[str] | None:
    """The chain of names from the root to `target` (e.g. a file's full path), or None."""
    if node.name == target:
        return [node.name]
    for c in node.children:
        rest = path_to(c, target)
        if rest is not None:
            return [node.name] + rest
    return None


def people_per_level(root: TreeNode) -> list[int]:
    """Industry example: how many people at each level of an org chart - level by level with a queue (V3-C9)."""
    counts: list[int] = []
    queue = deque([(root, 0)])
    while queue:
        node, level = queue.popleft()
        if level == len(counts):
            counts.append(0)
        counts[level] += 1
        queue.extend((c, level + 1) for c in node.children)
    return counts


def sample_folders() -> TreeNode:
    root = TreeNode("home")
    docs = root.add(TreeNode("documents"))
    docs.add(TreeNode("essay.txt", 12))
    docs.add(TreeNode("budget.xlsx", 30))
    photos = root.add(TreeNode("photos"))
    zoo = photos.add(TreeNode("zoo_trip"))
    zoo.add(TreeNode("lion.jpg", 400))
    zoo.add(TreeNode("zebra.jpg", 350))
    photos.add(TreeNode("beach.jpg", 500))
    root.add(TreeNode("notes.txt", 2))
    return root


if __name__ == "__main__":
    home = sample_folders()
    print("\n".join(show(home)))
    print("nodes:", count_nodes(home), "| height:", height(home), "| leaves:", leaves(home))
    print("total size (KB):", total_size(home), "| path to lion.jpg:", "/".join(path_to(home, "lion.jpg") or []))
    print("items per level:", people_per_level(home))
