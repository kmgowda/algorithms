"""Chapter 8 - Organizing Information: Strings, Dictionaries, and Sets.

Run:  python3 ch08_examples.py
"""

from __future__ import annotations


# ------------------------------------------------------------------ strings
def string_tour(sentence: str) -> dict[str, object]:
    """Common string operations on one sentence."""
    return {
        "upper": sentence.upper(),
        "words": sentence.split(),
        "first_word": sentence.split()[0] if sentence.split() else "",
        "has_zoo": "zoo" in sentence.lower(),
        "position_of_zoo": sentence.lower().find("zoo"),   # -1 if not found
        "replaced": sentence.replace("cats", "dogs"),
        "initials": "".join(word[0].upper() for word in sentence.split()),
    }


def is_palindrome(text: str) -> bool:
    """Practical example: reads the same forwards and backwards, ignoring case and non-letters."""
    letters = [ch.lower() for ch in text if ch.isalnum()]
    return letters == letters[::-1]


def make_username(full_name: str, birth_year: int) -> str:
    """Practical example: a school portal builds usernames like 'maya.rao2012'."""
    parts = full_name.strip().lower().split()
    return ".".join(parts) + str(birth_year)


# ------------------------------------------------------------------ dictionaries
def animal_sounds_demo() -> dict[str, str]:
    """Beginner example: a dictionary maps a key (animal) to a value (sound)."""
    sounds = {"dog": "woof", "cat": "meow", "cow": "moo"}
    sounds["duck"] = "quack"         # add a new key
    sounds["dog"] = "bark"           # change an existing key's value
    del sounds["cow"]                # remove a key
    return sounds


def word_frequencies(text: str) -> dict[str, int]:
    """Practical example: count how often each word appears (the counting pattern)."""
    counts: dict[str, int] = {}
    for word in text.lower().split():
        word = word.strip(".,!?;:\"'")
        if word:
            counts[word] = counts.get(word, 0) + 1
    return counts


def most_common_word(text: str) -> str | None:
    counts = word_frequencies(text)
    best_word = None
    best_count = 0
    for word, count in counts.items():
        if count > best_count:
            best_word, best_count = word, count
    return best_word


def group_by_first_letter(names: list[str]) -> dict[str, list[str]]:
    """The grouping pattern: each key holds a list."""
    groups: dict[str, list[str]] = {}
    for name in names:
        key = name[0].upper()
        if key not in groups:
            groups[key] = []
        groups[key].append(name)
    return groups


def restock_report(stock: dict[str, int], sold: dict[str, int], minimum: int = 5) -> list[str]:
    """Industry example: a shop's inventory system - which products need restocking?"""
    low = []
    for product, quantity in stock.items():
        remaining = quantity - sold.get(product, 0)
        if remaining < minimum:
            low.append(f"{product}: {remaining} left")
    return sorted(low)


# ------------------------------------------------------------------ sets
def unique_visitors(visits: list[str]) -> int:
    """A set keeps only one copy of each value."""
    return len(set(visits))


def is_username_available(taken: set[str], wanted: str) -> bool:
    """Industry example: sign-up pages check names instantly with a set."""
    return wanted.lower() not in taken


def mutual_friends(friends_a: set[str], friends_b: set[str]) -> set[str]:
    """Industry example: a social network's 'mutual friends' is a set intersection."""
    return friends_a & friends_b


def club_overview(chess: set[str], music: set[str]) -> dict[str, set[str]]:
    """Practical example: school clubs and the four classic set operations."""
    return {
        "both": chess & music,             # intersection
        "either": chess | music,           # union
        "only_chess": chess - music,       # difference
        "exactly_one": chess ^ music,      # symmetric difference
    }


if __name__ == "__main__":
    print(string_tour("My cats love the city zoo"))
    print(is_palindrome("Was it a car or a cat I saw?"), make_username("  Maya Rao ", 2012))
    print(animal_sounds_demo())
    story = "The lion saw the zebra. The zebra saw the lion and ran!"
    print(word_frequencies(story), most_common_word(story))
    print(group_by_first_letter(["Ana", "Ben", "Alex", "Bea", "Cy"]))
    print(restock_report({"milk": 20, "bread": 8, "eggs": 30}, {"milk": 17, "eggs": 5}))
    print(unique_visitors(["ana", "ben", "ana", "cy", "ben"]))
    print(is_username_available({"maya", "leo"}, "Maya"))
    print(mutual_friends({"Ana", "Ben", "Cy"}, {"Ben", "Cy", "Dev"}))
    print(club_overview({"Ana", "Ben", "Cy"}, {"Cy", "Dev"}))
