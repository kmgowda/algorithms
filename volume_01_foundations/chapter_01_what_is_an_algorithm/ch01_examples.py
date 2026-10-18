"""Chapter 1 - What Is an Algorithm?

These programs are a *sneak peek*. You do not need to understand every line yet.
Chapters 3-6 explain each piece. For now, run the file and compare what it prints
with the algorithms written in plain English in the chapter.

Run:  python3 ch01_examples.py
"""

from __future__ import annotations


def lemonade_steps(glasses: int) -> list[str]:
    """Beginner example: the lemonade algorithm, written as precise steps.

    Input:  how many glasses of lemonade we want.
    Output: the exact list of steps to follow.
    """
    if glasses < 1:
        return ["Nothing to make."]
    lemons = 2 * glasses
    spoons_of_sugar = 2 * glasses
    return [
        f"Take {lemons} lemons.",
        "Cut every lemon in half.",
        "Squeeze every half into a jug.",
        f"Add {glasses * 250} ml of cold water.",
        f"Add {spoons_of_sugar} spoons of sugar.",
        "Stir 20 times.",
        f"Pour into {glasses} glasses.",
    ]


def bus_or_walk(minutes_until_bus: int, minutes_until_school_starts: int) -> str:
    """Practical example: deciding how to get to school.

    The bus ride takes 10 minutes. Walking takes 25 minutes.
    """
    bus_ride = 10
    walk = 25
    if minutes_until_bus + bus_ride <= minutes_until_school_starts:
        return "Take the bus"
    if walk <= minutes_until_school_starts:
        return "Walk"
    return "Call a parent for a ride"


def atm_withdraw(balance: int, pin_ok: bool, amount: int) -> tuple[str, int]:
    """Industry example: a simplified ATM cash-withdrawal algorithm.

    Returns a message and the new balance. Real ATMs check much more,
    but the shape of the algorithm is the same.
    """
    if not pin_ok:
        return "Wrong PIN. Card returned.", balance
    if amount <= 0 or amount % 100 != 0:
        return "Amount must be a positive multiple of 100.", balance
    if amount > balance:
        return "Insufficient funds.", balance
    return f"Please take your {amount}.", balance - amount


def find_book_shelf(title: str) -> str:
    """Practical example: a library shelving rule.

    Books are shelved by the first letter of the title:
    A-H on shelf 1, I-P on shelf 2, Q-Z on shelf 3.
    """
    first = title.strip()[:1].upper()
    if not first.isalpha():
        return "Ask the librarian"
    if first <= "H":
        return "Shelf 1"
    if first <= "P":
        return "Shelf 2"
    return "Shelf 3"


def delivery_eta(distance_km: float, rider_speed_kmh: float, cooking_minutes: int) -> int:
    """Industry example: a food-delivery app estimating arrival time in minutes."""
    if rider_speed_kmh <= 0:
        raise ValueError("speed must be positive")
    travel_minutes = distance_km / rider_speed_kmh * 60
    return round(cooking_minutes + travel_minutes)


if __name__ == "__main__":
    print("Lemonade for 3 glasses:")
    for number, step in enumerate(lemonade_steps(3), start=1):
        print(f"  Step {number}: {step}")
    print("Bus or walk (bus in 5 min, school in 20 min):", bus_or_walk(5, 20))
    print("ATM:", atm_withdraw(balance=1000, pin_ok=True, amount=300))
    print("Library: 'Jungle Book' goes to", find_book_shelf("Jungle Book"))
    print("Delivery ETA:", delivery_eta(4, 20, 15), "minutes")
