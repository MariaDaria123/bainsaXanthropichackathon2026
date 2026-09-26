# Critic #1 — blind review of swarm/results/p4-proof-9c5676/result.md

Scope respected: I read only `result.md`, `problems/p4/cells/c6/cell.md`, `problems/p4/problem.md`,
`problems/p4/lib/congruence.py`, and the cited `scripts/check_L.py` (which I ran). I did not read
`notes.md`, `swarm/board/`, other results, or any log.

## 1. Statement check

The task goal is narrow: prove a finite-domain reduction lemma for k=25 (restrict moduli to
divisors of L=lcm(1..24), using primes 13,17,19,23 > k/2 and the density criterion
Σ 1/gcd(m_i,M) ≤ 1), written so a later search over the reduced domain would be a valid
certificate part 1. It is *not* asked to decide k=25, and the write-up is explicit that it does
not attempt that ("Status: OPEN (partial progress...)", "What remains open"). No claim is
silently weakened, no hidden extra hypothesis is smuggled in, and no special case is presented as
the general statement — the Main Reduction Theorem and Lemma 3 are stated for an arbitrary
size-25 counterexample, with quantifiers explicit. Good.

One vocabulary nitpick: CLAUDE.md's rule 1 says status must be `SOLVED` or `PARTIAL`, nothing in
between. The write-up's header says "Status: OPEN (partial progress...)". The parenthetical is
accurate, but the literal status token should be `PARTIAL`, not `OPEN`. Minor wording fix, not a
math issue.

## 2. Line-by-line proof check

**Lemma 1** (at most one index with v_p(m_i) ≥ e when p^e ≥ k): correct — standard "d|a, d|b ⇒
d|gcd(a,b)" applied to d=p^e, contradicting the counterexample hypothesis gcd ≤ 24 once two
indices qualify. (The proof text has a stray half-sentence "so p^e divides every common
divisor's... more precisely p^e | gcd..." — a leftover editing artifact, cosmetic only.)

**Corollary 1a/1b**: correct applications of Lemma 1 with e=E_p+1 (p≤23) and e=1 (p≥25). I
independently re-derived E_p = v_p(lcm(1..24)) = floor(log_p 24) by hand for every p≤23 and it
matches the table (checked below against the script too).

**Lemma 2** (lowering a dominant p-valuation preserves every pairwise gcd and disjointness): the
proof of part (i) case-splits primes q≠p (untouched exponents) and q=p (both mins collapse to
v_p(m_j) under the stated hypotheses) — correct. Part (ii) correctly transports disjointness via
criterion (*) since the relevant gcd is literally unchanged.

**Composability / Main Reduction Theorem**: the argument that Lemma-2 steps for different primes
don't interfere (a step only ever touches one modulus's one prime-exponent, so Corollaries 1a/1b
computed from the *original* family remain valid throughout) is correct, if terse — it deserves an
explicit induction on the (finite) list of primes processed rather than one paragraph of prose,
but I could not find a gap in it and it checks out.

**Lemma 3** (primes 13,17,19,23; density form): (a)'s forced-t=1 step uses 2p>24 for p∈{13,17,19,23}
(so gcd=p·t≤24 with p≥13 forces t=1) — correct and exactly matches the stated reason these four
primes (the ones with k/2<p<k) are special. (b) and (c) are immediate from criterion (*) and
counting an injection into Z/pZ. The explicit disclaimer that this does *not* extend to p≤11 (since
2p≤24 is possible there, so t=1 isn't forced) is correct and appropriately flagged as an open gap
rather than glossed over.

## 3. Independent computational stress-test

I could not test the lemmas directly at k=25 (no actual counterexample exists at any known k, that
being the point of the whole problem), so I tested the *general mechanism* — which does not depend
on k=25 specifically — on scaled-down analogues using `problems/p4/lib/congruence.py`'s `disjoint`/`meet`:

- Ran ~19,000 random trials of Lemma 2 in isolation (pick a random pairwise-disjoint family, lower
  one modulus's valuation for a random prime under the stated hypotheses, check gcds/disjointness
  preserved exactly): **0 failures**.
- Implemented the full reduction algorithm (Lemma 1/Corollary 1a-1b/Lemma 2, iterated over every
  prime dividing any modulus) generically for a threshold K, and ran it on ~1200 random
  pairwise-disjoint families with max gcd ≤ K−1 for K=13 (so L=lcm(1..12), analogous to the K=25
  case one dimension down): checked "at most one exceeder per prime" (this is the load-bearing
  claim of Corollary 1a/1b) via a hard assertion, checked every reduced modulus divides L, and
  checked the gcd multiset is exactly preserved: **all 1196 non-degenerate trials passed, 0
  assertion failures**.
- Tested Lemma 3's scaled analogue (half-range primes for K=13 are {7,11}): checked |I_p|≤p, gcd
  exactly p for pairs in I_p, and injectivity of residues mod p, on the same 1196 reduced families:
  **all passed**.

This is strong evidence the Main Reduction Theorem and Lemma 3 are correct as general
mechanisms, not just plausible-sounding prose.

## 4. Cited code

`scripts/check_L.py` — re-ran it: exits in 0.016s, exact integer arithmetic only (`math.lcm`,
`math.gcd`, trial-division), deterministic, well under 10 minutes. I independently hand-verified
its central numeric claim: lcm(1..20) = 2⁴·3²·5·7·11·13·17·19 = 232,792,560 (a well-known value),
and lcm(1..24) = lcm(1..20)·23 = 5,354,228,880, matching the script and the write-up exactly.
d(L) = (4+1)(2+1)(2)⁷ = 5·3·128 = 1920, also matches.

However: CLAUDE.md's non-negotiable #4 says "any proof step that relies on code must use
`tools/cert.py` ... and be reproducible by `tools/rerun.py`." `check_L.py` is a bare script with
plain `assert`s — it does not go through `tools.cert.Certificate`, writes no `cert/certificate.json`,
and is not laid out as `cert/search.py` under a cell dir the way `tools/rerun.py` expects. The
computation itself is trivial, exact, and exhaustive over what it claims (it's direct arithmetic,
not a combinatorial search, so the 5-part search-certificate machinery is arguably overkill for it),
but as written it does not literally satisfy the repo's blanket rule. This is a process gap, not a
correctness one — I could find no error in what the script computes.

## 5. Labels

- [PROVED] labels (Lemma 1, Corollaries 1a/1b, Lemma 2, Main Reduction Theorem, Lemma 3): each has
  a complete, checkable proof; none rely on an unstated computation. Correct use of the label.
- [COMPUTED] labels (the E_p table, L's factorization, d(L)=1920, the {13,17,19,23} identification):
  backed by an exact, deterministic, sub-second script; verified by me independently by hand and by
  rerun. Correct use of the label, modulo the tools/cert.py process point above.
- No [CONJECTURED]/[OBSERVED] material is presented as proved. The "What remains open" section is
  honest and specific (does not decide k=25, does not extend Lemma 3 below p=13, does not estimate
  or run the actual search).

## 6. Literature

"Cited vs ours" correctly attributes everything to the write-up itself, states that criterion (*)
and the two named trivial bounds are the only things taken from `problem.md`, and reports (without
using) a 2026 preprint on the k^{1−o(1)} asymptotic — explicitly not used as a black box for the
statement at hand. This matches rule 2/6 (citing ≠ proving) correctly.

## Summary of fixes needed for a clean pass

1. Change "Status: OPEN" to "Status: PARTIAL" (CLAUDE.md's fixed vocabulary).
2. Route `check_L.py`'s computation through `tools/cert.py` (or explicitly argue, in the write-up,
   why a non-search elementary arithmetic check is exempt from the `tools/cert.py`/`tools/rerun.py`
   pipeline that CLAUDE.md mandates for "any proof step that relies on code").
3. (Cosmetic) clean up the stray unfinished sentence in Lemma 1's proof, and turn the
   "Composability" paragraph into an explicit induction over the finite prime list for full rigor.

None of these affect the correctness of the mathematics, which I verified both by hand (L's
factorization, E_p table, the four half-range primes, d(L)) and by independent randomized testing
of the general reduction mechanism on scaled-down instances, finding zero failures.

VERDICT: MINOR
