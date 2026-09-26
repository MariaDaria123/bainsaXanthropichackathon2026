"""
Certificate-wrapped version of enumerate_patterns.py, using tools/cert.py's
Certificate object per CLAUDE.md rule 4. This is the swarm-stage certificate;
promoting this cell (problems/p4/cells/c6/) still requires copying this logic
into problems/p4/cells/c6/cert/search.py so that `python tools/rerun.py p4 c6`
and `python tools/gate.py p4 c6` can run against it directly (see "What remains
open" in result.md) - this task is only authorized to write inside
swarm/results/p4-manual-A-group-reductions/, so that copy step is left for promotion time.

Run: python3 swarm/results/p4-manual-A-group-reductions/scripts/cert_search.py
Writes: swarm/results/p4-manual-A-group-reductions/scripts/certificate.json
Runtime: < 1 second.
"""
import os
import sys
from itertools import combinations, permutations, product

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")))
from tools.cert import Certificate

PRIMES = (2, 3, 5)
SUBSETS = [frozenset(s) for r in range(1, 4) for s in combinations(PRIMES, r)]  # 7 nonempty subsets


def canonical(Dtuple):
    best = None
    for perm in permutations(PRIMES):
        remap = dict(zip(PRIMES, perm))
        relabeled = tuple(frozenset(remap[p] for p in D) for D in Dtuple)
        key = tuple(sorted(tuple(sorted(D)) for D in relabeled))
        if best is None or key < best:
            best = key
    return best


def valid(Dtuple):
    for i, j in combinations(range(6), 2):
        if len(Dtuple[i] & Dtuple[j]) != 1:
            return False
    return True


def main():
    cert = Certificate(
        problem="p4", cell="c6",
        domain="all functions D: {1,...,6} -> {7 nonempty subsets of {2,3,5}}, i.e. 7^6 = 117649 tuples",
        domain_proof=(
            "Sub-lemma (result.md): if every pairwise gcd(n_i,n_j) in a k=6 group-form "
            "counterexample lies in {2,3,4,5} (forced by Lemma 2 giving gcd>=2 and the "
            "counterexample hypothesis giving gcd<=5), then D_i := {p in {2,3,5}: p|n_i} "
            "is one of the 7 nonempty subsets of {2,3,5} for every i and |D_i & D_j| = 1 for "
            "i != j (any prime >=7 dividing gcd(n_i,n_j) would force that gcd >= 7 > 5, "
            "excluded). This is a NECESSARY condition only: D_i forgets exponents, and the "
            "exponent layer (Sub-lemma (c) in result.md) is a further necessary condition not "
            "encoded in this domain. Hence every "
            "D-tuple compatible with a k=6 counterexample lies in this 7^6-element domain, "
            "and the domain is exhaustive by construction (every one of the 7 subsets per "
            "index is tried, no restriction is assumed in advance)."
        ),
    )
    with cert.size(6) as rec:
        seen = {}
        n_valid = 0
        for Dtuple in product(SUBSETS, repeat=6):
            cert.node()
            if valid(Dtuple):
                n_valid += 1
                key = canonical(Dtuple)
                if key not in seen:
                    seen[key] = Dtuple
        rec["n_valid_tuples"] = n_valid
        for key, Dtuple in seen.items():
            cert.survivor(
                key,
                decision="classified: one of the 4 shared-prime patterns compatible with a k=6 "
                         "group-form counterexample's pairwise-gcd constraints (realizability by an "
                         "actual group is NOT decided by this search - see result.md)",
                minimal_part=key,
                minimality_proof=(
                    "The D-tuple itself is the object being classified; each of the 6 entries "
                    "and all 15 pairwise intersections are needed to state |D_i cap D_j|=1 for "
                    "every pair, so no proper sub-tuple determines membership in this pattern."
                ),
            )
    data = cert.finish()
    assert data["certified_sizes"] == [6], data
    assert rec["n_valid_tuples"] == 147, rec["n_valid_tuples"]
    assert len(seen) == 4, len(seen)
    print("OK: 117649 nodes visited, 147 valid tuples, 4 certified patterns.")


if __name__ == "__main__":
    main()
