"""Volume 4, Chapter 3 - Sets and Maps in Practice: Counting, Grouping, Deduplication.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations

from collections import Counter, defaultdict


def top_k_words(text: str, k: int) -> list[tuple[str, int]]:
    """Counting with Counter: the k most frequent words (ties broken alphabetically)."""
    counts = Counter(word.strip(".,!?").lower() for word in text.split() if word.strip(".,!?"))
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:k]


def group_by(records: list[dict[str, str]], field: str) -> dict[str, list[str]]:
    """Grouping with defaultdict(list): patients by ward, books by author, orders by city."""
    groups: defaultdict[str, list[str]] = defaultdict(list)
    for record in records:
        groups[record[field]].append(record["name"])
    return dict(groups)


def dedupe_keep_order(items: list[str]) -> list[str]:
    """Deduplicate but keep the first-seen order (a seen-set, V1-C8)."""
    seen: set[str] = set()
    out = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def reconcile(warehouse: list[str], website: list[str]) -> dict[str, list[str]]:
    """Industry example: which product codes are missing on each side? Set differences."""
    w, s = set(warehouse), set(website)
    return {"only_in_warehouse": sorted(w - s), "only_on_website": sorted(s - w), "in_both": sorted(w & s)}


def inverted_index(documents: dict[str, str]) -> dict[str, set[str]]:
    """Industry example: a search engine maps each word to the set of documents containing it."""
    index: defaultdict[str, set[str]] = defaultdict(set)
    for doc_id, text in documents.items():
        for word in text.lower().split():
            index[word.strip(".,!?")].add(doc_id)
    return dict(index)


def search_all(index: dict[str, set[str]], query: str) -> set[str]:
    """Documents containing EVERY query word: intersect the sets."""
    sets = [index.get(word, set()) for word in query.lower().split()]
    return set.intersection(*sets) if sets else set()


def anagram_buckets(words: list[str]) -> list[list[str]]:
    """Group words by a canonical key (sorted letters) - the key design idea for maps."""
    buckets: defaultdict[str, list[str]] = defaultdict(list)
    for word in words:
        buckets["".join(sorted(word))].append(word)
    return sorted(sorted(group) for group in buckets.values())


if __name__ == "__main__":
    story = "The lion saw the zebra. The zebra ran. The lion slept."
    print(top_k_words(story, 3))
    patients = [{"name": "Ana", "ward": "A"}, {"name": "Ben", "ward": "B"}, {"name": "Cy", "ward": "A"}]
    print(group_by(patients, "ward"))
    print(dedupe_keep_order(["mail", "news", "mail", "maps", "news"]))
    print(reconcile(["P1", "P2", "P3"], ["P2", "P3", "P4"]))
    idx = inverted_index({"d1": "Lions live in Africa.", "d2": "Lions and tigers.", "d3": "Tigers live in Asia."})
    print(sorted(search_all(idx, "lions live")), sorted(search_all(idx, "tigers")))
    print(anagram_buckets(["listen", "silent", "enlist", "lion", "loin", "zebra"]))
