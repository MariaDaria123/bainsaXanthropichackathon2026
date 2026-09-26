"""p4 — Disjoint congruence classes.

A class is a pair (a, m), m >= 1, meaning a (mod m).
(*)  a1 (mod m1) and a2 (mod m2) meet  <=>  gcd(m1, m2) | a1 - a2.
Question: k pairwise disjoint classes => some pair has gcd(m_i, m_j) >= k ?
A counterexample of size k is k pairwise disjoint classes with every pairwise gcd <= k-1.

`find_counterexample` is an EXPLORATORY bounded search (moduli <= M). It is not a
certificate on its own: turning it into one needs a proof that moduli can be
bounded (a reduction), which is the mathematical content of cells c3-c5. Use
tools/cert.py for any search that a proof relies on.
"""
from fractions import Fraction
from math import gcd
from itertools import combinations


def meet(c1, c2):
    (a1, m1), (a2, m2) = c1, c2
    return (a1 - a2) % gcd(m1, m2) == 0


def disjoint(c1, c2):
    return not meet(c1, c2)


def check_family(fam):
    """Return dict: pairwise_disjoint, max_gcd, gcds, density (exact), is_counterexample."""
    k = len(fam)
    pairs = list(combinations(range(k), 2))
    dis = all(disjoint(fam[i], fam[j]) for i, j in pairs)
    gcds = {(i, j): gcd(fam[i][1], fam[j][1]) for i, j in pairs}
    mx = max(gcds.values()) if gcds else None
    return {"k": k, "pairwise_disjoint": dis, "max_gcd": mx, "gcds": gcds,
            "density": sum(Fraction(1, m) for _, m in fam),
            "is_counterexample": dis and mx is not None and mx <= k - 1}


def normalise(fam):
    return sorted(((a % m, m) for a, m in fam), key=lambda t: (t[1], t[0]))


def find_counterexample(k, M, node_limit=None):
    """Search for k pairwise disjoint classes, moduli in [2, M], all pairwise gcd <= k-1.
    Bitset clique search. Returns (family or None, nodes_visited, finished)."""
    classes = [(a, m) for m in range(2, M + 1) for a in range(m)]
    n = len(classes)
    nbr = [0] * n                                   # compatible pairs: disjoint and gcd <= k-1
    for i in range(n):
        ai, mi = classes[i]
        for j in range(i + 1, n):
            aj, mj = classes[j]
            g = gcd(mi, mj)
            if g <= k - 1 and (ai - aj) % g != 0:
                nbr[i] |= 1 << j
                nbr[j] |= 1 << i
    nodes = 0
    stack = [((1 << n) - 1, [])]
    found = None
    while stack:
        cand, chosen = stack.pop()
        nodes += 1
        if node_limit and nodes > node_limit:
            return None, nodes, False
        if len(chosen) == k:
            found = [classes[i] for i in chosen]
            break
        if bin(cand).count("1") < k - len(chosen):
            continue
        c = cand
        while c:
            low = c & -c
            i = low.bit_length() - 1
            c ^= low
            stack.append((c & nbr[i], chosen + [i]))     # only later indices -> each set once
    return found, nodes, True


def _selftest():
    ex = check_family([(0, 2), (1, 4), (3, 8)])
    assert ex["pairwise_disjoint"] and sorted(ex["gcds"].values()) == [2, 2, 4] and ex["max_gcd"] == 4
    assert meet((0, 2), (0, 3))
    for k in range(2, 7):                            # sharpness example 1..k mod k
        r = check_family([(i, k) for i in range(1, k + 1)])
        assert r["pairwise_disjoint"] and r["max_gcd"] == k and not r["is_counterexample"]
    fam, nodes, done = find_counterexample(3, 12)
    assert done and fam is None, fam                 # sanity: none with moduli <= 12 for k = 3
    return "p4 congruence OK"


if __name__ == "__main__":
    print(_selftest())
