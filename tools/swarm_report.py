"""Generate SWARM_LOG.md: what the swarm did, with provenance for every finding.

usage: python tools/swarm_report.py [--problem p4]
Reads swarm/tasks, swarm/board, swarm/results and git history. Safe to run any time.
"""
import argparse, glob, json, os, subprocess, datetime
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SW = os.path.join(ROOT, "swarm")


def load(f):
    try:
        return json.load(open(f))
    except Exception:
        return None


def git_first_commit(path):
    p = subprocess.run(["git", "log", "--diff-filter=A", "--format=%h %ad", "--date=format:%H:%M", "--", path],
                       cwd=ROOT, capture_output=True, text=True)
    lines = p.stdout.strip().splitlines()
    return lines[-1] if lines else "uncommitted"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--problem", default="p4"); a = ap.parse_args()
    subprocess.run(["git", "pull", "-q", "--rebase"], cwd=ROOT, capture_output=True)
    tasks = {}
    for state in ("open", "claimed", "done"):
        for f in glob.glob(os.path.join(SW, "tasks", state, "*.json")):
            t = load(f)
            if t and t.get("problem") == a.problem:
                t["_state"] = state; tasks[t["id"]] = t
    rows = []
    for f in sorted(glob.glob(os.path.join(SW, "board", "*.jsonl"))):
        for line in open(f):
            try:
                r = json.loads(line)
            except Exception:
                continue
            if r.get("problem") == a.problem:
                rows.append(r)
    rows.sort(key=lambda r: r.get("t", ""))
    claims = [r for r in rows if r.get("type") != "new_task"]
    by_task = defaultdict(list)
    for r in claims:
        by_task[r.get("task")].append(r)

    out = [f"# Swarm log: {a.problem}", f"_generated {datetime.datetime.now().isoformat(timespec='minutes')} by tools/swarm_report.py; see SWARM_CONTEXT.md for how to read it_\n"]
    st = Counter(t["_state"] for t in tasks.values())
    lab = Counter(r.get("status") for r in claims)
    down = sum(1 for r in claims if r.get("claimed_status"))
    workers = sorted({r.get("worker") for r in rows} | {t.get("owner") for t in tasks.values() if t.get("owner")})
    out += ["## Summary",
            f"- **Tasks:** {st['done']} done, {st['claimed']} running, {st['open']} open ({sum(1 for t in tasks.values() if t.get('parent'))} spawned by agents)",
            f"- **Findings (excluding proposed tasks):** {len(claims)}: " + ", ".join(f"{k} {v}" for k, v in lab.most_common()),
            f"- **Passed the 2-critic gate** (kept a strong label): {sum(1 for r in claims if r.get('status') in ('proved','bounded','computed'))}",
            f"- **Downgraded by the gate** (claimed strong, not accepted twice): {down}",
            f"- **Workers:** {', '.join(w for w in workers if w)}\n"]

    out += ["## Accepted results (two blind ACCEPTs)"]
    acc = [r for r in claims if r.get("status") in ("proved", "bounded", "computed")]
    out += [f"- **[{r['status'].upper()}]** {r.get('statement','')}  \n  _{r.get('worker')} · task `{r.get('task')}` · {r.get('critic','')} · evidence `{r.get('evidence','')}`_" for r in acc] or ["- none yet"]

    out += ["\n## Near-proofs (claimed strong, downgraded by the gate)"]
    out += [f"- claimed **[{r['claimed_status'].upper()}]**, now [{r['status'].upper()}]: {r.get('statement','')}  \n  _{r.get('worker')} · task `{r.get('task')}` · {r.get('critic','')}_"
            for r in claims if r.get("claimed_status")] or ["- none"]

    out += ["\n## Dead ends and obstructions"]
    out += [f"- [{r.get('status','').upper()}] {r.get('statement','')}  _({r.get('worker')} · `{r.get('task')}`)_"
            for r in claims if r.get("status") in ("dead_end", "refuted") or r.get("type") == "obstruction"] or ["- none"]

    out += ["\n## Task timeline (done tasks)", "| Finished | Task | Worker | Minutes | Critics | Parent | Result |", "|---|---|---|---|---|---|---|"]
    for t in sorted((t for t in tasks.values() if t["_state"] == "done"), key=lambda t: t.get("finished_at", "")):
        res = os.path.join("swarm", "results", t["id"], "result.md")
        out.append(f"| {t.get('finished_at','')[11:16]} | {t['goal'][:70].replace('|','/')} | {t.get('owner')} | {round(t.get('seconds',0)/60)} | "
                   f"{t.get('critics') or 'not reviewed'} | {t.get('parent') or t.get('created_by','human')} | `{res}` ({git_first_commit(res)}) |")

    out += ["\n## Task tree (who spawned what)"]
    kids = defaultdict(list)
    for t in tasks.values():
        kids[t.get("parent")].append(t)
    def walk(pid, depth):
        for t in sorted(kids.get(pid, []), key=lambda t: t.get("created", "")):
            out.append(f"{'  ' * depth}- `{t['id']}` [{t['_state']}] {t['goal'][:100]}")
            walk(t["id"], depth + 1)
    walk(None, 0)

    open(os.path.join(ROOT, "SWARM_LOG.md"), "w").write("\n".join(out) + "\n")
    print(f"wrote SWARM_LOG.md ({len(tasks)} tasks, {len(claims)} findings)")


if __name__ == "__main__":
    main()
