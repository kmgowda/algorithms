"""Volume 3, Chapter 23 - Treaps: companion code for the Thinking Problems (Section 23.16).

Run:  python3 ch23_solutions.py
"""

from __future__ import annotations

import random

from ch23_examples import Treap, spine_rotations


def insert_then_delete(keys, priorities: dict, key, prio):
    """Thinking Problem 1: insert key with priority prio into the treap of keys, then delete it again.
    Returns (rotations of the insertion, rotations of the deletion, the tree is back to its old shape)."""
    t = Treap(keys, priorities=priorities)
    before = t.shape()
    t.insert(key, prio)
    up, spines = t.last_rotations, spine_rotations(t, key)
    assert up == spines
    t.delete(key)
    return up, t.last_rotations, t.shape() == before


class SNode:
    __slots__ = ("value", "prio", "size", "left", "right")

    def __init__(self, value, prio):
        self.value, self.prio, self.size, self.left, self.right = value, prio, 1, None, None


def _size(t) -> int:
    return t.size if t else 0


def _fix(t):
    t.size = 1 + _size(t.left) + _size(t.right)
    return t


def split_count(t, i):
    """Cut a sequence into (its first i items, the rest)."""
    if t is None:
        return None, None
    if _size(t.left) < i:
        t.right, rest = split_count(t.right, i - _size(t.left) - 1)
        return _fix(t), rest
    first, t.left = split_count(t.left, i)
    return first, _fix(t)


def merge_sized(a, b):
    if a is None or b is None:
        return a or b
    if a.prio > b.prio:
        a.right = merge_sized(a.right, b)
        return _fix(a)
    b.left = merge_sized(a, b.left)
    return _fix(b)


class ImplicitTreap:
    """Thinking Problem 2: a sequence (Maya's reservation queue) with insert and delete at any position in
    O(log n) expected time. The keys are implicit: an item's position is the number of items to its left."""

    def __init__(self, items=(), seed=1):
        self.root, self.rng = None, random.Random(seed)
        for x in items:
            self.insert_at(len(self), x)

    def __len__(self) -> int:
        return _size(self.root)

    def insert_at(self, i, value):
        if not 0 <= i <= len(self):
            raise IndexError(i)
        first, rest = split_count(self.root, i)
        self.root = merge_sized(merge_sized(first, SNode(value, self.rng.random())), rest)

    def delete_at(self, i):
        if not 0 <= i < len(self):
            raise IndexError(i)
        first, rest = split_count(self.root, i)
        gone, rest = split_count(rest, 1)
        self.root = merge_sized(first, rest)
        return gone.value

    def get(self, i):
        if not 0 <= i < len(self):
            raise IndexError(i)
        t = self.root
        while True:
            if i < _size(t.left):
                t = t.left
            elif i == _size(t.left):
                return t.value
            else:
                i, t = i - _size(t.left) - 1, t.right

    def to_list(self):
        out, stack, t = [], [], self.root
        while stack or t:
            while t:
                stack.append(t)
                t = t.left
            t = stack.pop()
            out.append(t.value)
            t = t.right
        return out

    def height(self) -> int:
        def h(t):
            return -1 if t is None else 1 + max(h(t.left), h(t.right))
        return h(self.root)


def arrival_priority_treap(keys) -> Treap:
    """Thinking Problem 3, the bug: the priority is the card's arrival number, so every new key wins."""
    return Treap(keys, priorities={k: i for i, k in enumerate(keys)})


if __name__ == "__main__":
    print("insert then delete:", insert_then_delete([1], {1: 5}, 2, 9))
    q = ImplicitTreap(["Ana", "Ben", "Chen"])
    q.insert_at(1, "class 4B")
    print(q.to_list(), q.delete_at(0), q.to_list())
    t = arrival_priority_treap([12, 25, 31, 47, 58, 63, 70, 84, 91])
    print("arrival numbers as priorities:", t.height(), t.rotations)
