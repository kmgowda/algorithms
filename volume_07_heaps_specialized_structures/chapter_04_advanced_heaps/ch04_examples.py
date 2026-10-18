"""Volume 7, Chapter 4 - Advanced Heaps: d-ary, Binomial, Pairing (and Fibonacci, by intuition).

Run:  python3 ch04_examples.py
"""

from __future__ import annotations

from typing import Any


class DaryHeap:
    """A min-heap where every node has d children: parent of i is (i-1)//d, children d*i+1 .. d*i+d.
    Shorter tree (log_d n levels) -> cheaper push; pop compares d children per level."""

    def __init__(self, d: int = 4) -> None:
        if d < 2:
            raise ValueError("d must be at least 2")
        self.d = d
        self.data: list[Any] = []
        self.comparisons = 0

    def push(self, value: Any) -> None:
        a, i = self.data, len(self.data)
        a.append(value)
        while i > 0:
            parent = (i - 1) // self.d
            self.comparisons += 1
            if a[parent] <= a[i]:
                break
            a[parent], a[i] = a[i], a[parent]
            i = parent

    def pop(self) -> Any:
        a = self.data
        if not a:
            raise IndexError("pop from empty heap")
        a[0], a[-1] = a[-1], a[0]
        smallest_value = a.pop()
        i, n = 0, len(a)
        while True:
            first = self.d * i + 1
            best = i
            for c in range(first, min(first + self.d, n)):
                self.comparisons += 1
                if a[c] < a[best]:
                    best = c
            if best == i:
                return smallest_value
            a[i], a[best] = a[best], a[i]
            i = best

    def __len__(self) -> int:
        return len(self.data)


class BinomialTree:
    """A binomial tree of order k has 2^k nodes: two order-(k-1) trees, one hung under the other's root."""

    def __init__(self, key: Any) -> None:
        self.key = key
        self.order = 0
        self.children: list[BinomialTree] = []


def link(a: BinomialTree, b: BinomialTree) -> BinomialTree:
    """Combine two trees of the same order: the larger root becomes a child of the smaller."""
    if b.key < a.key:
        a, b = b, a
    a.children.append(b)
    a.order += 1
    return a


class BinomialHeap:
    """A list of binomial trees with distinct orders - like the binary digits of n.
    Merging two heaps is like adding two binary numbers: O(log n)."""

    def __init__(self) -> None:
        self.trees: dict[int, BinomialTree] = {}       # order -> tree
        self.size = 0

    def _add_tree(self, tree: BinomialTree) -> None:
        while tree.order in self.trees:                 # 'carry' like binary addition
            tree = link(self.trees.pop(tree.order), tree)
        self.trees[tree.order] = tree

    def push(self, key: Any) -> None:
        self._add_tree(BinomialTree(key))
        self.size += 1

    def merge(self, other: "BinomialHeap") -> None:
        for tree in list(other.trees.values()):
            self._add_tree(tree)
        self.size += other.size
        other.trees, other.size = {}, 0

    def peek(self) -> Any:
        return min(t.key for t in self.trees.values())

    def pop(self) -> Any:
        if not self.size:
            raise IndexError("pop from empty heap")
        order = min(self.trees, key=lambda o: self.trees[o].key)
        root = self.trees.pop(order)
        for child in root.children:                     # its children are trees of orders 0..k-1
            self._add_tree(child)
        self.size -= 1
        return root.key


class PairingNode:
    def __init__(self, key: Any) -> None:
        self.key = key
        self.children: list[PairingNode] = []


def meld(a: PairingNode | None, b: PairingNode | None) -> PairingNode | None:
    """O(1): the larger root becomes a child of the smaller."""
    if a is None or b is None:
        return a or b
    if b.key < a.key:
        a, b = b, a
    a.children.append(b)
    return a


class PairingHeap:
    """A simple, fast-in-practice heap: push and meld are O(1); pop is O(log n) amortized (two-pass pairing)."""

    def __init__(self) -> None:
        self.root: PairingNode | None = None
        self.size = 0

    def push(self, key: Any) -> None:
        self.root = meld(self.root, PairingNode(key))
        self.size += 1

    def pop(self) -> Any:
        if self.root is None:
            raise IndexError("pop from empty heap")
        key, kids = self.root.key, self.root.children
        paired = [meld(kids[i], kids[i + 1] if i + 1 < len(kids) else None) for i in range(0, len(kids), 2)]
        root = None
        for tree in reversed(paired):                   # second pass: right to left
            root = meld(root, tree)
        self.root = root
        self.size -= 1
        return key


def merge_hospital_queues(a: list[int], b: list[int]) -> list[int]:
    """Industry example: two hospitals merge their waiting lists when one closes - binomial heaps merge fast."""
    ha, hb = BinomialHeap(), BinomialHeap()
    for x in a:
        ha.push(x)
    for x in b:
        hb.push(x)
    ha.merge(hb)
    return [ha.pop() for _ in range(ha.size)]


if __name__ == "__main__":
    for d in (2, 4, 8):
        h = DaryHeap(d)
        for x in range(1000, 0, -1):
            h.push(x)
        h.comparisons = 0
        out = [h.pop() for _ in range(1000)]
        print(f"d={d}: sorted={out == sorted(out)}, comparisons for 1000 pops: {h.comparisons}")
    bh = BinomialHeap()
    for x in [7, 3, 9, 1, 4]:
        bh.push(x)
    print("binomial tree orders for 5 items (5 = 101 in binary):", sorted(bh.trees))
    print(merge_hospital_queues([5, 2, 8], [3, 1, 9]))
    ph = PairingHeap()
    for x in [6, 2, 8, 1, 5]:
        ph.push(x)
    print("pairing heap pops:", [ph.pop() for _ in range(5)])
