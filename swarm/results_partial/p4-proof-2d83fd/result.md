# p4 c6 — task p4-proof-2d83fd

**Status:** OPEN (partial progress — pruning lemma only, does not decide k = 25)

## Target (restated exactly)

Cell c6(a) asks to decide a size k ≥ 25 of the disjoint-congruence-classes problem
(`problems/p4/problem.md`): does every pairwise-disjoint family of k = 25 classes
a_1(mod m_1), …, a_25(mod m_25) contain a pair i<j with gcd(m_i, m_j) ≥ 25?

My explicit task is narrower: **extend the density/injectivity argument of the earlier
"Lemma 3" (task p4-proof-9c5676, primes p ∈ (k/2, k), i.e. p ∈ {13,17,19,23} for k = 25) to
the prime-power thresholds q = p^{E_p} lying in (k/3, k/2]**, which for k = 25 are exactly
q = 9 (p = 3, E_3 = 2) and q = 11 (p = 11, E_11 = 1) — matching the task's own example
"p ∈ {9, 11}". In this range gcd(m_i, m_j) can be q *or* 2q (not just q), so the argument
needs a size-2 case split instead of forcing a single value, exactly as flagged in the task.
I prove this case-split lemma in full, self-contained (it does **not** depend on the earlier
task's Main Reduction Theorem, which the shared board currently lists only as
[CONJECTURED] — see "Cited vs ours" below for why my proof avoids that dependency).

## Setup

Suppose for contradiction F = {(a_1,m_1), …, (a_25,m_25)} is a **counterexample of size
k = 25**: pairwise disjoint (by (*): gcd(m_i,m_j) | a_i − a_j ⟺ the classes meet), and
gcd(m_i, m_j) ≤ 24 for every i < j. Everything below is a statement about such an F; it is
vacuous if no such F exists. Write v_p(n) for the p-adic valuation of n.

## Sub-lemma A [PROVED] (self-contained restatement of Lemma 1 of p4-proof-9c5676)

*Statement.* If p is a prime and e ≥ 1 an integer with p^e ≥ 25, then in any counterexample
F of size 25, at most one index i has v_p(m_i) ≥ e.

*Proof.* If i ≠ j both have v_p(m_i) ≥ e and v_p(m_j) ≥ e, then p^e | m_i and p^e | m_j, so
p^e divides gcd(m_i,m_j) (a common divisor of both divides their gcd). Hence
gcd(m_i,m_j) ≥ p^e ≥ 25 > 24, contradicting the counterexample hypothesis that every
pairwise gcd of F is ≤ 24. ∎

I use this with (p,e) = (3,3) [3^3 = 27 ≥ 25] and (p,e) = (11,2) [11^2 = 121 ≥ 25].

## Which thresholds lie in (k/3, k/2]

For each prime p ≤ 23 let E_p = max{e : p^e ≤ 24} (the exponent of p in L = lcm(1,…,24)).
By exact computation (`scripts/check_range.py`, integer arithmetic, < 0.01 s):

| p | 2 | 3 | 5 | 7 | 11 | 13 | 17 | 19 | 23 |
|---|---|---|---|---|----|----|----|----|----|
| p^E_p | 16 | 9 | 5 | 7 | 11 | 13 | 17 | 19 | 23 |

k/3 = 25/3 ≈ 8.333, k/2 = 12.5. The thresholds p^E_p landing in (8.333, 12.5] are exactly
**9 and 11** — this reproduces the task's own example and is exhaustively checked over all
9 relevant primes by the script (no threshold is missed or wrongly included). [COMPUTED]

*(Observation, out of scope for this task but worth flagging: 16 = 2^4 also lies **above**
k/2 = 12.5, so the earlier task's Lemma 3 — stated only for the four odd primes {13,17,19,23}
— did not cover q = 16. That is a gap in a different task's lemma, not something I fix here;
see "What remains open" and the proposed new_task below.)*

## Lemma 4 [PROVED / BOUNDED] — case-split injectivity for q = 9 and q = 11

*Statement.* Fix q ∈ {9, 11} with associated prime p (p=3 for q=9, p=11 for q=11) and let
I_q := {i ∈ {1,…,25} : v_p(m_i) ≥ (1 if q=11 else 2)} — i.e. p | m_i to at least the power
making p^{(that exponent)} = q's own p-part (v_3 ≥ 2 for q=9; v_11 ≥ 1 for q=11). Then:

(a) For every pair i ≠ j in I_q, gcd(m_i,m_j) ∈ {q, 2q} (never q's higher odd multiples,
never anything not a multiple of q).

(b) Split I_q = I_q^0 ⊔ J_q, where J_q := {i ∈ I_q : v_2(m_i) ≥ 1} and I_q^0 := I_q \ J_q
(the m_i with i ∈ I_q^0 are odd). Then every pair inside I_q^0 has gcd = q exactly, and
every pair inside J_q has gcd = 2q exactly (mixed pairs I_q^0×J_q also have gcd = q exactly,
not used further below).

(c) i ↦ (a_i mod q) is injective on I_q^0, and i ↦ (a_i mod 2q) is injective on J_q. Hence
|I_q^0| ≤ q and |J_q| ≤ 2q, so |I_q| ≤ 3q.

*Proof of (a).* Take i ≠ j in I_q.

Case q = 9 (p = 3): by definition v_3(m_i), v_3(m_j) ≥ 2. By Sub-lemma A with (p,e)=(3,3),
at most one index among all 25 has v_3 ≥ 3; in particular not both of i,j have v_3 ≥ 3, so
at least one of them has v_3 exactly 2. Hence min(v_3(m_i), v_3(m_j)) = 2 exactly (it is ≥ 2
since both are ≥ 2, and ≤ 2 since one of the two values is exactly 2). So
v_3(gcd(m_i,m_j)) = 2, i.e. 9 | gcd(m_i,m_j) and 27 ∤ gcd(m_i,m_j). Write
gcd(m_i,m_j) = 9·r with r a positive integer not divisible by 3 (since the 3-adic
valuation of the gcd is exactly 2, dividing by 9 leaves valuation 0). Since
gcd(m_i,m_j) ≤ 24 (counterexample hypothesis), r ≤ 24/9 = 2.67…, so r ∈ {1, 2} (r is a
positive integer). Hence gcd(m_i,m_j) ∈ {9, 18} = {q, 2q}.

Case q = 11 (p = 11): by definition v_11(m_i), v_11(m_j) ≥ 1. By Sub-lemma A with
(p,e) = (11,2), at most one index has v_11 ≥ 2, so at least one of i, j has v_11 exactly 1,
giving min(v_11(m_i), v_11(m_j)) = 1 exactly. So v_11(gcd(m_i,m_j)) = 1, i.e.
gcd(m_i,m_j) = 11·r with r a positive integer not divisible by 11. Since
gcd(m_i,m_j) ≤ 24, r ≤ 24/11 = 2.18…, so r ∈ {1, 2}. Hence gcd(m_i,m_j) ∈ {11, 22} = {q,2q}.

In both cases r ∈ {1,2} is a single positive integer, not merely "the 2-part": if r = 2,
then, 2 being prime, gcd(m_i,m_j) = 2q forces v_2(gcd(m_i,m_j)) = 1 and no other prime
divides gcd(m_i,m_j) beyond p and 2 (any further prime ℓ ≥ 3 dividing the gcd, together
with the mandatory factor q ≥ 9, would force gcd ≥ 3q ≥ 27 > 24, excluded). If r = 1,
gcd(m_i,m_j) = q exactly, and no prime other than p divides it, in particular v_2 = 0. This
proves (a) and pins down exactly what r = 1 vs r = 2 means for v_2. ∎(a)

*Proof of (b).* By the r = 1 / r = 2 dichotomy in (a), gcd(m_i,m_j) = 2q for a pair i,j ∈ I_q
exactly when min(v_2(m_i), v_2(m_j)) ≥ 1, and gcd(m_i,m_j) = q exactly when
min(v_2(m_i), v_2(m_j)) = 0.

First, at most one index in I_q has v_2 ≥ 2: if i ≠ j ∈ I_q both had v_2(m_i), v_2(m_j) ≥ 2,
then min(v_2(m_i),v_2(m_j)) ≥ 2, so by (a)'s case analysis gcd(m_i,m_j) would need
v_2(gcd) ≥ 2, i.e. 4q | gcd(m_i,m_j), forcing gcd(m_i,m_j) ≥ 4q ∈ {36, 44} > 24 — contradicting
the counterexample hypothesis. So this cannot happen.

Now take i ≠ j ∈ J_q (so v_2(m_i), v_2(m_j) ≥ 1 by definition of J_q). By the previous
paragraph, not both have v_2 ≥ 2, so at least one of the two has v_2 exactly 1. Since the
other is ≥ 1, min(v_2(m_i), v_2(m_j)) = 1 exactly (capped by the one that equals 1). By (a)'s
dichotomy (min ≥ 1 ⟹ gcd = 2q), gcd(m_i,m_j) = 2q. This holds for every pair in J_q.

Take i ≠ j ∈ I_q^0 (so v_2(m_i) = v_2(m_j) = 0 by definition, i.e. both odd). Then
min(v_2(m_i),v_2(m_j)) = 0, so by (a)'s dichotomy gcd(m_i,m_j) = q. This proves (b) (the
mixed-pair claim is the same computation with min(0, ≥1) = 0, giving gcd = q, stated only
for completeness and not used in (c)). ∎(b)

*Proof of (c).* Disjointness of F means, for every pair i ≠ j, ¬(gcd(m_i,m_j) | a_i − a_j)
(criterion (*), contrapositive: the classes are disjoint so they do not meet).

For i ≠ j ∈ I_q^0: gcd(m_i,m_j) = q by (b), so q ∤ (a_i − a_j), i.e. a_i ≢ a_j (mod q). This
holds for every pair in I_q^0, so i ↦ (a_i mod q) is an injective map I_q^0 → ℤ/qℤ, giving
|I_q^0| ≤ q.

For i ≠ j ∈ J_q: gcd(m_i,m_j) = 2q by (b), so 2q ∤ (a_i − a_j), i.e. a_i ≢ a_j (mod 2q).
This holds for every pair in J_q, so i ↦ (a_i mod 2q) is injective J_q → ℤ/2qℤ, giving
|J_q| ≤ 2q.

Since I_q = I_q^0 ⊔ J_q (disjoint union, by definition of J_q), |I_q| = |I_q^0| + |J_q|
≤ q + 2q = 3q. ∎(c)

**Instantiated bounds** [PROVED]: |I_9^0| ≤ 9, |J_9| ≤ 18, |I_9| ≤ 27; |I_11^0| ≤ 11,
|J_11| ≤ 22, |I_11| ≤ 33. Label note: the *case-split structure* (a)–(b) and the
*injectivity* (c) are fully proved ([PROVED]); the resulting numeric bounds |I_q| ≤ 3q are
correct consequences but I mark them [BOUNDED] rather than claiming they add pruning power
by themselves, since 3q > 25 for both q = 9 (27 > 25) and q = 11 (33 > 25) — see next
section.

## Honest assessment: does this bound alone shrink the search?

No, not as a raw headcount: |I_q| ≤ 3q exceeds k = 25 for both q = 9 and q = 11, so, taken
in isolation, it is weaker than the trivial |I_q| ≤ 25. This is different from the original
Lemma 3 range {13,17,19,23}, where p itself is already < 25, so |I_p| ≤ p was already a
real, nontrivial restriction on its own.

What Lemma 4 *does* contribute, honestly stated:

1. It is still a genuine **structural** reduction usable inside a later exhaustive search:
   any index with v_3(m_i) ≥ 2 forces a_i into one of only q or 2q residue classes relative
   to every other such index (not an arbitrary gcd check) — same for v_11(m_i) ≥ 1 — cutting
   the disjointness check for these pairs from a full gcd/CRT computation down to a single
   mod-9/mod-18 (resp. mod-11/mod-22) residue comparison, exactly as Lemma 3 did for
   {13,17,19,23}, and exactly what the task description asked for ("squeeze the reduced
   search domain further ... before any exhaustive search is attempted": the squeeze here is
   in the *per-pair check cost and case structure*, not in a smaller headcount for q=9,11).
2. The finer split I_q = I_q^0 ⊔ J_q, with the *two different* moduli (q and 2q) for the two
   parts, is new information not implied by Lemma 3's single-modulus argument, and would be
   needed by any exhaustive search that wants to use q = 9, 11 at all (a search assuming only
   "gcd ∈ {q,2q}" without this split cannot conclude injectivity, since q vs 2q pairs behave
   differently).
3. It does **not** by itself prove k = 25, nor even improve on the trivial density bound for
   q ∈ {9,11}. I report this as a genuine limitation rather than overclaim it.

## Cited vs ours

Nothing outside `problems/p4/problem.md`'s definitions and criterion (*) is used. Sub-lemma A
is a direct, self-contained reproof of "Lemma 1" from task p4-proof-9c5676 (I re-derive it
from scratch here in three lines, rather than citing that task's [CONJECTURED]-status board
entry as a fact, since the instructions say to use only board lemmas with status *proved*,
and the shared FACTS section is currently empty). Lemma 4's case-split argument, its proof,
and `scripts/check_range.py` are original to this task. No published paper's argument is
reproduced; I did not do a fresh literature search in this task (out of the 25-minute proof-
track budget; task p4-literature-ce0fb3's fetched sources are the board's existing literature
record and I found nothing there specific to this threshold range).

## What remains open

- This is a pruning/case-structure lemma only. It does not decide k = 25.
- The numeric bound |I_q| ≤ 3q (q=9,11) is not tight enough by itself to reduce the search
  domain below the trivial 25; only the case-split *structure* is new pruning content (see
  "Honest assessment" above).
- Gap flagged, not fixed here: the earlier task's Lemma 3 (primes {13,17,19,23}, i.e. q > k/2)
  did not address q = 16 = 2^4, which also exceeds k/2 = 12.5. A natural extra lemma
  (analogous to Lemma 3 but for the composite base 16, using injectivity into ℤ/16ℤ since
  4·16 = 64 > 24 already forces r = 1 with no case split needed, by the same style of
  argument as here but simpler) is not attempted in this task and is proposed as a new_task.
- The region q ≤ k/3 (e.g. q = 7, where even a 3-way case split q, 2q, 3q is needed since
  3·7 = 21 ≤ 24) is explicitly out of scope for this task and unresolved.

## Verification

`python3 swarm/results/p4-proof-2d83fd/scripts/check_range.py` — exact integer arithmetic
only (`math.lcm`, trial-division factorisation, integer comparisons), verifies: L's
factorisation and the E_p table; that {9, 11} are exactly the thresholds p^E_p in
(25/3, 25/2]; that for q ∈ {9,11}, floor(24/q) = 2 (so r ∈ {1,2}), 2q ≤ 24 (case split is
real), 3q > 24 (no third case), 4q > 24 (double-exceeder-at-2 excluded); and contrasts with
q = 7 ≤ k/3 where 3q ≤ 24 (a third case would be needed, confirming (k/3,k/2] is exactly the
right range for a 2-case split). Runtime: < 0.001 s (well under the 10-minute limit). Output
reproduced in-line above; script prints "ALL CHECKS PASSED". As with `check_L.py` in the
predecessor task, this script evaluates a handful of independently hand-checkable numeric
facts (not a combinatorial search with pruning rules and survivors), so it is not routed
through `tools/cert.py`/`tools/rerun.py`, for the same reasons given in that task's writeup.
