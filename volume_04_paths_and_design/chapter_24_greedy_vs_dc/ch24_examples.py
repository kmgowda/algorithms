"""Volume 4, Chapter 24 - Greedy versus Divide and Conquer: the same problems, two ways of thinking.

Run:  python3 ch24_examples.py
"""

from __future__ import annotations

VISITORS = [12, 7, 21, 15, 3, 18, 9, 26]


def max_greedy(values: list, counter: list) -> int:
    """Scan once, keeping the best so far: n - 1 comparisons."""
    best = values[0]
    for v in values[1:]:
        counter[0] += 1
        best = max(best, v)
    return best


def max_dc(values: list, counter: list) -> int:
    """Split, find each half's maximum, compare once: also n - 1 comparisons, but the halves are independent."""
    if len(values) == 1:
        return values[0]
    mid = len(values) // 2
    a, b = max_dc(values[:mid], counter), max_dc(values[mid:], counter)
    counter[0] += 1
    return max(a, b)


def depth(n: int) -> int:
    """Rounds needed if every comparison in a round can happen at once (Figure 24.2)."""
    return 0 if n <= 1 else 1 + depth((n + 1) // 2)


def sort_greedy(values: list, counter: list) -> list:
    """Selection sort: greedily take the smallest remaining item each time."""
    left, out = list(values), []
    while left:
        i = 0
        for j in range(1, len(left)):
            counter[0] += 1
            if left[j] < left[i]:
                i = j
        out.append(left.pop(i))
    return out


def sort_dc(values: list, counter: list) -> list:
    """Merge sort: split, sort the halves, merge."""
    if len(values) <= 1:
        return list(values)
    mid = len(values) // 2
    a, b = sort_dc(values[:mid], counter), sort_dc(values[mid:], counter)
    out, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        counter[0] += 1
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    return out + a[i:] + b[j:]


def stretch_greedy(values: list, log: list | None = None) -> int:
    """The best stretch in one pass (Figure 24.4): keep a running total, but drop the past whenever it would hurt,
    i.e. start again at the current hour when the total so far is negative. n - 1 additions, depth n."""
    run = best = values[0]
    if log is not None:
        log.append(run)
    for v in values[1:]:
        run = v if run < 0 else run + v
        best = max(best, run)
        if log is not None:
            log.append(run)
    return best


def stretch_dc_work(n: int) -> tuple[int, int]:
    """(steps, depth) of Chapter 18's best-stretch method on n values: each piece of size s does s crossing steps;
    the depth is the longest chain of steps that must follow one another (a crossing scan is s steps long)."""
    if n <= 1:
        return 1, 1
    a, b = n // 2, n - n // 2
    wa, da = stretch_dc_work(a)
    wb, db = stretch_dc_work(b)
    return wa + wb + n, max(da, db) + n


def stretch_summary_work(n: int) -> tuple[int, int]:
    """(steps, depth) of the four-number version (Chapter 18, Challenge 3): constant work per combine."""
    if n <= 1:
        return 1, 1
    wa, da = stretch_summary_work(n // 2)
    wb, db = stretch_summary_work(n - n // 2)
    return wa + wb + 1, max(da, db) + 1


def code_lengths_huffman(counts: dict) -> dict:
    """Greedy, bottom up: repeatedly join the two rarest groups (Chapter 16). Returns code length per symbol."""
    import heapq
    if len(counts) == 1:
        return {s: 1 for s in counts}
    heap = [(c, i, [s]) for i, (s, c) in enumerate(sorted(counts.items()))]
    heapq.heapify(heap)
    depth_of = {s: 0 for s in counts}
    k = len(heap)
    while len(heap) > 1:
        c1, _, g1 = heapq.heappop(heap)
        c2, _, g2 = heapq.heappop(heap)
        for s in g1 + g2:
            depth_of[s] += 1
        heapq.heappush(heap, (c1 + c2, k, g1 + g2))
        k += 1
    return depth_of


def code_lengths_split(counts: dict) -> dict:
    """Divide and conquer, top down (Shannon-Fano): sort by count, split into two groups with totals as equal as
    possible, give one group 0 and the other 1, and recurse. Fast and sensible, but not always the fewest bits."""
    items = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    lengths = {s: 0 for s in counts}

    def split(group):
        if len(group) <= 1:
            return
        total, run, best, cut = sum(c for _, c in group), 0, None, 1
        for i in range(1, len(group)):
            run += group[i - 1][1]
            gap = abs(total - 2 * run)
            if best is None or gap < best:
                best, cut = gap, i
        for s, _ in group:
            lengths[s] += 1
        split(group[:cut])
        split(group[cut:])
    if len(items) == 1:
        return {items[0][0]: 1}
    split(items)
    return lengths


def total_bits(counts: dict, lengths: dict) -> int:
    return sum(counts[s] * lengths[s] for s in counts)


def split_worse_count(trials: int = 1000, seed: int = 1) -> int:
    """How many random sets of 2 to 8 counts the top-down split codes with more bits than Huffman."""
    import random
    rng = random.Random(seed)
    worse = 0
    for _ in range(trials):
        cc = {chr(65 + i): rng.randint(1, 30) for i in range(rng.randint(2, 8))}
        if total_bits(cc, code_lengths_split(cc)) > total_bits(cc, code_lengths_huffman(cc)):
            worse += 1
    return worse


if __name__ == "__main__":
    a, b = [0], [0]
    print(max_greedy(VISITORS, a), a[0], max_dc(VISITORS, b), b[0], depth(8))
    for n in (8, 100, 1000):
        import random
        v = random.Random(n).sample(range(10 * n), n)
        c, d = [0], [0]
        sort_greedy(v, c); sort_dc(v, d)
        print(n, c[0], d[0], depth(n))
