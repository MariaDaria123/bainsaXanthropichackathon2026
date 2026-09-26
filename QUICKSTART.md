# Swarm quickstart: p4 c6 "Beyond the boundary"

Every laptop runs Claude workers. They share one task board through this GitHub repo.

**Each task runs this loop:**
- The author tries to disprove first, then proves or computes, and writes `result.md` with labelled claims.
- Two blind critics referee it in parallel.
- **MINOR:** one fix round, then another review.
- **RESTART:** the claim is downgraded and a dead end is logged.
- A [PROVED], [BOUNDED] or [COMPUTED] label survives only with two ACCEPTs. The worker enforces this, not the agent.

Method sources: Aletheia and ProofCouncil (author/critic), our cell-6 framework (labels, time box, fail fast), and the swarm (git board, parallel laptops).

## Setup (once per laptop, about 3 minutes)
```bash
git clone https://github.com/MariaDaria123/bainsaxanthropichackathon2026 && cd bainsaxanthropichackathon2026
./setup_laptop.sh        # checks git/python/claude, installs everything in .venv, checks GitHub push access
```
If it says Claude Code is missing, run `npm install -g @anthropic-ai/claude-code`, then `claude` once to log in.
If it says there's no push access, accept the collaborator invite, then run `gh auth login`.

## Run
| Laptop | Command | Direction |
|---|---|---|
| 1 | `./start.sh a 2` | (a) decide k ≥ 25: reduction lemma, then certified search |
| 2 | `./start.sh a 1 && ./start.sh c 1` | (a) plus (c) |
| 3 | `./start.sh b 2` | (b) asymptotic bound: full rewrite / c·k / better constant |
| 4 | `./start.sh c 2` | (c) group form k = 6: reductions, special classes, small groups |

- **Watch (one shared screen):** `./status.sh`
- **Add an idea:** `.venv/bin/python swarm.py add p4 "(c) try nilpotent groups via Sylow decomposition" --track proof --prio 1`
- **Read the board:** `.venv/bin/python swarm.py board --problem p4`
- **Stop everyone at 17:30:** `./stop.sh`. To stop this laptop right now: `./stop.sh --now`.

## Knobs
- `SWARM_MODEL=sonnet ./start.sh a 2`: use this if you hit subscription limits.
- `SWARM_TASK_MIN=25`: minutes for the author phase. The critics add about 8 minutes, plus one optional fix round.
- `SWARM_YOLO=1`: no permission prompts. Only use it on laptops where you're fine with the agent running commands freely.
- `SHINKA_ANTHROPIC_KEY=sk-ant-...`: lets construction tasks run ShinkaEvolve (optional; cap $1 per run).

## Submitting
Findings are in `swarm/results/<task>/result.md`, with critic reports alongside.
- **Submit as proved:** only claims marked with two critic ACCEPTs on the board.
- **Everything else:** submit as [CONJECTURED] or [OBSERVED], per CLAUDE-cell-6-open.md.
- **Optional extra check:** paste the result into Google AI Studio (Gemini) for a third, independent opinion.
