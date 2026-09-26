"""Build SWARM_DIGEST.md: every result.md (finished and partial) for one problem, with critic verdicts.
usage: python tools/swarm_digest.py [--problem p4]"""
import argparse, glob, json, os, re, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument("--problem", default="p4"); a = ap.parse_args()
tasks = {}
for st in ("done", "claimed", "open"):
    for f in glob.glob(os.path.join(ROOT, "swarm/tasks", st, "*.json")):
        t = json.load(open(f)); t["_state"] = st; tasks[t["id"]] = t
def verdicts(d):
    out = []
    for f in sorted(glob.glob(os.path.join(d, "critic_*_round*.md"))):
        m = re.findall(r"VERDICT:\s*(ACCEPT|MINOR|RESTART)", open(f).read())
        out.append(f"{os.path.basename(f)[:-3]}: {m[-1] if m else '?'}")
    return ", ".join(out) or "not reviewed"
secs = []
for kind, base in (("finished", "swarm/results"), ("partial (cut off at stop)", "swarm/results_partial")):
    for d in sorted(glob.glob(os.path.join(ROOT, base, f"{a.problem}-*"))):
        tid = os.path.basename(d); t = tasks.get(tid, {})
        r = os.path.join(d, "result.md")
        body = open(r).read().strip() if os.path.exists(r) else "_(no result.md written before the stop)_"
        secs.append((t.get("finished_at") or t.get("claimed_at") or "", f"## {t.get('goal', tid)[:140]}\n\n"
            f"- **Task:** `{tid}` · {kind} · worker {t.get('owner','?')} · track {t.get('track','?')}\n"
            f"- **Critics:** {verdicts(d)}\n- **Files:** `{os.path.relpath(d, ROOT)}/`\n\n{body}\n"))
secs.sort()
head = [f"# Swarm digest: {a.problem} c6 \"Beyond the boundary\"",
        f"_generated {datetime.datetime.now().isoformat(timespec='minutes')}. Every write-up the swarm produced, oldest first. "
        "Labels are the author's; the board (SWARM_LOG.md) shows which survived the 2-critic gate (none downgraded here are proofs yet)._\n",
        "## Contents"] + [f"- {s.splitlines()[0][3:]}" for _, s in secs] + [""]
open(os.path.join(ROOT, "SWARM_DIGEST.md"), "w").write("\n".join(head) + "\n---\n\n".join(s for _, s in secs))
print(f"wrote SWARM_DIGEST.md with {len(secs)} write-ups")
