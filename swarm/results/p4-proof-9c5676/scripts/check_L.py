"""Exact-arithmetic check of the numeric facts used in the reduction lemma for k = 25.
Runs in well under 1 second. Pure integer arithmetic (math.lcm / math.gcd), no floats.

Checks:
  1. L = lcm(1, ..., 24) and its prime factorisation.
  2. E_p := max{e : p^e <= 24} for every prime p <= 23, and that p^(E_p+1) >= 25
     (the threshold power that Lemma 1 / Corollary 1a needs).
  3. The set of primes p with k/2 < p < k (k=25), i.e. 13 <= p <= 24, is exactly
     {13, 17, 19, 23}, and 2p > 24 for each (so no modulus <= L-bounded search
     range can contain p^2, and t = gcd/p is forced to 1 in Lemma 3(a)).
  4. Number of divisors of L (size of the reduced per-modulus search domain).
"""
import math

K = 25
UPPER = K - 1  # = 24

L = 1
for i in range(1, UPPER + 1):
    L = math.lcm(L, i)


def factor(n):
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


def is_prime(n):
    if n < 2:
        return False
    return all(n % d for d in range(2, int(n ** 0.5) + 1))


def main():
    facL = factor(L)
    print("L = lcm(1..24) =", L)
    print("factorisation of L:", facL)
    assert L == 5354228880
    assert facL == {2: 4, 3: 2, 5: 1, 7: 1, 11: 1, 13: 1, 17: 1, 19: 1, 23: 1}

    primes_le_23 = [p for p in range(2, 24) if is_prime(p)]
    print("primes <= 23:", primes_le_23)
    assert primes_le_23 == [2, 3, 5, 7, 11, 13, 17, 19, 23]

    Ep = {}
    for p in primes_le_23:
        e = 0
        while p ** (e + 1) <= UPPER:
            e += 1
        Ep[p] = e
        thresh = p ** (e + 1)
        print(f"p={p}: E_p={e}, p^(E_p+1)={thresh}, >= {K}? {thresh >= K}")
        assert e == facL.get(p, 0), "E_p must equal v_p(L)"
        assert thresh >= K

    large = [p for p in primes_le_23 if 2 * p > UPPER]
    print("primes with 2p > 24 (forces t=1 in Lemma 3a):", large)
    assert large == [13, 17, 19, 23]
    for p in large:
        assert K / 2 < p < K

    ndiv = 1
    for e in facL.values():
        ndiv *= (e + 1)
    print("number of positive divisors of L:", ndiv)
    assert ndiv == 1920

    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
