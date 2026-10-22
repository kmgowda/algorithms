import random
import unittest

import ch08_examples as ex
import ch08_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_finish_formula_matches_round_robin(self) -> None:
        self.assertEqual(sol.finish_slots({}), {})
        self.assertEqual(sol.finish_slots({"Ana": 3, "Ben": 1, "Cai": 2}), {"Ana": 6, "Ben": 2, "Cai": 5})
        rng = random.Random(8)
        for _ in range(300):
            needs = {f"s{i}": rng.randint(1, 5) for i in range(rng.randint(1, 7))}
            done = {s: t for t, s, fin in ex.round_robin(needs) if fin}
            self.assertEqual(sol.finish_slots(needs), done)
            order = [s for _, s, fin in ex.round_robin(needs) if fin]
            self.assertEqual(order, sorted(needs, key=lambda s: needs[s]))   # stable: ties keep arrival order

    def test_last_reader_smallest(self) -> None:
        self.assertEqual(sol.last_reader(1, 0), 0)
        self.assertEqual(sol.last_reader(1, 5), 0)
        self.assertEqual(sol.last_reader(2, 0), 1)
        self.assertEqual(sol.last_reader(5, 2), 3)            # D, as in Challenge 1

    def test_last_reader_against_queue(self) -> None:
        for n in range(1, 30):
            for moves in range(0, 7):
                self.assertEqual(sol.last_reader(n, moves), sol.last_reader_by_queue(n, moves))

    def test_pour_always_fails(self) -> None:
        q = sol.PourAlwaysQueue()
        q.enqueue(1); q.enqueue(2)
        self.assertEqual(q.dequeue(), 1)
        q.enqueue(3)
        self.assertEqual(q.dequeue(), 3)                     # a real queue would return 2


if __name__ == "__main__":
    unittest.main()
