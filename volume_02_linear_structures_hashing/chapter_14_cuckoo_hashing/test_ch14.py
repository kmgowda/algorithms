import itertools
import random
import unittest

import ch14_examples as ex
import ch14_solutions as sol

F = [lambda k: ex.h1(k, 11), lambda k: ex.h2(k, 11)]


class TestCuckoo(unittest.TestCase):
    def shelf(self):
        c = ex.CuckooTable(11)
        for k in ex.SHELF:
            c.insert(k)
        return c

    def test_shelf_layout(self) -> None:
        c = self.shelf()
        self.assertEqual(c.T[0], [None, 12, None, 91, 70, None, None, 84, 63, 31, None])
        self.assertEqual(c.T[1], [None, None, 25, None, 47, 58, None, None, None, None, None])
        self.assertEqual((c.kicks, c.rehashes), (3, 0))

    def test_long_chain(self) -> None:
        c = self.shelf()
        before = len(c.log)
        c.insert(108)
        self.assertEqual(c.log[before:], [(108, 0, 9), (31, 1, 2), (25, 0, 3), (91, 1, 8)])
        self.assertTrue(all(c.find(k) for k in ex.SHELF + [108]))

    def test_cycle_and_rebuild(self) -> None:
        T = [[None] * 11, [None] * 11]
        for k in (25, 146):
            self.assertIsNone(ex.cuckoo_insert(T, F, k, 20)[0])
        left, moves = ex.cuckoo_insert(T, F, 267, 20)
        self.assertIsNotNone(left)
        self.assertEqual(moves, 20)
        self.assertFalse(ex.cuckoo_graph_has_room([25, 146, 267], F[0], F[1], 11))
        c = ex.CuckooTable(11)
        for k in (25, 146, 267):
            c.insert(k)
        self.assertEqual(c.rehashes, 1)
        self.assertTrue(all(c.find(k) for k in (25, 146, 267)))

    def test_every_case(self) -> None:
        c = ex.CuckooTable(11)
        self.assertFalse(c.find(5))                      # empty table
        self.assertFalse(c.delete(5))
        c.insert(5)
        c.insert(5)                                      # duplicate: no change
        self.assertEqual(c.size, 1)
        c = self.shelf()
        self.assertTrue(c.find(12) and c.find(58))       # in table 1, in table 2
        self.assertFalse(c.find(60))                     # absent: two looks
        self.assertTrue(c.delete(47))
        self.assertFalse(c.find(47))
        self.assertTrue(c.find(58))                      # no tombstone needed
        g = ex.CuckooTable(2)                            # load limit: grows past half full
        for k in range(1, 4):
            g.insert(k)
        self.assertEqual(g.m, 4)
        self.assertTrue(all(g.find(k) for k in range(1, 4)))

    def test_random_against_set(self) -> None:
        rng = random.Random(3)
        c, ref = ex.CuckooTable(4, hashes="random", seed=5), set()
        for _ in range(3000):
            k = rng.randrange(400)
            if rng.random() < 0.7:
                c.insert(k)
                ref.add(k)
            else:
                self.assertEqual(c.delete(k), k in ref)
                ref.discard(k)
            self.assertLessEqual(c.size, c.m)
        self.assertEqual(sorted(c.keys()), sorted(ref))
        self.assertEqual(c.size, len(ref))

    def test_room_condition_brute_force(self) -> None:
        for trial in range(400):
            r = random.Random(trial)
            m, n = r.randint(1, 4), r.randint(0, 7)
            A, B = [r.randrange(m) for _ in range(n)], [r.randrange(m) for _ in range(n)]
            brute = any(len({(c, A[k] if c == 0 else B[k]) for k, c in enumerate(ch)}) == n
                        for ch in itertools.product((0, 1), repeat=n))
            self.assertEqual(ex.cuckoo_graph_has_room(range(n), A.__getitem__, B.__getitem__, m), brute)

    def test_experiment(self) -> None:
        low, r1 = ex.insert_cost_experiment(500, 0.2, trials=3)
        high, _ = ex.insert_cost_experiment(500, 0.45, trials=3)
        self.assertLess(low, high)
        self.assertEqual(r1, 0)


class TestRobinHoodAndComparison(unittest.TestCase):
    def test_robin_hood(self) -> None:
        rh = ex.RobinHoodTable(11)
        for k in ex.SHELF:
            rh.insert(k)
        self.assertEqual([s and s[0] for s in rh.slots], [None, 12, None, 25, 47, 58, 91, 70, 84, 63, 31])
        self.assertEqual(max(s[1] for s in rh.slots if s), 3)
        self.assertEqual(rh.find(91), 4)
        self.assertEqual(rh.find(36), -5)                # home 3; slot 7 holds 70 at distance 3 < 4: stop
        empty = ex.RobinHoodTable(5)
        self.assertEqual(empty.find(3), -1)

    def test_compare(self) -> None:
        c = ex.compare()
        self.assertEqual(c["chaining"][1:], (4, 4, 11))
        self.assertEqual(c["linear"][1:], (8, 9, 11))
        self.assertEqual(c["robin hood"][1:], (4, 5, 11))
        self.assertEqual(c["cuckoo"][1:], (2, 2, 22))
        self.assertAlmostEqual(c["linear"][0], c["robin hood"][0])   # same total distance


class TestThinkingProblem(unittest.TestCase):
    def check(self, keys, f0, f1, m):
        T = sol.place_all(keys, f0, f1, m)
        self.assertEqual(T is not None, ex.cuckoo_graph_has_room(keys, f0, f1, m))
        if T:
            self.assertEqual(sorted(x for row in T for x in row if x is not None), sorted(keys))
            for k in keys:
                self.assertTrue(T[0][f0(k)] == k or T[1][f1(k)] == k)

    def test_smallest(self) -> None:
        self.assertEqual(sol.place_all([], *F, 11), [[None] * 11, [None] * 11])
        self.check([7], *F, 11)
        self.check([25, 146], *F, 11)                    # two keys, the same two homes: fits
        self.assertIsNone(sol.place_all([25, 146, 267], *F, 11))
        self.check(ex.SHELF + [108], *F, 11)

    def test_random(self) -> None:
        for trial in range(500):
            r = random.Random(trial)
            m, n = r.randint(1, 6), r.randint(0, 13)
            A, B = [r.randrange(m) for _ in range(n)], [r.randrange(m) for _ in range(n)]
            self.check(list(range(n)), A.__getitem__, B.__getitem__, m)


if __name__ == "__main__":
    unittest.main()
