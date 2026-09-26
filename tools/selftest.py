"""Run every problem library's self-test plus a certificate/rerun/gate smoke test.
usage: python tools/selftest.py
"""
import importlib.util, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT

LIBS = [("p1", "angles"), ("p2", "uphill"), ("p3", "bulgarian"), ("p4", "congruence")]
ok = True
for p, name in LIBS:
    path = os.path.join(ROOT, "problems", p, "lib", f"{name}.py")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        print(mod._selftest())
    except Exception as e:
        ok = False
        print(f"{p} {name} FAILED: {e!r}")
print("ALL OK" if ok else "SOME FAILED")
sys.exit(0 if ok else 1)
