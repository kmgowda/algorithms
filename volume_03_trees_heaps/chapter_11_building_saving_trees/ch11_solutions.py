"""Volume 3, Chapter 11 - Building and Saving Trees: companion code for the Thinking Problems (Section 11.16).

Run:  python3 ch11_solutions.py
"""

from __future__ import annotations

from ch11_examples import Node


def from_pre_post_full(pre: list, post: list):
    """Thinking Problem 1: rebuild a full binary tree (every node has 0 or 2 children, distinct values)
    from its preorder and postorder."""
    where = {v: i for i, v in enumerate(post)}

    def build(p0, q0, n):                         # pre[p0:p0+n] and post[q0:q0+n] describe one subtree
        if n == 0:
            return None
        node = Node(pre[p0])
        if n > 1:
            left_size = where[pre[p0 + 1]] - q0 + 1   # the left child ends the left subtree's postorder
            node.left = build(p0 + 1, q0, left_size)
            node.right = build(p0 + 1 + left_size, q0 + left_size, n - 1 - left_size)
        return node
    return build(0, 0, len(pre))


def bst_from_preorder(pre: list):
    """Thinking Problem 2: rebuild a search tree from its preorder alone in O(n). Each call takes the next
    key only if it lies inside the range (lo, hi) that its subtree allows."""
    i = 0

    def build(lo, hi):
        nonlocal i
        if i == len(pre) or not lo < pre[i] < hi:
            return None
        node = Node(pre[i])
        i += 1
        node.left = build(lo, node.value)
        node.right = build(node.value, hi)
        return node
    root = build(float("-inf"), float("inf"))
    if i != len(pre):
        raise ValueError("not the preorder of a search tree with distinct keys")
    return root


def count_only(text: str) -> bool:
    """Thinking Problem 3: the wrong check, 'one more # than values'."""
    toks = text.split()
    return toks.count("#") == len(toks) - toks.count("#") + 1


if __name__ == "__main__":
    from ch11_examples import complete, save, preorder
    print(save(from_pre_post_full([1, 2, 4, 5, 3], [4, 5, 2, 3, 1])))
    print(save(bst_from_preorder([8, 3, 1, 6, 10, 14])))
    for line in ["# 5 #", "5 # # # 7", "58 25 12 # # 47 # # 84 # 91 # #"]:
        print(line, count_only(line), complete(line))
    print(preorder(bst_from_preorder([58, 25, 12, 47, 84, 91])))
