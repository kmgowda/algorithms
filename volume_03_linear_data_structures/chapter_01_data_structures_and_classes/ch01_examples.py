"""Volume 3, Chapter 1 - What Is a Data Structure? Classes, Interfaces, and Invariants.

Run:  python3 ch01_examples.py
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator


# ------------------------------------------------------------------ beginner: a first class
class Animal:
    """A blueprint for zoo animals. Each Animal object has its own name, species, and meals."""

    def __init__(self, name: str, species: str) -> None:
        self.name = name              # attributes: data stored inside each object
        self.species = species
        self.meals_today = 0

    def feed(self) -> None:           # a method: a function that belongs to the object
        self.meals_today += 1

    def describe(self) -> str:
        return f"{self.name} the {self.species} has eaten {self.meals_today} meal(s)"


# ------------------------------------------------------------------ dataclass: less typing for simple records
@dataclass
class Book:
    title: str
    author: str
    year: int


# ------------------------------------------------------------------ industry: an invariant protected by methods
class BankAccount:
    """Invariant: the balance is never negative. Only the methods change it, and they check."""

    def __init__(self, owner: str, opening_balance: int = 0) -> None:
        if opening_balance < 0:
            raise ValueError("opening balance cannot be negative")
        self.owner = owner
        self._balance = opening_balance           # leading underscore: "please don't touch directly"
        self._history: list[str] = []

    @property
    def balance(self) -> int:                     # read-only view of the balance
        return self._balance

    def deposit(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self._balance += amount
        self._history.append(f"+{amount}")

    def withdraw(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("withdrawal must be positive")
        if amount > self._balance:
            raise ValueError("insufficient funds")
        self._balance -= amount
        self._history.append(f"-{amount}")

    def history(self) -> list[str]:
        return list(self._history)                # a copy, so callers can't change our records

    def __repr__(self) -> str:                    # how the object prints
        return f"BankAccount(owner={self.owner!r}, balance={self._balance})"


# ------------------------------------------------------------------ one interface, two implementations
class ListBag:
    """A 'bag' (multiset) of fruit stored as a plain list: add O(1), count O(n)."""

    def __init__(self) -> None:
        self._items: list[str] = []

    def add(self, item: str) -> None:
        self._items.append(item)

    def count(self, item: str) -> int:
        return sum(1 for x in self._items if x == item)

    def __len__(self) -> int:
        return len(self._items)

    def __contains__(self, item: str) -> bool:
        return item in self._items

    def __iter__(self) -> Iterator[str]:
        return iter(self._items)


class CountingBag:
    """The same interface stored as a dictionary of counts: add O(1), count O(1)."""

    def __init__(self) -> None:
        self._counts: dict[str, int] = {}
        self._size = 0

    def add(self, item: str) -> None:
        self._counts[item] = self._counts.get(item, 0) + 1
        self._size += 1

    def count(self, item: str) -> int:
        return self._counts.get(item, 0)

    def __len__(self) -> int:
        return self._size

    def __contains__(self, item: str) -> bool:
        return item in self._counts

    def __iter__(self) -> Iterator[str]:
        for item, times in self._counts.items():
            for _ in range(times):
                yield item


def fill_bag(bag: ListBag | CountingBag, fruits: list[str]) -> ListBag | CountingBag:
    """Code written against the INTERFACE works with either implementation."""
    for fruit in fruits:
        bag.add(fruit)
    return bag


if __name__ == "__main__":
    leo = Animal("Leo", "lion")
    leo.feed()
    leo.feed()
    print(leo.describe())
    print(Book("Matilda", "Roald Dahl", 1988))
    account = BankAccount("Maya", 100)
    account.deposit(50)
    account.withdraw(30)
    print(account, account.history())
    try:
        account.withdraw(1000)
    except ValueError as error:
        print("Refused:", error)
    fruits = ["apple", "mango", "apple", "kiwi", "apple"]
    for bag in (fill_bag(ListBag(), fruits), fill_bag(CountingBag(), fruits)):
        print(type(bag).__name__, len(bag), bag.count("apple"), "kiwi" in bag, sorted(bag))
