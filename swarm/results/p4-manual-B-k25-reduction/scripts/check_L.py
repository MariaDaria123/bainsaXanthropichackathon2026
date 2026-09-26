"""Exact-arithmetic check of the numeric facts used in the k = 25 reduction
(result.md, "Setup" and Lemma 3). Pure integers (math.lcm, math.isqrt, //, %);
no floats anywhere. Wrapped in tools/cert.py so tools/rerun.py-style reruns work.

Domain enumerated: the integers 1..24 (to build L = lcm(1..24)) and the integers
2..23 (to list primes <= 23). Nothing is pruned; there are no survivors.

Checks:
  1. L = lcm(1..24) = 5354228880 = 2^4 3^2 5 7 11 13 17 19 23.
  2. E_p = max{e : p^e <= 24} = v_p(L) for every prime p <= 23, and p^(E_p+1) >= 25.
  3. {p prime : 2p > 24, p <= 24} = {13,17,19,23}  (integer comparison 2p > 24).
  4. d(L) = 1920.
Run (from repo root): python3 swarm/results/p4-manual-B-k25-reduction/scripts/check_L.py
Writes: swarm/results/p4-manual-B-k25-reduction/scripts/certificate.json
"""
import math, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")))
from tools.cert import Certificate

K = 25
UPPER = K - 1


def factor(n):
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))


def main():
    cert = Certificate(
        problem="p4", cell="c6",
        domain="integers 1..24 (for L) and 2..23 (for primes <= 23); fixed numeric facts, no search",
        domain_proof="L = lcm(1..24) is by definition determined by 1..24; primes <= 23 lie in 2..23. "
                     "Every fact is also proved by hand in result.md (Setup); this run is a cross-check.",
    )
    with cert.size("numeric-facts-for-k25-reduction (NOT a decision of k=25)") as rec:
        L = 1
        for i in range(1, UPPER + 1):
            cert.node()
            L = math.lcm(L, i)
        facL = factor(L)
        print("L = lcm(1..24) =", L, facL)
        assert L == 5354228880
        assert facL == {2: 4, 3: 2, 5: 1, 7: 1, 11: 1, 13: 1, 17: 1, 19: 1, 23: 1}
        primes = [p for p in range(2, 24) if is_prime(p)]
        assert primes == [2, 3, 5, 7, 11, 13, 17, 19, 23]
        for p in primes:
            e = 0
            while p ** (e + 1) <= UPPER:
                e += 1
            print(f"p={p}: E_p={e}, p^(E_p+1)={p**(e+1)}")
            assert e == facL[p] and p ** (e + 1) >= K
        large = [p for p in primes if 2 * p > UPPER]
        assert large == [13, 17, 19, 23] and all(2 * p > K and p < K for p in large)
        ndiv = 1
        for e in facL.values():
            ndiv *= e + 1
        assert ndiv == 1920
        print("d(L) =", ndiv)
    cert.finish()
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
