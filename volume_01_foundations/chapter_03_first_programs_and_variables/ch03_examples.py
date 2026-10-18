"""Chapter 3 - Talking to the Computer: Your First Python Programs and Variables.

Each example is wrapped in a function (explained in Chapter 6) so it can be tested.
Inside each function you will find exactly the plain statements shown in the chapter.

Run:  python3 ch03_examples.py
"""

from __future__ import annotations


def animal_profile() -> str:
    """Beginner example: variables as labeled boxes."""
    animal = "Giraffe"          # str  - text
    legs = 4                    # int  - whole number
    height_m = 5.5              # float - number with a decimal point
    is_mammal = True            # bool - True or False
    return f"{animal}: {legs} legs, {height_m} m tall, mammal: {is_mammal}"


def bus_fare(adults: int, children: int) -> int:
    """Practical example: a city bus charges 30 per adult and 15 per child."""
    adult_price = 30
    child_price = 15
    total = adults * adult_price + children * child_price
    return total


def celsius_to_fahrenheit(celsius: float) -> float:
    """Practical example: converting temperature for a weather display."""
    fahrenheit = celsius * 9 / 5 + 32
    return fahrenheit


def savings_after_one_year(deposit: float, yearly_rate_percent: float) -> float:
    """Industry example: a bank account earning simple yearly interest."""
    interest = deposit * yearly_rate_percent / 100
    balance = deposit + interest
    return round(balance, 2)


def cart_total(item_price: float, quantity: int, discount_percent: float, tax_percent: float) -> float:
    """Industry example: how an online shop computes the final bill.

    Order matters: the discount is applied first, then tax on the discounted amount.
    """
    subtotal = item_price * quantity
    discount = subtotal * discount_percent / 100
    after_discount = subtotal - discount
    tax = after_discount * tax_percent / 100
    return round(after_discount + tax, 2)


def swap_seats(seat_a: str, seat_b: str) -> tuple[str, str]:
    """Two friends swap seats: the classic 'use a temporary box' trick."""
    temporary = seat_a
    seat_a = seat_b
    seat_b = temporary
    return seat_a, seat_b


def greet_from_input() -> str:
    """Reading input from the keyboard. input() always gives back text (str)."""
    name = input("What is your name? ")
    age_text = input("How old are you? ")
    age = int(age_text)             # convert text "12" into the number 12
    return f"Hello {name}! Next year you will be {age + 1}."


if __name__ == "__main__":
    print(animal_profile())
    print("Bus fare for 2 adults, 3 children:", bus_fare(2, 3))
    print("30 C in Fahrenheit:", celsius_to_fahrenheit(30))
    print("Savings:", savings_after_one_year(1000, 5))
    print("Cart total:", cart_total(499.0, 2, 10, 18))
    print("Swapped:", swap_seats("Ana", "Ben"))
    print(type(4), type(5.5), type("Giraffe"), type(True))
