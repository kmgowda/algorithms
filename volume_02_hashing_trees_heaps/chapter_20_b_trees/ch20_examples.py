"""Volume 2, Chapter 20 - B-Trees.

Run:  python3 ch20_examples.py
"""

from __future__ import annotations

import bisect
import math


class BNode:
    __slots__ = ("keys", "children")

    def __init__(self, keys=None, children=None):
        self.keys, self.children = keys or [], children or []

    @property
    def leaf(self) -> bool:
        return not self.children


class BTree:
    """A B-tree whose nodes hold at most max_keys = 2t - 1 keys and, except the root, at least
    min_keys = t - 1 keys (t is the minimum degree). Full nodes split on the way down (Figure 20.3);
    deletion repairs underfull nodes on the way back up by borrowing or merging (Figures 20.7 and 20.8)."""

    def __init__(self, max_keys: int = 3, keys=()):
        assert max_keys % 2 == 1 and max_keys >= 3
        self.max_keys = max_keys
        self.min_keys = max_keys // 2                     # t - 1, where t = (max_keys + 1) / 2
        self.root = BNode()
        self.splits = 0
        self.borrows = self.merges = self.shrinks = 0
        for k in keys:
            self.insert(k)

    def search(self, key) -> tuple[bool, int]:
        """Returns (found, nodes visited): each visited node is one disk read (Figure 20.2)."""
        n, visits = self.root, 0
        while True:
            visits += 1
            i = bisect.bisect_left(n.keys, key)
            if i < len(n.keys) and n.keys[i] == key:
                return True, visits
            if n.leaf:
                return False, visits
            n = n.children[i]

    def _split_child(self, parent: BNode, i: int) -> None:
        """Move the middle key of parent.children[i] up into parent (Figure 20.3)."""
        child = parent.children[i]
        mid = len(child.keys) // 2
        right = BNode(child.keys[mid + 1:], child.children[mid + 1:])
        parent.keys.insert(i, child.keys[mid])
        parent.children.insert(i + 1, right)
        child.keys, child.children = child.keys[:mid], child.children[:mid + 1]
        self.splits += 1

    def insert(self, key) -> None:
        if self.search(key)[0]:
            return
        if len(self.root.keys) == self.max_keys:          # a full root splits: the tree grows taller
            self.root = BNode([], [self.root])
            self._split_child(self.root, 0)
        n = self.root
        while not n.leaf:
            i = bisect.bisect_left(n.keys, key)
            if len(n.children[i].keys) == self.max_keys:
                self._split_child(n, i)
                if key > n.keys[i]:
                    i += 1
            n = n.children[i]
        bisect.insort(n.keys, key)

    def insert_bottom_up(self, key) -> None:
        """The other way to insert (Figure 20.4): put the key into its leaf first, and split a node only
        when it overflows to max_keys + 1 keys, pushing its middle key up; the parent may overflow in turn."""
        if self.search(key)[0]:
            return
        up = self._insert_up(self.root, key)
        if up is not None:                               # the root overflowed: a new root above it
            self.root = BNode([up[0]], [self.root, up[1]])

    def _insert_up(self, n: BNode, key):
        i = bisect.bisect_left(n.keys, key)
        if n.leaf:
            n.keys.insert(i, key)
        else:
            up = self._insert_up(n.children[i], key)
            if up is not None:
                n.keys.insert(i, up[0])
                n.children.insert(i + 1, up[1])
        if len(n.keys) <= self.max_keys:
            return None
        m = len(n.keys) // 2                             # overflowing: split, and hand the middle key up
        right = BNode(n.keys[m + 1:], n.children[m + 1:])
        middle = n.keys[m]
        n.keys, n.children = n.keys[:m], n.children[:m + 1]
        self.splits += 1
        return middle, right

    def delete(self, key) -> bool:
        """Remove key if present; returns whether it was there (Figures 20.7 and 20.8)."""
        removed = self._delete(self.root, key)
        if not self.root.keys and self.root.children:    # the root lost its last key: its one child is the root
            self.root = self.root.children[0]
            self.shrinks += 1
        return removed

    def _delete(self, n: BNode, key) -> bool:
        i = bisect.bisect_left(n.keys, key)
        here = i < len(n.keys) and n.keys[i] == key
        if n.leaf:
            if here:
                n.keys.pop(i)
            return here
        if here:                                         # an inner key: swap in its predecessor, delete that
            p = n.children[i]
            while not p.leaf:
                p = p.children[-1]
            n.keys[i] = key = p.keys[-1]
        removed = self._delete(n.children[i], key)
        if len(n.children[i].keys) < self.min_keys:       # the child fell below the minimum: repair it
            self._repair(n, i)
        return removed

    def _repair(self, parent: BNode, i: int) -> None:
        """Give parent.children[i] back its minimum: borrow from a sibling with a spare key, else merge."""
        child = parent.children[i]
        left = parent.children[i - 1] if i > 0 else None
        right = parent.children[i + 1] if i + 1 < len(parent.children) else None
        if left is not None and len(left.keys) > self.min_keys:     # borrow through the parent, from the left
            child.keys.insert(0, parent.keys[i - 1])
            parent.keys[i - 1] = left.keys.pop()
            if not left.leaf:
                child.children.insert(0, left.children.pop())
            self.borrows += 1
        elif right is not None and len(right.keys) > self.min_keys:  # or from the right
            child.keys.append(parent.keys[i])
            parent.keys[i] = right.keys.pop(0)
            if not right.leaf:
                child.children.append(right.children.pop(0))
            self.borrows += 1
        else:                                            # no spare key nearby: merge with a sibling
            j = i - 1 if left is not None else i
            a, b = parent.children[j], parent.children[j + 1]
            a.keys += [parent.keys.pop(j)] + b.keys      # the separator comes down between them
            a.children += b.children
            parent.children.pop(j + 1)
            self.merges += 1

    def valid(self) -> bool:
        """Sorted keys, keys between their separators, min_keys..max_keys keys per non-root node,
        one more child than keys in inner nodes, and every leaf at the same depth."""
        depths = set()

        def check(n, lo, hi, d, is_root):
            if n.keys != sorted(n.keys) or len(set(n.keys)) != len(n.keys):
                return False
            if any((lo is not None and k <= lo) or (hi is not None and k >= hi) for k in n.keys):
                return False
            if len(n.keys) > self.max_keys or (not is_root and len(n.keys) < self.min_keys):
                return False
            if n.leaf:
                depths.add(d)
                return True
            if len(n.children) != len(n.keys) + 1:
                return False
            bounds = [lo] + n.keys + [hi]
            return all(check(c, bounds[k], bounds[k + 1], d + 1, False) for k, c in enumerate(n.children))
        return check(self.root, None, None, 0, True) and len(depths) == 1

    def height(self) -> int:
        h, n = 0, self.root
        while not n.leaf:
            h, n = h + 1, n.children[0]
        return h

    def levels(self) -> list[list[list]]:
        """Keys of every node, level by level (for drawing and testing)."""
        out, level = [], [self.root]
        while level:
            out.append([n.keys for n in level])
            level = [c for n in level for c in n.children]
        return out

    def inorder(self, n=None) -> list:
        n = n or self.root
        if n.leaf:
            return list(n.keys)
        out = []
        for i, k in enumerate(n.keys):
            out += self.inorder(n.children[i]) + [k]
        return out + self.inorder(n.children[-1])

    def leaves_same_depth(self) -> bool:
        depths = set()

        def walk(n, d):
            if n.leaf:
                depths.add(d)
            for c in n.children:
                walk(c, d + 1)
        walk(self.root, 0)
        return len(depths) == 1


def drawers_opened(records: int, per_drawer: int) -> tuple[int, int]:
    """Section 20.9, a B+ tree: leaf drawers hold the records, inner drawers point to per_drawer drawers.
    Returns (leaf drawers needed, drawers opened by one lookup = number of levels)."""
    leaves = nodes = -(-records // per_drawer)
    levels = 1
    while nodes > 1:
        nodes = -(-nodes // per_drawer)
        levels += 1
    return leaves, levels


if __name__ == "__main__":
    t = BTree(3)
    for k in [58, 25, 84, 12, 47, 70, 91, 31, 63]:
        t.insert(k)
        print(k, t.levels())
    print(t.search(63), t.splits)
    for k in [47, 12, 91, 58, 25, 84, 31]:               # the clearing-out of Section 20.8
        t.delete(k)
        print("delete", k, t.levels(), t.borrows, t.merges, t.shrinks)
    print([drawers_opened(2_000_000, f) for f in (250, 167, 125)])
    big = BTree(199, range(1_000_000))
    print(big.height(), big.search(765_432), math.log2(1_000_000))
