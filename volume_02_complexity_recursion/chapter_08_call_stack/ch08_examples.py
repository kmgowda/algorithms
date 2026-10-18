"""Volume 2, Chapter 8 - Recursion II: The Call Stack, Recursion Trees, and Recursion to Loops.

Run:  python3 ch08_examples.py
"""

from __future__ import annotations

import sys
import traceback
from typing import Any


# ------------------------------------------------------------------ watching the call stack
def factorial_traced(n: int, depth: int = 0, trace: list[str] | None = None) -> tuple[int, list[str]]:
    """Factorial that records each call and return, indented by how deep the stack is."""
    if trace is None:
        trace = []
    indent = "    " * depth
    trace.append(f"{indent}call factorial({n})")
    if n == 0:
        result = 1
    else:
        result = n * factorial_traced(n - 1, depth + 1, trace)[0]
    trace.append(f"{indent}return {result}")
    return result, trace


def deepest_recursion_possible() -> int:
    """Recurse until Python refuses, and report how deep we got."""
    def dive(level: int) -> int:
        try:
            return dive(level + 1)
        except RecursionError:
            return level
    return dive(1)


def stack_trace_of_failure() -> list[str]:
    """Industry example: the 'stack trace' in an error report lists every call that was waiting."""
    def checkout(cart: dict[str, int]) -> int:
        return compute_total(cart)

    def compute_total(cart: dict[str, int]) -> int:
        total = 0
        for item, qty in cart.items():
            total += price_of(item) * qty
        return total

    def price_of(item: str) -> int:
        prices = {"apple": 30, "mango": 60}
        return prices[item]                     # KeyError for unknown items

    try:
        checkout({"apple": 2, "durian": 1})
    except KeyError:
        frames = traceback.extract_tb(sys.exc_info()[2])
        return [frame.name for frame in frames]
    return []


# ------------------------------------------------------------------ recursion trees
def fibonacci_naive(n: int, counter: dict[str, int] | None = None) -> int:
    """F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2). Two recursive calls -> a branching recursion tree."""
    if counter is not None:
        counter["calls"] = counter.get("calls", 0) + 1
    if n < 2:
        return n
    return fibonacci_naive(n - 1, counter) + fibonacci_naive(n - 2, counter)


def fibonacci_call_count(n: int) -> int:
    counter: dict[str, int] = {}
    fibonacci_naive(n, counter)
    return counter["calls"]


def calls_per_level(n: int) -> list[int]:
    """How many calls of the naive Fibonacci recursion sit at each depth of its recursion tree."""
    levels: list[int] = []

    def visit(k: int, depth: int) -> None:
        if depth == len(levels):
            levels.append(0)
        levels[depth] += 1
        if k >= 2:
            visit(k - 1, depth + 1)
            visit(k - 2, depth + 1)

    visit(n, 0)
    return levels


# ------------------------------------------------------------------ avoiding copies: pass an index
def sum_from(values: list[float], start: int = 0) -> float:
    """Sum of values[start:] without slicing: O(n) time instead of O(n^2)."""
    if start == len(values):
        return 0
    return values[start] + sum_from(values, start + 1)


def sum_with_accumulator(values: list[float], start: int = 0, total: float = 0) -> float:
    """Tail-recursive style: the running total travels down; nothing is left to do after the call."""
    if start == len(values):
        return total
    return sum_with_accumulator(values, start + 1, total + values[start])


# ------------------------------------------------------------------ recursion to loops with an explicit stack
def folder_size_recursive(folder: dict[str, Any]) -> int:
    total = sum(folder.get("files", {}).values())
    for sub_folder in folder.get("folders", {}).values():
        total += folder_size_recursive(sub_folder)
    return total


def folder_size_iterative(folder: dict[str, Any]) -> int:
    """Same answer with a loop: keep our OWN stack of folders still to visit."""
    total = 0
    to_visit = [folder]
    while to_visit:
        current = to_visit.pop()                 # take the most recently added folder
        total += sum(current.get("files", {}).values())
        to_visit.extend(current.get("folders", {}).values())
    return total


def nesting_depth_iterative(data: Any) -> int:
    """Industry example: how deeply nested is a JSON-like value? Works even for very deep data."""
    deepest = 0
    stack = [(data, 1)]
    while stack:
        value, depth = stack.pop()
        if isinstance(value, (list, dict)):
            deepest = max(deepest, depth)
            children = value.values() if isinstance(value, dict) else value
            stack.extend((child, depth + 1) for child in children)
    return deepest


def make_deep_list(depth: int) -> list[Any]:
    """[[[...[]...]]] nested `depth` levels - deeper than Python's default recursion limit if large."""
    root: list[Any] = []
    current = root
    for _ in range(depth - 1):
        child: list[Any] = []
        current.append(child)
        current = child
    return root


if __name__ == "__main__":
    print("\n".join(factorial_traced(3)[1]))
    print("Recursion limit setting:", sys.getrecursionlimit(), "| depth reached:", deepest_recursion_possible())
    print("Stack trace frames:", stack_trace_of_failure())
    for n in (10, 20, 25):
        print(f"fibonacci_naive({n}) = {fibonacci_naive(n)} using {fibonacci_call_count(n):,} calls")
    print("Calls per level for F(6):", calls_per_level(6))
    print("Sums:", sum_from([3, 1, 4, 1, 5]), sum_with_accumulator([3, 1, 4, 1, 5]))
    disk = {"files": {"a": 4}, "folders": {"b": {"files": {"c": 10}, "folders": {}}}}
    print("Folder size both ways:", folder_size_recursive(disk), folder_size_iterative(disk))
    print("Depth of a 5,000-level nested list:", nesting_depth_iterative(make_deep_list(5000)))
