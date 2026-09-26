# Proof Pursuit pipeline: context for comparison

Paste this whole file into a Claude session on the other laptop. The prompt at the bottom asks it to compare this pipeline with its own system and installed plugins.

## 1. The task
- **Event:** BAINSA hackathon "Climbing to the Frontier", track 3 "Proof Pursuit". 7 hours, ends about 18:05 CEST today.
- **Judged on:** the auto-research system we build, not only on how many cells are solved.
- **Problems:** 4, each with 6 cells of increasing difficulty (c6 is a genuinely open problem). Points per cell are 1, 2, 3, 5, 8, 13.
  - p1 Angles between lines (Fejes Tóth sum-of-angles conjecture)
  - p2 Uphill paths on the hypercube (IMO 2022 P6 generalised to Q_d, values U(Q3) to U(Q9))
  - p3 Bulgarian solitaire (D_B(n), max moves before cycling)
  - p4 Disjoint congruence classes (Z.-W. Sun's conjecture: k disjoint classes ⇒ some gcd(m_i,m_j) ≥ k)
- **Hard rules:**
  - Complete proofs; citing the result asked for scores nothing.
  - Computation only if the code is included, runs in under 10 minutes, and is exact or uses interval arithmetic.
  - p4 searches need a 5-part exhaustiveness certificate.
  - Say exactly what was established: a conjecture stays a conjecture, and a partial result is reported as partial.

## 2. Architecture
A Python orchestrator (`orchestrate.py`) runs each stage as a separate headless `claude -p` session over a shared git repo. The state lives in files, one folder per cell: `problems/pX/cells/cY/`.

| Stage | Kind | Reads | Writes | Status |
|---|---|---|---|---|
| Cell | human paste | site | `cell.md` | built |
| Parse | agent | problem.md, cell.md | `claim.json` (statement, deliverables, acceptance rules, traps) | built |
| Literature | agent + web | claim, earlier cells | `known.md` tagged [PROVED] [COMPUTED] [CONJ] [GAP] [UNVERIFIED-RECALL] | built |
| Explore | agent + Python | lib/, known.md | `data/`, `explore.md` (exact tables, extremal objects, patterns with checked range) | built |
| Construction search | tool (annealing/evolutionary) | lib/ | constructions (p2 labellings, p4 near-counterexamples) | planned |
| Prove | agent | all of the above + review.md | `proof.md` (fixed template), `cert/search.py` | built (1 prover) |
| Prove ×3 + Rank | agents | same | 3 drafts, ranker picks one | planned |
| Verify | agent, fresh context | cell, claim, proof, cert, lib | `review.md` with numbered FATAL/MAJOR/MINOR objections, `VERDICT: PASS/FAIL` | built |
| Rerun | Python tool | cert/ | `cert/rerun.json` | built |
| Gate | Python tool, no model | everything | `gate.json`, `submission.md` | built |
| Retro (meta-reviewer) | agent | all reviews, gates, logs, human notes | proposed prompt/tool fixes, human-approved | planned |

**Loop:** prove → rerun (if a certificate exists) → verify. On FAIL, the numbered objections go back to the prover. There are at most 3 rounds, and the last round must downgrade the claim to PARTIAL if gaps remain. The gate runs at the end.

## 3. Mechanisms that make it trustworthy
- **Blind verifier, enforced mechanically.** While the verifier runs, the orchestrator physically moves `work/`, `explore.md`, `known.md` and `log.jsonl` out of the cell folder. The verifier can only judge the written proof.
- **Fail-closed gate** (`tools/gate.py`). It checks that:
  - the cell text is real;
  - `claim.json` has the required keys;
  - the proof has every required section, and the status is exactly SOLVED or PARTIAL;
  - the verdict is PASS;
  - the review is newer than the proof and the code;
  - the rerun reproduced the counts and the script hash matches;
  - no pruning happened without a registered rule.
  It also warns on banned phrases ("clearly", "WLOG", "by symmetry") and on uncertified search sizes.
- **Certificate library** (`tools/cert.py`). A search registers each pruning rule with a statement and a proof, and counts nodes and prunes per size. Every survivor needs a decision, the minimal part that forces it, and a minimality proof. The library writes `certificate.json` and refuses to record an unregistered prune or an undecided "decided" survivor.
- **Rerun harness** (`tools/rerun.py`). It re-executes the search, compares per-size counts exactly, and enforces the 10-minute limit.
- **Logging.** Every stage records its time, cost, turns and verdict in `log.jsonl`. Human interventions are logged with `tools/human.py`. `tools/metrics.py` builds METRICS.md (pass rate, verifier rejection rate, share of cells passed with no human help), and `tools/ledger.py` builds LEDGER.md (known / ours / conjecture).
- **Problem libraries,** exact and self-tested:
  - `angles.py`: rigorous S enclosures via exact rational cos² and widened mpmath.
  - `uphill.py`: exact dynamic-programming path counter, brute force to Q3, annealing.
  - `bulgarian.py`: all depths via the functional graph.
  - `congruence.py`: family checker and an exploratory bitset clique search.

## 4. Findings so far (exploratory, not yet verified by the pipeline)
- **U(Q₃) = 14:** exhaustive over all 8! labellings.
- **Q₄:** annealing found a labelling with 34 uphill paths, an upper bound only.
- **Lower bound for p2:** U ≥ (#edges) + (#valleys). This gives 13 for Q₃ and 33 for Q₄.
- **p3:** D_B(T_k) = k² − k checked for k = 3..6. This matches Igusa (1985) and Etienne (1991).
- **p4:** O'Bryant (arXiv math/0604347) claims the conjecture for k ≤ 20 via a reduction lemma plus Mathematica, with no code published. Fornal–Sun (arXiv 2607.24655) give an asymptotic bound only.
- **p1:** only the planar case is settled in the literature (Bilyk–Matzke 2019). Lim–McCann (2020) recast the problem as a one-parameter family.

## 5. Known weaknesses
1. The live `claude -p` loop has not been run end to end yet.
2. The literature and explore stages run per cell; they should run once per problem.
3. Cells are climbed one after another; there's no parallelism across cells.
4. There's one prover, so no diverse attempts.
5. The same model is used for every stage.
6. There's no Retro agent, so the pipeline doesn't learn from its own failures.
7. `cell.md` is pasted by hand.
8. Lean isn't used, because setting it up doesn't fit in 7 hours; rigour comes from Python checkers and certificates instead.

## 6. Research basis
- **Aletheia (DeepMind 2026):** separate generator, verifier and reviser. 68.5% of its candidate answers were flawed.
- **AlphaProof Nexus (DeepMind 2026):** an LLM with Lean compiler feedback, and parallel sketches ranked by Elo. It solved 9 of 353 Erdős problems.
- **AlphaEvolve (2025):** evolutionary search over constructions.
- **Gemini Erdős case study (2026):** checking the literature was the hardest step.

---

## PROMPT FOR THE OTHER LAPTOP

You're helping a 4-person hackathon team. Above is the full context of our math auto-research pipeline. Do the following, concisely:

1. **List your own setup:** every installed plugin, skill, MCP server/connector, subagent and custom command you can see in this session, with one line each on what it does. Also describe any research or agent system already built on this laptop (read its repo or CLAUDE.md if there is one).
2. **Compare** that setup with our pipeline in a table. Rows are capabilities: literature search, exploration/compute, proof generation, independent verification, certificates/rerun, gating, parallelism, self-improvement, logging/metrics, formal verification. Columns are "Our pipeline" and "Your setup". Cells should be a few words each.
3. **For each of your plugins or tools, say:** does it replace, improve, or duplicate one of our stages? Name the stage.
4. **Top 5 changes,** ranked by payoff within about 5 hours. For each, give the concrete action (which file or prompt changes, or which plugin to call from which stage) and the expected gain.
5. **Flag risks:** anything in our design that is wrong, slow or likely to fail on the judges' criteria (checkable proofs, honest status, certificates for p4).

Do not rewrite our pipeline. Only recommend changes.
