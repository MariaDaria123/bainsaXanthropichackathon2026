"""TEMPLATE certificate search (copy to problems/pX/cells/cY/cert/search.py and adapt).

Example claim (toy, p4): there is no family of 3 pairwise disjoint classes with
moduli in [2, M] and all pairwise gcds equal to 2, for M = 8, 10, 12.
NOTE: bounded moduli alone do NOT settle the cell. A real certificate needs a proof
(in proof.md, "Computation") that nothing outside the enumerated set can be a counterexample.
"""
import os, sys
from math import gcd
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = next(p for p in [HERE, *[os.path.join(HERE, *[".."] * i) for i in range(1, 7)]]
            if os.path.exists(os.path.join(p, "tools", "cert.py")))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from cert import Certificate

C = Certificate(problem="p4", cell="example",
                domain="ordered triples (a_i mod m_i), i=1..3, with 2 <= m_i <= M, 0 <= a_i < m_i, "
                       "classes listed in increasing (m, a) order",
                domain_proof="toy: the domain is the claim itself (bounded moduli). Real cells need a reduction lemma.")
C.rule("R1", "Order: only increasing sequences (m1,a1) < (m2,a2) < (m3,a3) are enumerated.",
       "Pairwise disjointness and the gcd condition are symmetric in the family, so each unordered family "
       "is represented by exactly one increasing sequence; repeated classes are never disjoint from themselves.")
C.rule("R2", "Prune a partial family as soon as some pair has gcd != 2 or meets.",
       "Both conditions are pairwise and are inherited by every extension, so no extension can satisfy them.")

for M in (8, 10, 12):
    classes = [(m, a) for m in range(2, M + 1) for a in range(m)]
    with C.size(M):
        def extend(fam, start):
            C.node()
            if len(fam) == 3:
                C.survivor(fam, decision="counterexample", minimal_part=fam,
                           minimality_proof="a counterexample needs all 3 classes")
                return
            for idx in range(start, len(classes)):
                m, a = classes[idx]
                if any(gcd(m, m2) != 2 or (a - a2) % gcd(m, m2) == 0 for m2, a2 in fam):
                    C.prune("R2")
                    continue
                extend(fam + [(m, a)], idx + 1)
        extend([], 0)
C.finish()
