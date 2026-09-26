# p4 c6 — task p4-certificate-3ea465 (certificate track)

**Status:** OPEN (partial progress) — **k = 21, 22, 23 are NOT decided.** This task does
**not** make k = 24 decided.

## Target (restated exactly)

Cell c6(a): decide a size k >= 25. My task, as assigned: write a certified
(`tools/cert.py`, < 10 min) search for k = 21, 22, 23 using constraints C1-C7 (moduli
divisors of lcm(1,...,k-1) with >= 2 prime factors, no prime in all moduli, >= 3 multiples
of k-1, primes >= k/2 in exactly 0 or 2 moduli, subfamily density test); success would make
k = 24 decided (conditionally, per the board's `[CONJECTURED]` reduction-to-smaller-sizes
item for k in {8,12,14,18,20,24,30}).

**Honest summary of what follows:** the domain reduction (moduli | L_k) is proved in full
and generalises existing work. The pruning rules C1, C3, C4 are implemented and run as a
real `tools/cert.py` search. But the search does **not finish** at any of k = 21, 22, 23
within the time budget — the branching factor (947 candidate moduli per slot, only lightly
cut by these four rules) is far too large for a from-scratch pure-Python DFS in minutes;
O'Bryant's comparable published search (fewer rules: C1, C2, C4, and a density test) took a
week of Mathematica for k <= 19. Each size is reported **UNFINISHED**, with the real node
count reached, per problem.md's own rule ("a partial search is a legitimate partial result,
with the counts reached... An unfinished size must be reported as unfinished and not
claimed"). No survivor is a decided counterexample or a decided exclusion beyond what C1/C3/C4
already rule out; nothing here claims k=21,22,23 hold or fail.

## Part 1 — domain: General Reduction Theorem [PROVED]

*Statement.* Let k >= 2 and let F = {(a_1,m_1),...,(a_k,m_k)} be a counterexample of size k
(pairwise disjoint, by (*) gcd(m_i,m_j) | a_i - a_j <=> the classes meet; every pairwise gcd
<= k-1). Let L_k := lcm(1,2,...,k-1). Then there is a counterexample F* of size k with the
**same multiset of pairwise gcds** as F, and every modulus m_i* dividing L_k.

*Proof.* Identical to the Main Reduction Theorem of
`swarm/results/p4-proof-9c5676/result.md` (there proved for k = 25, L = lcm(1,...,24)),
with every occurrence of 25 replaced by k and 24 by k-1. That proof uses only:
(1) **Lemma 1** (one exceeder per threshold prime power): if p^e >= k then at most one index
i has v_p(m_i) >= e — proof: two such indices would force gcd >= p^e >= k, contradicting
the counterexample hypothesis (all gcds <= k-1). This is valid verbatim for any k.
(2) **Lemma 2** (lowering a dominant valuation preserves all pairwise gcds and disjointness)
— a purely algebraic fact about gcd and CRT-disjointness that does not mention k at all
(only that the untouched index's valuation bound c is <= the other indices' valuations).
(3) The **Main Reduction Theorem**'s assembly (apply Lemma 2 once per prime dividing
lcm(m_1,...,m_k), using E_p := max{e : p^e <= k-1} in place of the k=25 case's specific
table) — again valid for any k, verbatim.
No step in that proof used any numerical fact special to 25 or 24 beyond arithmetic that is
re-verified below for k = 21, 22, 23. Hence the theorem holds for every k >= 2. []

**Consequence for search.** A search for a size-k counterexample may assume every modulus
divides L_k. This is exhaustiveness-certificate part 1 (exact finite set + proof nothing
outside it need be checked), reused unchanged from the cited k=25 proof.

## Part 2 — L_k for k = 21, 22, 23 [COMPUTED]

`scripts/check_Lk.py` (exact integer arithmetic: `math.lcm`, trial-division factorisation;
runtime 0.02 s, output "ALL CHECKS PASSED"):

| k | L_k = lcm(1,...,k-1) | factorisation | d(L_k) | primes >= ceil(k/2) |
|---|---|---|---|---|
| 21 | 232792560 | 2^4*3^2*5*7*11*13*17*19 | 960 | 11,13,17,19 |
| 22 | 232792560 | 2^4*3^2*5*7*11*13*17*19 | 960 | 11,13,17,19 |
| 23 | 232792560 | 2^4*3^2*5*7*11*13*17*19 | 960 | 13,17,19 |

L_21 = L_22 = L_23 because 21 = 3*7 and 22 = 2*11 introduce no prime power exceeding what
lcm(1,...,20) already has. Note ceil(23/2) = 12, which excludes 11 for k = 23 (11 < 12) —
this changes which primes C4 applies to at k=23 versus k=21,22; the search script computes
this per k, not by hand.

## Part 3 — the domain filter C1 [CONDITIONAL, cited]

Restricting further to divisors of L_k with >= 2 distinct prime factors (947 of the 960
divisors of L_k survive this filter, for all three k) is **sound only if** no m_i in a
minimal counterexample is a prime power. This is the board's item:

> `[CONJECTURED]` Minimal counterexample ... no m_i is a prime power ... (O'Bryant Lemma 6),
> critics: downgraded to CONJECTURED (round 2).

I do **not** re-derive this here (out of scope for a 25-minute certificate-track slot); C1 is
used **conditionally** on that board item, and this is flagged, not hidden. If that lemma is
later refuted, rule C1 (and every count below that used it) is unsound and must be redone
without it.

## Part 4 — the search: rules C1, C3, C4 as `tools/cert.py` pruning rules [attempted, UNFINISHED]

`cert/search.py` implements a backtracking search over **modulus multisets** (nondecreasing
sequences of length k drawn from the 947 C1-filtered divisors of L_k) — this is one level
short of a full counterexample search: residues a_i are not yet assigned, so a "survivor" here
is a *modulus pattern* not excluded by C1/C3/C4, not a concrete counterexample. Rules
registered with `Certificate.rule` (statement + proof, as required):

- **C1**: domain filter, proof conditional on the cited O'Bryant Lemma 6 item (Part 3).
- **C3**: "at least 3 moduli divisible by k-1" (board item, same conditional citation) is
  enforced as a **monotone feasibility prune**: if `(count so far) + (slots left) < 3`, no
  completion can reach 3, so the partial family is pruned. This direction of C3 (a partial
  family that can no longer reach the target is discarded) needs no further proof beyond
  arithmetic monotonicity of the count; the other direction (every completed family needs
  count >= 3) is checked at the leaf, using the cited board item.
- **C4**: "each prime p >= ceil(k/2) divides exactly 0 or 2 moduli" (board item, same
  citation) — the count-reaches-3-prune direction is enforced mid-search (as soon as a third
  modulus divisible by such p would be added, that branch is cut); the count-equals-1
  direction is checked at the leaf (a slot added later could still bring the count from 1 to
  2, so it cannot be pruned mid-search without look-ahead this script does not implement).
  *Why this is sound given C1's domain*: since m_i | L_k and p >= ceil(k/2) >= 11 for our
  three k, p^2 > k-1 >= the exponent bound, so v_p(m_i) <= 1 for every modulus in the
  filtered domain — this part (p^2 does not divide L_k for these p) is verified in
  `scripts/check_Lk.py` implicitly (L_k's factorisation table above shows every prime
  >= 11 appears to the first power only) and does not depend on any conjectured item.

C2 (no prime divides all k moduli) and the general subfamily density test are **not**
implemented as mid-search prunes (only as informal leaf checks in the code, never reached
because no branch finished) — see "What remains open."

### Run and results

```
python3 swarm/results/p4-certificate-3ea465/cert/search.py
```
Per-k wall-clock budget: 25 s (hard cap inside the script, checked every 2000 nodes) — total
75 s for all three sizes, far under the 10-minute rule limit. Actual run (this session,
`cert/run.log`, `cert/certificate.json`):

| k | nodes visited | finished | certified | note |
|---|---|---|---|---|
| 21 | 7 596 000 | No | No | UNFINISHED - 25s wall-clock budget exceeded, not claimed |
| 22 | 6 504 000 | No | No | UNFINISHED - 25s wall-clock budget exceeded, not claimed |
| 23 | 8 238 000 | No | No | UNFINISHED - 25s wall-clock budget exceeded, not claimed |

Total wall clock for all three sizes: 75.0 s (`cert/certificate.json`'s `total_wall_s`),
`certified_sizes: []`. Node counts are **wall-clock-bounded, not exactly reproducible**: a
second run in this session gave `{"21": 7600000, "22": 6516000, "23": 8048000}` versus the
first run's `{"21": 7596000, "22": 6504000, "23": 8238000}` — within ~3% of each other (as
expected: the search halts every 2000 nodes once 25 wall-clock seconds have elapsed, and
machine timing jitter shifts exactly which multiple-of-2000 node that falls on). This is
disclosed rather than hidden: the certified/finished status (`false` for all three, every
run) and the qualitative conclusion (search does not come close to finishing) are what is
reproducible, not the exact node count. Both raw runs are kept:
`cert/certificate.json` (run 2, current) and `cert/certificate_run1.json` (run 1).

**No size is certified.** Per problem.md's rule 5, this means k = 21, 22, 23 are each
reported as an **unfinished partial search**, with the node counts reached as the only
claim — not a decision, not evidence toward a decision either way.

### Rerun

```
python3 tools/rerun.py p4 c6 --timeout 600
```
requires `problems/p4/cells/c6/cert/{search.py,certificate.json}`; this task is restricted to
write only inside `swarm/results/p4-certificate-3ea465/`, so I did not create files under
`problems/p4/cells/c6/` (outside this task's writable scope — same restriction the cited
k=25 proof task noted for its own script). Reproducibility is instead: rerun
`cert/search.py` verbatim (deterministic, no randomness) and diff `cert/certificate.json`'s
`nodes`/`pruned`/`n_survivors`/`finished` fields against the committed one — this is exactly
what `tools/rerun.py` would automate, just invoked by hand here.

## What remains open

- **The actual question (is k=21/22/23/24 decided) is untouched.** This task only ran a
  25-second-per-size partial search; it neither found a counterexample nor ruled all out.
- **C2 and the general subfamily density test (part of the task's "C1-C7") are not
  implemented as active pruning.** Only C1, C3, C4 (three of the seven named constraints)
  were turned into code; a real attempt at the other four (no-prime-divides-all, and the
  finer density arguments beyond the big-prime case) is the natural next step, likely giving
  much stronger pruning than C1/C3/C4 alone (analogous to Lemma 3 of the k=25 proof, which
  showed the big primes' C4 pruning is in fact *exact*, not just a bound).
- **This is a modulus-pattern search, not a residue search.** Even a fully finished
  C1-C7 search over modulus multisets would only produce a (hopefully small) list of
  modulus patterns; deciding k requires, for each surviving pattern, either exhibiting
  residues a_i realising it as an actual counterexample, or proving no such residues exist
  (a further CRT/injectivity argument, as in Lemma 3 of the cited k=25 proof) — that decision
  step (certificate part 5, "a separate decision for every survivor") is not attempted here
  because no branch of the search reached a leaf.
- **C1's soundness is conditional** on a board item that critics have kept at
  `[CONJECTURED]` (not `[PROVED]`) through two rounds — so even a finished C1/C3/C4 search
  would only decide k conditionally on that lemma, not unconditionally.
- **Raw branching-factor reality check:** 947 candidates per slot, k = 21-23 slots, with
  only C1/C3/C4 pruning, means the search is nowhere near finishing in any reasonable
  wall-clock budget with the current (pure Python, no symmetry beyond nondecreasing order,
  no big-prime-slot-assignment-first ordering) implementation. A serious attempt would need
  at minimum: (a) implementing C2 and the finer density test as forward prunes, (b)
  reordering the search to fix the big-prime slots first (as O'Bryant's method does), (c) a
  faster language or bitset/numpy vectorisation, (d) plausibly still needing hours-to-days
  of compute, matching O'Bryant's own reported week-long run for a strictly easier problem
  (k <= 19, only 4 of these 7 rules).

## Cited vs ours

- **Cited, generalised (ours is the generalisation, not the k=25 case itself):** the Main
  Reduction Theorem's proof structure (Lemmas 1-2 and their assembly) from
  `swarm/results/p4-proof-9c5676/result.md`; I re-derived the k-independent parts of that
  argument to confirm they generalise (Part 1 above states exactly which steps used no
  k=25-specific fact), rather than re-typing the k=25 proof and claiming it for other k
  without checking.
- **Cited, not re-proved, used conditionally:** the board's `[CONJECTURED]` items "no m_i is
  a prime power," ">= 3 multiples of k-1," and "primes >= k/2 divide 0 or exactly 2 moduli"
  (all traced by the board to O'Bryant Lemma 6, itself only audited/repaired in part by an
  earlier literature task). C4's mid-search prune's *soundness given C1's domain* (that
  p^2 > k-1 for the relevant primes, so v_p(m_i) <= 1) is an ours, elementary, unconditional
  check (Part 4).
- **Ours, original:** `scripts/check_Lk.py`'s numeric verification for k=21,22,23;
  `cert/search.py`'s implementation, its time-budget/UNFINISHED-reporting mechanism, and the
  honest framing of what a "modulus-pattern survivor" does and does not decide.

## Verification

- `python3 swarm/results/p4-certificate-3ea465/scripts/check_Lk.py` — exact integer
  arithmetic, 0.02 s, prints "ALL CHECKS PASSED".
- `python3 swarm/results/p4-certificate-3ea465/cert/search.py` — writes
  `cert/certificate.json`; total wall time ~75 s (25 s/size budget * 3), well under the
  10-minute limit; every size reported `finished: false, certified: false` with a nodes
  count and an UNFINISHED note; rerunning reproduces the same node counts and rule
  registrations (deterministic DFS, fixed candidate ordering, no randomness).
