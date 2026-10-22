"""Volume 3, Chapter 27 - Part III Side by Side.

The structures of Chapters 22-26 run on the same inputs as their classical rivals:
- a red-black tree (Chapter 8), a splay tree (Chapter 22) and a treap (Chapter 23) on the same keys and the same
  request sequences (Figures 27.1-27.3);
- the per-operation costs behind the three kinds of promise: worst case, amortized and expected (Figure 27.2);
- interval and k-d trees against a plain scan (Figure 27.4);
- the edge workloads of Section 27.8 (Figure 27.5).
Every comparison count is "nodes looked at": a search that finds its key at depth d makes d + 1 comparisons.

Run:  python3 ch27_examples.py
"""

from __future__ import annotations

import importlib.util
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(folder, module):
    path = os.path.join(os.path.dirname(HERE), folder, module + ".py")
    spec = importlib.util.spec_from_file_location(f"ch27_uses_{folder}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


rb = _load("chapter_08_red_black", "ch08_examples")
sp = _load("chapter_22_splay_trees", "ch22_examples")
tr = _load("chapter_23_treaps", "ch23_examples")
fh = _load("chapter_24_fibonacci_pairing_heaps", "ch24_examples")
it = _load("chapter_25_interval_trees", "ch25_examples")
kd = _load("chapter_26_kd_trees", "ch26_examples")

SHELF = [12, 25, 31, 47, 58, 63, 70, 84, 91]
ROLLS = tr.ROLLS                                    # the dice of Figure 23.1
REQUESTS = [12, 12, 12, 91, 47, 47, 47, 47, 63, 12]  # a morning at the desk (Figure 27.2)


def depth_of(root, key) -> int:
    """Depth of key in any binary search tree with .key/.left/.right, by a plain search (no changes)."""
    n, d = root, 0
    while n is not None and n.key != key:
        n, d = (n.left if key < n.key else n.right), d + 1
    if n is None:
        raise KeyError(key)
    return d


class Static:
    """A red-black tree or a treap: searching never changes the shape."""

    def __init__(self, tree):
        self.tree = tree

    def search_cost(self, key) -> int:
        return depth_of(self.tree.root, key) + 1


class Splay:
    """A splay tree: the cost is the depth before the splay, plus one; then the key moves to the root."""

    def __init__(self, tree):
        self.tree = tree

    def search_cost(self, key) -> int:
        c = depth_of(self.tree.root, key) + 1
        self.tree.search(key)
        return c


def three_trees(keys, priorities=None, seed=1):
    """The three rivals, each built by inserting keys in the given order."""
    return {"red-black": Static(rb.RedBlackTree(keys)),
            "splay": Splay(sp.SplayTree(keys)),
            "treap": Static(tr.Treap(keys, priorities=priorities, seed=seed))}


def cost_strips(keys=SHELF, requests=REQUESTS):
    """Figure 27.2: per-request comparisons on the shelf loaded in sorted order (treap with the printed rolls)."""
    trees = three_trees(sorted(keys), priorities=ROLLS)
    return {name: [t.search_cost(k) for k in requests] for name, t in trees.items()}


def sorted_load_shapes(keys=SHELF):
    """Figure 27.1: the shapes and heights after loading the shelf in increasing order."""
    bst = tr.plain_bst_shape(sorted(keys))
    r, s, t = rb.RedBlackTree(sorted(keys)), sp.SplayTree(sorted(keys)), tr.Treap(sorted(keys), priorities=ROLLS)
    return {"plain BST": (bst, len(keys) - 1), "red-black": (r.shape(), r.height()),
            "splay": (s.shape(), s.height()), "treap": (t.shape(), t.height())}


def workloads(n: int = 10_000, m: int = 20_000, seed: int = 1, hot: float = 0.9):
    """Figure 27.3: average comparisons per search on n shuffled keys for three request patterns.
    uniform: m random keys; hot: a share `hot` of m requests goes to 10 popular keys; sequential: 0, 1, ..., n-1."""
    rng = random.Random(seed)
    keys = list(range(n))
    rng.shuffle(keys)
    popular = rng.sample(keys, 10)
    patterns = {"uniform": [rng.randrange(n) for _ in range(m)],
                "hot": [rng.choice(popular) if rng.random() < hot else rng.randrange(n) for _ in range(m)],
                "sequential": list(range(n))}
    out = {}
    for name, reqs in patterns.items():
        trees = three_trees(keys, seed=seed)
        out[name] = {t: sum(tree.search_cost(k) for k in reqs) / len(reqs) for t, tree in trees.items()}
    return out


def hot_split(n: int = 10_000, m: int = 20_000, seed: int = 1, hot: float = 0.9):
    """Challenge 1: the splay tree's hot workload of Figure 27.3, split into requests for the 10 popular keys and
    the rest. Returns ((average comparisons, count) for hot requests, (the same) for the others)."""
    rng = random.Random(seed)
    keys = list(range(n))
    rng.shuffle(keys)
    popular = rng.sample(keys, 10)
    [rng.randrange(n) for _ in range(m)]                 # the uniform pattern, drawn first as in workloads()
    reqs = [(rng.choice(popular), True) if rng.random() < hot else (rng.randrange(n), False) for _ in range(m)]
    t = Splay(sp.SplayTree(keys))
    sums = {True: [0, 0], False: [0, 0]}
    for k, is_hot in reqs:
        sums[is_hot][0] += t.search_cost(k)
        sums[is_hot][1] += 1
    return tuple((sums[h][0] / sums[h][1], sums[h][1]) for h in (True, False))


def sorted_heights(n: int = 1000, seed: int = 1) -> dict:
    """Heights after loading 1..n in increasing order."""
    keys = list(range(1, n + 1))
    trees = {"red-black": rb.RedBlackTree(keys), "splay": sp.SplayTree(keys), "treap": tr.Treap(keys, seed=seed)}
    return {name: max(tr.node_depths(t.root)) for name, t in trees.items()}


def space_and_time(seed: int = 1) -> dict:
    """Figure 27.4: nodes looked at by one query, against a scan of every item."""
    m = it.measure(1000, seed=seed)
    return {"interval: one overlap": (m["find_one"], m["n"]), "interval: all k overlaps": (m["all"], m["n"]),
            "k": m["k"], "k-d nearest, d = 2": (kd.nearest_cost(10_000, 2, seed=seed), 10_000),
            "k-d nearest, d = 16": (kd.nearest_cost(10_000, 16, seed=seed), 10_000)}


def edge_cases():
    """Section 27.8: the smallest and most lopsided workloads, on all three trees."""
    out = {}
    empty = three_trees([])
    out["empty: search 5"] = {n: (t.tree.root is None) for n, t in empty.items()}
    one = three_trees([7], priorities={7: 1})
    out["one key: search it"] = {n: t.search_cost(7) for n, t in one.items()}
    five = three_trees([1, 2, 3, 4, 5], priorities={1: 50, 2: 90, 3: 70, 4: 20, 5: 60})
    out["sorted load of 5, search 1"] = {n: t.search_cost(1) for n, t in five.items()}
    out["then search 1 again"] = {n: t.search_cost(1) for n, t in five.items()}
    return out


def fib_insert_then_delete_min(n: int):
    """Thinking Problem 3: n inserts, then one delete-min. Returns (links made by that delete-min, roots left)."""
    h = fh.FibHeap()
    for k in range(1, n + 1):
        h.insert(k)
    before = h.links
    h.delete_min()
    return h.links - before, len(h.roots)


if __name__ == "__main__":
    for name, (shape, height) in sorted_load_shapes().items():
        print(f"{name:10s} height {height}")
    print("cost strips:", cost_strips())
    print("1,000 sorted keys, heights:", sorted_heights())
    for pattern, row in workloads().items():
        print(pattern, {k: round(v, 2) for k, v in row.items()})
    print(space_and_time())
    print(edge_cases())
    print("Fibonacci heap, 1,024 inserts then delete-min:", fib_insert_then_delete_min(1024))
