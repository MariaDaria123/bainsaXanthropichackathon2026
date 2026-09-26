# p4 c6 — task p4-proof-9c5676

**Status:** PARTIAL (finite-reduction lemma for k = 25, not a decision of k = 25)

## Target (restated exactly)

Cell c6(a): decide a size k ≥ 25 of the disjoint-congruence-classes problem (problem.md):
does every pairwise-disjoint family of k = 25 classes a_1(mod m_1), …, a_25(mod m_25) contain
a pair i<j with gcd(m_i, m_j) ≥ 25?

My task is narrower and explicit: **for k = 25, prove the strongest finite reduction**
that restricts the moduli to a computably finite set, using L = lcm(1,…,24) and the primes
13, 17, 19, 23 (the primes in (k/2, k)), via the density criterion Σ 1/gcd(m_i, M) ≤ 1.
I prove the reduction lemma in full (this is the mathematical content a later exhaustive
search over that finite set would need as its certificate part 1). I do **not** run the
resulting search and do **not** decide k = 25.

## Setup

Suppose for contradiction that F = {(a_1,m_1), …, (a_25,m_25)} is a **counterexample of
size k = 25**: pairwise disjoint (by (*): gcd(m_i,m_j) | a_i − a_j ⟺ the classes meet), and
gcd(m_i, m_j) ≤ 24 for every i < j. Everything below is a statement about such an F; it is
vacuous if no such F exists (which is exactly what k = 25 being decided TRUE would mean).

Write v_p(n) for the exponent of prime p in n (v_p(n) = 0 if p ∤ n). Let

  L := lcm(1, 2, …, 24).

By exact computation (`scripts/check_L.py`, integer arithmetic only, < 0.02 s):

  L = 5 354 228 880 = 2⁴ · 3² · 5 · 7 · 11 · 13 · 17 · 19 · 23,  d(L) = 1920 divisors.

For a prime p ≤ 23, let E_p := v_p(L) = max{e ≥ 0 : p^e ≤ 24}. Values (all [COMPUTED],
`scripts/check_L.py`):

| p | 2 | 3 | 5 | 7 | 11 | 13 | 17 | 19 | 23 |
|---|---|---|---|---|----|----|----|----|----|
| E_p | 4 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| p^(E_p+1) | 32 | 27 | 25 | 49 | 121 | 169 | 289 | 361 | 529 |

Every p^(E_p+1) ≥ 25 = k (checked exactly). For p ∉ {2,…,23} put E_p := 0 (consistent:
p ≥ 29 ⇒ p^(0+1) = p ≥ 29 ≥ 25).

## Lemma 1 [PROVED] — one exceeder per threshold prime power

*Statement.* Let p be a prime and e ≥ 1 an integer with p^e ≥ k = 25. In any counterexample
F of size 25, at most one index i ∈ {1,…,25} has v_p(m_i) ≥ e.

*Proof.* Suppose i ≠ j both satisfy v_p(m_i) ≥ e and v_p(m_j) ≥ e. Then p^e | m_i and
p^e | m_j, so p^e | gcd(m_i,m_j) (standard fact: d | a and d | b ⇒ d | gcd(a,b), here
d = p^e). Hence gcd(m_i,m_j) ≥ p^e ≥ 25 > 24, contradicting the counterexample hypothesis
that all pairwise gcds of F are ≤ 24. ∎

**Corollary 1a** [PROVED]. For each prime p ≤ 23, at most one index i has v_p(m_i) > E_p.
(Apply Lemma 1 with e = E_p + 1, which satisfies p^e ≥ 25 by the table above.)

**Corollary 1b** [PROVED]. For each prime p ≥ 25, at most one index i has p | m_i.
(Apply Lemma 1 with e = 1, since p^1 = p ≥ 25.)

## Lemma 2 [PROVED] — lowering a dominant valuation changes nothing observable

*Statement.* Fix index i, prime p, and integer c ≥ 0 with v_p(m_j) ≤ c for every j ≠ i
(c may be less than, equal to, or — trivially, no change needed — equal to v_p(m_i)).
Assume c ≤ v_p(m_i). Define

  m_i' := m_i / p^{v_p(m_i) − c}

(i.e. m_i with its p-exponent lowered from v_p(m_i) down to exactly c, every other prime's
exponent in m_i left untouched), and let F' be F with (a_i, m_i) replaced by (a_i, m_i')
(same integer a_i; every other pair unchanged). Then:

(i) gcd(m_i', m_j) = gcd(m_i, m_j) for every j ≠ i.
(ii) F' is pairwise disjoint and has exactly the same multiset of pairwise gcds as F.
In particular F' is again a counterexample of size 25 (all gcds ≤ 24, unchanged), and
m_i' ≤ m_i.

*Proof of (i).* Fix j ≠ i. gcd(m_i,m_j) = Π_q q^{min(v_q(m_i),v_q(m_j))} over all primes q.
For q ≠ p: v_q(m_i') = v_q(m_i) by construction (only the p-exponent was changed), so the
q-term of the product is identical for (m_i',m_j) and (m_i,m_j). For q = p: v_p(m_i') = c by
construction, and v_p(m_j) ≤ c by hypothesis, so min(v_p(m_i'),v_p(m_j)) = v_p(m_j); also
v_p(m_i) ≥ c ≥ v_p(m_j) by hypothesis, so min(v_p(m_i),v_p(m_j)) = v_p(m_j) too — the same
value. Every prime's exponent in the gcd is unchanged, so the two gcds are equal as
integers. ∎(i)

*Proof of (ii).* Pairs not involving i are untouched, so unaffected. For the pair (i,j),
j ≠ i: original disjointness of (a_i,m_i) and (a_j,m_j) means, by (*), gcd(m_i,m_j) ∤
(a_i − a_j). By (i), gcd(m_i',m_j) = gcd(m_i,m_j), and a_i, a_j are unchanged integers, so
gcd(m_i',m_j) ∤ (a_i − a_j) also holds; by (*) again, (a_i,m_i') and (a_j,m_j) are disjoint.
Every pairwise gcd of F' equals the corresponding gcd of F by (i) (pairs with i) or trivially
(pairs without i), so the gcd multisets agree and all remain ≤ 24. ∎(ii)

*Composability (explicit induction).* List the finitely many primes dividing
lcm(m_1,…,m_25) as p_1, p_2, …, p_r in any fixed order, and let F_0 := F, F_t := the family
obtained from F_{t-1} by the single Lemma-2 step at prime p_t (Main Reduction Theorem below
specifies that step; if no exceeder exists at p_t, F_t := F_{t-1}).

*Claim, by induction on t = 0,…,r:* F_t is a pairwise-disjoint counterexample of size 25 with
the same multiset of pairwise gcds as F, and for every j ≤ t, the p_j-adic valuations of
F_t's moduli already satisfy the target bound (≤ E_{p_j} if p_j ≤ 23, = 0 if p_j ≥ 25).

*Base case* t = 0: F_0 = F, trivially a counterexample with F's own gcds; the "for every
j ≤ 0" clause is vacuous.

*Inductive step:* assume the claim for t−1. By Lemma 2(ii) applied to F_{t-1} (or the
no-op case), F_t is again a pairwise-disjoint counterexample of size 25 with the same gcd
multiset as F_{t-1}, hence the same as F (gcds are preserved at each step, so equal all the
way back by transitivity). The step at p_t achieves the target bound for p_t on F_t by
construction (Corollary 1a/1b applied to F_{t-1}, which is valid: F_{t-1} is a
counterexample of size 25 — the corollaries hold for *any* such family, not only for F
itself). For j < t, Lemma 2(i) shows the step at p_t leaves v_{p_j}(m_i) unchanged for
every i (only the single prime p_t's exponent in the single chosen index is touched), so the
bound already established for p_j at step j persists into F_t. This proves the claim for t.

Taking t = r gives a family F_r =: F* in which every one of the finitely many primes
dividing any modulus already meets its target bound, which is exactly the Main Reduction
Theorem's conclusion below.

## Main Reduction Theorem [PROVED]

*Statement.* If a counterexample F of size k = 25 exists, then a counterexample F* of size
25 exists with the **same pairwise gcds as F** (in particular still all ≤ 24) and with every
modulus m_i* dividing L = lcm(1,…,24). Equivalently: if no counterexample of size 25 has all
moduli dividing L, then no counterexample of size 25 exists at all.

*Proof.* Let P be the (finite) set of primes dividing lcm(m_1,…,m_25) — finite because each
m_i is a fixed positive integer with finitely many prime factors. For each p ∈ P, in turn:

- If p ≤ 23: by Corollary 1a there is at most one index i_p with v_p(m_{i_p}) > E_p. If none
  exists, do nothing for this p (already v_p(m_j) ≤ E_p for all j). If i_p exists, every
  j ≠ i_p has v_p(m_j) ≤ E_p (that is what "at most one exceeder" means), so Lemma 2 applies
  with i = i_p, c = E_p: replace m_{i_p} by m_{i_p}' with v_p lowered to exactly E_p. By
  Lemma 2(ii) the family stays a counterexample with the same gcds.
- If p ≥ 25 (p ∉ {2,…,23}): by Corollary 1b at most one index i_p has p | m_{i_p}; if it
  exists, every j ≠ i_p has v_p(m_j) = 0, so Lemma 2 applies with c = 0: replace m_{i_p} by
  m_{i_p} with the entire p-part removed.

By the Composability remark, doing this for every p ∈ P (in any order) is valid: each step's
hypothesis ("all other indices already have v_p ≤ c") was established from the original F and
is never invalidated by steps at other primes. After processing all of P, call the result F*.
For every i and every prime p: if p ≤ 23 then v_p(m_i*) ≤ E_p (either it always was, or it was
lowered to exactly E_p); if p ≥ 25 then v_p(m_i*) = 0 (either it always was 0, or it was
zeroed). Hence m_i* | Π_{p≤23} p^{E_p} = L for every i. By repeated use of Lemma 2(ii), F* is
pairwise disjoint with the identical multiset of pairwise gcds as F, so it is again a
counterexample of size 25. ∎

**Consequence for search.** A search for a size-25 counterexample may assume, by the Main
Reduction Theorem above, that every modulus is one of the d(L) = 1920 divisors of L (each with its residue in [0, m_i)) — this is
exhaustiveness-certificate part 1 (exact finite set + proof nothing outside it need be
checked) for any later size-25 search. This reduction is *lossless*: it does not merely bound
the moduli, it produces a counterexample with the *same* gcd values, so it loses no
counterexamples and introduces no false ones.

## Lemma 3 [PROVED] — extra pruning from the primes 13, 17, 19, 23, and the density form

The task also asks to use the primes p ∈ {13,17,19,23} (exactly the primes with k/2 < p < k,
i.e. 12.5 < p < 25 — checked exactly in `scripts/check_L.py`) via the density criterion
Σ 1/gcd(m_i,M) ≤ 1. Working inside a reduced family F* from the theorem above (all m_i* | L,
so E_p = 1 for these four primes, i.e. v_p(m_i*) ∈ {0,1}):

*Statement.* Fix p ∈ {13,17,19,23}. Let I_p = {i : p | m_i*}. Then:
(a) for i ≠ j both in I_p, gcd(m_i*,m_j*) = p exactly;
(b) i ↦ (a_i mod p) is injective on I_p;
(c) |I_p| ≤ p, equivalently Σ_{i∈I_p} 1/gcd(m_i*,p) ≤ 1.

*Proof of (a).* i,j ∈ I_p ⇒ v_p(m_i*) = v_p(m_j*) = 1 exactly (it is ≥ 1 by membership in
I_p, and ≤ E_p = 1 since m_i*,m_j* | L). So v_p(gcd(m_i*,m_j*)) = min(1,1) = 1: write
gcd(m_i*,m_j*) = p·t, t a positive integer. Since gcd(m_i*,m_j*) ≤ 24 (F* is a
counterexample) and p ≥ 13, t ≤ 24/13 < 2, so t = 1, i.e. gcd(m_i*,m_j*) = p. ∎(a)

*Proof of (b).* If i ≠ j ∈ I_p had a_i ≡ a_j (mod p), then since gcd(m_i*,m_j*) = p by (a)
and p | (a_i − a_j), criterion (*) says the two classes meet — contradicting pairwise
disjointness of F*. So a_i ≢ a_j (mod p) for all such pairs, i.e. the map is injective. ∎(b)

*Proof of (c).* An injective map from I_p into the p-element set Z/pZ forces |I_p| ≤ p. Each
i ∈ I_p has gcd(m_i*,p) = p (since p | m_i*), so Σ_{i∈I_p} 1/gcd(m_i*,p) = |I_p|/p ≤ 1. ∎(c)

This is the requested density inequality Σ 1/gcd(m_i,M) ≤ 1 with M = p: the reduced-mod-p
images of the classes indexed by I_p are pairwise-disjoint singletons in Z/pZ (a genuinely
*exact*, not merely bounding, reduction, because (a) forces the gcd to be exactly p — no
information about m_i*, m_j* beyond "divisible by p" is lost). Concretely this gives
|I_13| ≤ 13, |I_17| ≤ 17, |I_19| ≤ 19, |I_23| ≤ 23 for any size-25 counterexample already
reduced to divide L — usable as an extra pruning rule in a later exhaustive search (on top of
"moduli divide L"), since it bounds how many of the 25 slots may be divisible by each of
these four primes, and reduces the disjointness check for such pairs to a single residue
comparison mod p instead of a full gcd/CRT check.

## Cited vs ours

Nothing outside `problems/p4/problem.md`'s definitions and criterion (*) and the two trivial
bounds already given there (gcd=1 ⇒ meet; density Σ 1/m_i ≤ 1) is used. Lemmas 1–3 and the
Main Reduction Theorem, their proofs, and `scripts/check_L.py` are original to this task; no
external paper's argument is reproduced or relied on (a brief literature search located a
2026 preprint, "On the problem of large gcd for disjoint residue classes," proving the
k^{1−o(1)} bound quoted in cell c6(b) and stating that the exact-gcd-≥k statement was
previously certified only up to some k < 25; I could not fetch its full text through this
session's network access, so I did not use or cite any technique from it beyond this
one-line acknowledgement that the target problem is a real, actively-studied open problem).

## What remains open

- This is a **reduction of the search domain only**. It does not decide k = 25: it does not
  say whether a counterexample with all moduli dividing L (1920 choices per slot, 25 slots,
  plus residues) exists or not. That decision needs an actual (possibly very large) exhaustive
  search — a `certify`-track task, out of scope for the 25-minute proof-track budget here.
- Lemma 3 only handles the four "half-range" primes 13,17,19,23. The same idea does not
  immediately give injectivity for smaller primes p ≤ 12 (2·p ≤ 24 is possible there, so
  Lemma 3(a)'s forced "t=1" step fails — e.g. gcd could be 2p, not p), so no analogous bound
  on |I_p| is claimed for p ≤ 11; that would need a different argument and is not attempted
  here.
- I have not attempted to run any search over the 1920^25-scale raw product; that number is
  not a claim of search cost (the real pruned search tree, with Lemma 3's rules and
  disjointness pruning, is what a certify task would need to bound and count — not estimated
  here).

## Verification

`python3 swarm/results/p4-proof-9c5676/scripts/check_L.py` — exact integer arithmetic
(`math.lcm`, `math.gcd`, trial-division factorisation), verifies: L's value and
factorisation, E_p for every prime ≤ 23, that p^(E_p+1) ≥ 25 for each, that {13,17,19,23} is
exactly the set of primes p with 2p > 24, and d(L) = 1920. Runtime: 0.016 s (well under the
10-minute limit). Output reproduced above; script prints "ALL CHECKS PASSED".

**Why this script does not go through `tools/cert.py`/`tools/rerun.py`.** That pipeline
(`Certificate.size()`/`.node()`/`.prune()`/`.survivor()`, and `rerun.py`'s comparison of
`cert/search.py` against `cert/certificate.json` under `problems/pX/cells/cY/cert/`) is built
for *exhaustiveness certificates*: a combinatorial domain that is searched, pruning rules
applied to it, and survivors each individually decided. `check_L.py` searches no domain and
decides no survivor — it evaluates four fixed numeric quantities (L, its factorisation, the
E_p table, d(L)) by direct exact integer computation, each independently re-checkable by hand
in one line (e.g. lcm(1..24) = lcm(1..20)·23, a single multiplication once lcm(1..20) is
known). Forcing it through the `Certificate` object would require inventing a fake "domain"
and "rules" for a computation that has neither, which would not make the arithmetic any more
exact or more reproducible than it already is. What rule 4 substantively requires — exact
arithmetic (no floats: `math.lcm`/`math.gcd`/trial division only), a runtime far under 10
minutes, and reproducibility — is satisfied and independently checked: both critics reran the
script verbatim and confirmed the output matches the document, and critic 1 additionally
hand-verified lcm(1..20) = 232 792 560 and d(L) = 5·3·2⁷ = 1920 without running any code. In
addition, this task's instructions restrict all writes to
`swarm/results/p4-proof-9c5676/`, so creating a `problems/p4/cells/c6/cert/` directory (what
`tools/rerun.py` expects) is outside this task's writable scope in any case; that step belongs
to the separate `certify`-track task already logged in `findings.jsonl` ("build an actual
exhaustiveness certificate ... reporting node counts").
