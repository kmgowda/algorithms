import random
import unittest

import ch17_solutions as sol


def brute_force(operations: list[str], bits: int = 8) -> tuple[list[int], int]:
    """Keep the count as a whole number; a reset simply sets it to 0. Returns (lamps, number of increments)."""
    value, incs = 0, 0
    for op in operations:
        if op == "inc":
            value = (value + 1) % (2 ** bits)
            incs += 1
        else:
            value = 0
    return [(value >> k) & 1 for k in range(bits)], incs


class TestChapter17Solutions(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.run_counter([]), ([0] * 8, []))
        self.assertEqual(sol.run_counter(["reset"]), ([0] * 8, [0]))
        self.assertEqual(sol.run_counter(["inc"]), ([1] + [0] * 7, [1]))
        self.assertEqual(sol.run_counter(["inc", "reset"]), ([0] * 8, [1, 1]))
        self.assertEqual(sol.run_counter(["reset", "reset"], bits=1), ([0], [0, 0]))

    def test_worked_example(self) -> None:
        lamps, costs = sol.run_counter(["inc"] * 13 + ["reset"] + ["inc"] * 3 + ["reset"])
        self.assertEqual(lamps, [0] * 8)
        self.assertEqual(costs[13], 4)
        self.assertEqual(costs[-1], 2)
        self.assertEqual(sum(costs), 33)

    def test_wrap_round(self) -> None:
        lamps, costs = sol.run_counter(["inc"] * 4 + ["reset"], bits=2)
        self.assertEqual((lamps, costs), ([0, 0], [1, 2, 1, 2, 0]))

    def test_against_brute_force(self) -> None:
        rng = random.Random(17)
        for _ in range(400):
            ops = [rng.choice(["inc", "inc", "inc", "reset"]) for _ in range(rng.randint(0, 60)) ]
            lamps, costs = sol.run_counter(ops, bits=8)
            expected, incs = brute_force(ops, bits=8)
            self.assertEqual(lamps, expected)
            self.assertLessEqual(sum(costs), 3 * incs)
            self.assertLessEqual(sum(costs), 3 * len(ops))


if __name__ == "__main__":
    unittest.main()
