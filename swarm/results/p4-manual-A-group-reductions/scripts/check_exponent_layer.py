"""
Exhaustive exact check of the PAIRWISE statements in the Sub-lemma of result.md,
over all pairs 1 <= a <= b <= N (N = 3000):
  if gcd(a,b) in {2,3,4,5} then, with D(x) = {p in {2,3,5} : p | x},
  (a) D(a), D(b) nonempty; (b) |D(a) & D(b)| = 1;
  (c) writing {p} = D(a) & D(b):  gcd(a,b) = p**min(v_p(a), v_p(b)),
      hence min(v_2) in {1,2} if p = 2, and min(v_p) = 1 if p in {3,5}.
This is a falsification test of a proved lemma (not a proof). Exact int only.
Run: python3 swarm/results/p4-manual-A-group-reductions/scripts/check_exponent_layer.py
"""
from math import gcd
import time

def v(p, x):
    e = 0
    while x % p == 0:
        x //= p; e += 1
    return e

N = 3000
t = time.time(); checked = 0
for a in range(1, N + 1):
    Da = {p for p in (2, 3, 5) if a % p == 0}
    for b in range(a, N + 1):
        g = gcd(a, b)
        if g not in (2, 3, 4, 5):
            continue
        checked += 1
        Db = {p for p in (2, 3, 5) if b % p == 0}
        I = Da & Db
        assert Da and Db and len(I) == 1, (a, b)
        (p,) = I
        m = min(v(p, a), v(p, b))
        assert g == p ** m, (a, b)
        assert (m in (1, 2)) if p == 2 else (m == 1), (a, b)
print(f"pairs with gcd in {{2,3,4,5}} checked: {checked}; all assertions hold; {time.time()-t:.1f}s")
