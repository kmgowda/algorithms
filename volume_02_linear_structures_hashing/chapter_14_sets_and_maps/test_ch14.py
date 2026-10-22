import random
import unittest
from collections import Counter

import ch14_examples as ex


class TestChapter32(unittest.TestCase):
    def test_every_case(self) -> None:
        self.assertEqual((ex.count_loans([]), ex.count_loans(["maps", "Maps"])), ({}, {"maps": 1, "Maps": 1}))
        self.assertEqual((ex.group_by([], len), ex.group_by(["a", "bb", "cc"], len)), ({}, {1: ["a"], 2: ["bb", "cc"]}))
        self.assertEqual((ex.intersection(set(), ex.POETRY), ex.intersection({"Ana"}, {"Ben"})), (set(), set()))
        self.assertEqual((ex.intersection(ex.POETRY, ex.POETRY), ex.intersection({"Cai"}, ex.SCIENCE)), (ex.POETRY, {"Cai"}))
        self.assertEqual(ex.reminders_fast([], ["x"]), {})
        self.assertEqual(ex.reminders_fast([("Ana", "A"), ("Ana", "B"), ("Ben", "C")], []), {"Ana": ["A", "B"], "Ben": ["C"]})
        self.assertEqual(ex.reminders_fast([("Ana", "A")], ["Ana"]), {})
        self.assertEqual(ex.reminders_fast([("Ana", "A"), ("Ana", "A")], []), {"Ana": ["A", "A"]})

    def test_everything(self) -> None:
        self.assertEqual(ex.intersection(ex.POETRY, ex.SCIENCE), {"Cai", "Dev"})
        rng = random.Random(1)
        for _ in range(200):
            a = {rng.randint(0, 30) for _ in range(rng.randint(0, 15))}
            b = {rng.randint(0, 30) for _ in range(rng.randint(0, 15))}
            self.assertEqual(ex.intersection(a, b), a & b)
            words = [rng.choice("abc") * rng.randint(1, 3) for _ in range(20)]
            self.assertEqual(ex.count_loans(words), dict(Counter(words)))
            overdue = [(f"r{rng.randint(1, 20)}", f"t{rng.randint(1, 9)}") for _ in range(30)]
            opted = [f"r{rng.randint(1, 20)}" for _ in range(6)]
            self.assertEqual(ex.reminders_fast(overdue, opted), ex.reminders_slow(overdue, opted))
        self.assertEqual(ex.count_loans(list("BANANA")), {"B": 1, "A": 3, "N": 2})
        self.assertEqual(ex.group_by(["map", "mat", "ant", "apt", "man"], key=lambda w: w[0]),
                         {"m": ["map", "mat", "man"], "a": ["ant", "apt"]})


if __name__ == "__main__":
    unittest.main()
