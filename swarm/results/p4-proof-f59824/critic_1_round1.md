# Blind critic #1 — p4-proof-f59824

Scope respected: judged only `swarm/results/p4-proof-f59824/result.md`, `problems/p4/cells/c6/cell.md`,
and the two cited scripts under `swarm/results/p4-proof-f59824/scripts/`. Did not read `notes.md`,
`swarm/board/`, other results, or logs.

## 1. Statement check

The "Target (restated exactly)" section matches `cell.md` part (c) verbatim in substance (group G,
finite-index subgroups G_1..G_k, pairwise disjoint cosets, question about gcd(n_i,n_j) ≥ k, known ≤5,
open ≥6). The "This task's goal" section matches the assigned sub-task (reductions (i)-(iii) plus the
k=6 numeric enumeration) with no silent narrowing of what's being claimed.

One real defect: the file's `Status:` line reads **`OPEN (partial progress — ...)`**. CLAUDE.md rule 1
is explicit: "Status is `SOLVED` or `PARTIAL`, nothing in between," and the repo's own gate
(`tools/gate.py:39`) only accepts `## Status:\s*(SOLVED|PARTIAL)`. "OPEN" is neither. The content
described (proved reductions + necessary-condition classification, realizability left open) is exactly
what "PARTIAL" means here — this is a wording fix, not a content fix, but it must be made before this
can pass the gate.

No claim silently weakens the cell or smuggles in an extra hypothesis: Lemma 1 is stated for a general
group G and general k; Lemma 2 and Lemma 3 are stated with full quantifiers ("for every choice of
x,y ∈ G", "for a pairwise disjoint family"); the k=6 classification is explicitly scoped as a
*necessary condition on the shared-prime structure*, not a claim to have enumerated literal integer
tuples (which is impossible — the tuples form an infinite family, as the write-up's own
`check_scaling.py` demonstrates by scaling with arbitrary coprime cofactors). This scope is honestly
disclosed in "What remains open," though it would be better disclosed *at the start* of the
classification section rather than only at the end (see §2).

## 2. Step-by-step check

**Lemma 1 (reduction to finite quotient).** Standard but correctly and fully proved from scratch:
Core_i = ker(action on G/G_i) is normal with [G:Core_i] | n_i! (checked directly, not asserted);
N = ∩Core_i is normal of finite index via the embedding G/N ↪ ∏ G/Core_i; N ⊆ G_i is checked; the
bijection G/G_i ↔ Ḡ/Ḡ_i and the double-coset-meet equivalence (part c) are proved in both directions
with no hand-waving. No banned words used without the argument attached (the two "WLOG"s in the file
each point at a specific, already-proved lemma, not a bare assertion).

**Lemma 2 (coprime ⟹ meet).** Reduces to the finite case via Lemma 1 applied to just the pair
{G_i,G_j}. Step 1 ([H:A∩B]=n_i n_j exactly) uses the tower law plus an explicit injective map
A/C → H/B — both directions of the inequality are proved, not assumed. Step 2 (|AB|=|H|, hence AB=H)
is proved by an explicit fiber-counting argument, not cited as the "product formula" black box (matches
CLAUDE.md rule 2). Step 3 correctly concludes xA∩yB≠∅ for all x,y from AB=H.

I independently stress-tested this lemma outside the cited scripts, on a genuinely non-abelian example
where G_i is *not* normal (S_3, A = ⟨(01)⟩ index 3, B = ⟨(012)⟩ index 2, gcd(3,2)=1): brute force over
all 6×6 coset pairs confirms every pair meets. This is consistent with, and a good independent check of,
Lemma 2's claim that non-normality doesn't matter.

**Lemma 3 (density bound).** Standard finite counting argument (|x_iG_i| = |G|/n_i via Lagrange, disjoint
subsets of a finite set), correctly reduced to the finite case via Lemma 1. No gap.

**Sub-lemma (shared-prime pattern).** Correct: values in {2,3,4,5} are each a prime power of a single
prime ≤5, and no prime ≥7 can divide a gcd ≤5, so D_i∩D_j (primes ≤5 dividing both n_i,n_j) has exactly
one element for every pair once gcd(n_i,n_j) ≥2 (Lemma 2) and ≤5 (counterexample hypothesis) are both
in force. The proof of part (a) is written as a proof-by-contradiction that is logically redundant
(once you already have |D_i∩D_j|=1 for the 15 pairs directly from the gcd values, nonemptiness of D_i
follows immediately, no separate contradiction argument is needed) — this is a style nit, not an error.

**Enumeration script (`enumerate_patterns.py`).** I reran it: `117649` tuples checked (=7^6, exactly
matching the claimed domain of functions {1..6}→{7 nonempty subsets of {2,3,5}}), `147` valid, `4`
canonical patterns under S_6×S_3 — identical to the numbers and the four listed patterns in the report.
Exact (frozenset/int only), deterministic, 0.08s. I hand-verified the combinatorial cross-check in the
write-up (3+6+3+3=15 labelled variants before the S_3 quotient) directly against the definition of
"valid" and confirmed it is arithmetically correct, and separately verified by hand why three distinct
doubletons {2,3},{2,5},{3,5} cannot be extended to a 6th slot (no singleton or triple satisfies all
three pairwise-intersection-size-1 constraints simultaneously) — matches the script's exclusion of that
case.

**Realizability script (`check_scaling.py`).** I reran it: for all 4 patterns, exact `Fraction` sums are
all comfortably < 1, and `math.gcd` confirms every one of the 15 pairwise gcds is exactly 2, for every
pattern, matching the printed output verbatim. This is exact and correctly demonstrates the density
bound never rules out any of the 4 patterns.

## 3. Testable-lemma checks (python)

- Reran both cited scripts verbatim — outputs match the write-up exactly (counts, patterns, gcds, sums).
- Independently coded a fresh, non-cited test of Lemma 2 on S_3 with a non-normal order-2 subgroup — all
  6×6 coset pairs meet, consistent with the claim.
- No failing check found; no counterexample to any stated lemma.

## 4. Cited-code / certificate audit

Both scripts are exact (int/frozenset or `Fraction`+`math.gcd`, no floats), deterministic, and finish in
well under 10 minutes (≈0.03–0.1s each, confirmed by timing my own reruns). Checking the 5-part
certificate the checklist asks for on p4 searches:
1. Domain + reduction proof: present (domain = 7 nonempty subsets of {2,3,5} per index, justified by the
   sub-lemma).
2. Pruning rule(s) proved: the sole filter (`|D_i∩D_j|=1`) is exactly the proved sub-lemma; there is no
   other pruning, which is fine for a direct 7^6 brute force.
3. Node counts + wall clock: present and reproduced exactly on rerun.
4. Reproducible rerun: reproduced by literally rerunning the script (identical output), but note this
   does **not** go through this repo's mandated `tools/cert.py` / `tools/rerun.py` machinery (no
   `cert/search.py`, no `cert/certificate.json`, no `python tools/rerun.py p4 c6`), which CLAUDE.md rule
   4 requires for any proof step relying on code. Per the repo README, swarm findings are raw material
   that get ported into `problems/p4/cells/c6/cert/search.py` and run through
   `orchestrate.py p4 c6 --from prove` at promotion time — so this is not fatal at the swarm-finding
   stage, but it is a required step before this result can pass `tools/gate.py p4 c6`, and should be
   listed explicitly as outstanding work in the write-up rather than left implicit.
5. Every survivor decided: yes — all 147 valid D-tuples are classified into exactly one of the 4 listed
   patterns, not a sample.

## 5. Labels

All strong claims are labelled and the labels are earned: Lemmas 1–3 are `[PROVED]` with complete,
checkable proofs (not citations); the enumeration and scaling constructions are `[COMPUTED]` with
runnable, exhaustive, exact scripts; nothing conjectural is presented as proved. The one label problem
is cosmetic: the section header "Classification of the numeric candidates for k = 6 [PROVED / COMPUTED]"
mixes two labels on one heading — the sub-claims underneath are each correctly and separately labelled,
so this is just an untidy top-level heading, not a mislabelled claim.

## 6. Literature

"Cited vs ours" is present and accurate: the two classical facts used (core = kernel of the coset
action with index dividing n!, and |AB|=|A||B|/|A∩B|) are named as classical but are *reproved in full*
in the body rather than invoked as black boxes, satisfying CLAUDE.md rule 2. Everything else is claimed,
correctly, as original to this task, and I found no published-result-as-black-box move anywhere in the
document for the actual statement asked.

## Required fixes (local, non-fatal)

1. Change `Status: OPEN (...)` to `Status: PARTIAL (...)` — required by CLAUDE.md rule 1 and by
   `tools/gate.py`'s regex.
2. Before promotion/gating: port `scripts/enumerate_patterns.py` (and, if desired, `check_scaling.py`)
   into `problems/p4/cells/c6/cert/search.py` using `tools/cert.py`'s `Certificate` object so
   `python tools/rerun.py p4 c6` can mechanically verify the counts, per CLAUDE.md rule 4.
3. Split the "[PROVED / COMPUTED]" section heading into its already correctly-labelled sub-parts only
   (cosmetic).
4. State up front (not only in "What remains open") that "enumerate all index 6-tuples" is answered by
   classifying the shared-prime pattern up to relabelling/reordering, because the literal set of integer
   tuples is infinite (as the scaling construction itself shows) — this is already true and disclosed,
   just should be foregrounded for a reader who hasn't reached the end.

None of these touch the correctness of the mathematics: Lemmas 1–3 are fully and correctly proved from
first principles, the k=6 classification is a valid necessary condition correctly derived and
exhaustively verified by a script I independently reran and cross-checked by hand, and the "what remains
open" framing (realizability by an actual group is not settled) is accurate and honestly stated.

VERDICT: MINOR
