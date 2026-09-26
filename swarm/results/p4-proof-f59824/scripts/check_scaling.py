"""
For each of the 4 patterns found by enumerate_patterns.py, exhibit an explicit
integer 6-tuple (n_1,...,n_6) realising that pattern, with every pairwise gcd
in {2,3,4,5} and sum(1/n_i) <= 1, using exact Fraction arithmetic.

This shows constraints (ii)+(iii) alone (necessary conditions on the *indices*)
do NOT rule out k=6: every pattern can be scaled to satisfy the density bound.
It does NOT construct an actual disjoint-coset counterexample (that would also
require realising these n_i as indices of subgroups of a single group G with
pairwise disjoint cosets, which is the open part of the problem).

Runtime: < 1 second.
"""
from fractions import Fraction
from math import gcd
from itertools import combinations

def report(name, ns):
    k = len(ns)
    pair_gcds = {(i, j): gcd(ns[i], ns[j]) for i, j in combinations(range(k), 2)}
    s = sum(Fraction(1, n) for n in ns)
    ok_range = all(2 <= g <= 5 for g in pair_gcds.values())
    ok_sum = s <= 1
    print(f"{name}: n = {ns}")
    print(f"  pairwise gcds = {sorted(pair_gcds.values())}  all in [2,5]: {ok_range}")
    print(f"  sum 1/n_i = {s}  <= 1: {ok_sum}")
    assert ok_range and ok_sum
    print()

# distinct primes >= 7, unused elsewhere, to serve as "private" cofactors
cof = [11, 13, 17, 19, 23, 29, 31]

# Pattern I: all six D_i = {2}
ns = [2 * cof[i] for i in range(6)]
report("Pattern I  (all singleton {2})", ns)

# Pattern II: one D_1 = {2,3}, five D_i = {2}
ns = [6 * cof[0]] + [2 * cof[i] for i in range(1, 6)]
report("Pattern II (one {2,3} + five {2})", ns)

# Pattern III: D_1={2,3}, D_2={2,5}, four D_i={2}
ns = [6 * cof[0], 10 * cof[1]] + [2 * cof[i] for i in range(2, 6)]
report("Pattern III (one {2,3}, one {2,5}, four {2})", ns)

# Pattern IV: D_1={2,3,5}, five D_i={2}
ns = [30 * cof[0]] + [2 * cof[i] for i in range(1, 6)]
report("Pattern IV (one {2,3,5} + five {2})", ns)

print("All 4 patterns realised with pairwise gcd in [2,5] and density <= 1.")
