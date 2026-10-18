"""Volume 5, Chapter 11 - Stability, In-Place Sorting, and Python's Timsort.

Run:  python3 ch11_examples.py
"""

from __future__ import annotations

from typing import Callable


def is_stable_result(original: list[tuple], result: list[tuple], key: Callable) -> bool:
    """Items with equal keys appear in `result` in the same relative order as in `original`."""
    position = {id(item): i for i, item in enumerate(original)}
    return all(position[id(a)] < position[id(b)] for a, b in zip(result, result[1:]) if key(a) == key(b))


def sort_by_columns(rows: list[dict], columns: list[str]) -> list[dict]:
    """Spreadsheet-style multi-column sort using STABILITY: sort by the LAST column first, then earlier ones."""
    out = list(rows)
    for col in reversed(columns):
        out.sort(key=lambda r: r[col])                 # each pass keeps the previous pass's order for ties
    return out


def find_runs(items: list) -> list[tuple[int, int]]:
    """Timsort's first insight: real data has 'runs' - stretches already in order. Returns [start, end) pairs.
    Strictly descending runs are reversed in place so every run ascends."""
    runs, i, n = [], 0, len(items)
    while i < n:
        j = i + 1
        if j < n and items[j] < items[i]:              # strictly descending run
            while j < n and items[j] < items[j - 1]:
                j += 1
            items[i:j] = reversed(items[i:j])
        else:
            while j < n and items[j] >= items[j - 1]:
                j += 1
        runs.append((i, j))
        i = j
    return runs


def min_run_length(n: int) -> int:
    """Timsort's minimum run length: between 32 and 64, chosen so n / minrun is close to a power of two."""
    r = 0
    while n >= 64:
        r |= n & 1
        n >>= 1
    return n + r


def simple_timsort(items: list) -> list:
    """A simplified Timsort: find natural runs, extend short ones to minrun with insertion sort,
    then merge neighbouring runs until one remains. (The real one adds galloping and a smarter merge order.)"""
    a = list(items)
    n = len(a)
    if n < 2:
        return a
    minrun = min_run_length(n)
    runs = []
    for start, end in find_runs(a):
        if runs and runs[-1][1] - runs[-1][0] < minrun:          # grow a short run by absorbing the next one
            s, _ = runs.pop()
            sub = a[s:end]
            for i in range(1, len(sub)):                         # insertion sort the combined stretch
                card, j = sub[i], i - 1
                while j >= 0 and sub[j] > card:
                    sub[j + 1] = sub[j]
                    j -= 1
                sub[j + 1] = card
            a[s:end] = sub
            runs.append((s, end))
        else:
            runs.append((start, end))
    while len(runs) > 1:
        merged = []
        for k in range(0, len(runs), 2):
            if k + 1 == len(runs):
                merged.append(runs[k])
                continue
            (s1, e1), (_, e2) = runs[k], runs[k + 1]
            left, right, out, i, j = a[s1:e1], a[e1:e2], [], 0, 0
            while i < len(left) and j < len(right):
                if right[j] < left[i]:                           # take from the right only if strictly smaller: stable
                    out.append(right[j])
                    j += 1
                else:
                    out.append(left[i])
                    i += 1
            out += left[i:] + right[j:]
            a[s1:e2] = out
            merged.append((s1, e2))
        runs = merged
    return a


def shop_listing(products: list[dict]) -> list[str]:
    """Industry example: sort by price (low to high), and for equal prices keep 'best rated first'."""
    by_rating = sorted(products, key=lambda p: -p["rating"])
    by_price = sorted(by_rating, key=lambda p: p["price"])     # stable: rating order survives within a price
    return [p["name"] for p in by_price]


if __name__ == "__main__":
    pupils = [("Ana", "B"), ("Ben", "A"), ("Cy", "B"), ("Dev", "A")]
    result = sorted(pupils, key=lambda p: p[1])
    print(result, is_stable_result(pupils, result, key=lambda p: p[1]))
    table = [{"city": "Pune", "name": "Zoe"}, {"city": "Agra", "name": "Ravi"}, {"city": "Pune", "name": "Amit"}]
    print([(r["city"], r["name"]) for r in sort_by_columns(table, ["city", "name"])])
    data = [1, 2, 3, 9, 8, 7, 4, 5, 6]
    print(find_runs(list(data)), min_run_length(1000), simple_timsort(data))
    print(shop_listing([{"name": "Mug A", "price": 5, "rating": 3.9}, {"name": "Mug B", "price": 5, "rating": 4.8},
                        {"name": "Cup", "price": 3, "rating": 4.1}]))
