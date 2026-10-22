import random
import unittest

import ch23_examples as ex
import ch23_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_split_identity(self) -> None:
        r = random.Random(23)
        for _ in range(200):
            a = "".join(r.choice("ABC") for _ in range(r.randint(1, 9)))
            b = "".join(r.choice("ABC") for _ in range(r.randint(0, 9)))
            self.assertEqual(max(ex.crossing(a, b)[3]), ex.lcs_full(a, b)[0])

    def test_edit_distance(self) -> None:
        self.assertEqual(sol.edit_distance_small("READING", "TRADING"), 2)
        r = random.Random(2)
        for _ in range(200):
            a = "".join(r.choice("ABC") for _ in range(r.randint(0, 9)))
            b = "".join(r.choice("ABC") for _ in range(r.randint(0, 9)))
            self.assertEqual(sol.edit_distance_small(a, b), sol.edit_distance_full(a, b))

    def test_alias_bug(self) -> None:
        self.assertEqual((sol.lcs_aliased("A", "AA"), ex.lcs_full("A", "AA")[0]), (2, 1))


if __name__ == "__main__":
    unittest.main()
