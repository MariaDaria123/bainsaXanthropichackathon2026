"""Re-execute search.py for each certified branch and compare counts (mirrors tools/rerun.py KEYS)."""
import json, os, subprocess, sys, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
KEYS = ["nodes", "pruned", "n_survivors", "n_undecided", "finished", "certified"]
sha = hashlib.sha256(open(os.path.join(HERE, "search.py"), "rb").read()).hexdigest()
ok = True
for name in sys.argv[1:]:
    claimed = json.load(open(os.path.join(HERE, f"certificate_{name}.json")))
    out = os.path.join(HERE, f"rerun_{name}.json")
    subprocess.run([sys.executable, os.path.join(HERE, "search.py"), name, "600"],
                   env=dict(os.environ, CERT_OUT=out), check=True, capture_output=True, timeout=600)
    new = json.load(open(out))
    diffs = [] if claimed["script_sha256"] == sha else ["search.py changed since certificate"]
    for a, b in zip(claimed["sizes"], new["sizes"]):
        diffs += [f"{k}: {a.get(k)} vs {b.get(k)}" for k in KEYS if a.get(k) != b.get(k)]
    ok &= not diffs
    print(name, "OK" if not diffs else diffs, new["sizes"][0]["nodes"], "nodes", new["total_wall_s"], "s")
print("ALL OK" if ok else "MISMATCH")
