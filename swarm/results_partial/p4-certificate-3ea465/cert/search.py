"""Certified search for size-k counterexamples to the disjoint-congruence-classes
claim, k = 21, 22, 23, restricted to moduli that are C1-filtered divisors of
L_k = lcm(1,...,k-1), applying constraints C1-C4 as pruning rules on the MODULUS
MULTISET (not yet full residue assignment -- see "What remains open").

Run: python3 search.py   (writes certificate.json next to this file; CERT_OUT overrides)
Time budget: hard wall-clock cap TIME_BUDGET_S per k, well under the 10-minute rule limit.
"""
import os, sys, time, math
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = next(p for p in [HERE, *[os.path.join(HERE, *[".."] * i) for i in range(1, 7)]]
            if os.path.exists(os.path.join(p, "tools", "cert.py")))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from cert import Certificate

TIME_BUDGET_S = 25          # per k; 3 sizes * 25s = 75s << 600s rule limit


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


def divisors_of(fac):
    ds = [1]
    for p, e in fac.items():
        ds = [d * p ** i for d in ds for i in range(e + 1)]
    return ds


def lcm_upto(n):
    L = 1
    for i in range(1, n + 1):
        L = math.lcm(L, i)
    return L


C = Certificate(
    problem="p4", cell="c6",
    domain="For each k in {21,22,23}: multisets (m_1<=...<=m_k) of size k drawn from "
           "D_k = { d : d | L_k, d has >= 2 distinct prime factors }, where "
           "L_k = lcm(1,...,k-1). (Residues a_i are NOT yet assigned at this stage: "
           "a survivor here is a MODULUS PATTERN, decided only if C1-C4 already refute it; "
           "patterns not refuted by C1-C4 are left as explicit undecided survivors, since "
           "deciding them needs a further residue/CRT search -- see result.md.)",
    domain_proof="Main Reduction Theorem (result.md): if a size-k counterexample F exists, "
                 "a size-k counterexample F* exists with the SAME pairwise gcds as F and "
                 "every modulus dividing L_k (generalises Lemma 1/2/Main-Reduction-Theorem "
                 "of swarm/results/p4-proof-9c5676/result.md, k=25 case, to general k, by the "
                 "identical argument with 25 -> k, 24 -> k-1, L -> L_k). C1 (>=2 prime "
                 "factors) additionally restricts the domain because a size-k counterexample "
                 "cannot have a modulus that is a prime power: OPEN-board item "
                 "'CONJECTURED: minimal counterexample ... no m_i is a prime power' "
                 "(O'Bryant Lemma 6, cited, not re-proved here) -- so this filter is sound "
                 "only conditionally on that cited lemma; flagged as such in result.md.")

C.rule("C1", "Domain restriction: only divisors of L_k with >= 2 distinct prime factors are "
             "enumerated.",
       "Cited: O'Bryant Lemma 6 (no m_i a prime power) applied to a reduced (all moduli | L_k) "
       "counterexample. Conditional on that cited lemma (see result.md); not re-derived here.")
C.rule("C4", "For every prime p with p >= ceil(k/2): among the chosen moduli, the count "
             "divisible by p must end at exactly 0 or 2, and is pruned as soon as it reaches 3.",
       "Domain restriction (C1/reduction) gives v_p(m_i) <= 1 for every such p (since "
       "p^2 > (k-1) for p >= ceil(k/2), k<=23, so p^2 does not divide L_k). Two moduli "
       "divisible by p then have gcd exactly p (Lemma-3 style argument, p4-proof-9c5676 "
       "result.md Lemma 3, generalised): if 3 moduli are divisible by p, the pigeonhole "
       "argument forcing injectivity mod p (Lemma 3(b)) still applies pairwise, but the "
       "board's C4 additionally excludes count=1 and count>=3 as part of O'Bryant Lemma 6's "
       "conjectured minimal-counterexample profile; the count>=3 half is what is pruned here "
       "(cited, conditional -- see result.md); count==1 is checked at the leaf, not pruned "
       "mid-search, since a later slot could still be forced.")
C.rule("C3", "At most k-3 of the remaining (unfilled) slots may be needed to reach 3 multiples "
             "of (k-1); prune a partial family if it can no longer reach >= 3 moduli divisible "
             "by (k-1) by the end.",
       "Board OPEN item: minimal counterexample has >= 3 m_i divisible by k-1 (cited, "
       "conditional, O'Bryant Lemma 6). This is a monotone counting constraint: the final "
       "count can only be reached by adding more divisible moduli, so if "
       "current_count + slots_left < 3 no completion of this partial family can satisfy it.")


def search_k(k, time_budget=TIME_BUDGET_S):
    Lk = lcm_upto(k - 1)
    fac = factorize(Lk)
    primes = sorted(fac)
    all_divs = divisors_of(fac)

    def n_prime_factors(x):
        return sum(1 for p in primes if x % p == 0)

    D = sorted(x for x in all_divs if n_prime_factors(x) >= 2)
    big_primes = [p for p in primes if p >= -(-k // 2)]   # ceil(k/2)
    km1 = k - 1

    t0 = time.perf_counter()
    nodes = 0
    survivors = []
    timed_out = False

    # state: chosen moduli so far (nondecreasing indices into D to kill permutation duplicates)
    big_count = {p: 0 for p in big_primes}
    km1_count = 0

    def leaf_ok(fam):
        # C2: no prime divides all k moduli
        for p in primes:
            if all(m % p == 0 for m in fam):
                return False, f"C2 violated: prime {p} divides all {k} moduli"
        # C3 exact check
        if km1_count < 3:
            return False, f"C3 violated: only {km1_count} moduli divisible by k-1={km1}"
        # C4 exact check (no count==1)
        for p in big_primes:
            if big_count[p] == 1:
                return False, f"C4 violated: prime {p}>=ceil(k/2) divides exactly 1 modulus"
        return True, "passes C1-C4 as a modulus pattern"

    def extend(start, chosen, depth):
        nonlocal nodes, km1_count, timed_out
        if timed_out:
            return
        nodes += 1
        C.node()
        if nodes % 2000 == 0 and time.perf_counter() - t0 > time_budget:
            timed_out = True
            return
        if depth == k:
            ok, why = leaf_ok(chosen)
            if ok:
                survivors.append(list(chosen))
            return
        # C3 feasibility prune: can we still reach >=3 multiples of km1?
        remaining = k - depth
        if km1_count + remaining < 3:
            C.prune("C3")
            return
        for idx in range(start, len(D)):
            m = D[idx]
            touched_big = [p for p in big_primes if m % p == 0]
            bad = False
            for p in touched_big:
                if big_count[p] + 1 > 2:
                    bad = True
                    break
            if bad:
                C.prune("C4")
                continue
            for p in touched_big:
                big_count[p] += 1
            if m % km1 == 0:
                km1_count += 1
            chosen.append(m)
            extend(idx, chosen, depth + 1)
            chosen.pop()
            if m % km1 == 0:
                km1_count -= 1
            for p in touched_big:
                big_count[p] -= 1
            if timed_out:
                return

    with C.size(k) as rec:
        extend(0, [], 0)
        if timed_out:
            rec["note"] = f"UNFINISHED - {time_budget}s per-size wall-clock budget exceeded, not claimed"
            raise TimeoutError(f"k={k} unfinished")
        for s in survivors:
            C.survivor(s, decision="undecided",
                       minimal_part=None, minimality_proof=None)
    return nodes, len(survivors), timed_out


if __name__ == "__main__":
    for k in (21, 22, 23):
        try:
            nodes, nsurv, to = search_k(k)
            print(f"k={k}: nodes={nodes} survivors(modulus-patterns)={nsurv} timed_out={to}")
        except TimeoutError as e:
            print(f"k={C.sizes[-1]['size']}: UNFINISHED, nodes reached={C.sizes[-1]['nodes']}")
    C.finish()
