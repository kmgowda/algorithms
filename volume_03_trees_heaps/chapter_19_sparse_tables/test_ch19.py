import random
import unittest

import ch19_examples as ex


class TestChapter59(unittest.TestCase):
    def test_every_case(self) -> None:
        s = ex.SparseTable([3, 1, 4, 1, 5, 9, 2, 6])
        self.assertEqual(s.query(0, 7), (1, (0, 7), (0, 7)))
        self.assertEqual(s.query(2, 5)[0], 1)
        self.assertEqual(s.query(4, 6), (2, (4, 5), (5, 6)))
        self.assertEqual((s.query(0, 0)[0], s.query(7, 7)[0]), (3, 6))
        self.assertEqual(ex.SparseTable([2, 2, 2]).query(0, 2), (2, (0, 1), (1, 2)))
        for a, b in ((5, 2), (0, 20), (-1, 3)):
            with self.assertRaises(IndexError):
                s.query(a, b)
        self.assertEqual((s.cells(), ex.SparseTable([]).cells(), ex.SparseTable([7]).query(0, 0)[0]), (21, 0, 7))

    def test_against_scans(self) -> None:
        rng = random.Random(1)
        for n in (1, 2, 7, 8, 33, 100):
            vals = [rng.randint(0, 50) for _ in range(n)]
            st = ex.SparseTable(vals)
            for _ in range(200):
                a = rng.randrange(n); b = rng.randrange(a, n)
                self.assertEqual(st.query(a, b)[0], min(vals[a:b + 1]))

    def test_examples(self) -> None:
        st = ex.SparseTable(ex.NOISE)
        self.assertEqual(st.table[1:], [[3, 3, 4, 4, 2, 2, 8], [3, 3, 2, 2, 2], [2]])
        self.assertEqual(st.query(1, 6), (2, (1, 4), (3, 6)))
        self.assertEqual(st.query(2, 4), (4, (2, 3), (3, 4)))
        self.assertEqual(len(ex.SparseTable(list(range(100))).table), 7)


    def test_lca(self) -> None:
        import random
        lca = ex.LCA(ex.SECTIONS, "Library")
        self.assertEqual(len(lca.tour), 2 * 11 - 1)
        self.assertEqual(lca.query("Algebra", "Physics"), "Science")
        self.assertEqual(lca.query("Mystery", "Geometry"), "Library")
        self.assertEqual(lca.query("Maths", "Geometry"), "Maths")
        self.assertEqual(lca.query("Fantasy", "Fantasy"), "Fantasy")
        r = random.Random(19)
        for _ in range(100):
            n = r.randint(1, 15)
            parent = {k: r.randrange(k) for k in range(1, n)}
            ch = {}
            for k, p in parent.items():
                ch.setdefault(p, []).append(k)
            lc = ex.LCA(ch, 0)

            def up(x):
                path = [x]
                while x in parent:
                    x = parent[x]
                    path.append(x)
                return path
            for _ in range(10):
                u, v = r.randrange(n), r.randrange(n)
                pu = up(u)
                self.assertEqual(lc.query(u, v), next(x for x in up(v) if x in pu))


if __name__ == "__main__":
    unittest.main()
