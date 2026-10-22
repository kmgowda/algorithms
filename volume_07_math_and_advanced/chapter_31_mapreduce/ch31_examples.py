"""Volume 7, Chapter 31 - MapReduce: split the data, map each piece, group by key, reduce each group.

Run:  python3 ch31_examples.py
"""

from __future__ import annotations

from collections import defaultdict

NEWSLETTERS = ["the club reads maps", "the club meets on monday", "maps and poems at the library", "the library opens late on monday"]


def map_reduce(records: list, mapper, reducer, machines: int = 3) -> dict:
    """Simulated MapReduce (Figure 31.1): split, map, group by key (the shuffle), reduce."""
    if machines < 1:
        raise ValueError("at least one machine is needed")
    shares = [records[i::machines] for i in range(machines)]
    pairs = [kv for share in shares for rec in share for kv in mapper(rec)]
    groups = defaultdict(list)
    for k, v in pairs:
        groups[k].append(v)
    return {k: reducer(k, vs) for k, vs in sorted(groups.items())}


def word_count(records: list, machines: int = 3) -> dict:
    return map_reduce(records, lambda line: [(w, 1) for w in line.split()], lambda k, vs: sum(vs), machines)


def inverted_index(records: list) -> dict:
    """Which newsletters mention each word (numbered from 1)."""
    return map_reduce(list(enumerate(records, 1)), lambda r: [(w, r[0]) for w in set(r[1].split())], lambda k, vs: sorted(vs))


LOANS = [("North", 2), ("North", 3), ("North", 2), ("North", 1), ("North", 2), ("East", 14)]   # (branch, books per visit)


def per_machine(records: list) -> list:
    """Each branch's records sit on its own machine."""
    by = defaultdict(list)
    for branch, v in records:
        by[branch].append(v)
    return list(by.values())


def average_wrong(records: list) -> float:
    """Averaging the machines' averages: wrong when machines hold different amounts (Figure 31.2)."""
    avgs = [sum(s) / len(s) for s in per_machine(records)]
    return sum(avgs) / len(avgs)


def average_right(records: list) -> float:
    """Each machine sends (sum, count); add those, then divide once."""
    totals = [(sum(s), len(s)) for s in per_machine(records)]
    return sum(t for t, _ in totals) / sum(c for _, c in totals)


def map_reduce_counted(records: list, mapper, reducer, machines: int = 3, combiner=None) -> tuple[dict, int]:
    """The same simulation, also counting the pairs sent through the shuffle (the network cost, Figure 31.3).
    A combiner reduces each machine's pairs for the same key before they are sent."""
    if machines < 1:
        raise ValueError("at least one machine is needed")
    shares = [records[i::machines] for i in range(machines)]
    sent = []
    for share in shares:
        pairs = [kv for rec in share for kv in mapper(rec)]
        if combiner:
            local = defaultdict(list)
            for k, v in pairs:
                local[k].append(v)
            pairs = [(k, combiner(k, vs)) for k, vs in local.items()]
        sent += pairs
    groups = defaultdict(list)
    for k, v in sent:
        groups[k].append(v)
    return {k: reducer(k, vs) for k, vs in sorted(groups.items())}, len(sent)


BRANCHES = [("North", "Ada Lane"), ("East", "Brook Road"), ("South", "Coral Street")]
VISITS = [("North", 2), ("North", 3), ("East", 14), ("North", 1), ("East", 4)]


def join(branches: list, visits: list) -> dict:
    """A reduce-side join (Figure 31.4): tag every record with its table, key it by branch, and let each reducer
    pair the branch's address with its visits."""
    records = [("B", b) for b in branches] + [("V", v) for v in visits]

    def mapper(rec):
        tag, row = rec
        return [(row[0], (tag, row[1]))]

    def reducer(key, vals):
        addresses = [v for t, v in vals if t == "B"]
        books = [v for t, v in vals if t == "V"]
        return [(a, b) for a in addresses for b in books]
    return map_reduce(records, mapper, reducer)


def sample_sort(values: list, machines: int, seed: int = 28) -> tuple[list, list]:
    """Sorting with MapReduce (TeraSort's idea): sample the data to choose machines - 1 split points, send each value
    to the machine for its range, sort each machine's share, and read the machines in order. Returns
    (sorted values, share sizes)."""
    import bisect
    import random
    r = random.Random(seed)
    sample = sorted(r.sample(values, min(len(values), 20 * machines)))
    splits = [sample[len(sample) * i // machines] for i in range(1, machines)]
    shares = [[] for _ in range(machines)]
    for v in values:
        shares[bisect.bisect_right(splits, v)].append(v)
    return [v for sh in shares for v in sorted(sh)], [len(sh) for sh in shares]


def matrix_vector(matrix: dict, vector: dict) -> dict:
    """y = M x with M stored as (row, column) -> value: map each entry to (row, value x x[column]), reduce by adding."""
    records = list(matrix.items())
    return map_reduce(records, lambda e: [(e[0][0], e[1] * vector.get(e[0][1], 0))], lambda k, vs: sum(vs))


def top_k_two_jobs(records: list, k: int, machines: int = 3) -> tuple[list, int]:
    """Top k words: a word count, then each machine sends only its local top k to a single reducer. Returns
    (top k, pairs the single reducer receives)."""
    counts = word_count(records, machines)
    items = list(counts.items())
    shares = [items[i::machines] for i in range(machines)]
    local = [sorted(sh, key=lambda t: (-t[1], t[0]))[:k] for sh in shares]
    received = [t for loc in local for t in loc]
    return sorted(received, key=lambda t: (-t[1], t[0]))[:k], len(received)


if __name__ == "__main__":
    wc = word_count(NEWSLETTERS)
    print(wc)
    print(word_count(NEWSLETTERS, 1) == wc, word_count(NEWSLETTERS, 10) == wc)
    idx = inverted_index(NEWSLETTERS)
    print(idx["monday"], idx["maps"], idx["the"])
    print(map_reduce(LOANS, lambda r: [(r[0], r[1])], lambda k, vs: sum(vs)), average_wrong(LOANS), average_right(LOANS))
    wcm = lambda line: [(w, 1) for w in line.split()]
    add = lambda k, vs: sum(vs)
    print(map_reduce_counted(NEWSLETTERS, wcm, add)[1], map_reduce_counted(NEWSLETTERS, wcm, add, combiner=add)[1])
    big = NEWSLETTERS * 250
    print(map_reduce_counted(big, wcm, add, machines=10)[1], map_reduce_counted(big, wcm, add, machines=10, combiner=add)[1])
    print(join(BRANCHES, VISITS))
    import random
    rr = random.Random(5)
    vals = [rr.randrange(10 ** 6) for _ in range(10000)]
    srt, sizes = sample_sort(vals, 4)
    print(srt == sorted(vals), sizes)
    print(matrix_vector({(0, 0): 2, (0, 1): 1, (1, 1): 3, (2, 0): 1, (2, 2): 4}, {0: 1, 1: 2, 2: 3}))
    print(top_k_two_jobs(NEWSLETTERS, 3))
