"""Falsification test (not a proof) of Lemma 2 and of the whole reduction procedure of
the Main Reduction Theorem, transplanted to general k: for random families of k classes
(k in 3..8, moduli up to 2000, seed 12) we
  (1) apply the reduction: for every prime p, if at most one index exceeds E_p(k) =
      max{e: p^e <= k-1}, lower that index's v_p to E_p(k) (Lemma 2 with c = E_p(k));
  (2) assert every pairwise gcd is unchanged, pairwise disjointness status of every pair
      is unchanged (criterion (*) via problems/p4/lib/congruence.py), and that if every
      prime had at most one exceeder then every reduced modulus divides lcm(1..k-1).
Exact integers only. Run: python3 swarm/results/p4-manual-B-k25-reduction/scripts/test_lemma2.py
"""
import math, os, random, sys, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "problems", "p4", "lib")))
from congruence import meet


def factor(n):
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1; n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def E(p, k):
    e = 0
    while p ** (e + 1) <= k - 1:
        e += 1
    return e


random.seed(12)
t = time.time(); trials = full = steps = 0
for _ in range(20000):
    k = random.randint(3, 8)
    ms = [random.randint(1, 2000) for _ in range(k)]
    As = [random.randint(0, 5000) for _ in range(k)]
    red = list(ms)
    primes = set()
    for m in ms:
        primes |= set(factor(m))
    all_ok = True
    for p in sorted(primes):
        c = E(p, k)
        exc = [i for i in range(k) if red[i] % p ** (c + 1) == 0]
        if len(exc) > 1:
            all_ok = False
            continue
        if exc:
            i = exc[0]
            while red[i] % p ** (c + 1) == 0:
                red[i] //= p
            steps += 1
    for i in range(k):
        for j in range(i + 1, k):
            assert math.gcd(red[i], red[j]) == math.gcd(ms[i], ms[j]), (ms, red)
            assert meet((As[i], red[i]), (As[j], red[j])) == meet((As[i], ms[i]), (As[j], ms[j]))
    if all_ok:
        full += 1
        Lk = math.lcm(*range(1, k))
        assert all(Lk % r == 0 for r in red), (ms, red, k)
    trials += 1
print(f"trials {trials}, lowering steps {steps}, fully reduced families {full}: all assertions hold; {time.time()-t:.1f}s")

# Theorem 2' normal-form loop, on random families whose pairwise gcds are all <= k-1
random.seed(12)
nf = 0; t2 = time.time()
while nf < 3000:
    k = random.randint(3, 8)
    ms = [random.randint(2, 3000) for _ in range(k)]
    if any(math.gcd(ms[i], ms[j]) > k - 1 for i in range(k) for j in range(i + 1, k)):
        continue
    As = [random.randint(0, 5000) for _ in range(k)]
    red = list(ms)
    changed = True
    while changed:
        changed = False
        primes = set()
        for m in red:
            primes |= set(factor(m))
        for p in sorted(primes):
            vals = []
            for m in red:
                e = 0
                while m % p ** (e + 1) == 0:
                    e += 1
                vals.append(e)
            top = max(vals)
            if top >= 1 and vals.count(top) == 1:
                i = vals.index(top)
                c = max(v for j, v in enumerate(vals) if j != i)
                red[i] //= p ** (top - c)
                changed = True
                break
    for i in range(k):
        for j in range(i + 1, k):
            assert math.gcd(red[i], red[j]) == math.gcd(ms[i], ms[j])
            assert meet((As[i], red[i]), (As[j], red[j])) == meet((As[i], ms[i]), (As[j], ms[j]))
    Lk = math.lcm(*range(1, k))
    assert all(Lk % r == 0 for r in red), (ms, red, k)
    nf += 1
print(f"Theorem 2' loop: {nf} families with all gcds <= k-1 normalised; gcds, meet relations preserved; all moduli divide lcm(1..k-1); {time.time()-t2:.1f}s")
