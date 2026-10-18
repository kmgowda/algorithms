"""Chapter 8 - Solutions to the exercises."""

from __future__ import annotations


def count_vowels_by_letter(text: str) -> dict[str, int]:
    """Exercise 1: how many of each vowel?"""
    counts = {vowel: 0 for vowel in "aeiou"}
    for ch in text.lower():
        if ch in counts:
            counts[ch] += 1
    return counts


def are_anagrams(first: str, second: str) -> bool:
    """Exercise 2: same letters, same counts ('listen' / 'silent'), ignoring spaces and case."""
    def letter_counts(text: str) -> dict[str, int]:
        counts: dict[str, int] = {}
        for ch in text.lower():
            if ch != " ":
                counts[ch] = counts.get(ch, 0) + 1
        return counts
    return letter_counts(first) == letter_counts(second)


def title_case(sentence: str) -> str:
    """Exercise 3: capitalize the first letter of each word."""
    return " ".join(word[:1].upper() + word[1:].lower() for word in sentence.split())


def invert_phone_book(book: dict[str, str]) -> dict[str, str]:
    """Exercise 4: name -> number becomes number -> name (reverse lookup)."""
    return {number: name for name, number in book.items()}


def first_repeated(items: list[str]) -> str | None:
    """Exercise 5: the first item seen twice, using a set of things already seen."""
    seen: set[str] = set()
    for item in items:
        if item in seen:
            return item
        seen.add(item)
    return None


def compress(text: str) -> str:
    """Exercise 6: 'aaabccdddd' -> 'a3b1c2d4'. Build pieces in a list, then join once."""
    if not text:
        return ""
    pieces: list[str] = []
    current = text[0]
    run = 1
    for ch in text[1:]:
        if ch == current:
            run += 1
        else:
            pieces.append(f"{current}{run}")
            current, run = ch, 1
    pieces.append(f"{current}{run}")
    return "".join(pieces)


def books_due(loans: dict[str, int], today: int) -> list[str]:
    """Exercise 7: a library dict of title -> due day; which are overdue?"""
    return sorted(title for title, due in loans.items() if due < today)


if __name__ == "__main__":
    print(count_vowels_by_letter("Elephant and Iguana"))
    print(are_anagrams("Listen", "Silent"), title_case("the jungle BOOK"))
    print(invert_phone_book({"Ana": "555-01", "Ben": "555-02"}))
    print(first_repeated(["lion", "zebra", "otter", "zebra"]), compress("aaabccdddd"))
    print(books_due({"Matilda": 10, "Holes": 14, "Wonder": 9}, 11))
