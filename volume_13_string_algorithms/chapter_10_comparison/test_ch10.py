import random
import unittest

import ch10_examples as ex
import ch10_solutions as sol


class TestComparison(unittest.TestCase):
    def test_all_matchers_agree(self) -> None:
        rng = random.Random(1)
        ms = ex.matchers()
        for _ in range(150):
            t = "".join(rng.choice("abc") for _ in range(rng.randint(1, 30)))
            p = "".join(rng.choice("abc") for _ in range(rng.randint(1, 4)))
            expected = [i for i in range(len(t) - len(p) + 1) if t[i:i + len(p)] == p]
            for name, f in ms.items():
                self.assertEqual(f(t, p), expected, name)

    def test_race_and_guide(self) -> None:
        r = ex.race(4000)
        worst = r["repetitive worst case"]
        self.assertLess(worst["KMP"], worst["naive"])
        self.assertLess(worst["suffix array, query only"], worst["suffix array"])
        picks = sol.pick_matchers()
        self.assertEqual(picks["block 5,000 banned chat words"], "Aho-Corasick")
        self.assertEqual(picks["find a word in a short email"], "built-in str.find")
        self.assertEqual(sol.break_even_queries(24.2, 0.003, 1.0), 25)
        self.assertEqual(sol.break_even_queries(10, 2, 1), -1)


if __name__ == "__main__":
    unittest.main()
