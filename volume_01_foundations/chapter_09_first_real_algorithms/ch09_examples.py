"""Chapter 9 - Your First Real Algorithms: Counting, Finding the Biggest, and Linear Search.

Run:  python3 ch09_examples.py
"""

from __future__ import annotations



# ------------------------------------------------------------------ find the biggest
def tallest(heights: list[float]) -> float:
    """Beginner example: find the tallest giraffe.

    Promise kept after every step (the loop invariant):
    `best` is the tallest height among the giraffes looked at so far.
    """
    if not heights:
        raise ValueError("no giraffes to measure")
    best = heights[0]
    for height in heights[1:]:
        if height > best:
            best = height
    return best


def index_of_cheapest(prices: list[float]) -> int:
    """Practical example: which bus company sells the cheapest ticket? Returns the position."""
    if not prices:
        raise ValueError("no prices given")
    best_index = 0
    for i in range(1, len(prices)):
        if prices[i] < prices[best_index]:
            best_index = i
    return best_index


def top_student(scores: dict[str, int]) -> tuple[str, int]:
    """Practical example: the class top scorer (ties go to the name seen first)."""
    if not scores:
        raise ValueError("no students")
    best_name = ""
    best_score = -1
    for name, score in scores.items():
        if score > best_score:
            best_name, best_score = name, score
    return best_name, best_score


def two_largest(values: list[int]) -> tuple[int, int]:
    """One pass, two 'best so far' variables: the largest and the second largest."""
    if len(values) < 2:
        raise ValueError("need at least two values")
    first, second = (values[0], values[1]) if values[0] >= values[1] else (values[1], values[0])
    for value in values[2:]:
        if value > first:
            first, second = value, first
        elif value > second:
            second = value
    return first, second


# ------------------------------------------------------------------ linear search
def linear_search(items: list[str], target: str) -> int:
    """Look at each item in turn. Return the index of the first match, or -1 if absent."""
    for index in range(len(items)):
        if items[index] == target:
            return index          # found: stop immediately
    return -1                     # looked at everything: not there


def linear_search_counting(items: list[str], target: str) -> tuple[int, int]:
    """Same search, but also report how many comparisons it needed."""
    comparisons = 0
    for index, item in enumerate(items):
        comparisons += 1
        if item == target:
            return index, comparisons
    return -1, comparisons


def find_all(items: list[str], target: str) -> list[int]:
    """Every position where target appears (cannot stop early)."""
    return [index for index, item in enumerate(items) if item == target]


def find_patient(records: list[dict[str, str]], patient_id: str) -> dict[str, str] | None:
    """Industry example: search an unsorted list of hospital records by ID."""
    for record in records:
        if record["id"] == patient_id:
            return record
    return None


# ------------------------------------------------------------------ yes/no questions over a list
def any_overdrawn(balances: list[float]) -> bool:
    """Industry example: does ANY account have a negative balance? Stop at the first one."""
    for balance in balances:
        if balance < 0:
            return True
    return False


def all_vaccinated(animals: dict[str, bool]) -> bool:
    """Practical example: are ALL the zoo animals vaccinated? Stop at the first 'no'."""
    for vaccinated in animals.values():
        if not vaccinated:
            return False
    return True


def cheapest_seller(offers: list[tuple[str, float, bool]]) -> str | None:
    """Industry example: a shopping site picks the cheapest seller that has stock.

    Each offer is (seller, price, in_stock). Combines filtering with 'best so far'.
    """
    best_seller = None
    best_price = float("inf")      # infinity: any real price is smaller
    for seller, price, in_stock in offers:
        if in_stock and price < best_price:
            best_seller, best_price = seller, price
    return best_seller


def running_average(values: list[float]) -> list[float]:
    """A sensor dashboard: the average of everything seen so far, after each reading."""
    averages = []
    total = 0.0
    for count, value in enumerate(values, start=1):
        total += value
        averages.append(round(total / count, 2))
    return averages


if __name__ == "__main__":
    print("Tallest giraffe:", tallest([4.8, 5.6, 5.1, 5.9, 4.3]))
    print("Cheapest bus is at index", index_of_cheapest([120, 95, 110, 95]))
    print("Top student:", top_student({"Ana": 88, "Ben": 92, "Cy": 92}))
    print("Two largest:", two_largest([3, 9, 4, 9, 1]))
    shelf = ["Matilda", "Holes", "Wonder", "Coraline", "Holes"]
    print("Linear search for Wonder:", linear_search(shelf, "Wonder"))
    print("With comparisons:", linear_search_counting(shelf, "Dune"))
    print("All Holes:", find_all(shelf, "Holes"))
    records = [{"id": "P7", "name": "Ana"}, {"id": "P3", "name": "Ben"}]
    print("Patient P3:", find_patient(records, "P3"))
    print("Any overdrawn?", any_overdrawn([200.0, 15.5, -3.0, 80.0]))
    print("All vaccinated?", all_vaccinated({"lion": True, "otter": False}))
    print("Cheapest in stock:", cheapest_seller([("A", 499, False), ("B", 520, True), ("C", 510, True)]))
    print("Running average:", running_average([20, 22, 27, 19]))
