# AGENTS.md

Companion code for the "Algorithms Simplified" book series. Book Markdown lives in the `books` repo at
`/root/projects/kmg/books/algorithms/kmg-book` (series plan in its `README.md`, authoring rules in its `AGENTS.md`).

Seven volumes; chapter numbers restart in each. All seven are written: `volume_01_foundations` (24 chapters),
`volume_02_linear_structures_hashing` (24), `volume_03_trees_heaps` (27), `volume_04_sorting_graphs` (28),
`volume_05_paths_greedy_divide` (27), `volume_06_backtracking_dp_strings` (38), `volume_07_math_and_advanced` (33).
Round 8 restructured the old six volumes into these seven topical ones (folders moved with `git mv`, chapter files
renamed `chNN_*` to the new numbers; `kmg-book/tools/restructure.py` records the mapping).
Every chapter folder holds `chNN_examples.py`, `test_chNN.py` (with `test_every_case`), and the Thinking Problem
solutions `chNN_solutions.py` with `test_chNN_solutions.py`. Round 9 moved old Volume 3 ch 28-30 to Volume 4 ch 1-3
(old Volume 4 ch 1-25 became 4-28).

## Conventions
- Python 3.10+, standard library only (pytest is NOT installed; tests use `unittest`).
- One folder per chapter: `volume_NN_<name>/chapter_NN_<name>/` with `chNN_examples.py`,
  `chNN_solutions.py`, `test_chNN.py`. Module names repeat across volumes (every volume has
  `ch01_examples`), so `run_tests.py` clears chapter modules from `sys.modules` before each folder.
- Every `def` shown in a chapter must match the companion file exactly.

## Verification
- `python3 run_tests.py` — all chapter tests.
- Book checks live in the books repo: `python3 tools/check_book.py` (from `algorithms/kmg-book`) verifies that
  every Python block in a chapter matches this repo.
- Run each `chNN_examples.py` / `chNN_solutions.py` directly to confirm the demos execute.
