# Critic 2 report — p4-proof-f59824

Scope: `swarm/results/p4-proof-f59824/result.md`, `problems/p4/cells/c6/cell.md`, the task
goal, and the two scripts it cites (`scripts/enumerate_patterns.py`,
`scripts/check_scaling.py`), which I ran. I did not read notes.md, board, other results,
or logs.

## 1. Statement check

The task goal has two parts: (I) prove the three reductions (i) WLOG-finite via
G/N with N = ∩ cores, (ii) coprime indices ⟹ cosets meet ⟹ gcd ≥ 2, (iii) Σ1/n_i ≤ 1;
(II) enumerate the index 6-tuples a k=6 counterexample could have subject to pairwise
gcd ∈ {2,3,4,5} (forced by (ii) plus "not already a witness for k=6") and Σ1/n_i ≤ 1.

- Lemma 1 states (i) with full quantifiers (all i,j, all x,y, general k) — matches.
- Lemma 2 states (ii) in the strong form "for every x,y ∈ G the cosets meet" whenever
  gcd(n_i,n_j)=1, then derives gcd ≥ 2 for disjoint families — matches, and is in fact
  stronger than needed (good).
- Lemma 3 states (iii) exactly — matches.
- For (II): actual integer 6-tuples (n_1,…,n_6) satisfying the two constraints form an
  infinite set (the `check_scaling.py` construction shows this directly, by scaling with
  arbitrary coprime cofactors), so a literal finite enumeration of tuples is impossible.
  The write-up substitutes a finite classification of the "shared-{2,3,5}-prime pattern"
  D_i = {p ∈ {2,3,5} : p | n_i}, proves this is a *necessary* invariant of any qualifying
  tuple (Sub-lemma), and enumerates it exhaustively (4 patterns up to S_6×S_3 symmetry).
  This is a defensible substitute for "enumerate all tuples" given the tuples are
  infinite, and the write-up is explicit about the gap in "What remains open" (it does
  NOT claim to have enumerated actual n_i values, only the necessary prime-sharing
  structure, plus one witness tuple per pattern). This should arguably be flagged nearer
  the top of the classification section rather than only at the end, but it is not
  presented as more than it is — no silent weakening here.

No claim silently narrows quantifiers, adds an unstated hypothesis, or proves a special
case while presenting it as the general one, as far as I can find.

## 2. Step-by-step check

I re-derived every step of Lemma 1(a)(b)(c), Lemma 2 steps 1–3, and Lemma 3 by hand;
no gap found. Specifically:
- Lemma 1(a): kernel-of-coset-action = core is correctly computed; N normal of finite
  index via embedding into ∏ G/Core_i is correctly argued (Core_i is separately shown
  a subgroup of G_i, which is used later).
- Lemma 1(b): the bijection ψ: G/G_i → Ḡ/Ḡ_i is well-defined/injective/surjective with
  all three checks spelled out.
- Lemma 1(c): both directions of the disjointness-transfer are argued explicitly with no
  hidden step.
- Lemma 2: Step 1 (tower law + injective map A/C ↪ H/B) correctly gives [H:C] = n_i n_j
  exactly (not just an inequality — both directions are proved). Step 2 correctly derives
  |AB| = |A||B|/|C| by exhibiting the fiber structure of the map A×B → H. Step 3 is a
  one-line translation. All fully written out, no "clearly"/"routine" steps hidden.
- Lemma 3: direct disjoint-union counting argument, correct.
- Sub-lemma (shared-prime pattern): correct — verified independently below.

The only place "WLOG" appears in an actual proof step (line 119, "By Lemma 1, WLOG G is
finite") is backed by an explicit citation of the already-proved Lemma 1, not a bare
assertion, so it does not violate the no-WLOG-without-argument rule.

## 3. Independent computational tests

I tested the two central reusable claims outside the cited scripts:

**Lemma 2 on an actual finite group.** Built S4 by hand (permutation composition),
took A = Stab(0) (order 6, index 4) and B = ⟨(0123),(02)⟩ (order 8, index 3),
gcd(4,3)=1, and brute-force checked xA ∩ yB ≠ ∅ for **all** 24×24 pairs (x,y) ∈ S4×S4.
Result: all 576 pairs meet, confirming Lemma 2's "for every x,y" claim on a concrete
non-abelian example (no counterexample).

**Sub-lemma faithfulness.** Brute-forced all integer pairs 2 ≤ a ≤ b ≤ 400 with
gcd(a,b) ∈ {2,3,4,5} and checked |D(a) ∩ D(b)| = 1 with D(n) = {p∈{2,3,5}: p|n}, using
Python's exact `math.gcd`. 0 violations over the full range — confirms the sub-lemma
that the write-up's D_i-abstraction is used to build.

## 4. Cited/computed code — reran

- `scripts/enumerate_patterns.py`: reran, reproduces exactly the claimed output
  (117649 tuples checked, 147 valid, 4 patterns up to S_6×S_3, listed patterns match
  the table in result.md), wall time 0.08 s. Domain (7 nonempty subsets of a 3-set)^6 is
  genuinely exhaustive by construction, arithmetic is exact (frozenset/int), no
  randomness.
- `scripts/check_scaling.py`: reran, reproduces the claimed n-tuples and gcd/sum values
  exactly (`Fraction` arithmetic), all four patterns pass the `assert`, wall time < 0.1 s.

**Certificate-protocol gap (this is the one real defect).** CLAUDE.md rule 4 is a
non-negotiable: "Any proof step that relies on code must use `tools/cert.py` ... and be
reproducible by `tools/rerun.py`." Checklist item 4 additionally asks specifically for
the p4 5-part certificate. Neither script uses the `Certificate` class from
`tools/cert.py`; neither writes to `problems/p4/cells/c6/cert/certificate.json`; the
scripts are not even placed at `problems/p4/cells/c6/cert/search.py`, which is the only
path `tools/rerun.py` (via `cell_dir`) knows how to rerun. I confirmed
`problems/p4/cells/c6/cert/` currently contains only a `.gitkeep` — no certificate has
ever been produced for this cell. So while the computations are exact, exhaustive, and I
independently reproduced them, they are **not currently certified** in the sense the repo's
own pipeline requires: `python tools/rerun.py p4 c6` cannot be run against them as they
stand, and `python tools/gate.py p4 c6` has nothing to check. This needs a local fix, not
a redo of the mathematics:
1. Move/adapt the logic of `enumerate_patterns.py` (and, if wanted, `check_scaling.py`)
   into `problems/p4/cells/c6/cert/search.py`, using `tools.cert.Certificate` to record
   the domain, domain proof, node counts (trivial here — no pruning rules are used, which
   is fine, just register none or a no-op), and mark the single "size" (k=6 D-pattern
   search) as finished/certified with `certificate.json` written to the standard path.
2. Run `python tools/rerun.py p4 c6` to produce `cert/rerun.json`.
3. Only then can `[COMPUTED]` be considered backed by the repo's own certificate
   machinery rather than an ad hoc, if verifiably-correct, script.

## 5. Labels

[PROVED] labels (Lemmas 1–3, sub-lemma) are backed by complete proofs — checked line by
line above, no gap found. [COMPUTED] labels (enumeration, realizability) are backed by
exhaustive exact scripts that I reran and that match the claims — but see §4 for the
missing formal certificate wrapper. No claim is conjectural/observed but mislabeled as
proved.

## 6. Literature

The "Cited vs ours" section correctly identifies the two classical facts used (kernel of
coset action = core; |AB| = |A||B|/|A∩B|) and states they are reproved from scratch
rather than cited as black boxes — I checked both proofs line by line in §2 and they are
in fact fully self-contained. No black-box citation of the actual statement being proved
(the group-form reductions or the k=6 pattern classification) — plausible, as this is a
fairly specific derived result not standard in textbooks.

## Minor fixes needed

1. Wrap the two scripts (or their logic) through `tools/cert.py` and place the search
   script at `problems/p4/cells/c6/cert/search.py` so `tools/rerun.py p4 c6` and
   `tools/gate.py p4 c6` can actually run against this work, per CLAUDE.md rule 4
   (non-negotiable). This is currently entirely missing — the cell has no certificate at
   all yet.
2. Move the one-sentence clarification that the classification is of shared-prime
   *patterns*, not literal n_i-tuples (currently only stated in "What remains open") up
   into the classification section itself, so a reader can't misread the 4-pattern table
   as "all possible tuples."
3. Cosmetic: the sub-lemma proof has a garbled clause "D_i∩D_j ⊆ D_i∩D_j can contain at
   most one prime" — fix the tautological subset reference (should just read "D_i∩D_j
   can contain at most one prime").

None of these touch the mathematical content, which I independently verified by hand and
by computation to be correct and complete as stated.

VERDICT: MINOR
