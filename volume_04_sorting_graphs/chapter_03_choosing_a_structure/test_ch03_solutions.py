import unittest

import ch03_examples as ex
import ch03_solutions as sol


class TestWaitingList(unittest.TestCase):
    def test_empty_and_one(self) -> None:
        w = sol.WaitingList()
        self.assertIsNone(w.serve())
        self.assertEqual(len(w), 0)
        self.assertFalse(w.leave("Ann"))
        self.assertTrue(w.join("Ann"))
        self.assertFalse(w.join("Ann"))
        self.assertEqual(w.serve(), "Ann")
        self.assertIsNone(w.serve())

    def test_leave_and_rejoin(self) -> None:
        w = sol.WaitingList()
        for r in ["Ann", "Ben", "Cal"]:
            w.join(r)
        w.leave("Ann")
        w.join("Dee")
        w.join("Ann")                       # Ann rejoins at the back
        self.assertEqual([w.serve() for _ in range(5)], ["Ben", "Cal", "Dee", "Ann", None])

    def test_bug(self) -> None:
        w = sol.NoTicketWaitingList()
        for r in ["Ann", "Ben", "Cal"]:
            w.join(r)
        w.leave("Ann")
        w.join("Dee")
        w.join("Ann")
        self.assertEqual(w.serve(), "Ann")  # served from her old place, ahead of Ben

    def test_against_list(self) -> None:
        import random
        rng = random.Random(30)
        w, model = sol.WaitingList(), []
        for _ in range(3000):
            op, r = rng.random(), rng.randrange(12)
            if op < 0.45:
                if r not in model:
                    model.append(r)
                w.join(r)
            elif op < 0.7:
                if r in model:
                    model.remove(r)
                w.leave(r)
            else:
                self.assertEqual(w.serve(), model.pop(0) if model else None)
            self.assertEqual(len(w), len(model))
        self.assertLessEqual(len(w.line), w.next_ticket)

    def test_workload(self) -> None:
        n, q, u = 100_000, 1_000_000, 1_000
        scan = sol.workload_cost({"range_sum": n, "update": 1}, {"range_sum": q, "update": u})
        fen = sol.workload_cost({"range_sum": 2 * 17, "update": 17}, {"range_sum": q, "update": u})
        self.assertEqual(scan, 100_000_001_000)
        self.assertEqual(fen, 34_017_000)
        pre = sol.workload_cost({"range_sum": 1, "update": n}, {"range_sum": q, "update": u})
        self.assertEqual(pre, 101_000_000)
        self.assertEqual((n - 1).bit_length(), 17)


class TestPartThree(unittest.TestCase):
    def test_part_three_jobs(self) -> None:
        got = {job: ex.recommend(**needs) for job, needs in ex.PART_III_JOBS.items()}
        self.assertEqual(got, {"room bookings that overlap": "interval tree", "nearest branch to a reader": "k-d tree",
                               "route planner's frontier": "pairing heap", "popular-titles lookup": "splay tree",
                               "splitting the catalogue at a call number": "treap"})

    def test_order_of_questions(self) -> None:
        r = ex.recommend
        self.assertEqual(r(intervals=True, extreme_only=True), "interval tree")
        self.assertEqual(r(many_decrease_keys=True), "array")          # a follow-up with nothing to refine
        self.assertEqual(r(needs_order=True, on_disk=True, hot_keys=True), "B-tree")
        self.assertEqual(r(hot_keys=True, exact_keys=True), "hash table")


if __name__ == "__main__":
    unittest.main()
