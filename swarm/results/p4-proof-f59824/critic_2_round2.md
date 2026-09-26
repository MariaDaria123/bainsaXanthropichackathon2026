# Critic #2 report — p4-proof-f59824

Scope: judged only `swarm/results/p4-proof-f59824/result.md`, `problems/p4/cells/c6/cell.md`, and the
scripts it cites (`scripts/enumerate_patterns.py`, `scripts/check_scaling.py`, `scripts/cert_search.py`,
`scripts/certificate.json`), all of which I ran myself. `notes.md`, `swarm/board/`, other results and
logs were not consulted.

## 1. Statement check

Task goal has four parts: (i) WLOG G finite, (ii) coprime indices ⇒ cosets meet ⇒ pairwise gcd ≥ 2,
(iii) Σ1/n_i ≤ 1, and (iv) enumerate the index 6-tuples an actual k=6 counterexample could have.

- **Lemma 1** states (i) with full quantifiers (N = ∩ cores, Ḡ = G/N finite, indices and disjointness
  both preserved exactly). Matches the target, no silent weakening.
- **Lemma 2** states (ii) as "for every x,y the cosets meet" when gcd(n_i,n_j)=1, hence gcd ≥ 2 in any
  disjoint family — correct generality, no hidden extra hypothesis.
- **Lemma 3** states (iii) exactly as in `problems/p4/problem.md`'s trivial-bounds section, reproved
  from scratch rather than merely cited (satisfies CLAUDE.md rule 2).
- The **enumeration** part is where the statement gets shaky (see §2/§4 below): the write-up explicitly
  (and honestly) flags that literal "all index 6-tuples" is an infinite set, and substitutes a coarser
  finite invariant. That substitution is disclosed up front, not silent — but the surrounding language
  ("lossless", "the finite invariant that actually controls the pairwise-gcd constraints") claims more
  than what is proved.

## 2. Every step — gaps found

**Lemmas 1–3:** I checked every line. All are complete, self-contained, and correct:
- Lemma 1(a): Core_i = ker(φ_i: G → Sym(G/G_i)) is verified by the stated four-way iff chain; N normal
  of finite index follows from the embedding G/N ↪ ∏ G/Core_i via ρ, kernel computed correctly as ∩Core_i.
- Lemma 1(b): the bijection ψ: G/G_i → Ḡ/Ḡ_i is checked well-defined/injective/surjective using N⊆G_i
  and G_iN=G_i; no missing case.
- Lemma 1(c): both directions of the transfer are given with explicit coset representatives.
- Lemma 2: reduces to a finite pair via Lemma 1, then proves [H:A∩B]=n_i n_j exactly (divisibility one
  way from the tower law + coprimality, ≤ the other way from an explicit injection A/C ↪ H/B), then
  |AB|=|H| by the fiber-counting argument for the product map A×B→H, then AB=H ⇒ cosets always meet.
  Every step is spelled out; the "standard" facts used (kernel-of-action-is-core, |AB| formula) are
  reproved in full as claimed in "Cited vs ours," not cited as black boxes.
- Lemma 3: a one-line finite counting argument, correct.

No instance of "clearly / obviously / routine / similarly / WLOG-without-argument" was found — every
`WLOG` in the text points to a fully proved reduction (Lemma 1).

**The classification section — the one real problem.** The Sub-lemma itself is stated and proved
correctly, and *only* in one direction: "if gcd(n_i,n_j)∈{2,3,4,5} for all pairs, then D_i≠∅ and
|D_i∩D_j|=1." That is a genuine necessary condition and the proof of it is fine.

But the prose around it overclaims. Line ~134: "this reduction is lossless for the gcd constraints,"
and line ~133: D_i "is the finite invariant that actually controls the pairwise-gcd constraints." Read
literally, this asserts D_i determines (or is equivalent to) the gcd-range condition. It does not: D_i
only records *which* primes ≤5 divide n_i, not their exponents, and the exponent of the shared prime is
exactly what decides whether gcd(n_i,n_j) stays ≤5. I tested this directly:

```
D1=D2={2} pattern, but n1=16,n2=32: gcd = 16  -- in {2,3,4,5}? False
```

Two indices with the *same* admissible D-pattern (both divisible by 2 only, among {2,3,5}) can still
violate the counterexample's own requirement gcd≤5 once the shared prime's valuation is large enough.
So the D-pattern is a necessary projection of the real constraint, not an equivalent ("lossless") one.
The complete necessary condition for "enumerate all index 6-tuples a counterexample could have" would
also need, per shared prime p and pair (i,j) with p ∈ D_i∩D_j: min(v_p(n_i), v_p(n_j)) capped so that
p^min ≤ 5 (i.e. for p=2 the cap is 4, so min(v_2)∈{1,2}; for p=3,5 the cap is p itself, so
min(v_p)=1 exactly). This refinement is simply missing from the classification — the write-up only
delivers the coarser prime-support layer of the full necessary-condition set.

This is a *local* problem, not a structural one: the same document's own closing section ("What
remains open") correctly walks the claim back to "necessary numeric conditions" and does not claim
equivalence there. The overclaim lives only in the scope-note prose (result.md) and is echoed verbatim
in `cert_search.py`'s `domain_proof` string ("this is the *only* information about n_i that the
pairwise-gcd constraints can see") — which is the same false-as-stated claim, though it does not affect
the certificate's actual validity (see §4).

**Fix needed:** reword "lossless" / "controls the pairwise-gcd constraints" / "only information ... can
see" to "necessary" throughout, and either (a) add the exponent-cap condition above to make the
enumeration answer the literal task ("all tuples a counterexample could have") more completely, or (b)
explicitly state that only the prime-support layer was classified and the exponent layer is left open,
rather than implying completeness.

## 3. Testable lemmas — verified by computation

- `enumerate_patterns.py` re-run: `tuples checked: 117649`, `valid tuples: 147`,
  `distinct patterns up to S_6 x S_3: 4` — matches the write-up exactly (0.078 s).
- `check_scaling.py` re-run: all four sample witnesses print gcds all `= 2` (within {2,3,4,5}) and
  `sum 1/n_i ≤ 1` via exact `Fraction`, all asserts pass.
- Hand cross-check (three distinct doubletons {2,3},{2,5},{3,5} admit no valid 4th entry; a full triple
  {2,3,5} forces the rest to a common singleton) reproduces the same 4 patterns independently — no
  discrepancy found with the brute-force search.

No failing test was found for the labelled lemmas themselves; the only substantive issue is the
overclaim described in §2.

## 4. Cited code / certificate

Ran all three scripts myself:
- `enumerate_patterns.py`: exact (`frozenset`/`int` only), deterministic, exhaustive by construction
  over 7^6, 0.08 s.
- `check_scaling.py`: exact `Fraction` + `math.gcd`, < 0.1 s.
- `cert_search.py` + `tools/cert.py`: wraps the same enumeration through the Certificate object.
  Re-ran and reproduced `certified_sizes: [6]`, `nodes: {"6": 117649}`, 147 valid / 4 survivors, each
  survivor carries a decision, `minimal_part`, and `minimality_proof` (n_undecided = 0). No pruning
  rules are claimed (`"rules": []`), which is consistent with this being a plain brute force rather than
  a pruned search — nothing to falsely certify there. This satisfies the 5-part certificate template
  *for the domain it actually claims* (D-tuples, not literal n-tuples) — domain+proof, no rules needed,
  node counts, reproducible rerun, every survivor decided.

The write-up is upfront that this certificate lives under `swarm/results/...` rather than
`problems/p4/cells/c6/cert/search.py`, so `tools/rerun.py p4 c6` / `tools/gate.py p4 c6` cannot run
against it yet — flagged as an explicit outstanding step, not concealed. That is an honest disclosure,
not a violation, but it does mean this cell cannot be gated as-is.

## 5. Labels

- Lemma 1, 2, 3 [PROVED]: labels are earned — complete proofs, no computation involved.
- Sub-lemma [PROVED]: the statement as literally written (necessity only) is earned; the label is fine,
  the problem is the un-labelled prose around it overselling what the label covers (see §2).
- Enumeration / realizability [COMPUTED]: labels are earned — both scripts are exact, exhaustive over
  their stated (finite) domains, deterministic, and fast; nothing here is presented as [PROVED] that
  should be [COMPUTED] or vice versa.
- Nothing in this document presents a conjecture or exploratory search as proved; the "What remains
  open" section is honest about the unresolved realizability question.

## 6. Literature

"Cited vs ours" section correctly separates classical facts (kernel-of-coset-action, |AB| formula) —
both are reproved in full above rather than invoked as black boxes, satisfying rule 2. No published
result for the group-form reductions or the k=6 pattern classification is cited as a substitute for
proof; this task's specific content is original as claimed.

## Summary

The three basic reductions (i), (ii), (iii) — the primary content of this task — are proved completely
and correctly, with no gaps, no banned unproved transitions, and correct scope/quantifiers. The
enumeration part is computationally verified and honestly scoped as a necessary-condition classification,
but the prose claims (in result.md's scope note and in cert_search.py's domain_proof) overstate this as
"lossless"/"the invariant that controls" the gcd constraints, which is false as literally written (shown
by direct counterexample) and omits the exponent-level refinement that a fully faithful enumeration of
"all tuples a counterexample could have" would need. This is a precise, local wording/completeness fix,
not a flaw in the underlying method or in Lemmas 1–3.

VERDICT: MINOR
