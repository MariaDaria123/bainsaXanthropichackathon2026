# Angles between lines
Discrete geometry. How large can the sum of pairwise angles between N lines through the origin be? Fejes Tóth conjectured in 1959 that orthogonal lines win.

## Definitions
A line always means a line through the origin of ℝ^d. The angle between two lines ℓ, ℓ′ is the acute (non-obtuse) angle θ(ℓ,ℓ′) ∈ [0, π/2]. If ℓ, ℓ′ are spanned by unit vectors x, x′, then

  θ(ℓ,ℓ′) = arccos |⟨x,x′⟩|.

For lines ℓ₁,…,ℓ_N in ℝ^d (repetitions allowed):

  S(ℓ₁,…,ℓ_N) = Σ_{1≤i<j≤N} θ(ℓ_i,ℓ_j).

## Conjecture (Fejes Tóth, 1959)
S is maximised by taking d mutually orthogonal lines, each used either ⌊N/d⌋ or ⌈N/d⌉ times. When N = d + k with 0 ≤ k ≤ d, this configuration (the d coordinate axes, k of them used twice) has

  S = ( C(N,2) − k ) · π/2,

because exactly k pairs of lines coincide and every other pair is orthogonal.

## Cells (each asks for this bound or a special case)
| Cell | Title | Points |
|---|---|---|
| c1 | Lines in the plane | 1 |
| c2 | An orthogonality lemma | 2 |
| c3 | d + 1 lines in ℝ^d | 3 |
| c4 | Five lines in ℝ³, six in ℝ⁴ | 5 |
| c5 | d + 2 lines in ℝ^d | 8 |
| c6 | N lines in ℝ^d — open question | 13 |

## Hand-in rules
- Unless a cell says otherwise, a complete proof is required. **Citing a published result for the statement you are asked to prove does not count.**
- For each cell attempted, hand in a written proof. A computer may be used to explore.
- A proof may rely on a computation only if the code is included, runs in under 10 minutes on a laptop, and is rigorous: exact or interval arithmetic, or an argument that bounds the numerical error.
- Say clearly which cells are solved and which are partial.

## Library
`lib/angles.py`: `S`, `S_enclosure` (rigorous, rational input), `fejes_toth_value(N,d)` (S in units of π/2), `maximize(N,d)` (numeric exploration only).
