import random
import unittest

import ch08_examples as ex


class TestChapter8(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual(ex.lcs(ex.ANA, ex.BEN)[:2], (4, ["Atlas", "Novel", "Diary", "Plays"]))
        n, s, t = ex.lcs("READING", "TRADING")
        self.assertEqual((n, "".join(s), t[3]), (6, "RADING", [0, 0, 1, 2, 2, 2, 2, 2]))

    def test_every_case(self) -> None:
        got = [ex.lcs(a, b)[:2] for a, b in (("", "ABC"), ("ABC", "ABC"), ("ABC", "XYZ"), ("ABC", "CBA"), ("AAAA", "AA"))]
        self.assertEqual(got, [(0, []), (3, list("ABC")), (0, []), (1, ["A"]), (2, ["A", "A"])])
        self.assertEqual("".join(ex.lcs("LIBRARY", "LITERARY")[1]), "LIRARY")
        ben2 = ["Poems", "Atlas", "Novel", "Comic", "Diary", "Maps", "Plays"]
        self.assertEqual((ex.lcs(ex.ANA, ben2)[0], ex.lcs("BOOK", "BACK")[1], ex.lcs("TREADING", "READING")[0], ex.lcs("TREADING", "TRADING")[0]), (5, ["B", "K"], 7, 7))
        r = random.Random(8)
        for _ in range(200):
            a = "".join(r.choice("AB C") for _ in range(r.randint(0, 7)))
            b = "".join(r.choice("ABC") for _ in range(r.randint(0, 7)))
            n, s, _ = ex.lcs(a, b)
            self.assertEqual(n, ex.brute(a, b))
            self.assertEqual(len(s), n)


    def test_all_lcs(self) -> None:
        self.assertEqual(ex.all_lcs(ex.ANA, ex.BEN), [["Atlas", "Novel", "Diary", "Plays"], ["Poems", "Novel", "Diary", "Plays"]])
        self.assertEqual([("".join(s)) for s in ex.all_lcs("ABC", "CBA")], ["A", "B", "C"])
        n, s, t = ex.lcs("CAT", "ACT")
        self.assertEqual((n, "".join(s), [r[1:] for r in t[1:]]), (2, "CT", [[0, 1, 1], [1, 1, 1], [1, 1, 2]]))
        self.assertEqual((ex.all_lcs("", "AB"), ex.all_lcs("READING", "TRADING")), ([[]], [list("RADING")]))


if __name__ == "__main__":
    unittest.main()
