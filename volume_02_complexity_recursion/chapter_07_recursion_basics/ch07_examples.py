"""Volume 2, Chapter 7 - Recursion I: Functions That Call Themselves.

Run:  python3 ch07_examples.py
"""

from __future__ import annotations

from typing import Any


# ------------------------------------------------------------------ beginner
def open_dolls(size: int) -> list[str]:
    """Russian dolls: open a doll; if there is a smaller doll inside, open that one too."""
    if size == 0:                                  # base case: nothing left inside
        return ["empty - done"]
    return [f"open doll {size}"] + open_dolls(size - 1)   # recursive case: a smaller problem


def countdown(n: int) -> list[int]:
    """Rocket launch countdown, written recursively."""
    if n == 0:
        return [0]
    return [n] + countdown(n - 1)


def countdown_loop(n: int) -> list[int]:
    result = []
    while n >= 0:
        result.append(n)
        n -= 1
    return result


# ------------------------------------------------------------------ classic small recursions
def factorial(n: int) -> int:
    """n! = n x (n - 1)!, and 0! = 1."""
    if n < 0:
        raise ValueError("factorial needs a non-negative number")
    if n == 0:
        return 1
    return n * factorial(n - 1)


def sum_list(values: list[float]) -> float:
    """The total of a list = first item + total of the rest. An empty list totals 0."""
    if not values:
        return 0
    return values[0] + sum_list(values[1:])


def largest(values: list[float]) -> float:
    """The largest item = the bigger of the first item and the largest of the rest."""
    if not values:
        raise ValueError("empty list")
    if len(values) == 1:
        return values[0]
    rest_best = largest(values[1:])
    return values[0] if values[0] > rest_best else rest_best


def reverse_text(text: str) -> str:
    """reverse('zoo') = reverse('oo') + 'z'."""
    if len(text) <= 1:
        return text
    return reverse_text(text[1:]) + text[0]


def is_palindrome(text: str) -> bool:
    """A word is a palindrome if its ends match and its middle is a palindrome."""
    if len(text) <= 1:
        return True
    if text[0] != text[-1]:
        return False
    return is_palindrome(text[1:-1])


# ------------------------------------------------------------------ recursion on nested data
Folder = dict[str, Any]   # {"files": {name: size}, "folders": {name: Folder}}


def folder_size(folder: Folder) -> int:
    """Industry example: disk usage. A folder's size = its files + the sizes of its sub-folders."""
    total = sum(folder.get("files", {}).values())
    for sub_folder in folder.get("folders", {}).values():
        total += folder_size(sub_folder)
    return total


def headcount(person: dict[str, Any]) -> int:
    """Industry example: people in an org chart = this person + everyone in each report's team."""
    return 1 + sum(headcount(report) for report in person.get("reports", []))


SAMPLE_DISK: Folder = {
    "files": {"notes.txt": 4},
    "folders": {
        "photos": {"files": {"lion.jpg": 3000, "zebra.jpg": 2800}, "folders": {}},
        "school": {
            "files": {"essay.docx": 120},
            "folders": {"maths": {"files": {"homework.pdf": 450}, "folders": {}}},
        },
    },
}

SAMPLE_ORG: dict[str, Any] = {
    "name": "Director",
    "reports": [
        {"name": "Head of Wards", "reports": [{"name": "Nurse A"}, {"name": "Nurse B"}]},
        {"name": "Head of Lab", "reports": [{"name": "Technician"}]},
        {"name": "Receptionist"},
    ],
}


if __name__ == "__main__":
    print(open_dolls(3))
    print(countdown(5))
    print("5! =", factorial(5), "| sum:", sum_list([3, 1, 4, 1, 5]), "| largest:", largest([3, 9, 2]))
    print(reverse_text("giraffe"), is_palindrome("racecar"), is_palindrome("zebra"))
    print("Disk usage (KB):", folder_size(SAMPLE_DISK))
    print("Hospital headcount:", headcount(SAMPLE_ORG))
