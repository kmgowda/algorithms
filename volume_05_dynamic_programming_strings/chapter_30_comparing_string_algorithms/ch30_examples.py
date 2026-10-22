"""Volume 5, Chapter 30 - Every String Algorithm Side by Side: the same searches, every method, counted.

Run:  python3 ch30_examples.py
"""

from __future__ import annotations

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(folder: str, name: str):
    spec = importlib.util.spec_from_file_location(name + "_v5", os.path.join(HERE, "..", folder, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


naive = _load("chapter_17_searching_text", "ch17_examples")
kmp = _load("chapter_18_kmp", "ch18_examples")
rk = _load("chapter_19_rabin_karp", "ch19_examples")
zalg = _load("chapter_20_z_algorithm", "ch20_examples")
bmh = _load("chapter_21_boyer_moore_horspool", "ch21_examples")
ac = _load("chapter_22_aho_corasick", "ch22_examples")
sa = _load("chapter_23_suffix_arrays", "ch23_examples")


def all_methods(text: str, pattern: str) -> dict:
    """Positions found by every single-pattern method (they must agree) and the work each reports."""
    s = sa.suffix_array_doubling(text)[0]
    results = {
        "naive": naive.naive_search(text, pattern),
        "Knuth-Morris-Pratt": kmp.kmp_search(text, pattern),
        "Rabin-Karp": rk.rabin_karp(text, pattern)[:2],
        "Z-algorithm": (zalg.z_search(text, pattern), zalg.z_array(pattern + "\0" + text)[1] if pattern else 0),
        "Horspool": bmh.horspool(text, pattern)[:2],
        "Boyer-Moore": bmh.boyer_moore(text, pattern)[:2],
        "Aho-Corasick": (sorted(i for i, _ in ac.search(text, [pattern])[0]), ac.search(text, [pattern])[1]),
        "suffix array": sa.find_all(text, s, pattern),
    }
    return results


def workloads(seed: int = 30) -> dict:
    """The three shared tasks of Part II; the random text is the same one Chapters 17, 19 and 21 use."""
    random_text = naive.random_text(10000, seed)
    return {"random text, 'library'": (random_text, "library"), "1,000 a's, 'aaaaaaaaab'": ("a" * 1000, "a" * 9 + "b"),
            "1,000 a's, 'baaaaaaaaa'": ("a" * 1000, "b" + "a" * 9)}


if __name__ == "__main__":
    for name, (t, p) in workloads().items():
        res = all_methods(t, p)
        assert len({tuple(v[0]) for v in res.values()}) == 1
        print(name, {k: v[1] for k, v in res.items()})
