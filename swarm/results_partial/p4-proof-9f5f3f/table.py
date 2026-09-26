# Exact integer check: which (k, l) survive the item-8 counting test k-l > maxprod(pi(k-1)-1, l)
# for k in {32,38,42,44,48} (k-1 prime). Runtime < 1 s.
from sympy import primepi, isprime, primerange
from math import prod
def maxprod(S, l):
    # largest product of l positive integers with sum <= S; 0 if l > S. Exhaustive recursion.
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
Ks = [32, 38, 42, 44, 48]
assert all(isprime(k-1) for k in Ks)
assert [k for k in range(31, 49) if isprime(k-1)] == Ks
for k in Ks:
    r = int(primepi(k-1))
    surv = []
    for l in range(3, k+1):
        mp = maxprod(r-1, l)
        if mp == 0: continue
        small = prod(list(primerange(2, 200))[:l])   # product of the l smallest primes
        if not (k - l > mp):
            surv.append((l, mp, k-l, 'omega-injective' if small >= k else 'collisions allowed'))
    print(f"k={k} r=pi(k-1)={r}: surviving l (l, maxprod, k-l, note):", surv)
