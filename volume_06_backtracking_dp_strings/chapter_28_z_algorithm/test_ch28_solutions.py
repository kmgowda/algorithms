import random
import unittest

import ch28_examples as ex
import ch28_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_comparisons(self) -> None:
        r = random.Random(28)
        for _ in range(300):
            s = "".join(r.choice("ab") for _ in range(r.randint(0, 40)))
            self.assertLessEqual(ex.z_array(s)[1], 2 * len(s))

    def test_rotation(self) -> None:
        self.assertTrue(sol.is_rotation("library", "rarylib"))
        self.assertFalse(sol.is_rotation("library", "yrarbil"))
        self.assertTrue(sol.is_rotation("", ""))
        r = random.Random(2)
        for _ in range(200):
            a = "".join(r.choice("ab") for _ in range(r.randint(1, 8)))
            b = "".join(r.choice("ab") for _ in range(len(a)))
            self.assertEqual(sol.is_rotation(a, b), any(a[k:] + a[:k] == b for k in range(len(a))))

    def test_no_separator(self) -> None:
        self.assertEqual((sol.z_search_no_sep("a", "aa"), ex.z_search("a", "aa")), ([-1], []))


if __name__ == "__main__":
    unittest.main()
