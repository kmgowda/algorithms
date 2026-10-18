"""Volume 6, Chapter 8 - Red-Black Trees: Balancing With Colors.

This is the LEFT-LEANING red-black tree (Sedgewick, 2008): the simplest red-black variant to code.
Rules: (1) red links lean left, (2) no node has two red links touching it,
(3) every path from the root to an empty link has the same number of BLACK links.

Run:  python3 ch08_examples.py
"""

from __future__ import annotations

from typing import Any, Iterator

RED, BLACK = True, False


class Node:
    def __init__(self, key: Any, value: Any = None) -> None:
        self.key, self.value = key, value
        self.left: Node | None = None
        self.right: Node | None = None
        self.color = RED                     # new nodes join with a red link


def is_red(node: Node | None) -> bool:
    return node is not None and node.color == RED


def rotate_left(h: Node) -> Node:
    """Turn a right-leaning red link into a left-leaning one."""
    x = h.right
    assert x is not None
    h.right, x.left = x.left, h
    x.color, h.color = h.color, RED
    return x


def rotate_right(h: Node) -> Node:
    """Turn a left-leaning red link into a right-leaning one (temporarily, during fixes)."""
    x = h.left
    assert x is not None
    h.left, x.right = x.right, h
    x.color, h.color = h.color, RED
    return x


def flip_colors(h: Node) -> None:
    """A node with two red children: push the red up one level (like splitting a full 2-3 tree node)."""
    h.color = not h.color
    assert h.left is not None and h.right is not None
    h.left.color = not h.left.color
    h.right.color = not h.right.color


def _insert(h: Node | None, key: Any, value: Any) -> Node:
    if h is None:
        return Node(key, value)
    if key < h.key:
        h.left = _insert(h.left, key, value)
    elif key > h.key:
        h.right = _insert(h.right, key, value)
    else:
        h.value = value
    # three local fixes, applied on the way back up
    if is_red(h.right) and not is_red(h.left):
        h = rotate_left(h)                   # a right-leaning red link -> lean it left
    if is_red(h.left) and h.left is not None and is_red(h.left.left):
        h = rotate_right(h)                  # two reds in a row on the left -> balance them
    if is_red(h.left) and is_red(h.right):
        flip_colors(h)                       # two red children -> pass red upward
    return h


class RedBlackTree:
    def __init__(self) -> None:
        self.root: Node | None = None
        self.size = 0

    def insert(self, key: Any, value: Any = None) -> None:
        if key not in self:
            self.size += 1
        self.root = _insert(self.root, key, value)
        self.root.color = BLACK              # the root is always black

    def get(self, key: Any) -> Any:
        node = self.root
        while node is not None:
            if key == node.key:
                return node.value
            node = node.left if key < node.key else node.right
        raise KeyError(key)

    def __contains__(self, key: Any) -> bool:
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def keys(self) -> Iterator[Any]:
        def walk(n: Node | None) -> Iterator[Any]:
            if n is not None:
                yield from walk(n.left)
                yield n.key
                yield from walk(n.right)
        return walk(self.root)

    def height(self) -> int:
        def hh(n: Node | None) -> int:
            return -1 if n is None else 1 + max(hh(n.left), hh(n.right))
        return hh(self.root)


def check(root: Node | None) -> int:
    """Verify order, 'no right reds', 'no two reds in a row', and equal black height. Returns the black height."""
    def visit(n: Node | None, low: Any, high: Any) -> int:
        if n is None:
            return 0
        assert (low is None or n.key > low) and (high is None or n.key < high), "order broken"
        assert not is_red(n.right), "red link leans right"
        assert not (is_red(n) and is_red(n.left)), "two reds in a row"
        left, right = visit(n.left, low, n.key), visit(n.right, n.key, high)
        assert left == right, "black heights differ"
        return left + (0 if is_red(n) else 1)
    assert not is_red(root), "root must be black"
    return visit(root, None, None)


def word_index(text: str) -> RedBlackTree:
    """Industry example: count words in sorted order - like Java's TreeMap or C++'s std::map, which are red-black trees."""
    tree = RedBlackTree()
    for w in text.lower().split():
        w = w.strip(".,!?")
        tree.insert(w, (tree.get(w) if w in tree else 0) + 1)
    return tree


if __name__ == "__main__":
    t = RedBlackTree()
    for k in "SEARCHXMPL":
        t.insert(k)
    print("keys:", "".join(t.keys()), "| height:", t.height(), "| black height:", check(t.root))
    big = RedBlackTree()
    for k in range(10_000):
        big.insert(k)
    print("10,000 sorted keys -> height", big.height(), "| black height", check(big.root))
    idx = word_index("the lion and the zebra and the eagle")
    print([(w, idx.get(w)) for w in idx.keys()])
