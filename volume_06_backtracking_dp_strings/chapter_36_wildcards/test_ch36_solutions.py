import random
import unittest

import ch36_examples as ex
import ch36_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def setUp(self) -> None:
        r = random.Random(36)
        self.cases = [("".join(r.choice("ab?*") for _ in range(r.randint(0, 6))), "".join(r.choice("ab") for _ in range(r.randint(0, 8))))
                      for _ in range(400)]

    def test_squash(self) -> None:
        for p, t in self.cases:
            self.assertEqual(ex.wildcard(p, t)[0], ex.wildcard(sol.squash_stars(p), t)[0])

    def test_two_rows(self) -> None:
        for p, t in self.cases:
            self.assertEqual(sol.wildcard_two_rows(p, t), ex.wildcard(p, t)[0])

    def test_one_letter_bug(self) -> None:
        self.assertFalse(sol.wildcard_one_letter_star("tr*", "treasure"))
        self.assertTrue(ex.wildcard("tr*", "treasure")[0])
        self.assertTrue(sol.wildcard_one_letter_star("tr*", "tre"))


if __name__ == "__main__":
    unittest.main()
