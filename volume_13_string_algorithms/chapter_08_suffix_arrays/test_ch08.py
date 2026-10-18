import random
import unittest

import ch08_examples as ex
import ch08_solutions as sol


class TestSuffixArrays(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            s = "".join(rng.choice("abc") for _ in range(rng.randint(0, 20)))
            sa = ex.suffix_array(s)
            self.assertEqual(sa, ex.suffix_array_simple(s))
            lcp = ex.lcp_array(s, sa)
            for i in range(len(s) - 1):
                a, b = s[sa[i]:], s[sa[i + 1]:]
                k = 0
                while k < min(len(a), len(b)) and a[k] == b[k]:
                    k += 1
                self.assertEqual(lcp[i], k)
            p = "".join(rng.choice("abc") for _ in range(rng.randint(1, 3)))
            self.assertEqual(ex.find_all(s, sa, p), [i for i in range(len(s) - len(p) + 1) if s[i:i + len(p)] == p])
            subs = {s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)}
            self.assertEqual(sol.count_distinct_substrings(s), len(subs))
            rep = ex.longest_repeated_substring(s)
            best = max((len(x) for x in subs if any(s[k:k + len(x)] == x for k in range(s.find(x) + 1, len(s)))), default=0)
            self.assertEqual(len(rep), best)
            t = "".join(rng.choice("abc") for _ in range(rng.randint(0, 10)))
            common = max((len(x) for x in subs if x in t), default=0)
            self.assertEqual(len(sol.longest_common_substring(s, t)), common)

    def test_examples(self) -> None:
        self.assertEqual(ex.suffix_array("banana"), [5, 3, 1, 0, 4, 2])
        self.assertEqual(ex.lcp_array("banana", [5, 3, 1, 0, 4, 2]), [1, 3, 0, 0, 2])
        self.assertEqual(ex.find_all("banana", [5, 3, 1, 0, 4, 2], "ana"), [1, 3])
        self.assertEqual(ex.longest_repeated_substring("mississippi"), "issi")
        self.assertEqual(ex.genome_index_queries("ACGTACGTTACGACG", ["ACG", "TAC", "GGG"]), {"ACG": 4, "TAC": 2, "GGG": 0})
        self.assertEqual(sol.count_distinct_substrings("banana"), 15)
        self.assertEqual(sol.longest_common_substring("xabxac", "abcabxabcd"), "abxa")
        self.assertEqual(sol.kth_suffix("banana", 2), "ana")


if __name__ == "__main__":
    unittest.main()
