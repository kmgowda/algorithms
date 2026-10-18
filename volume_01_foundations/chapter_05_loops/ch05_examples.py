"""Chapter 5 - Repeating Work: Loops.

Run:  python3 ch05_examples.py
"""

from __future__ import annotations


def count_sheep(how_many: int) -> str:
    """Beginner example: a for loop counting sheep to fall asleep."""
    words = ""
    for sheep in range(1, how_many + 1):
        words += f"{sheep} sheep... "
    return words + "Zzz"


def bus_countdown(stops: int) -> list[str]:
    """Practical example: a while loop announcing stops until we arrive."""
    announcements = []
    while stops > 0:
        announcements.append(f"{stops} stops to go")
        stops -= 1
    announcements.append("This is your stop!")
    return announcements


def times_table(number: int, up_to: int = 10) -> str:
    """Practical example: a multiplication table, one line per row."""
    lines = []
    for i in range(1, up_to + 1):
        lines.append(f"{number} x {i} = {number * i}")
    return "\n".join(lines)


def sum_up_to(n: int) -> int:
    """The accumulator pattern: add 1 + 2 + ... + n."""
    total = 0
    for value in range(1, n + 1):
        total += value
    return total


def count_letter(text: str, letter: str) -> int:
    """The counter pattern: how many times does a letter appear?"""
    count = 0
    for character in text:
        if character == letter:
            count += 1
    return count


def years_to_reach(start: float, target: float, yearly_rate_percent: float) -> int:
    """Industry example: how many years until savings reach a goal (compound interest)?"""
    if yearly_rate_percent <= 0 and start < target:
        raise ValueError("savings will never reach the target without interest")
    years = 0
    balance = start
    while balance < target:
        balance += balance * yearly_rate_percent / 100
        years += 1
    return years


def connect_with_retries(responses: list[bool], max_attempts: int = 5) -> tuple[bool, list[int]]:
    """Industry example: retrying a failed network request with growing waits.

    `responses` pretends to be the server's answers, attempt by attempt.
    Returns (succeeded, waits_used). Real systems really sleep; we just record the waits.
    """
    waits: list[int] = []
    wait_seconds = 1
    for attempt in range(max_attempts):
        if attempt < len(responses) and responses[attempt]:
            return True, waits
        waits.append(wait_seconds)
        wait_seconds *= 2           # 1, 2, 4, 8, ... (exponential backoff)
    return False, waits


def check_pin(attempts: list[str], correct_pin: str, max_tries: int = 3) -> str:
    """Using break: stop the loop the moment the PIN is right."""
    result = "Card blocked"
    tries = 0
    for pin in attempts:
        tries += 1
        if tries > max_tries:
            break                   # out of chances: leave the loop
        if pin == correct_pin:
            result = f"Welcome! (try {tries})"
            break                   # correct: no need to keep checking
    return result


def skip_closed_days(days: list[str]) -> list[str]:
    """Using continue: skip Mondays, when the zoo is closed."""
    open_days = []
    for day in days:
        if day == "Monday":
            continue
        open_days.append(day)
    return open_days


def seating_chart(rows: int, seats_per_row: int) -> list[str]:
    """Nested loops: every seat label in a cinema, like A1, A2, ... B1, ..."""
    labels = []
    for row in range(rows):
        row_letter = chr(ord("A") + row)
        for seat in range(1, seats_per_row + 1):
            labels.append(f"{row_letter}{seat}")
    return labels


def plant_growth(height_cm: float, days: int) -> float:
    """Practical example: a plant grows 10 percent of its height each day."""
    for _ in range(days):
        height_cm *= 1.10
    return round(height_cm, 2)


if __name__ == "__main__":
    print(count_sheep(5))
    print("\n".join(bus_countdown(3)))
    print(times_table(7, 5))
    print("1 + ... + 100 =", sum_up_to(100))
    print("a's in banana:", count_letter("banana", "a"))
    print("Years to double 1000 at 7%:", years_to_reach(1000, 2000, 7))
    print("Retries:", connect_with_retries([False, False, True]))
    print(check_pin(["1111", "4321", "1234"], "4321"))
    print(skip_closed_days(["Sunday", "Monday", "Tuesday"]))
    print(seating_chart(2, 3))
    print("Plant after 7 days:", plant_growth(10, 7), "cm")
