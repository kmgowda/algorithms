import unittest

import ch13_examples as ex
import ch13_solutions as sol


class TestPlan(unittest.TestCase):
    def test_plan(self) -> None:
        plan = ex.build_plan()
        self.assertEqual([d for d, _, _ in plan], list(range(1, 91)))
        all_topics = {t for _, _, topics in ex.PHASES for t in topics}
        self.assertEqual(sol.topics_covered(plan), all_topics)
        self.assertEqual(sum(days for _, days, _ in ex.PHASES), 90)
        self.assertEqual(ex.review_days(10), [11, 13, 17, 24, 40])
        self.assertEqual(ex.review_days(80), [81, 83, 87])
        load = ex.daily_load({1: 3})
        self.assertEqual([i for i, x in enumerate(load) if x], [2, 4, 8, 15, 31])
        self.assertEqual(sum(load), 15)

    def test_readiness(self) -> None:
        r = {"graphs": [True, False, True, True, True], "dp": [False, False, True, False, True, False]}
        self.assertEqual(ex.readiness(r), {"graphs": 0.8, "dp": 0.4})
        self.assertEqual(sol.weak_topics({"graphs": [True] * 5, "dp": [False, True, False], "tries": [False]}), ["tries", "dp"])
        short = sol.compressed_plan(30)
        self.assertEqual(len(short), 30)
        self.assertEqual(short[0][2], "Big O")


if __name__ == "__main__":
    unittest.main()
