"""Chapter 4 - Making Decisions: Conditions, Booleans, and Decision Trees.

Run:  python3 ch04_examples.py
"""

from __future__ import annotations


def banana_advice(color: str) -> str:
    """Beginner example: should I eat this banana?"""
    color = color.lower()
    if color == "green":
        return "Wait a few days"
    elif color == "yellow":
        return "Eat it now"
    elif color == "brown":
        return "Make banana bread"
    else:
        return "Unknown color - check again"


def ticket_price(age: int) -> int:
    """Practical example: a cinema charges by age group."""
    if age < 0:
        raise ValueError("age cannot be negative")
    if age < 3:
        return 0          # babies are free
    elif age < 13:
        return 80         # child
    elif age < 60:
        return 150        # adult
    else:
        return 100        # senior


def letter_grade(score: int) -> str:
    """Practical example: a school turns marks (0-100) into a grade."""
    if not 0 <= score <= 100:
        raise ValueError("score must be between 0 and 100")
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    if score >= 40:
        return "D"
    return "F"


def is_leap_year(year: int) -> bool:
    """Practical example: calendars. Divisible by 4, except centuries, unless divisible by 400."""
    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0


def baggage_fee(weight_kg: float, is_business_class: bool) -> int:
    """Industry example: an airline's checked-bag fee."""
    allowance = 30 if is_business_class else 20
    if weight_kg <= allowance:
        return 0
    if weight_kg > 32:
        return -1  # -1 means "too heavy, must be shipped as cargo"
    extra_kg = weight_kg - allowance
    return round(extra_kg * 10)


def is_suspicious_payment(amount: float, usual_country: str, payment_country: str,
                          payments_last_hour: int) -> bool:
    """Industry example: a (very simplified) card-fraud rule used by banks."""
    big_and_foreign = amount > 50_000 and payment_country != usual_country
    too_many = payments_last_hour > 10
    return big_and_foreign or too_many


def triage_level(breathing_ok: bool, bleeding_heavily: bool, pain_score: int) -> str:
    """Industry example: hospital emergency triage (simplified for teaching)."""
    if not breathing_ok or bleeding_heavily:
        return "RED - see immediately"
    if pain_score >= 7:
        return "YELLOW - see within 30 minutes"
    return "GREEN - see within 2 hours"


def read_age_safely(text: str) -> int | None:
    """Check input before trusting it. Returns None if the text is not a whole number."""
    text = text.strip()
    if text.isdigit():
        return int(text)
    return None


if __name__ == "__main__":
    print(banana_advice("Yellow"))
    for age in (2, 10, 35, 70):
        print(f"Age {age}: ticket costs {ticket_price(age)}")
    print("Grade for 82:", letter_grade(82))
    print("Is 2024 a leap year?", is_leap_year(2024), "| 1900?", is_leap_year(1900))
    print("Bag of 24 kg, economy:", baggage_fee(24, False))
    print("Suspicious?", is_suspicious_payment(80_000, "India", "Brazil", 1))
    print("Triage:", triage_level(True, False, 8))
    print("Reading 'twelve':", read_age_safely("twelve"))
