import random
import unittest

import ch57_examples as ex


class TestChapter57(unittest.TestCase):
    def test_against_plain_sums(self) -> None:
        rng = random.Random(1)
        for n in (1, 2, 5, 8, 13, 40):
            vals = [rng.randint(0, 9) for _ in range(n)]
            st = ex.SegmentTree(vals)
            for _ in range(200):
                if rng.random() < 0.4:
                    i, v = rng.randrange(n), rng.randint(0, 9)
                    st.update(i, v)
                    vals[i] = v
                a = rng.randrange(n); b = rng.randrange(a, n)
                self.assertEqual(st.query(a, b), sum(vals[a:b + 1]))

    def test_examples(self) -> None:
        st = ex.SegmentTree(ex.DAYS)
        self.assertEqual(st.t[1:16], [31, 9, 22, 4, 5, 14, 8, 3, 1, 4, 1, 5, 9, 2, 6])
        self.assertEqual(st.query(1, 6), 22)
        self.assertEqual(st.used_nodes(1, 6), [(1, 1), (2, 3), (4, 5), (6, 6)])
        self.assertEqual(st.used_nodes(0, 5), [(0, 3), (4, 5)])
        st.update(5, 4)
        self.assertEqual((st.t[1], st.query(1, 6)), (26, 17))


if __name__ == "__main__":
    unittest.main()
