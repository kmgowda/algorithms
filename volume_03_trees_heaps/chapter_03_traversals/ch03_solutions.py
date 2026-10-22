"""Volume 3, Chapter 3 - Tree Traversals: companion code for the Thinking Problems (Section 3.17).

Run:  python3 ch03_solutions.py
"""

from __future__ import annotations


def morris_inorder(root) -> list:
    """Thinking Problem 2: inorder in O(n) time with O(1) extra memory, no stack and no recursion.
    A temporary 'thread' from each node's predecessor back to the node replaces the stack; it is removed again,
    so the tree is unchanged at the end."""
    out, n = [], root
    while n is not None:
        if n.left is None:
            out.append(n.value)
            n = n.right
        else:
            p = n.left                                  # find n's predecessor: rightmost node on its left
            while p.right is not None and p.right is not n:
                p = p.right
            if p.right is None:                         # first visit: leave a thread back to n, go left
                p.right = n
                n = n.left
            else:                                       # second visit: the left side is done
                p.right = None
                out.append(n.value)
                n = n.right
    return out


def postorder_by_reversal(root) -> list:
    """Thinking Problem 3: the correct version. Preorder with the children swapped (node, right, left), reversed."""
    out, stack = [], [root] if root else []
    while stack:
        n = stack.pop()
        out.append(n.value)
        for c in (n.left, n.right):                     # right is pushed last, so it is popped first
            if c:
                stack.append(c)
    return out[::-1]


if __name__ == "__main__":
    from ch03_examples import from_array, preorder
    t = from_array([58, 25, 84, 12, 47, 70, 91])
    print(morris_inorder(t), preorder(t)[::-1], postorder_by_reversal(t))
