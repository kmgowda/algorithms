"""Volume 2, Chapter 8 - Solutions to the exercises."""

from __future__ import annotations

from typing import Any


def max_stack_depth_of_countdown(n: int) -> int:
    """Exercise 1: countdown(n) -> countdown(n-1) -> ... -> countdown(0): n + 1 frames at the deepest point."""
    return n + 1


def fibonacci_calls_formula(n: int) -> int:
    """Exercise 2: calls(n) = 1 + calls(n-1) + calls(n-2), with calls(0) = calls(1) = 1."""
    a, b = 1, 1          # calls(0), calls(1)
    if n == 0:
        return 1
    for _ in range(n - 1):
        a, b = b, 1 + a + b
    return b


def reverse_from(text: str, index: int = 0) -> str:
    """Exercise 3: reverse a string recursively without slicing, using an index."""
    if index == len(text):
        return ""
    return reverse_from(text, index + 1) + text[index]


def count_files_iterative(folder: dict[str, Any]) -> int:
    """Exercise 4: number of files in a folder tree, using an explicit stack."""
    count = 0
    stack = [folder]
    while stack:
        current = stack.pop()
        count += len(current.get("files", {}))
        stack.extend(current.get("folders", {}).values())
    return count


def all_paths(folder: dict[str, Any], prefix: str = "") -> list[str]:
    """Exercise 5: every file path, like 'school/maths/homework.pdf' (recursive)."""
    paths = [prefix + name for name in folder.get("files", {})]
    for name, sub in folder.get("folders", {}).items():
        paths.extend(all_paths(sub, prefix + name + "/"))
    return paths


def binary_strings(length: int) -> list[str]:
    """Exercise 6: every string of 0s and 1s of a given length - a recursion tree with 2 branches."""
    if length == 0:
        return [""]
    shorter = binary_strings(length - 1)
    return ["0" + s for s in shorter] + ["1" + s for s in shorter]


if __name__ == "__main__":
    print(max_stack_depth_of_countdown(5), fibonacci_calls_formula(20), reverse_from("zebra"))
    disk = {"files": {"a.txt": 1}, "folders": {"pics": {"files": {"b.jpg": 2, "c.jpg": 3}, "folders": {}}}}
    print(count_files_iterative(disk), all_paths(disk), binary_strings(3))
