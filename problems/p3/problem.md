# Bulgarian solitaire
Combinatorics and integer partitions. Repeatedly take one card from every pile and form a new pile. How many moves can it take before the piles start to cycle?

## Definitions
A partition of n is a weakly decreasing sequence λ = (λ₁,…,λ_s) of positive integers with λ₁+…+λ_s = n (n cards in s piles).

The shift B(λ) removes one card from every pile, discards piles that become empty, and adds one new pile of the s removed cards. Formally, B(λ) has parts: the positive numbers among λ₁−1,…,λ_s−1, together with one extra part equal to s.

λ is **cyclic** if B^i(λ) = λ for some i ≥ 1.

  d_B(λ) = min{ i ≥ 0 : B^i(λ) is cyclic },  D_B(n) = max{ d_B(λ) : λ a partition of n }.

T_k = k(k+1)/2, δ_k = (k, k−1, …, 1). Every n ≥ 1 satisfies T_{k−1} < n ≤ T_k for exactly one k, the **rank** of n.

Example: B(2,1,1,1,1) = (5,1); B(5,1) = (4,2); B(4,2) = (3,2,1); B(3,2,1) = (3,2,1). So d_B(2,1,1,1,1) = 3.

## Cells
| Cell | Title | Points |
|---|---|---|
| c1 | Cyclic partitions and cycles | 1 |
| c2 | D_B at triangular n | 2 |
| c3 | A general upper bound | 3 |
| c4 | One above a triangular number | 5 |
| c5 | Two above a triangular number | 8 |
| c6 | D_B(n) for every n — open question | 13 |

## Hand-in rules
- For each cell attempted, a written proof. A computer may be used to explore.
- A proof may rely on computation only if the code is included, runs in under 10 minutes, and the computation is **exhaustive over a finite set that your argument has reduced the problem to**.
- Where a cell asks to determine a quantity: give the exact value as a formula in k and prove both bounds; state any partitions used explicitly as functions of k.
- Say clearly which cells are solved and which are partial.
- Citing a published result for the statement asked does not count; a proof written out in full does, whatever its source.

## Library
`lib/bulgarian.py`: `B`, `partitions(n)`, `dB`, `analyse(n)` (all depths, cyclic set, cycles), `DB(n)` with maximisers, `table(nmax)`, `rank`, `T`, `staircase`. Run `python lib/bulgarian.py 40` for a table.
