"""Volume 16, Chapter 3 - Pattern Recognition: Mapping Problem Clues to Techniques.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations

CLUES: list[tuple[tuple[str, ...], str, str]] = [
    (("sorted", "find target", "minimum value such that", "first position"), "binary search", "V5-C2"),
    (("pair", "two numbers", "sorted array", "palindrome", "reverse"), "two pointers", "V4-C5"),
    (("substring", "subarray", "window", "consecutive", "at most k"), "sliding window", "V4-C7"),
    (("seen before", "count", "frequency", "anagram", "duplicate", "lookup"), "hash map", "V4-C3"),
    (("range sum", "sum of subarray", "cumulative"), "prefix sums", "V4-C8"),
    (("next greater", "previous smaller", "parentheses", "evaluate expression"), "stack", "V3-C7"),
    (("k largest", "k smallest", "top k", "median", "merge k"), "heap", "V7-C3"),
    (("intervals", "meetings", "overlap", "schedule"), "sort + sweep / greedy", "V10-C4"),
    (("tree", "ancestor", "depth", "root"), "tree recursion / DFS", "V6-C4"),
    (("grid", "islands", "shortest path unweighted", "minimum steps", "levels"), "BFS", "V8-C5"),
    (("dependencies", "prerequisites", "order of tasks"), "topological sort", "V8-C7"),
    (("connected", "groups", "union", "components"), "union-find / DFS", "V7-C5"),
    (("weighted", "cheapest route", "shortest path with costs"), "Dijkstra", "V9-C2"),
    (("all combinations", "all permutations", "all subsets", "generate all", "n-queens"), "backtracking", "V11-C2"),
    (("number of ways", "minimum cost", "maximum profit", "longest", "can you reach"), "dynamic programming", "V12-C3"),
    (("prefix of words", "autocomplete", "dictionary of words"), "trie", "V6-C11"),
    (("xor", "single number", "bits", "power of two"), "bit manipulation", "V14-C2"),
]


def suggest_techniques(problem: str, top: int = 3) -> list[tuple[str, str, int]]:
    """Score each technique by the clue phrases found in the problem text; longer (more specific) phrases count
    more. Returns up to `top` (technique, where it was taught, score), best first."""
    text = problem.lower()
    scored = []
    for phrases, technique, where in CLUES:
        score = sum(len(p.split()) for p in phrases if p in text)
        if score:
            scored.append((technique, where, score))
    scored.sort(key=lambda t: -t[2])
    return scored[:top]


def constraint_hint(n: int) -> str:
    """The input size narrows the choice (Chapter 1)."""
    if n <= 12:
        return "exponential is fine: backtracking or permutations"
    if n <= 25:
        return "2^n is fine: bitmask DP, subsets, meet in the middle"
    if n <= 500:
        return "O(n^3) is fine: interval or Floyd-Warshall style DP"
    if n <= 5000:
        return "O(n^2) is fine: 2-D DP, all pairs"
    if n <= 10 ** 6:
        return "need O(n log n): sorting, heaps, binary search"
    return "need O(n) or better: one pass, hashing, two pointers, math"


if __name__ == "__main__":
    problems = [
        "Find the longest substring without repeating characters.",
        "Given a sorted array, find the first position of a target.",
        "Return all subsets of a set of numbers.",
        "Count the number of ways to climb n stairs.",
        "Given course prerequisites, find an order to take all courses.",
        "Find the k largest elements in a stream.",
    ]
    for p in problems:
        print(p, "->", suggest_techniques(p, 2))
    print(constraint_hint(20), "|", constraint_hint(10 ** 5))
