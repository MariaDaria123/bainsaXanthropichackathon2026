"""Re-execute a cell's cert/search.py and check that it reproduces the certificate.

usage: python tools/rerun.py p4 c3 [--timeout 600]
Writes cert/rerun.json with ok: true/false and every discrepancy.
"""
import argparse, hashlib, json, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import cell_dir, log, now

KEYS = ["nodes", "pruned", "n_survivors", "n_undecided", "finished", "certified"]


def rerun(p, c, timeout=600):
    d = os.path.join(cell_dir(p, c), "cert")
    script, claimed_path = os.path.join(d, "search.py"), os.path.join(d, "certificate.json")
    out_path, rerun_cert = os.path.join(d, "rerun.json"), os.path.join(d, "rerun_certificate.json")
    res = {"t": now(), "ok": False, "diffs": []}
    if not os.path.exists(script):
        res["diffs"].append("no cert/search.py")
    elif not os.path.exists(claimed_path):
        res["diffs"].append("no cert/certificate.json - run search.py first")
    else:
        claimed = json.load(open(claimed_path))
        sha = hashlib.sha256(open(script, "rb").read()).hexdigest()
        if sha != claimed.get("script_sha256"):
            res["diffs"].append("search.py changed since certificate.json was produced - re-run search.py")
        env = dict(os.environ, CERT_OUT=rerun_cert)
        t = time.perf_counter()
        try:
            proc = subprocess.run([sys.executable, script], env=env, capture_output=True, text=True, timeout=timeout)
            res["wall_s"] = round(time.perf_counter() - t, 2)
            res["returncode"] = proc.returncode
            res["stderr_tail"] = proc.stderr[-2000:]
            if proc.returncode != 0:
                res["diffs"].append(f"search.py exited with {proc.returncode}")
        except subprocess.TimeoutExpired:
            res["wall_s"] = timeout
            res["diffs"].append(f"TIMEOUT after {timeout}s - over the 10 minute limit")
        if os.path.exists(rerun_cert) and not any("exited" in x or "TIMEOUT" in x for x in res["diffs"]):
            new = json.load(open(rerun_cert))
            a = {str(s["size"]): s for s in claimed["sizes"]}
            b = {str(s["size"]): s for s in new["sizes"]}
            if set(a) != set(b):
                res["diffs"].append(f"sizes differ: claimed {sorted(a)} rerun {sorted(b)}")
            for k in sorted(set(a) & set(b)):
                for key in KEYS:
                    if a[k].get(key) != b[k].get(key):
                        res["diffs"].append(f"size {k}: {key} claimed={a[k].get(key)} rerun={b[k].get(key)}")
            res["certified_sizes"] = new["certified_sizes"]
            res["nodes"] = {k: b[k]["nodes"] for k in b}
        res["ok"] = not res["diffs"]
    json.dump(res, open(out_path, "w"), indent=1)
    log(p, c, "rerun", ok=res["ok"], wall_s=res.get("wall_s"), diffs=res["diffs"][:10])
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("p"); ap.add_argument("c"); ap.add_argument("--timeout", type=int, default=600)
    a = ap.parse_args()
    r = rerun(a.p, a.c, a.timeout)
    print(json.dumps(r, indent=1))
    sys.exit(0 if r["ok"] else 1)
