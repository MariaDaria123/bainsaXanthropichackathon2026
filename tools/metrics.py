"""Build METRICS.md from every cell's log.jsonl: the system stats for the demo.

usage: python tools/metrics.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CELLS, PROBLEMS, ROOT, cell_dir, now, read_log


def main():
    rows, tot = [], {"cells_run": 0, "passed": 0, "passed_no_human": 0, "verify": 0, "verify_fail": 0,
                     "minutes": 0.0, "cost": 0.0, "human": 0, "reruns": 0, "rerun_fail": 0}
    for p in PROBLEMS:
        for c in CELLS:
            L = read_log(p, c)
            if not L:
                continue
            tot["cells_run"] += 1
            stages = [e for e in L if e["event"] == "stage"]
            ver = [e for e in stages if e.get("stage") == "verify"]
            vfail = [e for e in ver if e.get("verdict") != "PASS"]
            human = [e for e in L if e["event"] == "human"]
            reruns = [e for e in L if e["event"] == "rerun"]
            mins = sum(e.get("seconds", 0) for e in stages) / 60
            cost = sum(e.get("cost_usd") or 0 for e in stages)
            gates = [e for e in L if e["event"] == "gate"]
            passed = bool(gates and gates[-1].get("passed"))
            status = gates[-1].get("status") if passed else ""
            rounds = max([e.get("round", 0) for e in stages] or [0])
            tot["passed"] += passed
            tot["passed_no_human"] += passed and not human
            tot["verify"] += len(ver); tot["verify_fail"] += len(vfail)
            tot["minutes"] += mins; tot["cost"] += cost; tot["human"] += len(human)
            tot["reruns"] += len(reruns); tot["rerun_fail"] += sum(1 for e in reruns if not e.get("ok"))
            rows.append(f"| {p} {c} | {'PASS' if passed else 'open'} | {status} | {rounds} | {len(vfail)}/{len(ver)} | "
                        f"{len(human)} | {mins:.1f} | ${cost:.2f} |")
    rej = tot["verify_fail"] / tot["verify"] if tot["verify"] else 0
    auto = tot["passed_no_human"] / tot["passed"] if tot["passed"] else 0
    out = [f"# System metrics\n_generated {now()}_\n",
           f"- **Cells attempted:** {tot['cells_run']}  |  **passed gate:** {tot['passed']}",
           f"- **Passed with zero human interventions:** {tot['passed_no_human']} ({auto:.0%})",
           f"- **Verifier rejections:** {tot['verify_fail']}/{tot['verify']} reviews ({rej:.0%}) — errors caught before submission",
           f"- **Certificate reruns:** {tot['reruns']} ({tot['rerun_fail']} failed)",
           f"- **Agent time:** {tot['minutes']:.0f} min  |  **cost:** ${tot['cost']:.2f}  |  **human interventions:** {tot['human']}\n",
           "| Cell | Gate | Status | Rounds | Verifier FAIL/total | Human | Minutes | Cost |",
           "|---|---|---|---|---|---|---|---|", *rows]
    open(os.path.join(ROOT, "METRICS.md"), "w").write("\n".join(out) + "\n")
    print("\n".join(out[:7]))


if __name__ == "__main__":
    main()
