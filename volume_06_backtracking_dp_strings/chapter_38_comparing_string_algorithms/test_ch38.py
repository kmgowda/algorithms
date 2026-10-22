import random
import unittest

import ch38_examples as ex

NL = "the reading club meets on monday; the club reads maps and poems at the library"


class TestChapter30(unittest.TestCase):
    def test_workloads(self) -> None:
        want = {"random text, 'library'": (10350, 10344, 1624, 26, 10364, 1624), "1,000 a's, 'aaaaaaaaab'": (9910, 1991, 991, 18, 2009, 991),
                "1,000 a's, 'baaaaaaaaa'": (991, 1000, 9910, 18, 1010, 1000)}
        for name, (t, p) in ex.workloads().items():
            res = ex.all_methods(t, p)
            self.assertEqual(len({tuple(v[0]) for v in res.values()}), 1)
            self.assertEqual((res["naive"][1], res["Knuth-Morris-Pratt"][1], res["Horspool"][1], res["suffix array"][1],
                              res["Z-algorithm"][1], res["Boyer-Moore"][1]), want[name])

    def test_every_case(self) -> None:
        r = ex.all_methods(NL, "club")
        self.assertEqual({k: v[0] for k, v in r.items()}, {k: [12, 38] for k in r})
        self.assertEqual((r["naive"][1], r["Knuth-Morris-Pratt"][1], r["Horspool"][1], r["suffix array"][1]), (81, 78, 27, 13))
        for t, p, want in (("", "a", []), ("aaaa", "aa", [0, 1, 2]), ("abc", "abcd", [])):
            self.assertEqual({tuple(v[0]) for v in ex.all_methods(t, p).values()}, {tuple(want)})
        rng = random.Random(30)
        for _ in range(100):
            t = "".join(rng.choice("ab") for _ in range(rng.randint(1, 20)))
            p = "".join(rng.choice("ab") for _ in range(rng.randint(1, 4)))
            self.assertEqual(len({tuple(v[0]) for v in ex.all_methods(t, p).values()}), 1)


if __name__ == "__main__":
    unittest.main()
