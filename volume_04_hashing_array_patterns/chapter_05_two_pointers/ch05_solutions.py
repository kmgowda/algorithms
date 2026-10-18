"""Volume 4, Chapter 5 - Solutions to the exercises."""

from __future__ import annotations


def sort_colors(colors: list[int]) -> None:
    """Exercise 1 (LeetCode 75): Dutch national flag - 0s, then 1s, then 2s, in one pass, in place."""
    low, mid, high = 0, 0, len(colors) - 1
    while mid <= high:
        if colors[mid] == 0:
            colors[low], colors[mid] = colors[mid], colors[low]
            low += 1
            mid += 1
        elif colors[mid] == 1:
            mid += 1
        else:
            colors[mid], colors[high] = colors[high], colors[mid]
            high -= 1


def closest_pair_sum(a: list[int], b: list[int], target: int) -> tuple[int, int]:
    """Exercise 2: one item from each sorted list with sum closest to target."""
    i, j = 0, len(b) - 1
    best = (a[0], b[0])
    while i < len(a) and j >= 0:
        s = a[i] + b[j]
        if abs(s - target) < abs(sum(best) - target):
            best = (a[i], b[j])
        if s < target:
            i += 1
        elif s > target:
            j -= 1
        else:
            break
    return best


def trapped_rain(heights: list[int]) -> int:
    """Exercise 3 (LeetCode 42): water trapped between bars. Two pointers with running maxima."""
    left, right = 0, len(heights) - 1
    left_max = right_max = water = 0
    while left < right:
        if heights[left] < heights[right]:
            left_max = max(left_max, heights[left])
            water += left_max - heights[left]
            left += 1
        else:
            right_max = max(right_max, heights[right])
            water += right_max - heights[right]
            right -= 1
    return water


def remove_duplicates_keep_two(values: list[int]) -> int:
    """Exercise 4 (LeetCode 80): sorted list, keep at most two copies of each value, in place."""
    write = 0
    for v in values:
        if write < 2 or values[write - 2] != v:
            values[write] = v
            write += 1
    return write


if __name__ == "__main__":
    c = [2, 0, 2, 1, 1, 0]
    sort_colors(c)
    print(c, closest_pair_sum([1, 4, 5, 7], [10, 20, 30, 40], 32), trapped_rain([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))
    v = [1, 1, 1, 2, 2, 3]
    print(v[:remove_duplicates_keep_two(v)])
