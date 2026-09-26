# Critic 1 report — p4-proof-9c5676

Judged: `swarm/results/p4-proof-9c5676/result.md` against `problems/p4/cells/c6/cell.md`,
`problems/p4/problem.md`, and the task goal ("for k=25 prove the strongest finite
reduction ... using primes 13,17,19,23 > k/2 and the density criterion ... to shrink
the domain"). Cited code (`scripts/check_L.py`) was run. `notes.md`, `swarm/board/`,
other results and logs were not opened.

## 1. Statement check

**Status line:** "PARTIAL (finite-reduction lemma for k=25, not a decision of k=25)."
This is accurate and not inflated. The document never claims to decide c6(a); it
explicitly separates "reduction of the search domain" from "a decision of k=25" in
the "What remains open" section. No quantifier or range is silently weakened: every
lemma states its universe precisely (all i≠j in {1,…,25}, all primes p ≤23 vs p≥25,
the four named primes for Lemma 3). This matches the task's ask exactly (restrict
moduli to divisors of L=lcm(1..24); use the four primes >k/2 and the density
inequality) — no more, no less. **No issue.**

## 2. Step-by-step check

I worked through every proof (Lemma 1, Corollaries 1a/1b, Lemma 2 including the
composability argument, Main Reduction Theorem, Lemma 3) line by line.

- **Lemma 1** (at most one index with v_p(m_i) ≥ e when p^e ≥ 25): correct — direct
  contradiction, gcd ≥ p^e ≥ 25 > 24. Generalizes correctly from "no two indices" to
  "at most one index" (standard pigeonhole, not hidden).
- **Corollaries 1a/1b:** correct instantiations (e = E_p+1 for p≤23, e=1 for p≥25),
  and the needed inequality p^(E_p+1) ≥ 25 is exactly what `check_L.py` verifies.
- **Lemma 2** (lowering one index's p-valuation to the common ceiling c preserves
  every pairwise gcd and disjointness): I checked proof (i) prime-by-prime
  (q≠p unchanged trivially; q=p forced equal because both mins collapse to
  v_p(m_j)) and proof (ii) via criterion (*) — both correct.
- **Composability:** this is the one place a real gap could hide (does the
  "at-most-one-exceeder" property survive from F into F_{t-1} at each step?). The
  write-up's argument is correct: each single-prime step only touches the p-adic
  valuation of the one prime being processed (Lemma 2(i)), so it never invalidates
  a property already achieved at an earlier prime, and Corollary 1a/1b can be
  *re-applied fresh* to F_{t-1} at each step because F_{t-1} is still a bona-fide
  counterexample (same gcd multiset, by induction). This closes the loop rigorously;
  I did not find a gap here.
- **Main Reduction Theorem:** correctly assembles the above into "if a counterexample
  of size 25 exists, one exists with the same pairwise gcds and every modulus
  dividing L." The direction is the one actually needed for a later search
  (empty reduced search ⇒ no counterexample at all).
- **Lemma 3** (the four half-range primes force gcd exactly p, hence injective
  residues mod p, hence |I_p| ≤ p): correct, and the write-up's own explanation of
  *why* this fails for p ≤ 12 (2p ≤ 24 lets t = 2) is correct and matches what I
  found computationally (see §3).

No occurrence of "clearly/obviously/routine/similarly/WLOG" is used to skip an
argument; the few uses of "trivially" (lines calling out c = v_p(m_i) as a no-op,
and unchanged pairs in F′) are genuinely tautological, not disguised gaps.

## 3. Independent computational testing

I re-derived L, its factorization, and d(L)=1920 independently (matches). I then
wrote an independent test harness (not the author's script) that:

- Implements the Lemma-1/Lemma-2/Main-Reduction algorithm from scratch, from the
  paper description alone.
- Runs it against several genuine pairwise-disjoint families (the problem.md
  example, its base-3 analogue, a longer binary-tree chain, and the sharp
  1..k mod k example), each deliberately perturbed by multiplying one modulus per
  index by a large prime power *not* dividing L, across 800 randomized trials.
- In every trial: pairwise gcds were unchanged by perturbation (sanity), and after
  running the reduction algorithm, disjointness held, the gcd multiset was
  unchanged, and every reduced modulus divided the corresponding L — exactly the
  Main Reduction Theorem's claim.
- I also directly tested the necessity of the p > k/2 restriction in Lemma 3: for
  p=13 (half-range), two moduli both divisible by p force gcd = 13 exactly, and
  equal residues mod 13 force the classes to meet (as claimed); for p=5 (not
  half-range), gcd(10,20)=10=2p is achievable within the ≤24 bound, showing why
  Lemma 3's argument genuinely cannot extend to small primes, confirming the
  write-up's own disclaimer is correct rather than an excuse.

No counterexample to any tested lemma was found.

## 4. Cited code

`scripts/check_L.py` reruns in 0.016s, exact integer arithmetic only
(`math.lcm`/`math.gcd`/trial-division factorization, no floats), and reproduces
every numeric claim quoted in the text (L, its factorization, the E_p table,
{13,17,19,23} = primes with 2p>24, d(L)=1920). I hand-verified d(L) = 5·3·2^7 = 1920
independently. **Runs clean, output matches the document.**

**Process issue (the one real finding).** `CLAUDE.md` rule 4 ("Non-negotiables") reads:
"Any proof step that relies on code must use `tools/cert.py`, run under 10 minutes,
use exact arithmetic ..., and be reproducible by `tools/rerun.py`." This is stated
unconditionally, with no carve-out for non-search computations. `check_L.py` is a
proof step that relies on code (the Main Reduction Theorem's use of Corollary 1a
depends on the p^(E_p+1) ≥ 25 table; Lemma 3 depends on the primes-in-(k/2,k) set),
yet it does not go through `tools/cert.py`/`tools/rerun.py`. The write-up is
transparent about this and argues the `Certificate` class is built for exhaustive
searches (domain + pruning rules + survivors) and would need artificial invented
structure to wrap four fixed numeric facts. That argument is reasonable as far as
it goes — and the checklist I was given frames the 5-part certificate specifically
around "p4 searches" — but it does not satisfy the literal, unconditional wording of
the repo's own non-negotiable rule 4, which this session is instructed to follow
exactly as written. I could not find an exception in `tools/cert.py`/`tools/rerun.py`
for exactly this case (a fixed non-search numeric check), so this reads as a real
gap in the tooling meeting the rule, not a loophole the author is entitled to use
unilaterally.

*Local fix:* either (a) wrap `check_L.py` through `tools/cert.py` with a degenerate
one-node "domain" (e.g. `domain = "the four numeric facts above"`, one `size(1)`
block, `node(1)`, no rules needed since nothing is pruned) so `tools/rerun.py`
can reproduce it under the standard pipeline, or (b) get an explicit maintainer
ruling that CLAUDE.md rule 4's certificate machinery is scoped to exhaustive
searches only and does not apply to fixed, hand-checkable numeric facts. Until
one of these happens, the write-up is not in full compliance with the project's
own non-negotiables, even though the arithmetic itself is exact, fast, and (as I
independently confirmed) correct.

## 5. Labels

All [PROVED] claims carry complete proofs; all [COMPUTED] claims are backed by an
exact, sub-second, rerunnable (in the ordinary sense of "run the script again")
script. Nothing conjectural is presented as proved.

## 6. Literature

"Cited vs ours" correctly states nothing outside problem.md's own definitions is
used, and honestly discloses an unread 2026 preprint without using any of its
technique — compliant with the citing-≠-proving rule.

## Summary

The mathematics is correct and complete for the (deliberately narrow) scope the
write-up claims: a lossless reduction of size-25 counterexamples to moduli dividing
L=lcm(1..24), plus the extra |I_p|≤p pruning at the four primes in (k/2,k). I
re-derived and stress-tested every lemma independently and found no flaw and no
overclaim. The one outstanding issue is procedural: the cited numeric-fact script
does not go through `tools/cert.py`/`tools/rerun.py` as CLAUDE.md's rule 4 requires
unconditionally, and the write-up's own justification for the omission, while
reasonable in spirit, is not itself an exception granted by the rule as written.

VERDICT: MINOR
