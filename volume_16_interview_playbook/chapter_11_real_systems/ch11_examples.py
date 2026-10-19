"""Volume 16, Chapter 11 - Algorithms in Real Systems: Search Engines, Maps, Social Networks, Banking.

Run:  python3 ch11_examples.py
"""

from __future__ import annotations

import heapq
import math
from collections import Counter, defaultdict, deque


class SearchIndex:
    """A search engine in miniature: an inverted index (word -> documents) plus TF-IDF ranking."""

    def __init__(self, docs: dict[str, str]) -> None:
        self.docs = {name: Counter(text.lower().split()) for name, text in docs.items()}
        self.index: dict[str, set[str]] = defaultdict(set)
        for name, words in self.docs.items():
            for w in words:
                self.index[w].add(name)

    def search(self, query: str, k: int = 3) -> list[tuple[str, float]]:
        """Score = sum over query words of (count in doc) x log(N / docs containing the word). Rare words weigh more."""
        n = len(self.docs)
        scores: Counter[str] = Counter()
        for w in query.lower().split():
            holders = self.index.get(w, set())
            for name in holders:
                scores[name] += self.docs[name][w] * math.log(n / len(holders))
        return [(name, round(s, 3)) for name, s in heapq.nlargest(k, scores.items(), key=lambda kv: (kv[1], kv[0]))]


def fastest_route(roads: dict[str, list[tuple[str, float]]], start: str, goal: str) -> tuple[float, list[str]]:
    """Maps: Dijkstra over road segments weighted by travel minutes (V9-C2)."""
    dist, prev = {start: 0.0}, {}
    heap = [(0.0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if u == goal:
            break
        if d > dist[u]:
            continue
        for v, w in roads.get(u, []):
            if d + w < dist.get(v, math.inf):
                dist[v], prev[v] = d + w, u
                heapq.heappush(heap, (d + w, v))
    if goal not in dist:
        return math.inf, []
    path = [goal]
    while path[-1] != start:
        path.append(prev[path[-1]])
    return dist[goal], path[::-1]


def friend_suggestions(friends: dict[str, set[str]], user: str, k: int = 3) -> list[tuple[str, int]]:
    """Social networks: people at distance exactly 2, ranked by number of mutual friends."""
    mutual: Counter[str] = Counter()
    for f in friends.get(user, set()):
        for ff in friends.get(f, set()):
            if ff != user and ff not in friends[user]:
                mutual[ff] += 1
    return sorted(mutual.items(), key=lambda kv: (-kv[1], kv[0]))[:k]


def degrees_of_separation(friends: dict[str, set[str]], a: str, b: str) -> int:
    """BFS distance between two people (-1 if not connected)."""
    seen, q = {a: 0}, deque([a])
    while q:
        u = q.popleft()
        if u == b:
            return seen[u]
        for v in friends.get(u, set()):
            if v not in seen:
                seen[v] = seen[u] + 1
                q.append(v)
    return -1


def ledger(transactions: list[tuple[str, str, int]], opening: dict[str, int]) -> tuple[dict[str, int], list[int]]:
    """Banking: apply transfers in order; reject any that would overdraw. Returns (balances, rejected indices).
    Every accepted transfer keeps the total money unchanged - an invariant worth checking."""
    balance = dict(opening)
    rejected = []
    for i, (src, dst, amount) in enumerate(transactions):
        if amount <= 0 or balance.get(src, 0) < amount:
            rejected.append(i)
            continue
        balance[src] -= amount
        balance[dst] = balance.get(dst, 0) + amount
    return balance, rejected


def fraud_flags(card_events: list[tuple[int, str, str]], window: int) -> list[str]:
    """Banking: flag a card used in two different cities within `window` minutes (sliding window per card)."""
    last: dict[str, tuple[int, str]] = {}
    flagged = []
    for t, card, city in sorted(card_events):
        if card in last and last[card][1] != city and t - last[card][0] <= window and card not in flagged:
            flagged.append(card)
        last[card] = (t, city)
    return flagged


if __name__ == "__main__":
    idx = SearchIndex({"a": "cheap flights to goa", "b": "goa beach hotels and goa food", "c": "cheap hotels in pune"})
    print(idx.search("goa hotels"), idx.search("cheap"))
    roads = {"Home": [("Ring", 10), ("Market", 4)], "Market": [("Ring", 3), ("Office", 15)], "Ring": [("Office", 5)]}
    print(fastest_route(roads, "Home", "Office"))
    fr = {"asha": {"ben", "chen"}, "ben": {"asha", "dev", "eli"}, "chen": {"asha", "dev"}, "dev": {"ben", "chen"}, "eli": {"ben"}}
    print(friend_suggestions(fr, "asha"), degrees_of_separation(fr, "eli", "chen"))
    print(ledger([("A", "B", 50), ("B", "C", 80), ("A", "C", 60)], {"A": 100, "B": 40, "C": 0}))
    print(fraud_flags([(0, "card1", "Pune"), (30, "card1", "Delhi"), (10, "card2", "Goa"), (500, "card2", "Pune")], 60))
