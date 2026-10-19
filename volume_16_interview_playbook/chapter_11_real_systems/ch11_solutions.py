"""Volume 16, Chapter 11 - Solutions to the exercises."""

from __future__ import annotations

from collections import defaultdict

from ch11_examples import SearchIndex


def autocomplete(queries: dict[str, int], prefix: str, k: int = 3) -> list[str]:
    """Exercise 1: the k most popular past queries starting with prefix (a trie would avoid scanning all, V6-C11)."""
    matches = [q for q in queries if q.startswith(prefix)]
    return sorted(matches, key=lambda q: (-queries[q], q))[:k]


def phrase_and(index: SearchIndex, query: str) -> list[str]:
    """Exercise 2: documents containing EVERY query word - intersect the posting sets, smallest first."""
    sets = sorted((index.index.get(w, set()) for w in query.lower().split()), key=len)
    return sorted(set.intersection(*sets)) if sets else []


def connected_communities(friends: dict[str, set[str]]) -> list[list[str]]:
    """Exercise 3: groups of people linked by friendship chains (union-find, V7-C5)."""
    parent = {p: p for p in friends}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for p, fs in friends.items():
        for f in fs:
            parent[find(p)] = find(f)
    groups: dict[str, list[str]] = defaultdict(list)
    for p in friends:
        groups[find(p)].append(p)
    return sorted(sorted(g) for g in groups.values())


if __name__ == "__main__":
    print(autocomplete({"goa trip": 50, "goa hotels": 80, "good food": 30, "pune": 10}, "go"),
          connected_communities({"a": {"b"}, "b": {"a"}, "c": set()}))
