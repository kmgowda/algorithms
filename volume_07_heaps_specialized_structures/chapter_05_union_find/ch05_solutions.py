"""Volume 7, Chapter 5 - Solutions to the exercises."""

from __future__ import annotations

from ch05_examples import UnionFind


def provinces(adjacent: list[list[int]]) -> int:
    """Exercise 1 (LeetCode 547): cities connected directly or indirectly form a province."""
    uf = UnionFind()
    for i in range(len(adjacent)):
        uf.add(i)
        for j in range(i):
            if adjacent[i][j]:
                uf.union(i, j)
    return uf.groups


def merge_accounts(accounts: list[list[str]]) -> list[list[str]]:
    """Exercise 2 (LeetCode 721): accounts sharing an email belong to one person. [name, email, email, ...]"""
    uf, owner = UnionFind(), {}
    for name, *emails in accounts:
        for e in emails:
            owner[e] = name
            uf.union(emails[0], e)
    groups: dict[str, list[str]] = {}
    for e in owner:
        groups.setdefault(uf.find(e), []).append(e)
    return sorted([owner[root]] + sorted(es) for root, es in groups.items())


def satisfiable(equations: list[str]) -> bool:
    """Exercise 3 (LeetCode 990): 'a==b' and 'a!=b' - union all equalities, then check inequalities."""
    uf = UnionFind()
    for eq in equations:
        if eq[1] == "=":
            uf.union(eq[0], eq[3])
    return all(not uf.connected(eq[0], eq[3]) for eq in equations if eq[1] == "!")


def largest_group(pairs: list[tuple[str, str]]) -> int:
    """Exercise 4: the size of the biggest friend circle."""
    uf = UnionFind()
    for a, b in pairs:
        uf.union(a, b)
    return max((uf.group_size(x) for x in uf.parent), default=0)


if __name__ == "__main__":
    print(provinces([[1, 1, 0], [1, 1, 0], [0, 0, 1]]))
    print(merge_accounts([["Ana", "a@x", "b@x"], ["Ana", "c@x"], ["Ana", "b@x", "d@x"], ["Ben", "e@x"]]))
    print(satisfiable(["a==b", "b!=a"]), satisfiable(["a==b", "b==c", "a!=d"]), largest_group([("a", "b"), ("c", "d"), ("b", "e")]))
