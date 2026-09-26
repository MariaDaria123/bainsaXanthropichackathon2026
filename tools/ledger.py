"""Build LEDGER.md: per problem, what is Known (cited), Established by us (gated), and Conjectured.

usage: python tools/ledger.py
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CELLS, PROBLEMS, ROOT, cell_dir, now, problem_dir


def section(text, header):
    m = re.search(rf"^## {re.escape(header)}\s*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""


def main():
    out = [f"# Ledger — Known / Ours / Conjecture\n_generated {now()}_\n"]
    for p in PROBLEMS:
        title = open(os.path.join(problem_dir(p), "problem.md")).readline().lstrip("# ").strip()
        out.append(f"\n## {p} — {title}\n")
        out.append("| Cell | Gate | Status | Established by us (claim) |\n|---|---|---|---|")
        known, conj = [], []
        for c in CELLS:
            d = cell_dir(p, c)
            g = json.load(open(os.path.join(d, "gate.json"))) if os.path.exists(os.path.join(d, "gate.json")) else {}
            claim = ""
            if g.get("pass") and os.path.exists(os.path.join(d, "proof.md")):
                claim = section(open(os.path.join(d, "proof.md")).read(), "Claim").replace("\n", " ")[:300]
            out.append(f"| {c} | {'PASS' if g.get('pass') else ('fail' if g else '—')} | {g.get('status') or ''} | {claim} |")
            kp = os.path.join(d, "known.md")
            if os.path.exists(kp):
                for line in open(kp):
                    if re.match(r"\s*- \[(PROVED|COMPUTED|GAP)\]", line):
                        known.append(f"{c}: {line.strip()[2:]}")
                    elif re.match(r"\s*- \[CONJ\]", line):
                        conj.append(f"{c}: {line.strip()[2:]}")
            ep = os.path.join(d, "explore.md")
            if os.path.exists(ep):
                for line in open(ep):
                    if "PATTERN" in line:
                        conj.append(f"{c} (ours, numerical): {line.strip().lstrip('- ')}")
        out.append("\n**Known (cited)**\n" + ("\n".join(f"- {k}" for k in dict.fromkeys(known)) or "- none yet"))
        out.append("\n**Conjectures / numerical evidence (not established)**\n" + ("\n".join(f"- {k}" for k in dict.fromkeys(conj)) or "- none yet"))
    open(os.path.join(ROOT, "LEDGER.md"), "w").write("\n".join(out) + "\n")
    print("wrote LEDGER.md")


if __name__ == "__main__":
    main()
