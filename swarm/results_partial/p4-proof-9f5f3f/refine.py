# Refined omega count for l>=4, k in {32,38,42,44,48}. Exact integers. Runtime a few seconds.
# Config = sizes (n_1..n_l) of P_1..P_l (n_s>=1, sum<=pi(k-1)-1) and placement of each small prime
# q in SMALL (primes<k, !=p, in some bad triple) into a coordinate or 'none'.
# For a 3-set T of coordinates, bound(T) = prod_{s in T} n_s - R_T + R_T * prod_{s notin T} n_s,
# where R_T = number of bad triples rainbow on T (three primes in three distinct P_s, s in T).
# Claim: k-l <= min_T bound(T). The configuration is excluded if k-l > min_T bound(T).
from itertools import combinations, product
from math import prod
from sympy import primepi, primerange
def bad_triples(k):
    ps = list(primerange(2, k))
    return [t for t in combinations(ps, 3) if prod(t) < k]
def compositions(S, l):
    # all tuples of l positive ints with sum <= S
    def rec(rem, parts):
        if parts == 0:
            yield (); return
        for x in range(1, rem - (parts - 1) + 1):
            for rest in rec(rem - x, parts - 1):
                yield (x,) + rest
    yield from rec(S, l)
Ks = {32:[4,5], 38:[4,5,6], 42:[4,5,6], 44:[4,5,6,7], 48:[4,5,6,7,8]}
nodes = 0
for k, ls in Ks.items():
    r = int(primepi(k-1)); B = bad_triples(k)
    small = sorted(set(q for t in B for q in t))
    for l in ls:
        worst = None
        for n in compositions(r-1, l):
            if n != tuple(sorted(n, reverse=True)):   # coordinates are interchangeable only up to
                pass                                   # relabelling; we do NOT use symmetry: check all
            for place in product(range(-1, l), repeat=len(small)):
                cnt = [0]*l
                for c in place:
                    if c >= 0: cnt[c] += 1
                if any(cnt[s] > n[s] for s in range(l)): continue
                pos = dict(zip(small, place))
                nodes += 1
                best = None
                for T in combinations(range(l), 3):
                    RT = sum(1 for t in B if all(pos[q] in T for q in t) and len({pos[q] for q in t}) == 3)
                    rest = prod(n[s] for s in range(l) if s not in T)
                    b = prod(n[s] for s in T) - RT + RT * rest
                    best = b if best is None else min(best, b)
                if worst is None or best > worst[0]: worst = (best, n, place)
        status = "EXCLUDED" if k - l > worst[0] else "survives"
        print(f"k={k} l={l}: k-l={k-l}, max over configs of min_T bound = {worst[0]} (at sizes {worst[1]}, placement of {small} = {worst[2]}) -> {status}")
print("configs checked:", nodes)
