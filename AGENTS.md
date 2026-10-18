# AGENTS.md

Companion code for the "Algorithms Simplified" book series. Book Markdown lives in the `books` repo at
`/root/projects/kmg/books/algorithms/kmg-book` (series plan in its `README.md`).

## Conventions
- Python 3.10+, standard library only (pytest is NOT installed; tests use `unittest`).
- One folder per chapter: `volume_NN_<name>/chapter_NN_<name>/` with `chNN_examples.py`,
  `chNN_solutions.py`, `test_chNN.py`. Module names repeat across volumes (every volume has
  `ch01_examples`), so `run_tests.py` clears chapter modules from `sys.modules` before each folder.
- Every `def` shown in a chapter must match the companion file exactly.
- Book chapters must contain headings with: comparison, exercises, solutions, FAQ, summary.

## Verification
- `python3 run_tests.py` — all chapter tests.
- `python3 tools/check_book.py /root/projects/kmg/books/algorithms/kmg-book` — Mermaid
  syntax/section checks. (`mmdc` is installed but broken: Node 10 is too old, so rendering is not verified.)
- Run each `chNN_examples.py` / `chNN_solutions.py` directly to confirm the demos execute.
