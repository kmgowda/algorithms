"""Volume 13, Chapter 10 - The Big Comparison: Every String Matcher Side by Side.

The matchers are loaded from the earlier chapter folders, so the race uses exactly the code from the book.

Run:  python3 ch10_examples.py
"""

from __future__ import annotations

import importlib.util
import random
import timeit
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def load(folder: str, module: str):
    """Import chNN_examples.py from a sibling chapter folder under a unique name."""
    spec = importlib.util.spec_from_file_location(f"v13_{module}", HERE / folder / f"{module}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)                          # type: ignore[union-attr]
    return mod


naive = load("chapter_02_naive_matching", "ch02_examples")
rk = load("chapter_03_rabin_karp", "ch03_examples")
kmp = load("chapter_04_kmp", "ch04_examples")
zbm = load("chapter_05_z_boyer_moore", "ch05_examples")
dfa = load("chapter_06_finite_automata", "ch06_examples")
ac = load("chapter_07_tries_aho_corasick", "ch07_examples")
sa = load("chapter_08_suffix_arrays", "ch08_examples")


def matchers() -> dict[str, callable]:
    """Every single-pattern matcher, each returning the list of occurrences."""
    return {
        "naive": lambda t, p: naive.naive_search(t, p)[0],
        "Rabin-Karp": lambda t, p: rk.rabin_karp(t, p)[0],
        "KMP": lambda t, p: kmp.kmp_search(t, p)[0],
        "Z": zbm.z_search,
        "Horspool": lambda t, p: zbm.horspool(t, p)[0],
        "automaton": lambda t, p: dfa.dfa_search(t, p, "".join(sorted(set(t + p)))),
        "Aho-Corasick": lambda t, p: [i for i, _ in ac.AhoCorasick([p]).search(t)],
        "suffix array": lambda t, p: sa.find_all(t, sa.suffix_array(t), p),
        "str.find": find_all_builtin,
    }


def find_all_builtin(text: str, pattern: str) -> list[int]:
    """Python's C-coded search, repeated for every occurrence (Chapter 1)."""
    out, i = [], text.find(pattern)
    while i != -1:
        out.append(i)
        i = text.find(pattern, i + 1)
    return out


def texts(n: int, seed: int = 0) -> dict[str, tuple[str, str]]:
    rng = random.Random(seed)
    english = zbm.english_like(n, seed)
    dna = "".join(rng.choice("ACGT") for _ in range(n))
    return {
        "English-like, long pattern": (english, "the lazy dog near the river"),
        "random DNA, 12 letters": (dna, dna[n // 2:n // 2 + 12]),
        "repetitive worst case": ("a" * n, "a" * 29 + "b"),
    }


def race(n: int = 20000) -> dict[str, dict[str, float]]:
    """Milliseconds for each matcher on each kind of text (best of 3)."""
    out: dict[str, dict[str, float]] = {}
    for label, (t, p) in texts(n).items():
        out[label] = {name: min(timeit.repeat(lambda f=f: f(t, p), number=1, repeat=3)) * 1000
                      for name, f in matchers().items()}
        index = sa.suffix_array(t)                         # built once, outside the timing
        out[label]["suffix array, query only"] = min(timeit.repeat(lambda: sa.find_all(t, index, p), number=1, repeat=3)) * 1000
    return out


def choose_matcher(features: set[str]) -> str:
    """The decision guide for Volume 13."""
    if "many patterns" in features:
        return "Aho-Corasick"
    if "one text, many queries" in features:
        return "suffix array"
    if "palindromes" in features:
        return "Manacher"
    if "stream or guaranteed linear time" in features:
        return "KMP"
    if "long pattern, varied text" in features:
        return "Boyer-Moore-Horspool"
    if "same-length patterns or document fingerprints" in features:
        return "Rabin-Karp"
    return "built-in str.find"


if __name__ == "__main__":
    for label, row in race().items():
        print(label)
        for name, ms in sorted(row.items(), key=lambda kv: kv[1]):
            print(f"   {name:<25} {ms:8.3f} ms")
    print(choose_matcher({"many patterns"}))
