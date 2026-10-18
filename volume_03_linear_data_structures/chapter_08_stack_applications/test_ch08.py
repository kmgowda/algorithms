import itertools
import random
import unittest

import ch08_examples as ex
import ch08_solutions as sol


class TestExpressions(unittest.TestCase):
    def test_tokenize(self) -> None:
        self.assertEqual(ex.tokenize("12 + 3*(4-1)"), ["12", "+", "3", "*", "(", "4", "-", "1", ")"])
        with self.assertRaises(ValueError):
            ex.tokenize("2 $ 3")

    def test_postfix(self) -> None:
        self.assertEqual(ex.evaluate_postfix(["3", "4", "+", "2", "*"]), 14)
        with self.assertRaises(ValueError):
            ex.evaluate_postfix(["3", "+"])
        with self.assertRaises(ValueError):
            ex.evaluate_postfix(["3", "4"])

    def test_shunting_yard(self) -> None:
        self.assertEqual(ex.infix_to_postfix(ex.tokenize("12 + 3*(4-1)")), ["12", "3", "4", "1", "-", "*", "+"])
        self.assertEqual(ex.infix_to_postfix(ex.tokenize("8-3-2")), ["8", "3", "-", "2", "-"])
        with self.assertRaises(ValueError):
            ex.infix_to_postfix(ex.tokenize("(1+2"))
        with self.assertRaises(ValueError):
            ex.infix_to_postfix(ex.tokenize("1+2)"))

    def test_calculator_matches_python(self) -> None:
        rng = random.Random(3)
        for _ in range(300):
            parts = [str(rng.randint(1, 20))]
            for _ in range(rng.randint(0, 5)):
                parts += [rng.choice("+-*/"), str(rng.randint(1, 20))]
            if rng.random() < 0.5 and len(parts) >= 3:
                parts = ["("] + parts[:3] + [")"] + parts[3:]
            expression = " ".join(parts)
            self.assertAlmostEqual(ex.calculate(expression), eval(expression), places=9)


class TestMonotonic(unittest.TestCase):
    def brute_next_greater(self, values: list[int]) -> list[int]:
        return [next((v for v in values[i + 1:] if v > x), -1) for i, x in enumerate(values)]

    def test_next_greater_and_warmer(self) -> None:
        rng = random.Random(8)
        for _ in range(300):
            values = [rng.randint(0, 20) for _ in range(rng.randint(0, 15))]
            self.assertEqual(ex.next_greater(values), self.brute_next_greater(values))
            warmer = [next((j - i for j in range(i + 1, len(values)) if values[j] > values[i]), 0)
                      for i in range(len(values))]
            self.assertEqual(ex.days_until_warmer(values), warmer)

    def test_stock_span(self) -> None:
        self.assertEqual(ex.stock_span([100, 80, 60, 70, 60, 75, 85]), [1, 1, 1, 2, 1, 4, 6])
        rng = random.Random(1)
        for _ in range(200):
            prices = [rng.randint(1, 10) for _ in range(rng.randint(0, 12))]
            brute = []
            for i, p in enumerate(prices):
                span = 1
                while i - span >= 0 and prices[i - span] <= p:
                    span += 1
                brute.append(span)
            self.assertEqual(ex.stock_span(prices), brute)


class TestSolutions(unittest.TestCase):
    def test_rpn(self) -> None:
        self.assertEqual(sol.evaluate_rpn(["2", "1", "+", "3", "*"]), 9)
        self.assertEqual(sol.evaluate_rpn(["4", "13", "5", "/", "+"]), 6)
        self.assertEqual(sol.evaluate_rpn(["-7", "2", "/"]), -3)

    def test_previous_smaller(self) -> None:
        self.assertEqual(sol.previous_smaller([4, 5, 2, 10, 8]), [-1, 4, -1, 2, 2])

    def test_rectangle(self) -> None:
        rng = random.Random(5)
        for _ in range(200):
            h = [rng.randint(0, 9) for _ in range(rng.randint(0, 10))]
            brute = max([min(h[i:j + 1]) * (j - i + 1) for i in range(len(h)) for j in range(i, len(h))] + [0])
            self.assertEqual(sol.largest_rectangle(h), brute)

    def test_remove_k_digits(self) -> None:
        self.assertEqual(sol.remove_k_digits("1432219", 3), "1219")
        self.assertEqual(sol.remove_k_digits("10200", 1), "200")
        self.assertEqual(sol.remove_k_digits("10", 2), "0")
        for number in ("52913", "11111", "90210"):
            for k in range(len(number) + 1):
                best = min(("".join(c).lstrip("0") or "0" for c in itertools.combinations(number, len(number) - k)),
                           key=lambda s: (len(s), s)) if k < len(number) else "0"
                self.assertEqual(sol.remove_k_digits(number, k), best)


if __name__ == "__main__":
    unittest.main()
