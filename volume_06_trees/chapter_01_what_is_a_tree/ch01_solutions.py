"""Volume 6, Chapter 1 - Solutions to the exercises."""

from __future__ import annotations

from ch01_examples import TreeNode


def largest_folder(node: TreeNode) -> tuple[str, int]:
    """Exercise 1: the folder (a node with children) whose total size is largest."""
    best = ("", -1)

    def visit(n: TreeNode) -> int:
        nonlocal best
        total = n.size + sum(visit(c) for c in n.children)
        if n.children and total > best[1]:
            best = (n.name, total)
        return total

    visit(node)
    return best


def find_files(node: TreeNode, extension: str) -> list[str]:
    """Exercise 2: every leaf name ending with an extension, like a file search."""
    if not node.children:
        return [node.name] if node.name.endswith(extension) else []
    return [f for c in node.children for f in find_files(c, extension)]


def build_from_paths(paths: list[str]) -> TreeNode:
    """Exercise 3: build a folder tree from paths like 'home/photos/lion.jpg'."""
    root = TreeNode(paths[0].split("/")[0]) if paths else TreeNode("")
    for path in paths:
        node = root
        for part in path.split("/")[1:]:
            match = next((c for c in node.children if c.name == part), None)
            node = match if match else node.add(TreeNode(part))
    return root


def max_children(node: TreeNode) -> int:
    """Exercise 4: the largest number of direct children any node has (the widest manager's team)."""
    return max([len(node.children)] + [max_children(c) for c in node.children])


if __name__ == "__main__":
    from ch01_examples import sample_folders, show
    home = sample_folders()
    print(largest_folder(home), find_files(home, ".jpg"), max_children(home))
    print("\n".join(show(build_from_paths(["zoo/cats/lion", "zoo/cats/tiger", "zoo/birds/eagle"]))))
