"""Chapter 2 - How a Computer Thinks.

Part 1 is your very first Python program: just print statements and arithmetic.
Part 2 is a sneak peek: a *pretend* computer (a "toy CPU") written in Python,
so you can watch the fetch -> decode -> execute cycle step by step.

Run:  python3 ch02_examples.py
"""

from __future__ import annotations


def first_program() -> None:
    """Your first program: the computer as a very fast, very obedient calculator."""
    print("Hello, World!")
    print("Hello from the zoo!")
    print(2 + 3)          # addition
    print(10 - 4)         # subtraction
    print(6 * 7)          # multiplication
    print(20 / 8)         # division gives a decimal answer: 2.5
    print(20 // 8)        # whole-number division: 2
    print(20 % 8)         # remainder after division: 4
    print(2 ** 10)        # power: 2 multiplied by itself 10 times = 1024
    print("Seconds in one day:", 24 * 60 * 60)


def to_binary(number: int) -> str:
    """Show how a whole number looks as bits (0s and 1s) inside the computer."""
    if number < 0:
        raise ValueError("this simple version handles only zero and positive numbers")
    return bin(number)[2:]


def run_tiny_computer(program: list[tuple[str, ...]], trace: bool = False) -> dict[str, int]:
    """A toy CPU with named memory boxes.

    Each instruction is a tuple such as ("SET", "apples", "5") or ("ADD", "total", "apples", "pears").
    The CPU fetches one instruction, decodes what it means, executes it, then moves on.

    Supported instructions:
      SET  box value          put a number into a memory box
      ADD  box a b            box = a + b
      SUB  box a b            box = a - b
      MUL  box a b            box = a * b
      PRINT box               show the value in a box
    """
    memory: dict[str, int] = {}
    counter = 0  # which instruction to run next (real CPUs call this the program counter)
    while counter < len(program):
        instruction = program[counter]                 # FETCH
        operation, *arguments = instruction            # DECODE
        if operation == "SET":                         # EXECUTE
            memory[arguments[0]] = int(arguments[1])
        elif operation in ("ADD", "SUB", "MUL"):
            left, right = memory[arguments[1]], memory[arguments[2]]
            if operation == "ADD":
                memory[arguments[0]] = left + right
            elif operation == "SUB":
                memory[arguments[0]] = left - right
            else:
                memory[arguments[0]] = left * right
        elif operation == "PRINT":
            print(f"{arguments[0]} = {memory[arguments[0]]}")
        else:
            raise ValueError(f"unknown instruction: {operation}")
        if trace:
            print(f"  after step {counter + 1} {instruction}: memory = {memory}")
        counter += 1
    return memory


FRUIT_SHOP_PROGRAM: list[tuple[str, ...]] = [
    ("SET", "apples", "5"),
    ("SET", "pears", "3"),
    ("ADD", "fruits", "apples", "pears"),
    ("SET", "price", "20"),
    ("MUL", "bill", "fruits", "price"),
    ("PRINT", "bill"),
]


if __name__ == "__main__":
    first_program()
    print("13 in binary is", to_binary(13))
    print("\nRunning the tiny computer:")
    run_tiny_computer(FRUIT_SHOP_PROGRAM, trace=True)
