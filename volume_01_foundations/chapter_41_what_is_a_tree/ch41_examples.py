"""Volume 1, Chapter 41 - What Is a Tree?

Run:  python3 ch41_examples.py
"""

from __future__ import annotations

SECTIONS = {"Library": ["Fiction", "Science", "History"], "Fiction": ["Mystery", "Fantasy"],
            "Science": ["Physics", "Biology", "Maths"], "History": ["Ancient"], "Maths": ["Algebra", "Geometry"]}


def parents(children: dict) -> dict:
    """Map each node to its single parent (one pass over the children lists)."""
    return {kid: p for p, kids in children.items() for kid in kids}


def path_from_root(children: dict, node) -> list:
    """Walk up through parents to the root, then reverse (Section 41.8): O(depth)."""
    up, path = parents(children), [node]
    while path[-1] in up:
        path.append(up[path[-1]])
    return path[::-1]


def height(children: dict, root) -> int:
    """One more than the tallest subtree; a leaf has height 0."""
    kids = children.get(root, [])
    return 0 if not kids else 1 + max(height(children, k) for k in kids)


def leaves(children: dict, root) -> list:
    kids = children.get(root, [])
    return [root] if not kids else [leaf for k in kids for leaf in leaves(children, k)]


def max_nodes(h: int) -> int:
    """Most nodes a binary tree of height h can hold: 2^(h+1) - 1."""
    return 2 ** (h + 1) - 1


if __name__ == "__main__":
    print(path_from_root(SECTIONS, "Geometry"), height(SECTIONS, "Library"), leaves(SECTIONS, "Library"))
    print([max_nodes(h) for h in (3, 4, 9, 19)])
