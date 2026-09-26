# Disjoint congruence classes
Number theory. If congruence classes are pairwise disjoint, must two of their moduli share a large common factor?

## Definitions
For integers a and m ≥ 1, a (mod m) = { a + mt : t ∈ ℤ }. A finite family a₁ (mod m₁), …, a_k (mod m_k) is **pairwise disjoint** if a_i (mod m_i) ∩ a_j (mod m_j) = ∅ whenever i < j. Nothing is assumed about the moduli beyond m_i ≥ 1: moduli may repeat, and residues may repeat as well.

By CRT:  a_i (mod m_i) ∩ a_j (mod m_j) ≠ ∅  ⟺  gcd(m_i, m_j) | a_i − a_j.   (∗)

## Question
Let k ≥ 2 and let a₁ (mod m₁), …, a_k (mod m_k) be pairwise disjoint. Must there be a pair i < j with gcd(m_i, m_j) ≥ k?

Believed true for every k. Sharp: the k classes 1, 2, …, k (mod k) are pairwise disjoint and every pairwise gcd equals k.

Examples: 0 (mod 2), 1 (mod 4), 3 (mod 8) are pairwise disjoint with gcds 2, 2, 4. By contrast 0 (mod 2) and 0 (mod 3) meet at 0.

## Trivial bounds (count for NOTHING if presented as progress)
1. gcd(m_i, m_j) = 1 ⇒ the classes meet. So in a disjoint family every pairwise gcd is ≥ 2; this settles k = 2, and a counterexample of size k has all pairwise gcds in [2, k−1].
2. Density: Σ 1/m_i ≤ 1, so some m_i ≥ k. This says nothing about any gcd; the two together settle no k ≥ 3. Every cell needs a genuinely new argument.

## Cells
| Cell | Title | Points |
|---|---|---|
| c1 | Three classes | 1 |
| c2 | Four classes | 2 |
| c3 | Every k up to 8 | 3 |
| c4 | Every k up to 12 | 5 |
| c5 | The certified boundary | 8 |
| c6 | Beyond the boundary — open question | 13 |

## Hand-in rules
- For each cell attempted, a written proof. A computer may be used to explore.
- A proof may rely on computation only if the code is included, runs in under ten minutes, and the computation is exhaustive over a finite set that **your own argument** has reduced the problem to.
- A computational cell is accepted only with an **exhaustiveness certificate**, all of:
  1. an exact description of the finite set enumerated, with the proof that nothing outside it can be a counterexample;
  2. every pruning rule, stated precisely, each with the proof that it discards only objects that cannot be completed to a counterexample;
  3. the node count at each size claimed, and the wall clock;
  4. a rerun that reproduces those counts;
  5. if anything survives pruning at a claimed size, a separate decision for every survivor (not a sample), with, for each one, the smallest part that already forces the decision and a proof that no smaller part does. An undecided survivor means the size is not certified.
- "I searched and found nothing" without 1–5 scores nothing. An unfinished size must be reported as unfinished and not claimed; a partial search is a legitimate partial result, with the counts reached.
- Where a cell asks to determine a boundary, state the exact value claimed. Claim only what is certified.
- Citing a published result for the statement asked does not count; a proof written out in full does. If you rely on a published argument you are responsible for checking it, and must report it if it does not hold up.

## Library
`lib/congruence.py`: `meet`, `disjoint`, `check_family` (exact, returns max gcd and density), `find_counterexample(k, M)` (exploratory bounded bitset search, NOT a certificate). Certificate template: `examples/cert_template_search.py`.
