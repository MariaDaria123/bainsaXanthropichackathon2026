# Cell 6 (open problem): Pioneer rules for swarm workers

Every swarm task on an open cell follows these rules. Adapted from the team's cell-6
framework and the Proof Pursuit kit, for many workers on many laptops.

## Time box (hard)
Each task gets SWARM_TASK_MIN minutes (default 25) for the author phase. Run `date` at the start.
Two blind critics then run automatically (about 8 min). Finish early with an honest partial
result rather than run over. The worker kills the session at the limit.

| Share of time | Do | Output |
|---|---|---|
| first 25% | One fast exploration script (<= 60 s). OEIS for integer sequences. Use the board and known literature; no long literature crawls unless the task is a literature task. | results dir: explore.txt |
| next 10% | Only if the task has a computable score, SHINKA_ANTHROPIC_KEY is set and `shinka_run` exists: launch ShinkaEvolve in the background (see Tools). Otherwise skip. | shinka.log |
| next 30% | Bounded verification: exact / SAT / Z3 / tools/cert.py search for every case up to the largest K that finishes in under 5 minutes. | [COMPUTED] |
| next 25% | Write the strongest claim you can defend (a bound, an infinite family, the [COMPUTED] result). | result.md |
| last 10% | Label every claim. Write findings.jsonl. | findings.jsonl |

## Labels (every claim carries exactly one)
- [PROVED]      full proof.
- [BOUNDED]     a rigorously proved bound, even if not tight.
- [COMPUTED]    exhaustive exact / interval / SAT / Z3 verification for all cases up to K, with code that runs in < 10 min.
- [CONJECTURED] precise statement, strong evidence, no proof.
- [OBSERVED]    a pattern in data, not yet a precise statement.
[PROVED]/[BOUNDED]/[COMPUTED] survive only if TWO blind critics return VERDICT: ACCEPT. The worker
enforces this mechanically: anything else is downgraded to [CONJECTURED] on the board.

## Cardinal rules
0. Compute to discover; only exact computation proves. Floats and Monte Carlo are evidence.
1. Balanced start: try to disprove before proving.
2. Literature for techniques. For p4 the rules accept a published argument written out in full
   and checked line by line; a black-box citation of the asked statement scores nothing.
3. Fail fast, pivot hard. Solver hangs, induction breaks, critic RESTART: log a dead_end with
   the reason, lower the ambition (exact result -> bound -> infinite family -> bounded
   verification) and propose the lower-ambition task as a new_task.
4. Partial credit is real: settle any family or case not covered by earlier cells.
5. A computation beats an argument: if a script contradicts a claim, the claim is refuted.

## Tools (installed by setup_laptop.sh)
- sympy, numpy, scipy: exploration and symbolic work.
- python-sat (CaDiCaL), z3-solver: finite "nothing does better" and integer side conditions.
  A bare UNSAT is not a certificate for p4: register the reduction and pruning in tools/cert.py,
  or emit and check a DRAT proof.
- mpmath, python-flint: interval arithmetic.
- ortools CP-SAT: constraint search.
- ShinkaEvolve (optional): `cp -r search/_template <results>/search`, write scorer.py (exact
  validate + score, higher is better) and initial.py, test with
  `python <dir>/evaluate.py --program_path <dir>/initial.py --results_dir <dir>/test`, then
  `ANTHROPIC_API_KEY="$SHINKA_ANTHROPIC_KEY" nohup shinka_run --task-dir <dir> --results_dir <dir>/shinka
   --num_generations 10 --max-proposal-jobs 3 --set evo.llm_models='["claude-haiku-4-5-20251001"]'
   --set evo.embedding_model=null --set evo.max_api_costs=1 > <dir>/shinka.log 2>&1 &`
  Re-validate the best construction with scorer.py before using it. Kill it at the end of the task.

## Output: result.md (Format A)
```markdown
**Status:** OPEN (partial progress)  or  SOLVED
**Claim** [LABEL]: precise statement of what you showed
**Argument / Evidence.** Proofs of every PROVED/BOUNDED part; the computation and its results.
**What remains open:** the precise gap.
**Verification:** e.g. "python swarm/results/<id>/verify.py : exhaustive, exact, 40 s".
```
