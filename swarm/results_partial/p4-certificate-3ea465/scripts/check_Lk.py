"""Exact check of L_k = lcm(1,...,k-1) and its factorisation for k = 21, 22, 23.
Integer arithmetic only (math.lcm, trial-division factorisation). Runtime < 0.1 s.
"""
import math


def factorize(n):
    fac, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            fac[d] = fac.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        fac[n] = fac.get(n, 0) + 1
    return fac


def ndivisors(fac):
    p = 1
    for e in fac.values():
        p *= (e + 1)
    return p


if __name__ == "__main__":
    Ls = {}
    for k in (21, 22, 23):
        L = 1
        for i in range(1, k):
            L = math.lcm(L, i)
        Ls[k] = L
        fac = factorize(L)
        print(f"k={k}: L_k=lcm(1..{k-1})={L}  factorisation={fac}  d(L_k)={ndivisors(fac)}")
    assert Ls[21] == Ls[22] == Ls[23] == 232792560, "expected all three L_k equal"
    fac = factorize(232792560)
    assert fac == {2: 4, 3: 2, 5: 1, 7: 1, 11: 1, 13: 1, 17: 1, 19: 1}
    assert ndivisors(fac) == 960
    big_primes = {k: sorted(p for p in fac if p >= -(-k // 2)) for k in (21, 22, 23)}
    print("primes >= ceil(k/2):", big_primes)
    assert big_primes[21] == [11, 13, 17, 19]
    assert big_primes[22] == [11, 13, 17, 19]
    assert big_primes[23] == [13, 17, 19]      # ceil(23/2)=12 excludes 11
    print("ALL CHECKS PASSED")
