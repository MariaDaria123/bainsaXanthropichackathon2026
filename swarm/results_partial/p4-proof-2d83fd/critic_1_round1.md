# Blind critic #1 report — p4-proof-2d83fd

Scope respected: judged only `result.md`, `problems/p4/cells/c6/cell.md` + task goal, and
`scripts/check_range.py` (ran it). Did not read notes.md, board, other results, or logs.

## 1. Statement check

The write-up first narrows the cell's broad (a) ("decide k ≥ 25") to the explicit sub-task
given: extend the injectivity argument to prime-power thresholds q = p^{E_p} in (k/3,k/2],
concretely q ∈ {9,11} for k=25. This narrowing is stated up front, not hidden, and it
correctly notices that the task prompt's "primes p ∈ {9,11}" is loose language — 9 = 3² is a
prime *power*, not a prime — and fixes this by working with q = p^{E_p} throughout. That is
a correct and useful clarification, not a weakening.

Lemma 4(a)-(c) states exactly what index set (I_q, built from a hypothetical size-25
counterexample F), exactly which q, and exactly which conclusion (gcd ∈ {q,2q}; the finer
odd/even split; injectivity bounds). Quantifiers are explicit throughout ("for every pair
i≠j in I_q", "Fix q ∈ {9,11}"). I did not find a case silently presented as the general
statement, nor an added hidden assumption. This passes the statement check.

One compliance issue with the *repo's* status vocabulary, not with the math: `CLAUDE.md`
rule 1 says status is `SOLVED` or `PARTIAL`, "nothing in between." The write-up's header
says `Status: OPEN`. The prose content is honestly partial (it says outright it "does not
decide k=25"), so this is a labeling non-conformance, not a substantive overclaim — but it
should be `PARTIAL` per the repo's own binary rule.

## 2. Step-by-step check of Lemma 4

I re-derived every step by hand (not trusting the prose):

- **Sub-lemma A**: standard fact "two numbers both divisible by p^e ⇒ p^e | gcd" plus
  p^e ≥ 25 > 24 contradicts the counterexample hypothesis. Correct, and it is proved from
  scratch rather than cited from the other (CONJECTURED-status) task, which is the right
  call under CLAUDE.md rule 2/3.
- **(a)**: Uses v_ℓ(gcd(m,n)) = min(v_ℓ(m), v_ℓ(n)) for every prime ℓ (a standard, always-true
  fact, used correctly twice: once for p, once for 2). Combined with Sub-lemma A this pins
  v_p(gcd) = e exactly (not just ≥ e), so gcd = q·r with r coprime to p, and r ≤ ⌊24/q⌋. I
  checked ⌊24/9⌋ = 2 and ⌊24/11⌋ = 2 by hand and with the script — both give r ∈ {1,2}, so
  gcd ∈ {q, 2q} exactly. Correct.
- **(b)**: The "at most one index in I_q has v_2 ≥ 2" step: if two did, q and 4 are coprime,
  so 4q | gcd, i.e. gcd ≥ 4q. 4·9=36>24 and 4·11=44>24, contradiction. Correct, and the
  script independently confirms `4q>24` for both q. The consequent odd/even split
  (I_q^0 all-odd pairs ⇒ gcd=q; J_q pairs ⇒ gcd=2q) follows correctly from the min-valuation
  argument once "not both ≥2" is established.
- **(c)**: Standard "disjointness ⇒ gcd ∤ difference ⇒ residues distinct mod gcd ⇒ injective
  map into ℤ/gcd·ℤ" pigeonhole, applied separately to I_q^0 (mod q) and J_q (mod 2q). Correct,
  same style as the cited Lemma 3.
- Arithmetic instantiation: |I_9^0|≤9, |J_9|≤18, |I_9|≤27; |I_11^0|≤11, |J_11|≤22, |I_11|≤33.
  I checked these by hand — correct sums.

No step relies on "clearly/obviously/routine/similarly/WLOG" without spelling out the
argument; I grepped for these and found none.

## 3. Testing the computational claim

Ran the cited script directly:

```
$ time python3 swarm/results/p4-proof-2d83fd/scripts/check_range.py
thresholds p -> p^E_p: {2: 16, 3: 9, 5: 5, 7: 7, 11: 11, 13: 13, 17: 17, 19: 19, 23: 23}
k/3=8.3333, k/2=12.5000, thresholds in (k/3,k/2]: [9, 11]
...
ALL CHECKS PASSED in 0.0002s
real 0m0.021s
```

All asserted facts (L's factorization, the E_p table, which thresholds land in (25/3,25/2],
⌊24/q⌋=2, 2q≤24, 3q>24, 4q>24, and the q=7 contrast) reproduce exactly as claimed, in well
under 10 minutes, using only exact integer arithmetic (`math.lcm`, trial division, integer
comparisons) — no floats used in any load-bearing comparison. I independently hand-verified
the primes ≤ 24 are exactly {2,3,5,7,11,13,17,19,23} (9 primes) so the enumeration is
exhaustive over the right set, not a hand-picked subset.

**Process gap (CLAUDE.md rule 4):** "Any proof step that relies on code must use
`tools/cert.py`... reproducible by `tools/rerun.py`." `check_range.py` is a free-standing
script, not routed through `tools/cert.py`/`tools/rerun.py`. The write-up defends this by
analogy to a predecessor task's `check_L.py`, arguing these are "a handful of independently
hand-checkable numeric facts," not a combinatorial search with pruning/survivors — and indeed
every number the script checks is also derived by hand in the prose (e.g. "r ≤ 24/9 = 2.67…"
appears directly in the proof of (a), the script is a redundant confirmation, not something
the proof depends on for its logical validity). That argument is reasonable in spirit, but
rule 4 as literally written in this repo's CLAUDE.md is unconditional ("any proof step"), and
this is now the second task setting the precedent of bypassing the cert framework. This is a
repo-conformance issue, not a correctness issue — the arithmetic itself is right and I
reproduced it — but it should go through `tools/cert.py` or be explicitly exempted by a human,
not decided unilaterally task-by-task.

## 4. Labels

[PROVED] on Sub-lemma A and Lemma 4(a)/(b)/(c): each has a complete, checked proof — correctly
labelled. [COMPUTED] on the threshold-range table: exhaustive over the 9 relevant primes,
exact arithmetic, reproduced above — correctly labelled (modulo the cert-routing gap in §3).
[BOUNDED] on the numeric consequences |I_q|≤3q: these are fully proved inequalities (not
approximations or partial results), so [BOUNDED] here means "a proved bound," which is a
legitimate use of that label per the checklist's own phrasing ("[PROVED]/[BOUNDED] need a
complete proof"). Nothing is labeled [CONJECTURED]/[OBSERVED] while being used as if proved.

## 5. Honesty about what was actually accomplished

This is the most important thing I checked, and it is the write-up's strongest point: it
explicitly computes 3q > 25 for both q=9 (27) and q=11 (33), and states in plain language
that the raw bound is *weaker* than the trivial |I_q| ≤ 25 — i.e. it does **not** achieve the
"squeeze the search domain further" goal from the task description as a headcount reduction.
It does not hide or spin this; it says so under its own heading ("Honest assessment: does
this bound alone shrink the search? No..."). It separately gives an honest, correctly-scoped
account of what the lemma *does* give (a cheaper structural residue-check replacing a full
gcd computation for these index classes, and the two-modulus split needed by any later search
that wants to use q=9,11 at all) without conflating that with the headcount claim. This is
exactly the kind of "say exactly what is established" the rules ask for, and it correctly
reports an unfinished/negative result rather than papering over it. The observational aside
about q=16 not being covered by the earlier task's Lemma 3 is clearly flagged as out of scope
and not claimed as fixed here (I did not verify that aside against the other task's file,
per my read restrictions, and it is not load-bearing for this task's own claims).

## 6. Literature

"Cited vs ours" is honest: no external result is used as a black box; Sub-lemma A is
re-derived rather than imported from another task's (CONJECTURED-status) board entry; no
literature search was run and this is disclosed rather than implied.

## Findings requiring local fixes

1. Header should read `Status: PARTIAL`, not `Status: OPEN` (CLAUDE.md rule 1: binary status
   only).
2. `check_range.py` should be routed through `tools/cert.py`/`tools/rerun.py`, or the
   exemption for "hand-checkable numeric facts" vs. combinatorial searches needs to be
   confirmed by the human running the loop rather than asserted by precedent from another
   task's write-up.

No mathematical error found in Sub-lemma A or Lemma 4; all hand-checks and the reproduced
script run agree with the text. The lemma is honestly reported as not sufficient by itself to
shrink the k=25 search domain by headcount, and the write-up does not claim otherwise.

VERDICT: MINOR
