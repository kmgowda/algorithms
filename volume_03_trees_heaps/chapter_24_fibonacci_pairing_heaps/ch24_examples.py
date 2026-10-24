"""Volume 3, Chapter 24 - Fibonacci and Pairing Heaps.

A Fibonacci heap keeps a root list of heap-ordered trees. Insert and meld only add roots (Figure 24.2);
delete-min links roots of equal degree (consolidation, Figure 24.3); decrease-key cuts a node out and, through
marks, makes cascading cuts (Figure 24.4). With the potential Phi = t(H) + 2 m(H) (t roots, m marked nodes),
insert, meld, find-min and decrease-key cost O(1) amortized and delete-min O(log n) (Section 24.7). The degree
bound of Figure 24.5 is checked by `valid()` on every node: size(x) >= F(d + 2).

A pairing heap (Section 24.8, Figure 24.6) is one heap-ordered tree: meld links two roots, decrease-key cuts a
subtree and melds it back, and delete-min melds the root's children in two passes.

Children and roots are kept in Python dicts used as ordered sets, so a cut removes a node in O(1) and the order
in which children were linked is kept (oldest first) for the degree argument.

Run:  python3 ch24_examples.py
"""

from __future__ import annotations

import heapq
import math
import random

PHI = (1 + math.sqrt(5)) / 2


def fib(k: int) -> int:
    """Fibonacci numbers F(0) = 0, F(1) = 1, F(2) = 1, F(3) = 2, ..."""
    a, b = 0, 1
    for _ in range(k):
        a, b = b, a + b
    return a


def degree_bound(n: int) -> int:
    """D(n) = floor(log_phi n): no node of an n-item Fibonacci heap has more children than this."""
    return int(math.floor(math.log(n, PHI) + 1e-9)) if n > 0 else 0


# ---------------------------------------------------------------- Fibonacci heap

class FibNode:
    __slots__ = ("key", "item", "parent", "children", "mark")

    def __init__(self, key, item=None):
        self.key, self.item, self.parent, self.children, self.mark = key, item, None, {}, False

    @property
    def degree(self) -> int:
        return len(self.children)


class FibHeap:
    """Counters: links, cuts (every cut, including cascading ones), cascading (cuts made by the cascade),
    work (the actual cost of the last operation, in the units of Section 24.6)."""

    def __init__(self, keys=()):
        self.roots: dict = {}
        self.min = None
        self.n = 0
        self.marked = 0
        self.links = self.cuts = self.cascading = 0
        self.work = 0
        self.link_log = []                           # (child key, parent key) of every link, in order
        for k in keys:
            self.insert(k)

    def __len__(self) -> int:
        return self.n

    def potential(self) -> int:
        return len(self.roots) + 2 * self.marked

    def _add_root(self, x):
        x.parent = None
        if x.mark:                                   # roots are never marked
            x.mark = False
            self.marked -= 1
        self.roots[x] = None

    def insert(self, key, item=None):
        x = FibNode(key, item)
        self._add_root(x)                            # lazy: just one more root
        if self.min is None or key < self.min.key:
            self.min = x
        self.n += 1
        self.work = 1
        return x

    def find_min(self):
        return None if self.min is None else (self.min.key, self.min.item)

    def meld(self, other: "FibHeap") -> "FibHeap":
        """Move every root of other into this heap in O(1) work (Python's dict update copies the root list, a
        linked-list splice would not); other is left empty."""
        self.roots.update(other.roots)
        if other.min is not None and (self.min is None or other.min.key < self.min.key):
            self.min = other.min
        self.n += other.n
        self.marked += other.marked
        other.roots, other.min, other.n, other.marked = {}, None, 0, 0
        self.work = 1
        return self

    def _link(self, y, x):
        """Make root y a child of root x (x.key <= y.key)."""
        del self.roots[y]
        x.children[y] = None
        y.parent = x
        if y.mark:
            y.mark = False
            self.marked -= 1
        self.links += 1
        self.link_log.append((y.key, x.key))

    def consolidate(self):
        """Link roots of equal degree until all degrees differ (Figure 24.3)."""
        by_degree = {}                                     # degree -> the one root of that degree so far
        for x in list(self.roots):
            d = x.degree
            while d in by_degree:                          # another root has the same degree: link them
                y = by_degree.pop(d)
                if y.key < x.key:
                    x, y = y, x                            # x is the smaller root and stays a root
                self._link(y, x)
                d += 1
            by_degree[d] = x
        self.roots = {by_degree[d]: None for d in sorted(by_degree)}
        self.min = None
        for x in self.roots:
            if self.min is None or x.key < self.min.key:
                self.min = x

    def delete_min(self):
        z = self.min
        if z is None:
            raise IndexError("delete_min from an empty heap")
        for c in list(z.children):                   # every child of the minimum becomes a root
            self._add_root(c)
        z.children = {}
        del self.roots[z]
        self.n -= 1
        self.work = len(self.roots)                  # roots examined by consolidation (links included)
        self.consolidate()
        return z.key, z.item

    def _cut(self, x):
        """Move x, with its subtree, from its parent's child list to the root list."""
        del x.parent.children[x]
        self._add_root(x)
        self.cuts += 1

    def decrease_key(self, x, key):
        if key > x.key:
            raise ValueError("decrease_key cannot raise a key")
        x.key = key
        p = x.parent
        before = self.cuts
        if p is not None and x.key < p.key:      # heap order broken: cut x out
            self._cut(x)
            self._cascade(p)
        if x.key < self.min.key:
            self.min = x
        self.work = 1 + self.cuts - before

    def _cascade(self, y):
        while y.parent is not None:              # roots are never marked
            if not y.mark:                       # y loses its first child: mark it
                y.mark = True
                self.marked += 1
                return
            p = y.parent                         # y loses a second child: cut it too
            self._cut(y)
            self.cascading += 1
            y = p

    def delete(self, x):
        """Remove any node: cut it to the root list (with the cascade), make it the minimum, delete-min."""
        if x.parent is not None:
            p = x.parent
            self._cut(x)
            self._cascade(p)
        self.min = x
        return self.delete_min()

    # ------------------------------------------------------------ inspection

    def nodes(self):
        stack = list(self.roots)
        while stack:
            x = stack.pop()
            yield x
            stack.extend(x.children)

    def forest(self):
        """The root list as nested shapes (key, marked, [children oldest first])."""
        def shape(x):
            return (x.key, x.mark, [shape(c) for c in x.children])
        return [shape(r) for r in self.roots]

    def max_degree(self) -> int:
        return max((x.degree for x in self.nodes()), default=0)

    def valid(self) -> bool:
        """Heap order, parent links, unmarked roots, mark count, size, min pointer, and the degree bound
        size(x) >= F(degree + 2) at every node."""
        count, marks = 0, 0

        def size(x):
            nonlocal count, marks
            count += 1
            marks += x.mark
            s = 1
            for c in x.children:
                if c.parent is not x or c.key < x.key:
                    raise AssertionError("heap order or parent link broken")
                s += size(c)
            if s < fib(x.degree + 2):
                raise AssertionError("degree bound broken")
            return s
        try:
            for r in self.roots:
                if r.parent is not None or r.mark:
                    return False
                size(r)
        except AssertionError:
            return False
        if count != self.n or marks != self.marked:
            return False
        if self.n == 0:
            return self.min is None
        return self.min in self.roots and all(self.min.key <= r.key for r in self.roots)


# ---------------------------------------------------------------- pairing heap

class PairNode:
    __slots__ = ("key", "item", "parent", "children")

    def __init__(self, key, item=None):
        self.key, self.item, self.parent, self.children = key, item, None, {}


class PairingHeap:
    """One heap-ordered tree; children are kept oldest first, so the newest child is the last one."""

    def __init__(self, keys=()):
        self.root = None
        self.n = 0
        self.links = 0
        self.passes = []                             # after each delete-min: (keys after pass 1, final root)
        for k in keys:
            self.insert(k)

    def __len__(self) -> int:
        return self.n

    def _link(self, a, b):
        """Meld two trees: the larger root becomes the newest child of the smaller (ties keep a on top)."""
        if a is None:
            return b
        if b is None:
            return a
        if b.key < a.key:
            a, b = b, a
        a.children[b] = None
        b.parent = a
        self.links += 1
        return a

    def insert(self, key, item=None):
        x = PairNode(key, item)
        self.root = self._link(self.root, x)
        self.n += 1
        return x

    def find_min(self):
        return None if self.root is None else (self.root.key, self.root.item)

    def meld(self, other: "PairingHeap") -> "PairingHeap":
        self.root = self._link(self.root, other.root)
        self.n += other.n
        other.root, other.n = None, 0
        return self

    def delete_min(self):
        z = self.root
        if z is None:
            raise IndexError("delete_min from an empty heap")
        kids = list(z.children)[::-1]            # newest child first
        for c in kids:
            c.parent = None
        pairs = [self._link(kids[i], kids[i + 1] if i + 1 < len(kids) else None)
                 for i in range(0, len(kids), 2)]                    # pass 1: link pairs, left to right
        root = None
        for t in reversed(pairs):                                    # pass 2: meld right to left
            root = self._link(t, root)
        self.root = root
        self.n -= 1
        self.passes.append(([t.key for t in pairs], None if root is None else root.key))
        return z.key, z.item

    def decrease_key(self, x, key):
        if key > x.key:
            raise ValueError("decrease_key cannot raise a key")
        x.key = key
        if x.parent is not None:                 # cut x's subtree and meld it with the root
            del x.parent.children[x]
            x.parent = None
            self.root = self._link(self.root, x)

    def shape(self):
        def s(x):
            return (x.key, [s(c) for c in x.children])
        return None if self.root is None else s(self.root)

    def valid(self) -> bool:
        if self.root is None:
            return self.n == 0
        count, stack = 0, [self.root]
        if self.root.parent is not None:
            return False
        while stack:
            x = stack.pop()
            count += 1
            for c in x.children:
                if c.parent is not x or c.key < x.key:
                    return False
                stack.append(c)
        return count == self.n


# ---------------------------------------------------------------- Dijkstra with three heaps

def dijkstra(adj: dict, start, heap_class=FibHeap):
    """Shortest distances with a heap that offers decrease-key; returns (dist, counts)."""
    heap, handle, dist, done = heap_class(), {}, {start: 0}, set()
    counts = {"insert": 1, "delete_min": 0, "decrease_key": 0}
    handle[start] = heap.insert(0, start)
    while len(heap):
        d, u = heap.delete_min()
        counts["delete_min"] += 1
        done.add(u)
        for v, w in adj[u]:
            if v in done:
                continue
            if v not in dist:
                dist[v] = d + w
                handle[v] = heap.insert(d + w, v)
                counts["insert"] += 1
            elif d + w < dist[v]:
                dist[v] = d + w
                heap.decrease_key(handle[v], d + w)      # one reservation upgraded in place
                counts["decrease_key"] += 1
    return dist, counts


def dijkstra_heapq(adj: dict, start):
    """Volume 5, Chapter 2's lazy deletion: push a new entry on every improvement, skip stale ones."""
    dist, done, heap = {start: 0}, set(), [(0, start)]
    counts = {"push": 1, "pop": 0, "stale": 0, "largest heap": 1}
    while heap:
        d, u = heapq.heappop(heap)
        counts["pop"] += 1
        if u in done:
            counts["stale"] += 1
            continue
        done.add(u)
        for v, w in adj[u]:
            if v not in done and d + w < dist.get(v, math.inf):
                dist[v] = d + w
                heapq.heappush(heap, (d + w, v))
                counts["push"] += 1
                counts["largest heap"] = max(counts["largest heap"], len(heap))
    return dist, counts


def random_graph(n: int, m: int, seed: int = 1, max_w: int = 100) -> dict:
    """A connected directed graph: a random spanning path from 0, then random roads up to m in all."""
    rng = random.Random(seed)
    adj = {v: [] for v in range(n)}
    order = list(range(1, n))
    rng.shuffle(order)
    prev, edges = 0, 0
    for v in order:
        adj[prev].append((v, rng.randint(1, max_w)))
        prev, edges = v, edges + 1
    while edges < m:
        a, b = rng.randrange(n), rng.randrange(n)
        if a != b:
            adj[a].append((b, rng.randint(1, max_w)))
            edges += 1
    return adj


def dijkstra_report(n: int = 10_000, m: int = 100_000, seed: int = 1) -> dict:
    """Operation counts of the three heaps on one random graph (Section 24.9); all three distances agree."""
    adj = random_graph(n, m, seed)
    made = []

    def make(cls):
        made.append(cls())
        return made[-1]
    dist_f, out_f = dijkstra(adj, 0, lambda: make(FibHeap))
    dist_p, out_p = dijkstra(adj, 0, lambda: make(PairingHeap))
    dist_q, out_q = dijkstra_heapq(adj, 0)
    assert dist_f == dist_p == dist_q
    fh, ph = made
    out_f.update(links=fh.links, cuts=fh.cuts, cascading=fh.cascading)
    out_p.update(links=ph.links)
    return {"fibonacci": out_f, "pairing": out_p, "heapq": out_q}


# ---------------------------------------------------------------- the chapter's running example

BRANCH_A = [58, 25, 91, 12, 70]          # Main branch reservations (priority numbers: smaller = more urgent)
BRANCH_B = [47, 84, 31, 63]              # Harbour branch


def reservation_story():
    """Meld the two branch lists, serve the most urgent, then upgrade two readers (Figures 24.2-24.4).
    Returns the forests after each step and the counters."""
    a, b = FibHeap(), FibHeap()
    na = {k: a.insert(k) for k in BRANCH_A}
    nb = {k: b.insert(k) for k in BRANCH_B}
    nodes = na | nb
    a.meld(b)
    steps = [("meld", a.forest(), a.potential())]
    a.delete_min()
    steps.append(("delete-min", a.forest(), a.potential()))
    a.decrease_key(nodes[63], 20)                  # a teacher's request: 63 -> 20; its parent 31 is marked
    steps.append(("63 -> 20", a.forest(), a.potential()))
    a.decrease_key(nodes[47], 15)                  # 47 -> 15: cut 47, and the marked 31 is cut too (cascade)
    steps.append(("47 -> 15", a.forest(), a.potential()))
    return steps, a


def heap_sort_with(cls, keys):
    h = cls()
    for k in keys:
        h.insert(k)
    return [h.delete_min()[0] for _ in range(len(keys))]


def degree_experiment(n: int = 2000, ops: int = 20_000, seed: int = 3):
    """A seeded random workload of inserts, delete-mins and decrease-keys. Every 100 operations, record the
    largest degree and the heap size. Returns the worst (largest degree, size, floor(log_phi size))."""
    rng = random.Random(seed)
    h, live, where = FibHeap(), [], {}                  # live nodes, and each node's place in the list

    def add(key):
        x = h.insert(key)
        where[x] = len(live)
        live.append(x)
    for _ in range(n):
        add(rng.randrange(10**9))
    worst = (0, 0, 0)
    for step in range(ops):
        r = rng.random()
        if r < 0.3 or not live:
            add(rng.randrange(10**9))
        elif r < 0.5:
            z = h.min
            h.delete_min()
            i, last = where.pop(z), live.pop()           # swap the last node into z's place
            if last is not z:
                live[i], where[last] = last, i
        else:
            x = live[rng.randrange(len(live))]
            h.decrease_key(x, x.key - rng.randrange(10**8))
        if step % 100 == 0 and len(h):
            worst = max(worst, (h.max_degree(), len(h), degree_bound(len(h))))
    return worst


# Leftist and skew heaps (Section 24.9): a heap is None or a tuple (key, left, right[, rank])

def leftist_meld(a, b):
    """Meld two leftist heaps (key, left, right, rank). Rank = length of the rightmost path; every node keeps its
    left child's rank at least its right child's, so the right spine has at most log2(n + 1) nodes."""
    if a is None:
        return b
    if b is None:
        return a
    if b[0] < a[0]:
        a, b = b, a
    key, left, right, _ = a
    right = leftist_meld(right, b)
    rank = lambda h: h[3] if h else 0
    if rank(left) < rank(right):
        left, right = right, left
    return (key, left, right, rank(right) + 1)


def skew_meld(a, b):
    """Meld two skew heaps (key, left, right): like leftist, but always swap the children, keeping no ranks.
    O(log n) amortized (Sleator and Tarjan, 1986)."""
    if a is None:
        return b
    if b is None:
        return a
    if b[0] < a[0]:
        a, b = b, a
    key, left, right = a
    return (key, skew_meld(right, b), left)


def meld_sort(meld, items: list, leaf) -> list:
    """Insert every item by melding a one-node heap, then pop the minimum (meld the root's two children)."""
    h = None
    for x in items:
        h = meld(h, leaf(x))
    out = []
    while h is not None:
        out.append(h[0])
        h = meld(h[1], h[2])
    return out


def right_spine(h) -> int:
    n = 0
    while h is not None:
        n, h = n + 1, h[2]
    return n


if __name__ == "__main__":
    steps, h = reservation_story()
    for name, forest, phi in steps:
        print(f"{name:12s} Phi={phi:2d}  {forest}")
    print("links", h.links, "cuts", h.cuts, "cascading", h.cascading)
    print("pairing passes on the shelf:")
    p = PairingHeap([58, 25, 91, 12, 70, 47, 84, 31, 63])
    print(p.shape())
    p.delete_min()
    print(p.passes[-1], p.shape())
    print(dijkstra_report())
