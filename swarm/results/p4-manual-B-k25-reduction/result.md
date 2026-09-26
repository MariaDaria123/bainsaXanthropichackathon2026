# p4 c6(a) — finite reduction for k = 25 (manual-claude, item B)

**Status:** OPEN — partial progress. This is a reduction of the search domain for k = 25. **It does not decide k = 25.**

**What we establish.**
1. **[PROVED]** (Lemma 1, Cor. 1a/1b) In a size-25 counterexample, for each prime power p^e ≥ 25 at most one modulus is divisible by p^e.
2. **[PROVED]** (Lemma 2) Lowering the p-adic valuation of the unique exceeder to the common cap c changes no pairwise gcd and no disjointness relation.
3. **[PROVED]** (Main Reduction Theorem, and the stronger Theorem 2′) If a size-25 counterexample exists, one exists with the same residues a_i, the same gcd for every pair, and every modulus dividing L = lcm(1..24) = 5 354 228 880 (1920 divisors); moreover (Theorem 2′) one in which, for every prime, the maximum valuation is 0 or attained at least twice, so for p ∈ {13,17,19,23} the number of moduli divisible by p is 0 or in [2, p] and their cofactors are pairwise coprime.
4. **[PROVED]** (Lemma 3) In such a reduced counterexample, for p ∈ {13,17,19,23}: any two moduli divisible by p have gcd exactly p, residues mod p are distinct on I_p = {i : p | m_i}, so |I_p| ≤ p.
5. **[COMPUTED]** Numeric facts about L (value, factorisation, E_p table, d(L) = 1920), cross-checked by an exact script wrapped in `tools/cert.py`; each fact is also proved by hand below.
6. **[OBSERVED]** Falsification test: Lemma 2, the reduction procedure and the Theorem 2′ normal-form loop, transplanted to k = 3..8, preserve every gcd and every disjointness relation on 20 000 random families (seed 12); no failure.

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

*Hand proof of the factorisation.* For a prime p, v_p(lcm(1..24)) = max{v_p(i) : 1 ≤ i ≤ 24}
= max{e : p^e ≤ 24} (the integer p^e itself is in 1..24 exactly when p^e ≤ 24, and any i ≤ 24
with v_p(i) = e satisfies p^e ≤ i ≤ 24). The primes ≤ 24 are 2,3,5,7,11,13,17,19,23; the largest
powers ≤ 24 are 2⁴ = 16 (2⁵ = 32 > 24), 3² = 9 (3³ = 27 > 24), 5 (25 > 24), 7 (49), 11 (121),
13, 17, 19, 23 (squares ≥ 169). Primes > 24 divide no i ≤ 24. Hence
  L = 2⁴ · 3² · 5 · 7 · 11 · 13 · 17 · 19 · 23 = 5 354 228 880,
and d(L) = (4+1)(2+1)(1+1)^7 = 5 · 3 · 128 = 1920. The product and d(L) are cross-checked
by `scripts/check_L.py` (exact integers, `math.lcm`/`math.isqrt`, no floats, < 0.1 s).

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
(if c = v_p(m_i) then m_i' = m_i below and there is nothing to prove).
Assume c ≤ v_p(m_i). Define

  m_i' := m_i / p^{v_p(m_i) − c}

(i.e. m_i with its p-exponent lowered from v_p(m_i) down to exactly c, every other prime's
exponent in m_i left untouched), and let F' be F with (a_i, m_i) replaced by (a_i, m_i')
(same integer a_i; every other pair unchanged). Then:

(i) gcd(m_i', m_j) = gcd(m_i, m_j) for every j ≠ i.
(ii) F' is pairwise disjoint and has exactly the same gcd as F for every pair (i, j).
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
Every pairwise gcd of F' equals the corresponding gcd of F by (i) (pairs with i) or because
both moduli are unchanged (pairs without i), so gcd(pair) is unchanged for every pair and all remain ≤ 24. ∎(ii)

*Composability (explicit induction; the order of primes is fixed once and arbitrary, and no step below depends on which order was chosen, because each step reads and changes only the valuation at its own prime).* List the finitely many primes dividing
lcm(m_1,…,m_25) as p_1, p_2, …, p_r in any fixed order, and let F_0 := F, F_t := the family
obtained from F_{t-1} by the single Lemma-2 step at prime p_t (Main Reduction Theorem below
specifies that step; if no exceeder exists at p_t, F_t := F_{t-1}).

*Claim, by induction on t = 0,…,r:* F_t is a pairwise-disjoint counterexample of size 25 with
the same gcd as F for every pair (i, j), and for every j ≤ t, the p_j-adic valuations of
F_t's moduli already satisfy the target bound (≤ E_{p_j} if p_j ≤ 23, = 0 if p_j ≥ 25).

*Base case* t = 0: F_0 = F, which is a counterexample with F's own gcds by assumption; the "for every
j ≤ 0" clause is vacuous.

*Inductive step:* assume the claim for t−1. By Lemma 2(ii) applied to F_{t-1} (or the
no-op case), F_t is again a pairwise-disjoint counterexample of size 25 with the same gcd
for every pair as F_{t-1}, hence the same as F (gcds are preserved at each step, so equal all the
way back by transitivity). The step at p_t achieves the target bound for p_t on F_t by
construction (Corollary 1a/1b applied to F_{t-1}, which is valid: F_{t-1} is a
counterexample of size 25 — the corollaries hold for *any* such family, not only for F
itself). For j < t, the step at p_t leaves v_{p_j}(m_i) unchanged for
every i, by the definition of m_i' in Lemma 2 (m_i' = m_i / p_t^{v_{p_t}(m_i) − c} changes only the exponent of p_t, and only in the single chosen index), so the
bound already established for p_j at step j persists into F_t. This proves the claim for t.

Taking t = r gives a family F_r =: F* in which every one of the finitely many primes
dividing any modulus already meets its target bound, which is exactly the Main Reduction
Theorem's conclusion below.

## Main Reduction Theorem [PROVED]

*Statement.* If a counterexample F of size k = 25 exists, then a counterexample F* of size
25 exists with the **same gcd as F for every pair (i, j)** (in particular still all ≤ 24) and with every
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

By the Composability induction, doing this for every p ∈ P in the fixed order is valid: at the
step for prime p, Corollary 1a/1b is applied to the current family F_{t-1} (itself a size-25
counterexample by the induction), and steps at other primes never change any v_p. After processing all of P, call the result F*.
For every i and every prime p: if p ≤ 23 then v_p(m_i*) ≤ E_p (either it always was, or it was
lowered to exactly E_p); if p ≥ 25 then v_p(m_i*) = 0 (either it always was 0, or it was
zeroed). Hence m_i* | Π_{p≤23} p^{E_p} = L for every i. By repeated use of Lemma 2(ii), F* is
pairwise disjoint with the same gcd as F for every pair (i, j), so it is again a
counterexample of size 25. ∎

**Consequence for search.** A search for a size-25 counterexample may assume, by the Main
Reduction Theorem above, that every modulus is one of the d(L) = 1920 divisors of L (each residue may be taken in [0, m_i*): replacing a_i by a_i mod m_i* keeps the same class a_i (mod m_i*), and (∗) involves only the moduli and residue differences modulo the gcds, which do not change) — this is
exhaustiveness-certificate part 1 (exact finite set + proof nothing outside it need be
checked) for any later size-25 search. Direction of the reduction: every counterexample maps to a
reduced counterexample with the same gcds, so an exhaustive search over the reduced domain that
finds nothing proves that no counterexample of size 25 exists. (Conversely any reduced
family found is itself a counterexample, since it is a family of 25 classes.)

## Theorem 2′ [PROVED] — a stronger normal form

*Statement.* If a size-25 counterexample exists, then one exists, with the same a_i and the same gcd for every pair (i, j), in which **for every prime p the maximum of v_p(m_i) over i is either 0 or attained by at least two indices**. Every such family has all moduli dividing L.

*Proof.* Start from any counterexample F. While some prime p has max_i v_p(m_i) = e ≥ 1 attained by exactly one index i, let c = max_{j≠i} v_p(m_j) (so c < e and v_p(m_j) ≤ c for all j ≠ i) and apply Lemma 2 with this i, p, c. By Lemma 2 the result is again a counterexample of size 25 with the same a_i and the same gcd for every pair, and m_i strictly decreases (divided by p^{e−c} ≥ p), so Σ m_i strictly decreases. Σ m_i is a positive integer, so the loop stops, and when it stops the stated property holds for every prime (the primes dividing no modulus have maximum 0).
For the second sentence: if max_i v_p(m_i) = e ≥ 1 is attained at two indices i ≠ j, then p^e divides gcd(m_i, m_j) ≤ 24, so p^e ≤ 24, i.e. e ≤ E_p (and p ≤ 23). So v_p(m_i) ≤ E_p for all i and all p, i.e. every m_i divides L. ∎

*Consequences (in a family in this normal form).* (N1) For each prime p, |I_p| := |{i : p | m_i}| is 0 or ≥ 2. (N2) For p ∈ {13,17,19,23}: |I_p| ∈ {0} ∪ [2, p] (with Lemma 3(c) below). (N3) For p ∈ {13,17,19,23} and i ≠ j in I_p: v_p(m_i) = v_p(m_j) = 1 and gcd(m_i, m_j) = p (Lemma 3(a)), so gcd(m_i/p, m_j/p) = gcd(m_i, m_j)/p = 1: the cofactors are pairwise coprime. (N4) The maximum 2-adic valuation (if ≥ 1) and the maximum 3-adic valuation (if ≥ 1) are each attained at least twice.
Theorem 2′ strengthens the Main Reduction Theorem; we do not claim that it is the strongest possible reduction.

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
(The conclusion gcd = p uses only p | gcd and gcd ≤ 24 < 2p; the reduced setting m_i* | L is needed only for the statement v_p = 1 used in (N3) of Theorem 2′.)

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
external paper's argument is reproduced or relied on (The k^{1−o(1)} bound quoted in cell c6(b) is [KNOWN — source unverified]; nothing from it is used here.)

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

`python3 swarm/results/p4-manual-B-k25-reduction/scripts/check_L.py` — exact integer arithmetic
(`math.lcm`, `math.gcd`, trial-division factorisation), verifies: L's value and
factorisation, E_p for every prime ≤ 23, that p^(E_p+1) ≥ 25 for each, that {13,17,19,23} is
exactly the set of primes p with 2p > 24, and d(L) = 1920. Runtime: 0.016 s (well under the
10-minute limit). Output reproduced above; script prints "ALL CHECKS PASSED".

- `python3 swarm/results/p4-manual-B-k25-reduction/scripts/test_lemma2.py` — exact integers, seed 12, 0.6 s: falsification test of Lemma 2 and of the reduction procedure for k = 3..8 (20 000 random families, 129 273 lowering steps, 7 313 fully reduced families; every gcd and every meet/disjoint relation unchanged; every fully reduced modulus divides lcm(1..k−1)); plus the Theorem 2′ loop on 3 000 random families with all pairwise gcds ≤ k−1 (k = 3..8, moduli ≤ 3000, seed 12; 0.3 s): gcds and meet relations unchanged and every normalised modulus divides lcm(1..k−1). Evidence only; the proofs do not depend on it.

`check_L.py` goes through `tools/cert.py` (it writes `scripts/certificate.json`; the recorded "size" is the label "numeric-facts-for-k25-reduction (NOT a decision of k=25)", 24 nodes = the integers 1..24, no pruning, no survivors). `problems/` is read-only for this worker, so it is not wired into `tools/rerun.py p4 c6`; it reruns standalone with the command above. No proof step depends on the script: every numeric fact is proved by hand in "Setup".
