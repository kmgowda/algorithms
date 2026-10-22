import random
import unittest

import ch35_examples as ex
import ch35_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_rle_round_trip(self) -> None:
        r = random.Random(35)
        for _ in range(300):
            s = "".join(r.choice("aab") for _ in range(r.randint(0, 600)))
            runs = ex.rle_encode(s)
            self.assertEqual(ex.rle_decode(runs), s)
            self.assertLessEqual(len(runs), len(s))

    def test_bwt_runs(self) -> None:
        self.assertEqual(sol.runs_after_bwt(ex.POEM), (51, 29))

    def test_slice_bug(self) -> None:
        t = ex.lz77_encode("abababab")
        self.assertEqual((sol.lz77_decode_slice(t), ex.lz77_decode(t)), ("ababb", "abababab"))


if __name__ == "__main__":
    unittest.main()
