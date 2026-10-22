import random
import unittest

import ch23_examples as ex


def is_subsequence(s: str, t: str) -> bool:
    it = iter(t)
    return all(ch in it for ch in s)


class TestChapter15(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.lcs_full("READING", "TRADING"), ex.lcs_two_rows("READING", "TRADING")), ((6, "RADING", 64), (6, 16)))
        self.assertEqual(ex.hirschberg("READING", "TRADING"), "RADING")
        r = random.Random(15)
        a = "".join(r.choice("ACGT") for _ in range(2000))
        b = "".join(r.choice("ACGT") for _ in range(2000))
        self.assertEqual((ex.lcs_two_rows(a, b), ex.lcs_full(a, b)[2]), ((1294, 4002), 4004001))

    def test_every_case(self) -> None:
        self.assertEqual((ex.lcs_two_rows("", "ABC"), ex.hirschberg("", "ABC"), ex.hirschberg("A", "XAY"), ex.hirschberg("ABC", "ABC")),
                         ((0, 8), "", "A", "ABC"))
        self.assertEqual(len(ex.hirschberg("ABC", "CBA")), 1)
        left, right = ex.last_row("REA", "TRADING"), ex.last_row("GNID", "GNIDART")[::-1]
        self.assertEqual(max(range(8), key=lambda j: left[j] + right[j]), 3)
        r = random.Random(3)
        for _ in range(200):
            a = "".join(r.choice("ABC") for _ in range(r.randint(0, 9)))
            b = "".join(r.choice("ABC") for _ in range(r.randint(0, 9)))
            h = ex.hirschberg(a, b)
            self.assertEqual(len(h), ex.lcs_full(a, b)[0])
            self.assertTrue(is_subsequence(h, a) and is_subsequence(h, b))


    def test_crossing(self) -> None:
        k, fwd, bwd, sums = ex.crossing("READING", "TRADING")
        self.assertEqual((k, fwd, bwd, sums), (3, [0, 0, 1, 2, 2, 2, 2, 2], [4, 4, 4, 4, 3, 2, 1, 0], [4, 4, 5, 6, 5, 4, 3, 2]))
        self.assertEqual(ex.hirschberg_cells("READING", "TRADING"), 91)
        self.assertEqual(ex.crossing("REA", "TRA"), (2, [0, 0, 1, 1], [1, 1, 1, 0], [1, 1, 2, 1]))
        self.assertEqual((ex.hirschberg_cells("", "AB"), ex.hirschberg_cells("A", "AB")), (0, 2))
        import random
        r = random.Random(15)
        a = "".join(r.choice("ACGT") for _ in range(400))
        b = "".join(r.choice("ACGT") for _ in range(400))
        self.assertLess(ex.hirschberg_cells(a, b), 2 * 400 * 400)
        for _ in range(100):
            a = "".join(r.choice("AB") for _ in range(r.randint(0, 9)))
            b = "".join(r.choice("AB") for _ in range(r.randint(0, 9)))
            if a:
                k, fwd, bwd, sums = ex.crossing(a, b)
                self.assertEqual(max(sums), ex.lcs_full(a, b)[0])


if __name__ == "__main__":
    unittest.main()
