import random
import unittest
from collections import Counter

import ch30_examples as ex
import ch30_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_expected_overcount(self) -> None:
        r = random.Random(30)
        words = [f"w{r.randrange(500)}" for _ in range(5000)]
        others = sum(1 for w in words if w != "w7")
        avg = sum(sol.one_row_overcount(words, "w7", 100, str(s)) for s in range(200)) / 200
        self.assertLess(abs(avg - others / 100), 0.1 * others / 100)     # about N / width, within sampling noise

    def test_top_k(self) -> None:
        r = random.Random(30)
        words = [f"w{r.randrange(500)}" for _ in range(5000)]
        stream = ["dragons"] * 300 + ["maps"] * 200 + ["poems"] * 150 + words
        r.shuffle(stream)
        self.assertEqual(sol.top_k_sketch(stream, 3), [w for w, _ in Counter(stream).most_common(3)])
        self.assertEqual(sol.top_k_sketch([], 3), [])

    def test_same_hash(self) -> None:
        cm = sol.SameHashCountMin(50, 4)
        for i in range(2000):
            cm.add(f"x{i % 300}")
        self.assertTrue(all(row == cm.rows[0] for row in cm.rows))
        one = sol.SameHashCountMin(50, 1)
        for i in range(2000):
            one.add(f"x{i % 300}")
        self.assertEqual([cm.estimate(f"x{i}") for i in range(50)], [one.estimate(f"x{i}") for i in range(50)])


if __name__ == "__main__":
    unittest.main()
