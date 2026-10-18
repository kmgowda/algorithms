"""Volume 6, Chapter 5 - Binary Search Trees: Insert, Search, Delete.

Rule (the BST invariant): everything in a node's LEFT subtree is smaller, everything in its RIGHT subtree is larger.

Run:  python3 ch05_examples.py
"""

from __future__ import annotations

from typing import Any, Iterator


class Node:
    def __init__(self, key: Any, value: Any = None) -> None:
        self.key, self.value = key, value
        self.left: Node | None = None
        self.right: Node | None = None


class BST:
    """A map from keys to values, kept in sorted order by the BST invariant. Distinct keys."""

    def __init__(self) -> None:
        self.root: Node | None = None
        self.size = 0

    def search(self, key: Any) -> Any:
        """Walk down: go left if smaller, right if larger. O(h)."""
        node = self.root
        while node is not None:
            if key == node.key:
                return node.value
            node = node.left if key < node.key else node.right
        raise KeyError(key)

    def __contains__(self, key: Any) -> bool:
        try:
            self.search(key)
            return True
        except KeyError:
            return False

    def insert(self, key: Any, value: Any = None) -> None:
        """Walk down as in search; attach a new leaf where the search falls off. O(h)."""
        if self.root is None:
            self.root, self.size = Node(key, value), 1
            return
        node = self.root
        while True:
            if key == node.key:
                node.value = value               # existing key: update
                return
            side = "left" if key < node.key else "right"
            child = getattr(node, side)
            if child is None:
                setattr(node, side, Node(key, value))
                self.size += 1
                return
            node = child

    def delete(self, key: Any) -> None:
        """Three cases: a leaf (just remove), one child (lift the child up), two children
        (copy in the successor - the smallest key in the right subtree - then delete that). O(h)."""
        self.root = self._delete(self.root, key)
        self.size -= 1

    def _delete(self, node: Node | None, key: Any) -> Node | None:
        if node is None:
            raise KeyError(key)
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.key, node.value = successor.key, successor.value
            node.right = self._delete(node.right, successor.key)
        return node

    def minimum(self) -> Any:
        node = self.root
        if node is None:
            raise ValueError("empty tree")
        while node.left is not None:
            node = node.left
        return node.key

    def maximum(self) -> Any:
        node = self.root
        if node is None:
            raise ValueError("empty tree")
        while node.right is not None:
            node = node.right
        return node.key

    def floor(self, key: Any) -> Any:
        """The largest key <= key (None if none) - e.g. the latest bus at or before a given time."""
        node, best = self.root, None
        while node is not None:
            if node.key == key:
                return key
            if node.key < key:
                best, node = node.key, node.right
            else:
                node = node.left
        return best

    def ceiling(self, key: Any) -> Any:
        """The smallest key >= key (None if none)."""
        node, best = self.root, None
        while node is not None:
            if node.key == key:
                return key
            if node.key > key:
                best, node = node.key, node.left
            else:
                node = node.right
        return best

    def keys(self) -> Iterator[Any]:
        """Inorder traversal (Chapter 3) gives the keys in SORTED order."""
        def walk(node: Node | None) -> Iterator[Any]:
            if node is not None:
                yield from walk(node.left)
                yield node.key
                yield from walk(node.right)
        return walk(self.root)

    def range(self, low: Any, high: Any) -> list[Any]:
        """All keys in [low, high], skipping subtrees that can't contain any. O(h + answer size)."""
        out: list[Any] = []

        def walk(node: Node | None) -> None:
            if node is None:
                return
            if low < node.key:
                walk(node.left)
            if low <= node.key <= high:
                out.append(node.key)
            if node.key < high:
                walk(node.right)

        walk(self.root)
        return out

    def height(self) -> int:
        def h(node: Node | None) -> int:
            return -1 if node is None else 1 + max(h(node.left), h(node.right))
        return h(self.root)


def is_valid_bst(node: Node | None, low: Any = None, high: Any = None) -> bool:
    """LeetCode 98: check the invariant by passing the allowed (low, high) range DOWN the tree."""
    if node is None:
        return True
    if (low is not None and node.key <= low) or (high is not None and node.key >= high):
        return False
    return is_valid_bst(node.left, low, node.key) and is_valid_bst(node.right, node.key, high)


if __name__ == "__main__":
    library = BST()
    for code, title in [(500, "Science"), (300, "Social"), (800, "Literature"), (100, "Philosophy"),
                        (400, "Language"), (700, "Arts"), (900, "History")]:
        library.insert(code, title)
    print("sorted:", list(library.keys()), "| height:", library.height(), "| 400 ->", library.search(400))
    print("floor(650):", library.floor(650), "| ceiling(650):", library.ceiling(650), "| range 250-750:", library.range(250, 750))
    library.delete(500)
    print("after deleting the root:", list(library.keys()), "| new root:", library.root.key, "| valid:", is_valid_bst(library.root))  # type: ignore[union-attr]
