"""Volume 4, Chapter 3 - Solutions to the exercises."""

from __future__ import annotations

from collections import Counter, defaultdict


def is_ransom_note_possible(note: str, magazine: str) -> bool:
    """Exercise 1 (LeetCode 383): can the note be cut out of the magazine's letters?"""
    need, have = Counter(note), Counter(magazine)
    return all(have[ch] >= count for ch, count in need.items())


def intersection_with_counts(a: list[int], b: list[int]) -> list[int]:
    """Exercise 2 (LeetCode 350): items in both lists, as many times as they appear in both."""
    return sorted((Counter(a) & Counter(b)).elements())


def first_seen_day(visits: list[tuple[int, str]]) -> dict[str, int]:
    """Exercise 3: the first day each visitor came (setdefault keeps the first value)."""
    first: dict[str, int] = {}
    for day, person in visits:
        first.setdefault(person, day)
    return first


def friends_in_common(friends: dict[str, set[str]]) -> dict[tuple[str, str], int]:
    """Exercise 4: for every pair of people, how many friends they share."""
    names = sorted(friends)
    return {(a, b): len(friends[a] & friends[b]) for i, a in enumerate(names) for b in names[i + 1:]}


def tags_to_items(items: dict[str, list[str]]) -> dict[str, list[str]]:
    """Exercise 5: invert 'item -> tags' into 'tag -> items' (e.g. recipes by ingredient)."""
    out: defaultdict[str, list[str]] = defaultdict(list)
    for item, tags in items.items():
        for tag in tags:
            out[tag].append(item)
    return {tag: sorted(v) for tag, v in out.items()}


if __name__ == "__main__":
    print(is_ransom_note_possible("zoo", "oozebra"), intersection_with_counts([1, 2, 2, 1], [2, 2]))
    print(first_seen_day([(1, "Ana"), (2, "Ben"), (3, "Ana")]))
    print(friends_in_common({"A": {"x", "y"}, "B": {"y", "z"}, "C": {"x", "y", "z"}}))
    print(tags_to_items({"pancakes": ["egg", "milk"], "omelette": ["egg"]}))
