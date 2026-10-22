"""Volume 4, Chapter 18 - Every Sort Side by Side: all the sorts of Part II on the same data.

Run:  python3 ch18_examples.py
"""

from __future__ import annotations

import importlib.util
import itertools
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.setrecursionlimit(20_000)


def _load(folder: str, module: str):
    spec = importlib.util.spec_from_file_location(f"v3_{module}", os.path.join(HERE, "..", folder, f"{module}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sel = _load("chapter_05_selection_sort", "ch05_examples")
ins = _load("chapter_06_insertion_sort", "ch06_examples")
bub = _load("chapter_07_bubble_and_shell_sort", "ch07_examples")
mer = _load("chapter_08_merge_sort", "ch08_examples")
qui = _load("chapter_09_quicksort", "ch09_examples")
pra = _load("chapter_10_quicksort_in_practice", "ch10_examples")
hea = _load("chapter_11_heapsort", "ch11_examples")
cnt = _load("chapter_13_counting_and_radix_sort", "ch13_examples")
tim = _load("chapter_15_stability_and_timsort", "ch15_examples")

PILE = [58, 25, 91, 12, 70, 47, 84, 31, 63]


def _with_counter(fn):
    def run(a):
        c = {"comparisons": 0}
        r = fn(a, c)
        return (r if isinstance(r, list) else a), c["comparisons"]
    return run


SORTS = {
    "selection": lambda a: (a, sel.selection_sort(a)["comparisons"]),
    "insertion": lambda a: (a, ins.insertion_sort(a)["comparisons"]),
    "bubble": lambda a: (a, bub.bubble_sort(a)["comparisons"]),
    "Shell": lambda a: (a, bub.shell_sort(a)["comparisons"]),
    "merge": _with_counter(lambda a, c: mer.merge_sort(a, c)),
    "quick (random pivot)": _with_counter(lambda a, c: pra.quicksort_random(a, counter=c)),
    "quick (practical)": _with_counter(lambda a, c: pra.quicksort_practical(a, counter=c)),
    "heap": _with_counter(lambda a, c: hea.heapsort(a, c)),
    "Timsort (teaching)": _with_counter(lambda a, c: tim.timsort(a, c)),
}

PROPERTIES = {  # stable, in place, adaptive, worst case
    "selection": ("no", "yes", "no", "n\u00b2"), "insertion": ("yes", "yes", "yes", "n\u00b2"),
    "bubble": ("yes", "yes", "yes", "n\u00b2"), "Shell": ("no", "yes", "partly", "about n^1.5"),
    "merge": ("yes", "no", "no", "n log n"), "quick (random pivot)": ("no", "yes", "no", "n\u00b2 (rare)"),
    "quick (practical)": ("no", "yes", "no", "n\u00b2 (very rare)"), "heap": ("no", "yes", "no", "n log n"),
    "Timsort (teaching)": ("yes", "no", "yes", "n^1.5 (full Timsort: n log n)"), "counting": ("yes", "no", "no", "n + k"),
}


def run_all(data: list) -> dict:
    """Comparisons and milliseconds for every comparison sort on the same data; each result checked."""
    out, want = {}, sorted(data)
    for name, fn in SORTS.items():
        a = list(data)
        t = time.perf_counter()
        res, comps = fn(a)
        ms = (time.perf_counter() - t) * 1e3
        assert res == want, name
        out[name] = (comps, round(ms, 1))
    a = list(data)
    t = time.perf_counter()
    if all(isinstance(x, int) and x >= 0 for x in data):
        assert cnt.counting_sort(a, max(data) if data else 0) == want
        out["counting"] = (0, round((time.perf_counter() - t) * 1e3, 1))
    t = time.perf_counter()
    sorted(data)
    out["sorted() built in"] = (None, round((time.perf_counter() - t) * 1e3, 1))
    return out


# ---------------------------------------------------------------- sorting networks (Section 18.6)

def odd_even_merge(lo: int, n: int, r: int, out: list) -> None:
    """Comparators merging the two sorted halves of wires lo .. lo + n - 1, looking at every r-th wire."""
    step = 2 * r
    if step < n:
        odd_even_merge(lo, n, step, out)          # the even-numbered wires
        odd_even_merge(lo + r, n, step, out)      # the odd-numbered wires
        for i in range(lo + r, lo + n - r, step):
            out.append((i, i + r))                # one last layer fixes neighbours
    else:
        out.append((lo, lo + r))


def odd_even_merge_sort(lo: int, n: int, out: list) -> None:
    """Batcher's odd-even merge sort on wires lo .. lo + n - 1 (n a power of two)."""
    if n > 1:
        half = n // 2
        odd_even_merge_sort(lo, half, out)
        odd_even_merge_sort(lo + half, half, out)
        odd_even_merge(lo, n, 1, out)


def sorting_network(n: int) -> list[tuple[int, int]]:
    """Batcher's network for any n >= 0: build it for the next power of two, then drop every comparator that
    touches a wire >= n (those wires would hold +infinity, which never moves)."""
    size = 1
    while size < n:
        size *= 2
    out: list[tuple[int, int]] = []
    odd_even_merge_sort(0, size, out)
    return [(i, j) for i, j in out if j < n]


def stages(network: list[tuple[int, int]]) -> list[list[tuple[int, int]]]:
    """Group the comparators into parallel stages: each goes in the first stage after the last one using its wires."""
    ready: dict[int, int] = {}
    layers: list[list[tuple[int, int]]] = []
    for i, j in network:
        t = max(ready.get(i, 0), ready.get(j, 0))
        if t == len(layers):
            layers.append([])
        layers[t].append((i, j))
        ready[i] = ready[j] = t + 1
    return layers


def apply_network(network: list[tuple[int, int]], a: list, counter: dict | None = None) -> list:
    """Run the items through the comparators in order; each comparator puts the smaller item on wire i < j."""
    a = list(a)
    for i, j in network:
        if counter is not None:
            counter["comparisons"] += 1
        if a[j] < a[i]:
            a[i], a[j] = a[j], a[i]
    return a


def sorts_all_01(network: list[tuple[int, int]], n: int) -> bool:
    """The 0-1 principle as a test: a network sorts every input if it sorts all 2**n inputs of 0s and 1s."""
    return all(apply_network(network, bits) == sorted(bits) for bits in itertools.product((0, 1), repeat=n))


def network_sort(a: list, counter: dict | None = None) -> list:
    """Sort with Batcher's network for len(a) wires (the network row of Figure 18.4)."""
    return apply_network(sorting_network(len(a)), a, counter)


SORTS["odd-even network"] = _with_counter(network_sort)


if __name__ == "__main__":
    for k, v in run_all(PILE).items():
        print(k, v)
    rng = random.Random(1)
    for n in (2000, 20000):
        data = [rng.randrange(1_000_000) for _ in range(n)]
        r = run_all(data) if n == 2000 else run_all(data)
        print(n, r)
