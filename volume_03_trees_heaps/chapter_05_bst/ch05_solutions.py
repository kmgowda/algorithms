"""Volume 3, Chapter 5 - Binary Search Trees: companion code for the Thinking Problems (Section 5.16).

Run:  python3 ch05_solutions.py
"""

from __future__ import annotations

from ch05_examples import BST


def pair_with_sum(tree: BST, target):
    """Thinking Problem 2: two different keys a < b with a + b = target, or None. O(n) time, O(h) memory.
    Two inorder walks with explicit stacks: one upwards from the smallest key, one downwards from the largest."""
    low, high = [], []

    def slide(n, stack, side):                     # push n and its whole left (or right) spine
        while n is not None:
            stack.append(n)
            n = getattr(n, side)
    slide(tree.root, low, "left")
    slide(tree.root, high, "right")
    while low and high:
        a, b = low[-1], high[-1]
        if a.key >= b.key:                          # the two walks have met
            return None
        s = a.key + b.key
        if s == target:
            return a.key, b.key
        if s < target:                              # a is too small for every remaining b: step a up
            low.pop()
            slide(a.right, low, "left")
        else:                                       # b is too large for every remaining a: step b down
            high.pop()
            slide(b.left, high, "right")
    return None


def buggy_delete(tree: BST, key) -> None:
    """Thinking Problem 3: a two-children delete that copies the successor up and then simply cuts the
    successor's old node off, losing the successor's right subtree."""
    parent, n = None, tree.root
    while n is not None and n.key != key:
        parent, n = n, (n.left if key < n.key else n.right)
    if n is None:
        return
    if n.left is None or n.right is None:
        child = n.left or n.right
        if parent is None:
            tree.root = child
        elif parent.left is n:
            parent.left = child
        else:
            parent.right = child
        return
    sp, s = n, n.right
    while s.left is not None:
        sp, s = s, s.left
    n.key = s.key
    if sp.left is s:                                # the bug: s.right is thrown away with s
        sp.left = None
    else:
        sp.right = None


def shape(tree: BST):
    def walk(n):
        return None if n is None else (n.key, walk(n.left), walk(n.right))
    return walk(tree.root)


if __name__ == "__main__":
    from ch05_examples import ORDER
    print(pair_with_sum(BST(ORDER), 116), pair_with_sum(BST(ORDER), 100))
    t = BST(ORDER + [40])
    buggy_delete(t, 25)
    print(t.inorder())
    a, b = BST([25, 12, 47, 31]), BST([25, 12, 47, 31])
    a.delete(12); a.delete(25); b.delete(25); b.delete(12)
    print(shape(a), shape(b))
