"""Headless orchestrator: runs the fail-closed pipeline on one cell or climbs a whole column.

  python orchestrate.py p3 c1                 # one cell
  python orchestrate.py p3 --climb            # c1 -> c6, skipping cells that already passed
  python orchestrate.py p3 c2 --from verify   # resume at a stage
  python orchestrate.py p3 c1 --dry-run       # print prompts, call nothing

Each stage is a separate `claude -p` session. The verifier runs with the prover's
scratch (work/, explore.md, known.md, log.jsonl) physically moved out of the cell,
so it can only judge the proof as written.
"""
import argparse, json, os, re, shutil, subprocess, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools"))
from common import CELLS, ROOT, cell_dir, cell_filled, log, problem_dir, rel, verdict
from rerun import rerun
from gate import gate

AGENTS = os.path.join(ROOT, ".claude", "agents")
STAGES = ["parse", "lit", "explore", "prove", "verify", "gate"]
OUTPUT = {"parse": "claim.json", "lit": "known.md", "explore": "explore.md"}
HIDDEN_FROM_VERIFIER = ["work", "explore.md", "known.md", "log.jsonl"]


def load_agent(name):
    txt = open(os.path.join(AGENTS, f"{name}.md")).read()
    fm, body = re.match(r"---\n(.*?)\n---\n(.*)", txt, re.S).groups()
    tools = re.search(r"tools:\s*(.*)", fm).group(1).strip()
    return body, [t.strip() for t in tools.split(",")]


def fill(body, p, c):
    return (body.replace("{PROBLEM}", rel(problem_dir(p))).replace("{CELL}", rel(cell_dir(p, c)))
                .replace("{P}", p).replace("{C}", c))


def build_prompt(stage, p, c, rnd=1, rounds=3):
    body, tools = load_agent({"prove": "prove", "verify": "verifier"}.get(stage, stage))
    prompt = fill(body, p, c)
    if stage == "prove":
        cert_body, cert_tools = load_agent("certify")
        prompt += "\n\n---\n# If any step is computational, follow this CERTIFY procedure\n" + fill(cert_body, p, c)
        tools = sorted(set(tools) | set(cert_tools))
    header = [f"Working directory: the repo root ({ROOT}). Problem {p}, cell {c}.",
              "Read CLAUDE.md first. Use the problem library in "
              f"{rel(problem_dir(p))}/lib/ instead of rewriting it."]
    if stage in ("prove", "verify"):
        header.append(f"This is round {rnd} of at most {rounds}.")
    if stage == "prove" and rnd == rounds:
        header.append("FINAL ROUND: if you cannot resolve every FATAL/MAJOR objection, downgrade the claim to the "
                      "strongest statement you can fully prove and set Status: PARTIAL.")
    if stage == "prove" and rnd > 1:
        header.append(f"The verifier rejected the previous version. Its objections are in {rel(cell_dir(p, c))}/review.md. "
                      "Answer every numbered objection in the 'Response to review' section.")
    return "\n".join(header) + "\n\n" + prompt, tools


def call_claude(prompt, tools, args):
    cmd = ["claude", "-p", prompt, "--output-format", "json"]
    if args.model:
        cmd += ["--model", args.model]
    if args.yolo:
        cmd += ["--dangerously-skip-permissions"]
    else:
        cmd += ["--permission-mode", "acceptEdits", "--allowedTools", ",".join(tools)]
    t = time.time()
    try:
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=args.stage_timeout)
        out = json.loads(proc.stdout) if proc.stdout.strip().startswith("{") else {"result": proc.stdout[-3000:]}
        err = proc.returncode != 0 or out.get("is_error")
    except subprocess.TimeoutExpired:
        out, err = {"result": "TIMEOUT"}, True
    return out, err, time.time() - t


def run_stage(stage, p, c, args, rnd=1):
    prompt, tools = build_prompt(stage, p, c, rnd, args.rounds)
    if args.dry_run:
        print(f"\n===== {stage} (round {rnd}) tools={tools} =====\n{prompt[:1500]}{' ...' if len(prompt) > 1500 else ''}")
        return True
    d = cell_dir(p, c)
    quarantine = os.path.join(ROOT, ".quarantine", p, c)
    moved = []
    if stage == "verify":                                   # enforce independence mechanically
        os.makedirs(quarantine, exist_ok=True)
        for name in HIDDEN_FROM_VERIFIER:
            src = os.path.join(d, name)
            if os.path.exists(src):
                shutil.move(src, os.path.join(quarantine, name)); moved.append(name)
    try:
        print(f"[{p} {c}] {stage} round {rnd} ...", flush=True)
        out, err, secs = call_claude(prompt, tools, args)
    finally:
        for name in moved:
            shutil.move(os.path.join(quarantine, name), os.path.join(d, name))
    v = verdict(p, c) if stage == "verify" else None
    log(p, c, "stage", stage=stage, round=rnd, seconds=round(secs, 1), error=bool(err), verdict=v,
        cost_usd=out.get("total_cost_usd"), turns=out.get("num_turns"), summary=str(out.get("result", ""))[:500])
    print(f"[{p} {c}] {stage} done in {secs/60:.1f} min{' verdict ' + v if v else ''}{' ERROR' if err else ''}")
    return not err


def run_cell(p, c, args):
    d = cell_dir(p, c)
    if not cell_filled(p, c):
        print(f"[{p} {c}] cell.md is a placeholder - paste the cell text from the site first. Skipping (fail-closed).")
        return False
    start = STAGES.index(args.start) if args.start else 0
    for stage in ["parse", "lit", "explore"]:
        if STAGES.index(stage) < start:
            continue
        if os.path.exists(os.path.join(d, OUTPUT[stage])) and not args.force:
            print(f"[{p} {c}] {stage}: {OUTPUT[stage]} exists, skipping (use --force to redo)")
            continue
        run_stage(stage, p, c, args)
    if args.dry_run:
        run_stage("prove", p, c, args, 1); run_stage("verify", p, c, args, 1); return True
    deadline = time.time() + args.budget_min * 60
    for rnd in range(1, args.rounds + 1):
        if rnd > 1 and time.time() > deadline:
            print(f"[{p} {c}] budget of {args.budget_min:.0f} min used up - stopping rounds")
            log(p, c, "budget_exhausted", round=rnd)
            break
        if not (start > STAGES.index("prove") and rnd == 1):   # --from verify skips the first prove
            run_stage("prove", p, c, args, rnd)
        if os.path.exists(os.path.join(d, "cert", "search.py")):
            r = rerun(p, c)
            print(f"[{p} {c}] rerun ok={r['ok']} {r['diffs'][:3]}")
        run_stage("verify", p, c, args, rnd)
        if verdict(p, c) == "PASS":
            break
    g = gate(p, c)
    print(f"[{p} {c}] GATE {'PASS (' + str(g['status']) + ')' if g['pass'] else 'FAIL: ' + '; '.join(g['reasons'][:4])}")
    return g["pass"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("problem"); ap.add_argument("cell", nargs="?")
    ap.add_argument("--climb", action="store_true", help="run c1..c6 in order")
    ap.add_argument("--from", dest="start", choices=STAGES)
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--budget-min", type=float, default=60, help="per-cell wall-clock budget; no new round starts after it")
    ap.add_argument("--stage-timeout", type=int, default=1500, help="seconds per claude call")
    ap.add_argument("--model", default=None)
    ap.add_argument("--force", action="store_true", help="redo parse/lit/explore even if outputs exist")
    ap.add_argument("--yolo", action="store_true", help="--dangerously-skip-permissions (sandboxed machines only)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    cells = CELLS if args.climb or not args.cell else [args.cell]
    for c in cells:
        gpath = os.path.join(cell_dir(args.problem, c), "gate.json")
        if args.climb and os.path.exists(gpath) and json.load(open(gpath)).get("pass"):
            print(f"[{args.problem} {c}] already passed, skipping"); continue
        t = time.time()
        ok = run_cell(args.problem, c, args)
        if args.climb and not ok:
            print(f"[{args.problem} {c}] not passed after {(time.time()-t)/60:.0f} min - moving on (partial work kept)")
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "ledger.py")], cwd=ROOT)
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "metrics.py")], cwd=ROOT)


if __name__ == "__main__":
    main()
