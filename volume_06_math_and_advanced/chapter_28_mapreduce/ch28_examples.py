"""Volume 6, Chapter 28 - MapReduce: split the data, map each piece, group by key, reduce each group.

Run:  python3 ch28_examples.py
"""

from __future__ import annotations

from collections import defaultdict

NEWSLETTERS = ["the club reads maps", "the club meets on monday", "maps and poems at the library", "the library opens late on monday"]


def map_reduce(records: list, mapper, reducer, machines: int = 3) -> dict:
    """Simulated MapReduce (Figure 28.1): records are split among machines, each maps its share to (key, value) pairs,
    the pairs are grouped by key (the shuffle), and each group is reduced."""
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
    """Which newsletters mention each word."""
    return map_reduce(list(enumerate(records)), lambda r: [(w, r[0]) for w in set(r[1].split())], lambda k, vs: sorted(vs))


LOANS = [("North", 2), ("North", 3), ("North", 2), ("North", 1), ("North", 2), ("East", 14)]   # (branch, books per visit)


def per_machine(records: list) -> list:
    """Each branch's records sit on its own machine."""
    by = defaultdict(list)
    for branch, v in records:
        by[branch].append(v)
    return list(by.values())


def average_wrong(records: list) -> float:
    """Averaging the machines' averages: wrong when machines hold different amounts (Figure 28.3)."""
    avgs = [sum(s) / len(s) for s in per_machine(records)]
    return sum(avgs) / len(avgs)


def average_right(records: list) -> float:
    """Each machine sends (sum, count); add those, then divide once."""
    totals = [(sum(s), len(s)) for s in per_machine(records)]
    return sum(t for t, _ in totals) / sum(c for _, c in totals)


if __name__ == "__main__":
    wc = word_count(NEWSLETTERS)
    print(wc)
    print(word_count(NEWSLETTERS, 1) == wc, word_count(NEWSLETTERS, 10) == wc)
    idx = inverted_index(NEWSLETTERS)
    print(idx["monday"], idx["maps"], idx["the"])
    print(map_reduce(LOANS, lambda r: [(r[0], r[1])], lambda k, vs: sum(vs)), average_wrong(LOANS), average_right(LOANS))
