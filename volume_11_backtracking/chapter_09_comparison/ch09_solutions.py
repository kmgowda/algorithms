"""Volume 11, Chapter 9 - Solutions to the exercises."""

from __future__ import annotations

from collections import Counter

from ch09_examples import choose_search


def pick_methods() -> dict[str, str]:
    """Exercise 1: choose a search method for each scenario."""
    return {
        "fill a crossword grid": choose_search({"rules can be checked on partial solutions"}),
        "cheapest delivery round for 15 stops": choose_search({"need the best value, with a good optimistic bound"}),
        "subset sum with 40 numbers": choose_search({"splits into independent halves to combine"}),
        "count ways to climb stairs": choose_search({"subproblems repeat"}),
        "check 6 possible seating orders": choose_search({"tiny input"}),
    }


def meet_in_middle_count(values: list[int], target: int) -> int:
    """Exercise 2: HOW MANY subsets reach the target - count sums in each half, then pair them up."""
    def sums(part: list[int]) -> Counter:
        out = Counter({0: 1})
        for v in part:
            new = Counter()
            for s, c in out.items():
                new[s] += c
                new[s + v] += c
            out = new
        return out

    half = len(values) // 2
    left, right = sums(values[:half]), sums(values[half:])
    return sum(c * right[target - s] for s, c in left.items())


if __name__ == "__main__":
    print(pick_methods())
    print(meet_in_middle_count([1, 2, 3, 4, 5], 5))
