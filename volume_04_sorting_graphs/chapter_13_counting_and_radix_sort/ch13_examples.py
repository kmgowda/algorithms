"""Volume 4, Chapter 13 - Counting Sort and Radix Sort: sorting without comparing.

Run:  python3 ch13_examples.py
"""

from __future__ import annotations

import random
import time

PILE = [58, 25, 91, 12, 70, 47, 84, 31, 63]
GRADES = [3, 1, 4, 1, 5, 2, 4, 3, 1, 5, 2, 4]            # books borrowed by twelve readers (0..5)


def counting_sort(a: list, k: int, key=lambda x: x) -> list:
    """Stable counting sort of items whose key is 0..k (Figure 13.2): count, running total, place from the right."""
    count = [0] * (k + 1)
    for x in a:
        count[key(x)] += 1
    for v in range(1, k + 1):
        count[v] += count[v - 1]                      # count[v] = how many keys are <= v: the group ends
    out = [None] * len(a)
    for x in reversed(a):                             # right to left keeps equal keys in order: stable
        count[key(x)] -= 1
        out[count[key(x)]] = x
    return out


def group_ends(a: list, k: int, key=lambda x: x) -> tuple[list, list]:
    """The counts and the running totals (group ends) that counting sort computes (Figures 13.1 and 13.2)."""
    count = [0] * (k + 1)
    for x in a:
        count[key(x)] += 1
    ends = list(count)
    for v in range(1, k + 1):
        ends[v] += ends[v - 1]
    return count, ends


def radix_sort(a: list, digits: int, base: int = 10, passes: list | None = None) -> list:
    """Least-significant-digit radix sort: one stable counting sort per digit (Figure 13.4)."""
    for d in range(digits):
        div = base ** d
        a = counting_sort(a, base - 1, key=lambda x: (x // div) % base)
        if passes is not None:
            passes.append(list(a))
    return a


def counting_sort_unstable(a: list, k: int, key=lambda x: x) -> list:
    """A broken variant for Section 13.5: it fills each group from its END while walking from the LEFT, so equal
    keys come out reversed. Sorted by key, but not stable."""
    count = [0] * (k + 1)
    for x in a:
        count[key(x)] += 1
    for v in range(1, k + 1):
        count[v] += count[v - 1]
    out = [None] * len(a)
    for x in a:
        count[key(x)] -= 1
        out[count[key(x)]] = x
    return out


def radix_sort_unstable(a: list, digits: int, base: int = 10) -> list:
    """LSD radix sort built on the unstable pass: shows why stability is the step the proof needs."""
    for d in range(digits):
        div = base ** d
        a = counting_sort_unstable(a, base - 1, key=lambda x: (x // div) % base)
    return a


def sorted_by_last_digits(a: list, t: int, base: int = 10) -> bool:
    """The invariant of Section 13.5: is a in order when each key is cut down to its last t digits?"""
    m = base ** t
    return all(a[i] % m <= a[i + 1] % m for i in range(len(a) - 1))


def step_counts(n: int, k: int, digits: int, base: int = 10) -> dict:
    """Basic steps (reads and writes of one item or one counter) for each method, against comparisons for a
    comparison sort (Section 13.6)."""
    import math
    return {"counting sort": 2 * n + 2 * (k + 1), "radix sort": digits * (2 * n + 2 * base),
            "comparison sort (about n log2 n)": round(n * math.log2(n)) if n > 1 else 0}


def counting_sort_any(a: list) -> list:
    """Section 13.7: counting sort for any whole numbers, including negatives, by shifting keys to start at 0."""
    if not a:
        return []
    lo, hi = min(a), max(a)
    return counting_sort(a, hi - lo, key=lambda x: x - lo)


def timing(n: int = 1_000_000, seed: int = 1) -> dict:
    rng = random.Random(seed)
    small = [rng.randint(0, 100) for _ in range(n)]
    six = [rng.randint(0, 999_999) for _ in range(n)]
    out = {}
    t = time.perf_counter(); counting_sort(small, 100); out["counting, keys 0-100"] = (time.perf_counter() - t) * 1e3
    t = time.perf_counter(); radix_sort(six, 6); out["radix, 6-digit keys"] = (time.perf_counter() - t) * 1e3
    t = time.perf_counter(); sorted(small); out["sorted(), keys 0-100"] = (time.perf_counter() - t) * 1e3
    t = time.perf_counter(); sorted(six); out["sorted(), 6-digit keys"] = (time.perf_counter() - t) * 1e3
    return {k: round(v) for k, v in out.items()}


TITLES = ["maps", "map", "mars", "atlas", "art", "maze", "arts", "ant", "mat"]   # Section 13.6


def lsd_strings(words: list, width: int) -> list:
    """Sort strings that all have the same length by counting sort on each position, last to first."""
    for pos in range(width - 1, -1, -1):
        words = counting_sort(words, 256, key=lambda w: ord(w[pos]))
    return words


def msd_strings(words: list, pos: int = 0, looks: list | None = None) -> list:
    """Most significant digit first: split by the letter at pos (words that have ended go first), then sort each
    group on the next letter. Words of any length; each letter is looked at only while it still matters."""
    if len(words) <= 1:
        return list(words)
    ended, groups = [], {}
    for w in words:
        if looks is not None:
            looks[0] += 1
        if len(w) == pos:
            ended.append(w)
        else:
            groups.setdefault(w[pos], []).append(w)
    out = ended
    for letter in sorted(groups):
        out += msd_strings(groups[letter], pos + 1, looks)
    return out


if __name__ == "__main__":
    print(counting_sort(GRADES, 5), group_ends(GRADES, 5))
    p = []
    print(radix_sort(PILE, 2, passes=p), p)
    print(timing())
    looks = [0]
    print(msd_strings(TITLES, 0, looks), looks[0], lsd_strings(["cab", "abc", "bca", "acb"], 3))
