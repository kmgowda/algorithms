import unittest

import ch04_examples as ex


class TestChapter4(unittest.TestCase):
    def test_trail(self) -> None:
        dist, parent, order = ex.dag_shortest(ex.STOPS, ex.PATHS, "Gate")
        self.assertEqual(order, ["Gate", "Maps", "Poetry", "Stories", "Science", "Cafe", "Stage"])
        self.assertEqual(dist, {"Gate": 0, "Poetry": 4, "Maps": 3, "Science": 4, "Stories": 6, "Cafe": 5, "Stage": 7})
        self.assertEqual(ex.route(parent, "Stage"), ["Gate", "Maps", "Poetry", "Stories", "Science", "Cafe", "Stage"])
        ld, lp, _ = ex.dag_shortest(ex.STOPS, ex.PATHS, "Gate", longest=True)
        self.assertEqual((ld["Stage"], ex.route(lp, "Stage")), (16, ["Gate", "Poetry", "Science", "Stage"]))

    def test_every_case(self) -> None:
        d = ex.dag_shortest(ex.STOPS, ex.PATHS, "Stories")[0]
        self.assertEqual((d["Gate"], d["Science"], d["Stage"]), (float("inf"), -2, 1))
        self.assertIsNone(ex.topological_order(["A", "B"], [("A", "B", 1), ("B", "A", 1)]))
        with self.assertRaises(ValueError):
            ex.dag_shortest(["A", "B"], [("A", "B", 1), ("B", "A", 1)], "A")
        self.assertEqual(ex.dag_shortest(["A"], [], "A")[0], {"A": 0})
        self.assertEqual(ex.dag_shortest(["A", "B"], [("A", "B", 0)], "A")[0], {"A": 0, "B": 0})

    def test_counts_and_build(self) -> None:
        count = {"Gate": 1}
        for v in ex.topological_order(ex.STOPS, ex.PATHS):
            for a, b, _ in ex.PATHS:
                if a == v:
                    count[b] = count.get(b, 0) + count[v]
        self.assertEqual(count["Stage"], 15)
        self.assertEqual(ex.dag_shortest(ex.STOPS, [p for p in ex.PATHS if p[2] != -2], "Gate")[0]["Stage"], 13)
        tasks = ["start", "frame", "tents", "lights", "sound", "signs", "rehearsal"]
        after = [("start", "frame", 0), ("start", "tents", 0), ("frame", "lights", 3), ("frame", "sound", 3),
                 ("tents", "signs", 5), ("lights", "rehearsal", 2), ("sound", "rehearsal", 4), ("signs", "rehearsal", 1)]
        self.assertEqual(ex.dag_shortest(tasks, after, "start", longest=True)[0]["rehearsal"] + 2, 9)


if __name__ == "__main__":
    unittest.main()
