"""Exact integer checks for the k/3 < q <= k/2 prime-power extension, k=25.
Verifies: L, E_p table; which q=p^E_p fall in (k/3,k/2]; the case-split bound
(other-part = gcd/q in {1,2}); the double-exceeder exclusion (4q>24);
and that 3q<=24 (triple split) is excluded for q in this range but not below it.
Pure integer arithmetic. Runtime printed.
"""
import time, math

t0 = time.time()
k = 25
K1 = k - 1  # 24, the max allowed pairwise gcd in a counterexample

L = 1
for i in range(1, k - 1 + 1):
    L = math.lcm(L, i)
assert L == 5354228880

def factorize(n):
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f

Lfac = factorize(L)
assert Lfac == {2: 4, 3: 2, 5: 1, 7: 1, 11: 1, 13: 1, 17: 1, 19: 1, 23: 1}

# E_p = exponent of p in L, for primes p <= 23
E = dict(Lfac)

# thresholds q = p^E_p
thresholds = {p: p ** e for p, e in E.items()}
print("thresholds p -> p^E_p:", thresholds)

lo, hi = k / 3, k / 2
in_range = sorted(q for q in thresholds.values() if lo < q <= hi)
print(f"k/3={lo:.4f}, k/2={hi:.4f}, thresholds in (k/3,k/2]: {in_range}")
assert in_range == [9, 11], in_range

# region q > k/2 (single-case-forcing region in general; note this task only
# extends the (k/3,k/2] range, so q=16=2^4 also lying above k/2 is out of scope
# here -- flagged as an observation, not claimed or used below)
above = sorted(q for q in thresholds.values() if q > hi)
print("thresholds > k/2 (informational; includes 16=2^4, out of scope here):", above)
assert set(above) >= {13, 17, 19, 23}

# For each q in {9,11}: check other_part = K1 // q bound, i.e. floor(24/q),
# check 2q <= 24 (case B possible), 3q > 24 (case C impossible),
# and 4q > 24 (double-exceeder-at-2 excluded).
for q in (9, 11):
    max_other = K1 // q  # gcd/q can be at most this many (integer floor)
    print(f"q={q}: floor(24/q)={max_other}, 2q={2*q}<=24:{2*q<=24}, "
          f"3q={3*q}>24:{3*q>24}, 4q={4*q}>24:{4*q>24}")
    assert max_other == 2  # other part in {1,2} only
    assert 2 * q <= K1
    assert 3 * q > K1
    assert 4 * q > K1

# Contrast: q=7 (E_7=1, threshold 7) is <= k/3, so a THIRD case (3q<=24) is
# possible there -- confirms 9,11 are exactly the q's needing a 2-case (not
# 1-case, not >=3-case) split.
q = 7
print(f"q=7 (below k/3={lo:.4f}): 3q={3*q}<=24:{3*q<=K1}")
assert 3 * q <= K1

print(f"ALL CHECKS PASSED in {time.time()-t0:.4f}s")
