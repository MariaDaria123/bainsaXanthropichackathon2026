# Critic #2 report — p4-proof-2d83fd

Scope respected: judged only `swarm/results/p4-proof-2d83fd/result.md`, `problems/p4/cells/c6/cell.md`,
`problems/p4/problem.md`, the cited library (`problems/p4/lib/congruence.py`), and the cited script
`swarm/results/p4-proof-2d83fd/scripts/check_range.py`, which I ran. Did not read `notes.md`, `swarm/board/`,
other results, or logs.

## 1. Statement check

- **Sub-lemma A** ("at most one index has v_p(m_i) ≥ e when p^e ≥ 25, inside a counterexample F of size 25"):
  stated with full quantifiers (p prime, e ≥ 1, p^e ≥ 25, "any counterexample F"), proof is a direct
  two-line divisibility argument, correct. No weakening.
- **Range table / [COMPUTED] claim** ("the thresholds p^{E_p} landing in (25/3, 25/2] are exactly 9 and 11"):
  states the exact range and exact set, matches the task's own example. Verified independently below.
- **Lemma 4** ("case-split injectivity for q ∈ {9,11}"): the statement is precise — I_q, I_q^0, J_q are all
  defined before use, part (a) claims gcd ∈ {q,2q} only (not "≤" or "roughly"), part (b) claims the exact
  value in each sub-case, part (c) claims injectivity into ℤ/qℤ and ℤ/2qℤ respectively with the resulting
  bounds q, 2q, 3q. No silent weakening, no hidden extra hypothesis. The label split ([PROVED] for the
  case-split structure and injectivity, [BOUNDED] only for the resulting numeric bound) is used correctly
  and is *more* conservative than it needed to be, not less — good practice.
- The "Honest assessment" section is explicit that |I_q| ≤ 3q > 25 for both q, i.e. the lemma does **not**
  shrink the raw search headcount for q ∈ {9,11}, unlike the predecessor Lemma 3's primes {13,17,19,23}
  where p itself is < 25. This is disclosed prominently, not buried. No overclaiming found.

## 2. Every step — gap hunt

Went through Sub-lemma A and Lemma 4(a)/(b)/(c) line by line.

- Part (a): "at least one of i,j has v_p exactly at the threshold" correctly follows from Sub-lemma A
  (not both can be at/above the next power). "gcd = p^e·r, r coprime to p, r ≤ ⌊24/q⌋" is a correct
  application of v_p(gcd) = min(v_p(m_i), v_p(m_j)). The extra paragraph re-deriving "no other prime ℓ ≥ 3
  divides the gcd" is redundant (this already follows immediately once r ∈ {1,2} is fixed as a literal
  integer) but not incorrect — a style nit, not a gap.
- Part (b): the "at most one index in I_q has v_2 ≥ 2" step correctly uses part (a)'s dichotomy
  (v_2(gcd) ∈ {0,1} only) to contradict v_2(gcd) ≥ 2; the alternative phrasing via "4q | gcd ⟹ gcd ≥ 4q > 24"
  is also valid (4 and p^{e_q} are coprime, so their product divides gcd). No gap.
- Part (c): injectivity from disjointness via criterion (*) is applied correctly and matches
  `problems/p4/lib/congruence.py`'s `meet`/`disjoint` definitions (checked against the library source).
- No use of "clearly / obviously / routine / similarly / WLOG" anywhere in the mathematical argument.

No gaps found in the proof as written.

## 3. Testing the lemmas on small cases

Brute-forced part (a)'s core claim independently (not the author's script, a fresh one), for m ranging
over 1..2000:

```
q=9,  p=3,  threshold v_3≥2: 0 counterexamples (every pair with gcd≤24 has gcd ∈ {9,18})
q=11, p=11, threshold v_11≥1: 0 counterexamples (every pair with gcd≤24 has gcd ∈ {11,22})
```

Confirms Lemma 4(a) computationally over a range well beyond what hand-checking alone would give confidence in.

## 4. Cited code — ran it

```
$ python3 swarm/results/p4-proof-2d83fd/scripts/check_range.py
thresholds p -> p^E_p: {2: 16, 3: 9, 5: 5, 7: 7, 11: 11, 13: 13, 17: 17, 19: 19, 23: 23}
k/3=8.3333, k/2=12.5000, thresholds in (k/3,k/2]: [9, 11]
...
ALL CHECKS PASSED in 0.0001s
```

Matches every number quoted in the write-up exactly. It is exact integer arithmetic (`math.lcm`, `math.gcd`,
trial-division factorisation), deterministic, well under 10 minutes, and its assertions are individually
hand-checkable (I did so above and in §3). It is *not* a combinatorial search with pruning rules / node
counts / survivors, so the 5-part exhaustiveness certificate format doesn't apply to it, and none of the
paper's actual mathematical conclusions depend on trusting the script — every number in it is also derived
by hand in the prose (e.g. 3²=9, 3³=27, 24/9≈2.67, etc.).

However: CLAUDE.md rule 4 says *"any proof step that relies on code must use `tools/cert.py`... and be
reproducible by `tools/rerun.py`"* with no stated exception for small arithmetic sanity checks. The
write-up runs a bare script outside that framework and defends this by analogy to a predecessor task's
similar choice (which I'm not allowed to check). Since the math here doesn't actually depend on the script
(it's independently verified by hand in the text and by me above), I don't think this is a substantive
defect, but it is a literal non-compliance with a "non-negotiable" repo rule and should be fixed for
process hygiene — either route `check_range.py` through `tools/cert.py` in a trivial single-size wrapper,
or drop the script and rely purely on the (already complete) hand computation.

## 5. Labels

All labels ([PROVED], [BOUNDED], [COMPUTED]) are used correctly and, where in doubt, the author under-claims
rather than over-claims (e.g. downgrading the numeric consequence to [BOUNDED] even though the derivation
supporting it is fully proved). No [CONJECTURED]/[OBSERVED] material is presented as proved.

One header-level nit: CLAUDE.md rule 1 requires status to be exactly `SOLVED` or `PARTIAL`. The write-up's
header says **"Status: OPEN (partial progress...)"**. Since this task doesn't decide k=25, `PARTIAL` is the
compliant word; `OPEN` is not one of the two allowed statuses. Cosmetic, but should be corrected to keep
every result.md in the same fixed vocabulary.

## 6. Literature

No black-box citation of the target statement. Sub-lemma A is re-derived from scratch in the write-up
itself rather than citing the predecessor task's (reportedly [CONJECTURED]) Lemma 1, which is the right
call given the instructions to use only board facts with status *proved*. "Cited vs ours" section is
present and accurate about what is original here (Lemma 4's case split and its proof, `check_range.py`) vs.
re-derived (Sub-lemma A). No literature search was done for this narrow sub-task, and that is disclosed,
not hidden.

## Overall

This is a correctly proved, precisely scoped extension of the injectivity/density argument to the
prime-power thresholds q ∈ {9,11} exactly as the task goal asked (size-2 case split q vs 2q instead of a
forced single value). I could not find a mathematical gap after checking every step and cross-checking
computationally. The write-up is unusually careful about not overclaiming: it explicitly reports that the
resulting bound |I_q| ≤ 3q does *not* shrink the raw search headcount below 25 for q ∈ {9,11} (unlike the
predecessor range where p < 25 already gave a real restriction), which is an honest and important caveat
about how much this actually "squeezes the search domain" in the sense the task goal literally asks for.

Fixes needed (both cosmetic/process, not mathematical):
1. Change header "Status: OPEN" → "Status: PARTIAL" to match the repo's fixed two-word status vocabulary.
2. Either route `check_range.py` through `tools/cert.py`/`tools/rerun.py`, or state explicitly and
   prominently that no conclusion in the proof depends on the script (only on the hand computation already
   in the prose), to fully satisfy CLAUDE.md rule 4's literal wording.

VERDICT: MINOR
