# AGENTS.md

Companion code for the "Algorithms Simplified" book series. Book Markdown lives in the `books` repo at
`/root/projects/kmg/books/algorithms/kmg-book` (series plan in its `README.md`, authoring rules in its `AGENTS.md`).

Six volumes; chapter numbers restart in each. Written so far: `volume_01_foundations` (29 chapters),
`volume_02_hashing_trees_heaps` (35), `volume_03_searching_sorting_graphs` (in progress). Other `volume_NN_*` folders
are first-draft code from an earlier plan.

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
