# Critic 1 report — p4-proof-f59824 (blind, independent)

Scope respected: judged only `result.md`, `problems/p4/cells/c6/cell.md`, the task
goal, and the three cited scripts (`enumerate_patterns.py`, `check_scaling.py`,
`cert_search.py`), all of which I ran myself. Did not read notes.md, board, other
results, or logs.

## 1. Statement check

Target restated in `result.md` matches the assigned task goal exactly: reductions
(i)–(iii) plus enumeration of index 6-tuples with pairwise gcd in [2,5] and
Σ1/n_i ≤ 1. No silent weakening of the reduction lemmas: Lemma 1 is stated for
general k (not just pairs), Lemma 2's statement correctly says "for **every**
choice of x,y", Lemma 3 is the plain density bound. Good — no smuggled special
case.

The one place a scope decision is made explicitly, not silently, is the
enumeration: the write-up notes up front that the literal set of integer
6-tuples is infinite (correctly demonstrated by `check_scaling.py`'s scaling
argument) and substitutes the finite shared-prime-pattern invariant D_i =
{p∈{2,3,5}: p|n_i}. This is flagged in a "Scope note, up front" rather than
buried, which is the right way to handle an assignment that is literally
impossible to satisfy verbatim (an infinite enumeration).

## 2. Lemma-by-lemma check

**Lemma 1 (reduction to finite G).** Standard core-of-subgroup argument, but
written out fully rather than cited (as CLAUDE.md rule 2 requires): kernel of
the coset-action homomorphism = core, N = ∩ cores is normal of finite index via
embedding G/N ↪ ∏ G/Core_i, N ⊆ Core_i ⊆ G_i correctly justified. Part (b)'s
index-preserving bijection G/G_i ↔ Ḡ/Ḡ_i is checked well-defined / injective /
surjective, not asserted. Part (c)'s two directions are both spelled out
(the ⇐ direction correctly uses "N ⊆ G_i" to show a lift of a coset-intersection
witness lands in the original cosets). No gaps found.

**Lemma 2 (coprime ⟹ meet).** Reduces to the finite case via Lemma 1 applied to
just the pair. Step 1 (tower law argument for [H:A∩B] = n_i n_j) is a genuine
proof, not a citation — both divisibility and the reverse inequality (via an
explicit injection A/C ↪ H/B) are argued. Step 2 proves |AB|=|A||B|/|C| from
scratch (fiber-counting via the equivalence a'=ac⁻¹, b'=cb), not just invoking
the product formula as a black box — this satisfies rule 2 ("citing ≠ proving")
better than most write-ups I've seen for this fact. Step 3 correctly converts
"AB=H" into "every coset pair meets." No gaps found.

**Lemma 3 (density bound).** Immediate finite counting argument; correct and
complete.

## 3. Testing the enumeration lemma and code

Ran all three cited scripts myself:

```
enumerate_patterns.py: tuples checked 117649, valid tuples 147, distinct patterns 4
check_scaling.py: all 4 patterns' gcds in [2,5] and Σ1/n_i < 1, exact Fraction arithmetic, asserts pass
cert_search.py: certified_sizes [6], nodes 117649, n_survivors 4, n_undecided 0, certified True
```

All match the write-up's claimed numbers exactly. Runtime for all three is well
under a second, far inside the 10-minute budget.

**Independent verification of the "exactly 4 patterns, 147 raw tuples" claim
(without trusting the script):** I hand-counted the orbit sizes under S_6×S_3
directly from the stated patterns:
- Pattern I (all six singletons, same prime): 3 raw tuples (choice of prime).
- Pattern II (five singleton-p + one doubleton ⊇{p}): 6 (position of the
  doubleton) × 3 (choice of p) × 2 (choice of the second prime in the
  doubleton) = 36.
- Pattern III (four singleton-p + two distinct doubletons both containing p):
  3 (choice of p) × C(6,2) (which two slots) × 2 (which doubleton in which
  slot) = 3×15×2 = 90.
- Pattern IV (five singleton-p + one full set {2,3,5}): 6 (position) × 3
  (choice of p) = 18.

3+36+90+18 = **147**, matching the brute-force count exactly. I also checked by
hand that no other configuration is possible: three pairwise-distinct
doubletons {2,3},{2,5},{3,5} satisfy the pairwise-intersection-size-1 condition
among themselves but cannot be extended to a 4th index (no singleton or
4th subset meets the "exactly one common element with each of the three
doubletons" requirement, and only 3 distinct doubletons exist over a 3-element
ground set) — so they fill exactly 3 slots and cannot reach k=6, exactly as the
write-up's hand argument states. This is a solid independent corroboration of
both the code and the informal argument, from two different directions.

**Sub-lemma correctness.** For g ∈ {2,3,4,5}, exactly one prime ≤5 divides g,
and no prime ≥7 can divide it (g≤5<7); since D_i∩D_j is precisely the set of
primes ≤5 dividing gcd(n_i,n_j), this directly gives |D_i∩D_j|=1 whenever
gcd(n_i,n_j)∈{2,3,4,5}. The write-up's proof reaches the same conclusion by a
slightly more roundabout contradiction argument, but it is valid.

## 4. Cited-code / certificate check (checklist item 4)

Domain (7^6 D-tuples) is proved exhaustive: the domain_proof in `cert_search.py`
correctly argues that only primes in {2,3,5} can matter (any prime ≥7 dividing
a pairwise gcd forces that gcd ≥7>5, excluded), so each D_i is one of exactly
7 nonempty subsets, and no restriction is assumed before the search. No pruning
rules are used (correct — this is a plain exhaustive scan, not a pruned
search), all 4 survivors are given a decision, minimal_part and
minimality_proof (each is the whole D-tuple itself, correctly justified since
all 6 entries and all 15 pairwise intersections are needed to state the
defining condition). `certificate.json` shows `certified: true`,
`n_undecided: 0`. This satisfies the 5-part certificate template as far as the
classification step goes.

**One real outstanding item, correctly self-flagged, not hidden:**
`problems/p4/cells/c6/cert/` contains only `.gitkeep` — no `search.py`. I
confirmed `tools/rerun.py` requires `cert/search.py` under the cell directory
and will report "no cert/search.py" if run for p4 c6 right now. The write-up
discloses this directly under "Certificate-protocol gap" rather than claiming
`tools/gate.py p4 c6` has been run. This is honest reporting of an unresolved
mechanical step (copying `cert_search.py`'s logic into the canonical location),
not a false claim — but it does mean the promotion pipeline (`tools/rerun.py`,
`tools/gate.py`) has not actually validated this cell yet.

## 5. Points needing local fixes (do not require a restart)

1. **"Lossless" is stated too strongly.** The write-up says the D_i-pattern
   reduction is "lossless for the gcd constraints." What is actually shown is
   (a) necessity — any counterexample's gcd-in-{2,3,4,5} constraint forces a
   valid D-pattern (proved), and (b) achievability — each of the 4 patterns has
   at least one integer realization meeting both constraints (computed). That
   is not the same as losslessness/equivalence: a given D-pattern does not by
   itself guarantee gcd∈{2,3,4,5} for an arbitrary tuple realizing it (e.g. two
   numbers both divisible by 4 could have gcd 4, 8, 16, ... — nothing pins the
   gcd to the shared prime alone). The proof is correct, but "lossless" should
   be replaced with something like "necessary, and achievable" to avoid
   suggesting an if-and-only-if that isn't proved (and isn't needed for the
   argument to go through).
2. **Close the certificate-protocol gap before promotion**: copy
   `cert_search.py`'s logic into `problems/p4/cells/c6/cert/search.py` and run
   `tools/rerun.py p4 c6` / `tools/gate.py p4 c6`, per the write-up's own
   "What remains open" section. This is bookkeeping, not a mathematical gap,
   but it means the cell is not yet gate-certified in the repo's canonical
   sense.

## 6. Banned-word check

Both uses of "WLOG" in the document are backed by an explicit argument (Lemma 1
itself, or an explicit citation back to Lemma 1) rather than used as a
hand-wave. No unexplained "clearly / obviously / routine / similarly" found.

## 7. Cited vs ours

The "Cited vs ours" section correctly identifies the two facts drawn from
standard group theory (kernel-of-coset-action = core; |AB|=|A||B|/|A∩B|) and
states both are reproved from scratch rather than invoked as black boxes,
consistent with what I verified in section 2. Everything else is claimed as
original for this task, and I found nothing in the document that looks lifted
from a cited source without derivation.

## Summary

Lemmas 1–3 are fully proved with no gaps I could find. The sub-lemma and the
4-pattern classification are correct — I independently reconstructed the same
147/4 split by hand from the stated patterns' orbit sizes, which is strong
corroboration beyond just rerunning the script. All three cited scripts run,
are deterministic, exact, and reproduce every number quoted in the text. The
two issues above are local wording/bookkeeping fixes, not defects in the
mathematics.

VERDICT: MINOR
