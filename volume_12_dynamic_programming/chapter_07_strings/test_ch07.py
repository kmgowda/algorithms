import itertools
import random
import unittest

import ch07_examples as ex
import ch07_solutions as sol


def is_pal(x):
    return x == x[::-1]


class TestStrings(unittest.TestCase):
    def test_palindromes(self) -> None:
        rng = random.Random(1)
        for _ in range(150):
            s = "".join(rng.choice("abc") for _ in range(rng.randint(0, 9)))
            subs = [s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)]
            self.assertEqual(ex.count_palindromic_substrings(s), sum(map(is_pal, subs)))
            self.assertEqual(len(ex.longest_palindromic_substring(s)), max((len(x) for x in subs if is_pal(x)), default=0))
            best_seq = max((r for r in range(len(s) + 1) for c in itertools.combinations(s, r) if is_pal("".join(c))), default=0)
            self.assertEqual(ex.longest_palindromic_subsequence(s), best_seq)
            self.assertEqual(sol.min_insertions_to_palindrome(s), len(s) - best_seq)
            if s:
                best_cuts = min(bin(m).count("1") for m in range(1 << (len(s) - 1))
                                if all(is_pal(p) for p in self._pieces(s, m)))
                self.assertEqual(sol.min_palindrome_cuts(s), best_cuts)

    @staticmethod
    def _pieces(s, mask):
        out, cur = [], s[0]
        for i in range(1, len(s)):
            if mask >> (i - 1) & 1:
                out.append(cur)
                cur = s[i]
            else:
                cur += s[i]
        return out + [cur]

    def test_word_break(self) -> None:
        rng = random.Random(2)
        words = ["a", "ab", "ba", "bb", "aba"]
        for _ in range(100):
            t = "".join(rng.choice("ab") for _ in range(rng.randint(0, 8)))
            sentences = sol.all_sentences(t, words)
            self.assertEqual(ex.word_break(t, words), bool(sentences))
            self.assertTrue(all(s.replace(" ", "") == t for s in sentences))
        self.assertTrue(ex.word_break("applepenapple", ["apple", "pen"]))
        self.assertFalse(ex.word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]))
        self.assertEqual(sol.all_sentences("catsanddog", ["cat", "cats", "and", "sand", "dog"]), ["cat sand dog", "cats and dog"])
        self.assertEqual(ex.segment_hashtag("bestpizzainmumbai", ["best", "pizza", "in", "mumbai", "be", "st", "pi", "zza", "mum", "bai"]),
                         ["best", "pizza", "in", "mumbai"])
        self.assertIsNone(ex.segment_hashtag("xyz", ["x", "y"]))


if __name__ == "__main__":
    unittest.main()
