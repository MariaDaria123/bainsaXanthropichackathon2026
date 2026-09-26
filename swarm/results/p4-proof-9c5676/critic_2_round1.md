# Critic #2 report — p4-proof-9c5676

Scope of review: `swarm/results/p4-proof-9c5676/result.md`, `problems/p4/cells/c6/cell.md`,
`problems/p4/problem.md`, and the cited `scripts/check_L.py` (executed). I did not read
`notes.md`, `swarm/board/`, other results, or any log.

## 1. Statement check

The write-up's own framing of the task is narrower than cell c6(a) itself, and it says so
explicitly up front: it does not claim to decide k=25, only to prove a finite-reduction
lemma that a later exhaustive search over the reduced domain could use as certificate part 1.
This matches exactly what the task goal asked for ("Full proof of the reduction lemma, written
so that a search over the reduced set is a valid certificate") — it does not silently weaken
or overclaim the cell. No claim in the document states or implies that k=25 has been decided.

Each numbered claim (Lemma 1, Corollaries 1a/1b, Lemma 2, Main Reduction Theorem, Lemma 3)
states its quantifiers precisely: "any counterexample F of size 25," "for each prime p≤23,"
"fix index i, prime p, and integer c≥0 with...". I did not find a claim that quietly narrows
scope (e.g. to a special case) while presenting itself as general.

## 2. Step-by-step check

**Lemma 1** (one exceeder per threshold prime power): correct. If two indices had
v_p(m_i), v_p(m_j) ≥ e with p^e ≥ 25, then p^e | gcd(m_i,m_j), forcing gcd ≥ 25, contradicting
the counterexample hypothesis (all pairwise gcds ≤ 24). No gap.

**Corollaries 1a, 1b**: direct substitution of e = E_p+1 (resp. e=1 for p≥25) into Lemma 1;
correctness reduces to the arithmetic fact p^(E_p+1) ≥ 25 for all p ≤ 23, which I verified
independently (see §3). Correct.

**Lemma 2** (lowering a dominant valuation): this is the technical heart of the reduction — a
compression/shifting argument. I checked the two-case proof of gcd-invariance (q≠p trivial;
q=p uses v_p(m_i')=c and v_p(m_j)≤c so both mins equal v_p(m_j)) and it is correct. I also
stress-tested it computationally on 20,000 random synthetic (m_i, m_j, p, c) instances
satisfying the lemma's hypotheses — zero mismatches (see §3). No gap.

**Main Reduction Theorem**: correctly assembles Lemma 2 across all primes p ∈ P (finite, since
each of the 25 moduli has finitely many prime factors). The "Composability" argument — that
processing one prime never disturbs another prime's valuations or any gcd, so Corollary
1a/1b's "at most one exceeder" fact keeps holding at every subsequent step regardless of
order — is correct and in fact slightly stronger than needed: since Lemma 1 is a fact about
*any* size-25 counterexample and Lemma 2(ii) keeps every intermediate family a
counterexample, the "at most one exceeder" fact can be re-derived at each step directly,
without needing the persistence argument at all. Either way, no gap. The conclusion m_i* | L
for every i follows correctly from v_p(m_i*) ≤ E_p (p≤23) and v_p(m_i*)=0 (p≥25) for every
prime, via unique factorization.

**Lemma 3** (pruning via 13,17,19,23): part (a)'s derivation is correct — since p | m_i*,
p | m_j* forces p | gcd(m_i*,m_j*), and gcd ≤ 24 with p ≥ 13 means the only multiple of p that
is ≤ 24 is p itself (2p ≥ 26 > 24 for all four primes — checked). Part (b) is a direct,
correctly-invoked application of criterion (*). Part (c) (injective map into Z/pZ ⇒
|I_p| ≤ p) is immediate. The "density criterion Σ 1/gcd(m_i,M) ≤ 1" language in the task is
correctly instantiated at M = p for each of the four named primes; the write-up does not
overclaim a general-M version (which is false in general — e.g. M=1 gives gcd=1 for every i
and a sum of k > 1) — it only proves the instance actually requested, and says so.

## 3. Testable lemmas — ran them

- `python3 swarm/results/p4-proof-9c5676/scripts/check_L.py`: reran it. Output matches the
  document exactly (L = 5354228880, factorisation, E_p table, {13,17,19,23} as the primes
  with 2p>24, d(L)=1920). Runtime 0.03s, well under 10 minutes, exact integer arithmetic
  (`math.lcm`/`math.gcd`, trial-division factoring — no floats). Deterministic, reproducible.
- I independently wrote a synthetic property test for Lemma 2's gcd-invariance claim (20,000
  random trials over primes {2,3,5,7,11,13} and random exponents/cofactors satisfying the
  lemma's hypotheses): 0 failures. This is the one lemma in the chain doing real algebraic
  work, and it holds up.
- Lemma 1's and Lemma 3's core facts reduce to small arithmetic checks (p^e ≥ 25, 2p > 24)
  that `check_L.py` already verifies exactly for every relevant p.

No lemma failed testing; no counterexample found.

## 4. Certificate completeness (checklist item 4)

The task explicitly scopes this piece of work to *part 1* of the 5-part exhaustiveness
certificate (finite domain + proof nothing outside it survives) plus one extra proved pruning
rule (Lemma 3), not a full search. The document is honest about this: it states in "What
remains open" that no search has been run, no node counts exist, and no survivors have been
decided, and it does not claim a certificate is complete. Given the narrower task goal stated
verbatim in this critic's brief ("Full proof of the reduction lemma..."), this scoping is
appropriate, not a dodge — the full 5-part certificate was never asked for here.

## 5. Labels

[PROVED] is used for Lemma 1, Corollaries 1a/1b, Lemma 2, the Main Reduction Theorem, and
Lemma 3 — all five have complete proofs as written, matching the label. [COMPUTED] is used
only for the numeric facts in the L-table, backed by the exact script. No [CONJECTURED] or
[OBSERVED] claim is presented as proved. Labels are used correctly throughout.

## 6. Literature

"Cited vs ours" correctly separates: nothing beyond problem.md's definitions and criterion
(*) is used; Lemmas 1–3 and the reduction theorem are claimed original, and I found no
published argument being silently reused. The one literature mention (a 2026 preprint on the
k^{1-o(1)} bound) is disclosed as unread/unused beyond acknowledging the problem is
actively studied — correctly not counted as progress and not passed off as this work's own.

## Issues found (both minor / non-mathematical)

1. **Status label deviates from repo convention.** CLAUDE.md non-negotiable #1: "Status is
   `SOLVED` or `PARTIAL`, nothing in between." The document's header reads
   `**Status:** OPEN (partial progress ...)`. The content is genuinely a partial result, so
   the fix is cosmetic: change the label to `PARTIAL` (the parenthetical already correctly
   describes what kind of partial progress it is).

2. **One banned word appears without re-argument.** CLAUDE.md non-negotiable #5 bans
   "WLOG" (among others) "without the argument." Line 127, "Consequence for search," says a
   search "may assume WLOG that every modulus is one of the d(L) = 1920 divisors of L." The
   underlying argument *was* given in full immediately above (the Main Reduction Theorem), so
   this isn't a skipped step in substance — but the literal word is banned by the repo's own
   rule regardless of context. Local fix: replace "may assume WLOG that" with "may assume, by
   the Main Reduction Theorem above, that."

Neither issue affects the correctness or completeness of the mathematics; both are one-line
text fixes.

## Overall assessment

This is a correct, honestly-scoped, and non-trivial piece of mathematics: a genuine
compression/shifting argument (Lemma 2) assembled into a lossless reduction of an infinite
search space to a finite one (1920 divisors of L per slot), plus a sharp extra pruning rule
for the four "half-range" primes matching exactly what the task requested. It does not
overclaim, it labels correctly, its one computational claim is exact and reproducible, and it
does not decide k=25 or claim to. The only defects are two small compliance nits (status
label wording, one instance of a banned transition word whose argument is in fact present).

VERDICT: MINOR
