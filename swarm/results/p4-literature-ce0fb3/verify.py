"""Exact checks for the O'Bryant 2006 Lemma 6 audit. Run: python verify.py  (< 5 s)."""
from math import gcd, lcm, prod
from itertools import combinations, product
from functools import reduce
from sympy import primepi, primerange, divisors, factorint

def maxprod(S, l):
    # max prod of l positive integers with sum <= S (0 if infeasible); exhaustive over partitions
    if l > S: return 0
    best = 0
    def rec(rem, parts, cur):
        nonlocal best
        if parts == 0:
            best = max(best, cur); return
        for x in range(1, rem - (parts - 1) + 1):
            rec(rem - x, parts - 1, cur * x)
    rec(S, l, 1)
    return best

print("== item 8 pigeonhole table: need k-l > maxprod(pi(k-1)-1, l) for 3<=l ==")
fails = []
for k in range(7, 31):
    r = int(primepi(k - 1))
    for l in range(3, k + 1):
        mp = maxprod(r - 1, l)
        if mp == 0: continue          # l disjoint nonempty P_s impossible
        if not (k - l > mp): fails.append((k, r, l, mp))
print("r values:", {k: int(primepi(k-1)) for k in range(7, 31)})
print("failures (k,r,l,maxprod):", fails)
print("paper table rows:", {r: [maxprod(r-1, l) for l in range(3, 10)] for r in range(4, 11)})

print("== section 4.3: k with k-1 prime, 7<=k<=30 ==")
print([k for k in range(7, 31) if factorint(k-1).keys() == {k-1}])

def lemma5_ok(ms):
    g = [gcd(a, b) for a, b in combinations(ms, 2)]
    M = reduce(lcm, g, 1)
    return sum(__import__('fractions').Fraction(1, gcd(m, M)) for m in ms) <= 1

def all_subsets_ok(ms):
    return all(lemma5_ok(list(s)) for t in range(2, len(ms)+1) for s in combinations(ms, t))

print("== k=7 example 20,15,12,6,6,6,6 ==")
ex = [20, 15, 12, 6, 6, 6, 6]
print("pairwise gcd in (1,7):", all(1 < gcd(a, b) < 7 for a, b in combinations(ex, 2)))
print("whole family passes Lemma5 with M=lcm gcds:", lemma5_ok(ex))
print("subset 15,12,6,6,6,6 passes:", lemma5_ok([15, 12, 6, 6, 6, 6]))

print("== Sun's Huhn-Megyesi counterexample 10,15,36,42,66 ==")
S = [10, 15, 36, 42, 66]
print("every subset passes Lemma5:", all_subsets_ok(S))
# exhaustive: a_1 = 0 by translation (translation preserves disjointness); others over full residue range
found = None
for a in product(range(15), range(36), range(42), range(66)):
    A = (0,) + a
    ok = True
    for i in range(5):
        for j in range(i+1, 5):
            if (A[i] - A[j]) % gcd(S[i], S[j]) == 0: ok = False; break
        if not ok: break
    if ok: found = A; break
print("disjoint residues exist:", found)

print("== section 4.1 small k: admissible moduli (divisors of L_k, >=2 prime factors) ==")
for k in range(3, 7):
    L = reduce(lcm, range(1, k), 1)
    print(k, L, [d for d in divisors(L) if len(factorint(d)) > 1])
