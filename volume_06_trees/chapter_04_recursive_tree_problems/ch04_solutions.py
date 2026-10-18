"""Volume 6, Chapter 4 - Solutions to the exercises."""

from __future__ import annotations

from ch04_examples import Node, lowest_common_ancestor


def min_depth(node: Node | None) -> int:
    """Exercise 1 (LeetCode 111): nodes on the SHORTEST root-to-leaf path. Careful: a missing child is not a leaf."""
    if node is None:
        return 0
    if node.left is None:
        return 1 + min_depth(node.right)
    if node.right is None:
        return 1 + min_depth(node.left)
    return 1 + min(min_depth(node.left), min_depth(node.right))


def is_symmetric(root: Node | None) -> bool:
    """Exercise 2 (LeetCode 101): is the tree a mirror image of itself?"""
    def mirror(a: Node | None, b: Node | None) -> bool:
        if a is None or b is None:
            return a is b
        return a.value == b.value and mirror(a.left, b.right) and mirror(a.right, b.left)
    return mirror(root.left, root.right) if root else True


def count_good_nodes(root: Node | None) -> int:
    """Exercise 3 (LeetCode 1448): a node is 'good' if no value on the path above it is larger."""
    def visit(node: Node | None, best: float) -> int:
        if node is None:
            return 0
        good = 1 if node.value >= best else 0
        best = max(best, node.value)
        return good + visit(node.left, best) + visit(node.right, best)
    return visit(root, float("-inf"))


def distance_between(root: Node, a, b) -> int:
    """Exercise 4: edges between two nodes = depth(a) + depth(b) - 2 * depth(LCA)."""
    def depth(node: Node | None, target, d: int = 0) -> int:
        if node is None:
            return -1
        if node.value == target:
            return d
        left = depth(node.left, target, d + 1)
        return left if left >= 0 else depth(node.right, target, d + 1)

    lca = lowest_common_ancestor(root, a, b)
    assert lca is not None
    return depth(root, a) + depth(root, b) - 2 * depth(root, lca.value)


if __name__ == "__main__":
    t = Node(1, Node(2, Node(3), Node(4)), Node(2, Node(4), Node(3)))
    print(min_depth(t), is_symmetric(t), count_good_nodes(Node(3, Node(1, Node(3)), Node(4, Node(1), Node(5)))))
    named = Node("a", Node("b", Node("d"), Node("e")), Node("c"))
    print(distance_between(named, "d", "c"))
