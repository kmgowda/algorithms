import random
import unittest

import ch38_examples as ex
import ch38_solutions as sol


class TestChapter38Solutions(unittest.TestCase):
    def test_z_values(self) -> None:
        self.assertEqual(sol.z_values(""), [])
        self.assertEqual(sol.z_values("a"), [1])
        self.assertEqual(sol.z_values("aabxaab"), [7, 1, 0, 0, 3, 1, 0])

    def test_one_mismatch(self) -> None:
        self.assertEqual(sol.one_mismatch_search("the club and the clue", "club"), [4, 17])
        self.assertEqual(sol.one_mismatch_search("", "a"), [])
        self.assertEqual(sol.one_mismatch_search("a", "b"), [0])
        self.assertEqual(sol.one_mismatch_search("ab", "abc"), [])
        self.assertEqual(sol.one_mismatch_search("abc", ""), [0, 1, 2, 3])
        rng = random.Random(38)
        for _ in range(400):
            t = "".join(rng.choice("ab") for _ in range(rng.randint(0, 25)))
            p = "".join(rng.choice("ab") for _ in range(rng.randint(1, 6)))
            self.assertEqual(sol.one_mismatch_search(t, p), sol.one_mismatch_brute(t, p))

    def test_skip_after_match_bug(self) -> None:
        self.assertEqual(sol.skip_after_match_search("aaaa", "aa"), [0, 2])
        self.assertEqual(ex.all_methods("aaaa", "aa")["naive"][0], [0, 1, 2])
        self.assertEqual(sol.skip_after_match_search("", "a"), [])
        t = ex.workloads()["random text, 'library'"][0]
        rng = random.Random(7)
        for _ in range(100):
            i = rng.randrange(len(t) - 6)
            p = t[i:i + 6]
            self.assertEqual(sol.skip_after_match_search(t, p), ex.all_methods(t, p)["naive"][0])


if __name__ == "__main__":
    unittest.main()
