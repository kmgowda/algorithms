"""Volume 12, Chapter 3 - Solutions to the exercises."""

from __future__ import annotations


def max_points_deleting(nums: list[int]) -> int:
    """Exercise 1 (LeetCode 740): taking value v earns v but deletes all v-1 and v+1.
    State: best over values up to v. Choice: take all v's or not. It's the tutor problem over values."""
    if not nums:
        return 0
    top = max(nums)
    earn = [0] * (top + 1)
    for x in nums:
        earn[x] += x
    take, skip = 0, 0
    for v in range(top + 1):
        take, skip = skip + earn[v], max(take, skip)
    return max(take, skip)


def paint_houses(costs: list[list[int]]) -> int:
    """Exercise 2 (LeetCode 256): paint houses red/blue/green, neighbours different, cheapest.
    State: (house, its colour). Transition: cost + cheapest previous house of a different colour."""
    if not costs:
        return 0
    prev = list(costs[0])
    for row in costs[1:]:
        prev = [row[c] + min(prev[d] for d in range(3) if d != c) for c in range(3)]
    return min(prev)


def describe_recipe(problem: str) -> dict[str, str]:
    """Exercise 3: the four ingredients for the tutor problem, as a checklist."""
    recipes = {
        "tutor": {"state": "best[i] = most money from the first i days",
                  "choice": "work day i-1 or rest",
                  "transition": "best[i] = max(best[i-1], best[i-2] + offer)",
                  "base": "best[0] = 0, best[1] = first offer"},
    }
    return recipes[problem]


if __name__ == "__main__":
    print(max_points_deleting([3, 4, 2]), max_points_deleting([2, 2, 3, 3, 3, 4]),
          paint_houses([[17, 2, 17], [16, 16, 5], [14, 3, 19]]), describe_recipe("tutor")["state"])
