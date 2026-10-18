"""Volume 8, Chapter 1 - What Is a Graph? Cities, Friends, and Web Pages.

A graph here is a dictionary: each vertex maps to a list of the vertices it connects to.

Run:  python3 ch01_examples.py
"""

from __future__ import annotations

from typing import Hashable

Graph = dict[Hashable, list[Hashable]]


def make_undirected(roads: list[tuple[str, str]]) -> Graph:
    """Two-way roads: each road appears in both cities' lists."""
    graph: Graph = {}
    for a, b in roads:
        graph.setdefault(a, []).append(b)
        graph.setdefault(b, []).append(a)
    return graph


def neighbours(graph: Graph, v: Hashable) -> list[Hashable]:
    return graph.get(v, [])


def can_reach(graph: Graph, start: Hashable, goal: Hashable) -> bool:
    """A first taste of exploring (Chapter 4 does it properly): keep a to-visit list and a visited set."""
    to_visit, visited = [start], {start}
    while to_visit:
        city = to_visit.pop()
        if city == goal:
            return True
        for nxt in neighbours(graph, city):
            if nxt not in visited:
                visited.add(nxt)
                to_visit.append(nxt)
    return False


def friend_suggestions(friends: Graph, person: Hashable) -> list[tuple[Hashable, int]]:
    """Industry example: 'people you may know' = friends of friends, ranked by how many mutual friends."""
    mine = set(friends.get(person, []))
    counts: dict[Hashable, int] = {}
    for f in mine:
        for ff in friends.get(f, []):
            if ff != person and ff not in mine:
                counts[ff] = counts.get(ff, 0) + 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], str(kv[0])))


def most_linked_pages(links: Graph) -> list[tuple[Hashable, int]]:
    """Industry example: count incoming links per page (a first idea behind search ranking)."""
    incoming: dict[Hashable, int] = {page: 0 for page in links}
    for page, targets in links.items():
        for t in targets:
            incoming[t] = incoming.get(t, 0) + 1
    return sorted(incoming.items(), key=lambda kv: (-kv[1], str(kv[0])))


if __name__ == "__main__":
    roads = make_undirected([("Pune", "Mumbai"), ("Mumbai", "Surat"), ("Pune", "Nashik"), ("Goa", "Panaji")])
    print(roads)
    print("Pune -> Surat?", can_reach(roads, "Pune", "Surat"), "| Pune -> Goa?", can_reach(roads, "Pune", "Goa"))
    friends = make_undirected([("Ana", "Ben"), ("Ana", "Cy"), ("Ben", "Dev"), ("Cy", "Dev"), ("Cy", "Eve")])
    print("suggestions for Ana:", friend_suggestions(friends, "Ana"))
    web = {"home": ["about", "shop"], "about": ["home"], "shop": ["home", "cart"], "cart": ["shop"], "blog": ["home"]}
    print("most linked:", most_linked_pages(web)[:2])
