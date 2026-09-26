# Proof Pursuit — auto-research pipeline

A fail-closed pipeline in which AI agents climb the four problem ladders and every claim has to pass an independent verifier and a mechanical gate before it is submitted.

```
cell.md ─► parse ─► lit ─► explore ─► prove / certify ─► verify ─► rerun ─► GATE ─► submission.md
                                         ▲                  │
                                         └── objections ────┘   (max N rounds, then PARTIAL)
```

## Setup (5 min, each laptop)

1. Clone: `git clone <your repo> && cd proofpursuit`.
2. Install: `pip install -r requirements.txt`.
3. Check that the libraries work: `python tools/selftest.py` (should print `ALL OK`).
4. Paste each cell's text from the site into `problems/pX/cells/cY/cell.md`, replacing the placeholder. The pipeline refuses to run on a placeholder.
5. Run a cell: `python orchestrate.py p3 c1`.
6. Climb a whole column: `python orchestrate.py p3 --climb`.

## Roles (one problem each + one system component)

| Person | Problem | System component |
|---|---|---|
| A | p4 Congruence classes | `orchestrate.py`, logs, `tools/metrics.py` |
| B | p2 Hypercube | `tools/cert.py`, `tools/rerun.py`, solver searches |
| C | p1 Angles | verifier prompt, interval-arithmetic checks |
| D | p3 Bulgarian solitaire | `tools/lit` prompt, `LEDGER.md`, submissions and demo |

Each person runs `--climb` on their own problem in a terminal and only steps in at the gate. **Log every intervention**: `python tools/human.py p3 c2 "fixed off-by-one in rank definition"`. The intervention log is your pitch.

## Files per cell (`problems/pX/cells/cY/`)

| File | Written by | Purpose |
|---|---|---|
| `cell.md` | human (paste) | Exact cell statement |
| `claim.json` | parse | Type, deliverables, acceptance rules |
| `known.md` | lit | Literature tagged `[PROVED] [COMPUTED] [CONJ] [GAP]` |
| `data/`, `explore.md` | explore | Small-case data, patterns, candidate conjectures |
| `proof.md` | prove | Fixed template, status SOLVED / PARTIAL |
| `cert/search.py`, `cert/certificate.json` | certify | Exhaustive search + certificate |
| `review.md` | verify (fresh context) | Numbered objections, `VERDICT: PASS/FAIL` |
| `cert/rerun.json` | `tools/rerun.py` | Reproduced counts + wall clock |
| `gate.json` | `tools/gate.py` | Mechanical pass/fail with reasons |
| `submission.md` | `tools/gate.py` | What you paste into the site |
| `work/` | anyone | Scratch. The verifier is told not to read it. |
| `log.jsonl` | orchestrator | Stage timings, cost, rounds, human notes |

## Commands

| Command | Does |
|---|---|
| `python orchestrate.py p2 c1` | Full pipeline on one cell |
| `python orchestrate.py p2 --climb` | c1 → c6 in order, stops at `--budget-min` |
| `python orchestrate.py p2 c3 --from verify` | Resume at a stage |
| `python orchestrate.py p2 c1 --dry-run` | Print prompts only |
| `python tools/gate.py p2 c1` | Run the gate by hand |
| `python tools/rerun.py p2 c4` | Re-execute a certificate and compare counts |
| `python tools/ledger.py` | Rebuild `LEDGER.md` (Known / Ours / Conjecture) |
| `python tools/metrics.py` | Rebuild `METRICS.md` (system stats for the demo) |
| `python tools/human.py p2 c1 "note"` | Log a human intervention |

## Rules the system enforces

- **Fail-closed.** Nothing reaches `submission.md` unless `gate.json` says `pass: true`.
- **Independent verifier.** A fresh `claude -p` session sees only the statement, the proof and the code, never the prover's scratch or log.
- **Freshness.** `review.md` must be newer than `proof.md` and the certificate, or the gate fails.
- **Exact arithmetic.** Certificates use integers or `Fraction`, and `mpmath.iv` for real analysis. Floats are only for exploring.
- **Honest status.** `SOLVED` only with a `PASS` verdict. Anything else ships as `PARTIAL`, stating exactly what was established.
- **Budget.** Each cell gets at most `--rounds` prove↔verify rounds (default 3), then it ships as PARTIAL and the climb moves on.

## Swarm mode (open cells, many laptops)

The git repo is the shared board: tasks, claims and findings are all files. A worker claims a task by pushing, so two workers can never take the same one. Findings go to one file per worker, so there are no merge conflicts.

1. One person: push this repo to GitHub, then `python swarm.py seed` (12 starter tasks across the four c6 cells).
2. Every laptop: `git clone <repo> && cd proofpursuit && pip install -r requirements.txt`.
3. Every laptop, one terminal tab per worker (2–3 per laptop): `python swarm.py work --name <you>-1`.
   Each worker auto-clones into `~/swarm-workers/<name>` so they never clash.
   Optional: `--problem p2` to pin to one problem, `--tracks proof,obstruction` to pin tracks.
4. Projector / one shared screen: `watch -n 20 python swarm.py status`.
5. Humans inject ideas as tasks: `python swarm.py add p2 "Try induction on d via Q_(d-1) x K2" --track proof --prio 1`.
6. Read everything found so far: `python swarm.py board --problem p2`.
7. At 17:30: `python swarm.py stop` — every worker exits after its current task.

Env: `SWARM_MODEL=opus` (model), `SWARM_TASK_MIN=35` (time box per task), `SWARM_YOLO=1` (skip permission prompts on sandboxed machines).
Swarm findings are raw material: promote the best ones into `problems/pX/cells/c6/` and run `python orchestrate.py pX c6 --from prove` so they still pass the verifier and the gate.
