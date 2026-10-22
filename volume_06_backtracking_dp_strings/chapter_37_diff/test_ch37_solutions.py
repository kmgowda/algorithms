import random
import unittest

import ch37_examples as ex
import ch37_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_fewest_changes(self) -> None:
        r = random.Random(37)
        for _ in range(200):
            a = [r.choice("ABC") for _ in range(r.randint(0, 8))]
            b = [r.choice("ABC") for _ in range(r.randint(0, 8))]
            kept, gone, added = ex.changes(ex.diff(a, b))
            k = sol.lcs_length(a, b)
            self.assertEqual((kept, gone, added), (k, len(a) - k, len(b) - k))

    def test_undo(self) -> None:
        self.assertEqual(sol.undo_diff(ex.diff(ex.OLD, ex.NEW)), ex.OLD)
        r = random.Random(2)
        for _ in range(200):
            a = [r.choice("ABC") for _ in range(r.randint(0, 8))]
            b = [r.choice("ABC") for _ in range(r.randint(0, 8))]
            d = ex.diff(a, b)
            self.assertEqual((sol.undo_diff(d), ex.apply_diff(a, d)), (a, b))

    def test_set_diff(self) -> None:
        a, b = ["A", "B", "A"], ["B", "A", "A"]
        self.assertEqual(sol.set_diff(a, b), [])
        self.assertNotEqual(sol.apply_set_diff(a, sol.set_diff(a, b)), b)
        self.assertEqual(ex.apply_diff(a, ex.diff(a, b)), b)


if __name__ == "__main__":
    unittest.main()
