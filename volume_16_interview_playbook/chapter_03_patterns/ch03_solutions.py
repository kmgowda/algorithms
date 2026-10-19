"""Volume 16, Chapter 3 - Solutions to the exercises."""

from __future__ import annotations

from ch03_examples import constraint_hint, suggest_techniques


def classify_set() -> dict[str, str]:
    """Exercise 1: the top technique for each classic problem statement."""
    problems = {
        "LC 3": "Longest substring without repeating characters, using a window.",
        "LC 20": "Check whether the parentheses in a string are balanced.",
        "LC 200": "Count the islands in a grid of land and water.",
        "LC 322": "Find the minimum cost in coins to make an amount; count the number of ways too.",
        "LC 347": "Return the top k most frequent elements.",
        "LC 56": "Merge all overlapping intervals.",
    }
    return {k: suggest_techniques(v, 1)[0][0] for k, v in problems.items()}


def combined_hint(problem: str, n: int) -> str:
    """Exercise 2: combine the text clues with the size hint into one sentence to say aloud."""
    tech = suggest_techniques(problem, 1)
    first = tech[0][0] if tech else "brute force first"
    return f"clues suggest {first}; n = {n} means {constraint_hint(n)}"


if __name__ == "__main__":
    print(classify_set())
    print(combined_hint("Return all subsets of the numbers.", 15))
