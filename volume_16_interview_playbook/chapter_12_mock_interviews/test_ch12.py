import itertools
import random
import unittest

import ch12_examples as ex
import ch12_solutions as sol


class TestMocks(unittest.TestCase):
    def test_against_brute(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            nums = [rng.randint(-5, 5) for _ in range(rng.randint(0, 9))]
            self.assertEqual(sorted(ex.three_sum(nums)), ex.three_sum_brute(nums))
            if len(nums) >= 3:
                t = rng.randint(-8, 8)
                best = min((sum(c) for c in itertools.combinations(nums, 3)), key=lambda s: abs(s - t))
                self.assertEqual(abs(sol.three_sum_closest(nums, t) - t), abs(best - t))
            words = ["".join(rng.choice("ab") for _ in range(rng.randint(1, 3))) for _ in range(rng.randint(1, 4))]
            s = "".join(rng.choice("ab") for _ in range(rng.randint(0, 8)))
            self.assertEqual(ex.word_break(s, words), ex.word_break_brute(s, words))
            sentences = sol.word_break_all(s, words)
            self.assertEqual(bool(sentences) if s else True, ex.word_break(s, words))
            self.assertTrue(all(x.replace(" ", "") == s for x in sentences))

    def test_ladder(self) -> None:
        self.assertEqual(ex.ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]), 5)
        self.assertEqual(ex.ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log"]), 0)
        self.assertEqual(ex.ladder_length("a", "c", ["a", "b", "c"]), 2)
        plain, memo = ex.count_calls("a" * 18 + "b", ["a", "aa", "aaa"])
        self.assertGreater(plain, 1000 * memo)
        self.assertEqual(sol.word_break_all("catsanddog", ["cat", "cats", "and", "sand", "dog"]), ["cat sand dog", "cats and dog"])
        self.assertEqual(sol.self_review({"clarified": True, "tested": False}),
                         ["gave examples", "stated brute force", "explained improvement", "tested", "gave complexity"])


if __name__ == "__main__":
    unittest.main()
