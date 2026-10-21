"""Volume 3, Chapter 21 - Every Sort Side by Side: all the sorts of Part II on the same data.

Run:  python3 ch21_examples.py
"""

from __future__ import annotations

import importlib.util
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


sel = _load("chapter_08_selection_sort", "ch08_examples")
ins = _load("chapter_09_insertion_sort", "ch09_examples")
bub = _load("chapter_10_bubble_and_shell_sort", "ch10_examples")
mer = _load("chapter_11_merge_sort", "ch11_examples")
qui = _load("chapter_12_quicksort", "ch12_examples")
pra = _load("chapter_13_quicksort_in_practice", "ch13_examples")
hea = _load("chapter_14_heapsort", "ch14_examples")
cnt = _load("chapter_16_counting_and_radix_sort", "ch16_examples")
tim = _load("chapter_18_stability_and_timsort", "ch18_examples")

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
    "Timsort (teaching)": ("yes", "no", "yes", "n log n"), "counting": ("yes", "no", "no", "n + k"),
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


if __name__ == "__main__":
    for k, v in run_all(PILE).items():
        print(k, v)
    rng = random.Random(1)
    for n in (2000, 20000):
        data = [rng.randrange(1_000_000) for _ in range(n)]
        r = run_all(data) if n == 2000 else run_all(data)
        print(n, r)
