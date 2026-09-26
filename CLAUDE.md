# Proof Pursuit repo — rules for every Claude session here

This repo is a fail-closed math auto-research pipeline for a 7-hour hackathon. Four problems (p1–p4), each with six cells c1–c6 of increasing difficulty; c6 is an open problem.

## Non-negotiables
1. **Say exactly what is established.** A conjecture stays a conjecture. An unfinished search is not a verification. Status is `SOLVED` or `PARTIAL`, nothing in between.
2. **Citing ≠ proving.** A published result for the statement asked does not count. You may reuse a published argument, but you must write it out in full and check it yourself; if it fails, report that.
3. **Separate contribution from literature.** Every proof has a section "Cited vs ours".
4. **Computation only through certificates.** Any proof step that relies on code must use `tools/cert.py`, run under 10 minutes, use exact arithmetic (int / Fraction) or interval arithmetic (`mpmath.iv`), and be reproducible by `tools/rerun.py`.
5. **Never write "clearly", "routine", "it is easy to see", "similarly", "WLOG" without the argument.** Expand every step.
6. **Scratch goes in `work/`.** Final artefacts go in their fixed files (see README).
7. **Never edit `review.md`, `gate.json`, `cert/rerun.json` or `log.jsonl` by hand.** They are written by the verifier or the tools.

## Problem libraries (use them, don't rewrite them)
- `problems/p1/lib/angles.py` — S(lines), interval evaluation, numeric maximiser.
- `problems/p2/lib/uphill.py` — exact uphill-path counter, valleys, brute force for Q3, local search, labelling I/O.
- `problems/p3/lib/bulgarian.py` — shift B, d_B, D_B(n), cycle structure, rank.
- `problems/p4/lib/congruence.py` — disjointness test (*), family checker, exploratory counterexample search.

## Running the loop interactively
If a human says "run p3 c2", do: parse → lit → explore → prove (or certify) → verify (as the `verifier` subagent, fresh context) → `python tools/rerun.py` if there is a certificate → `python tools/gate.py p3 c2`. On FAIL, feed the numbered objections back to the prover. Max 3 rounds, then ship PARTIAL.
The same loop runs headless via `python orchestrate.py p3 c2`.
