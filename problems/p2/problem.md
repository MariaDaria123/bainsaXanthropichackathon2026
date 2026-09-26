# Uphill paths on the hypercube
Graph theory and combinatorics. Label the vertices of the hypercube to make as few uphill paths as possible. IMO 2022 settled the grid; the cube is still open.

## Definitions
Let G be a finite simple graph on n vertices. A labelling of G is a bijection f : V(G) → {1,…,n}. Fix a labelling.
- A vertex v is a **valley** if every neighbour w of v has f(w) > f(v). An isolated vertex counts as a valley.
- An **uphill path** is a sequence (v₁,…,v_k), k ≥ 1, where v₁ is a valley, v_i and v_{i+1} are adjacent for each i, and f(v₁) < f(v₂) < … < f(v_k). A valley on its own (k = 1) counts as an uphill path.

U(G) is the smallest possible number of uphill paths over all labellings of G.

IMO 2022 Problem 6 asks for U of the n×n grid graph; the answer is 2n² − 2n + 1.

This column asks about the d-dimensional hypercube Q_d: vertex set {0,1}^d, two vertices adjacent when they differ in exactly one coordinate. Q_d has 2^d vertices and d·2^{d−1} edges.

## Cells
| Cell | Title | Points |
|---|---|---|
| c1 | U(Q₃) and U(Q₄) | 1 |
| c2 | U(Q₅) | 2 |
| c3 | U(Q₆) | 3 |
| c4 | U(Q₇) and U(Q₈) | 5 |
| c5 | Bounds for U(Q₉) | 8 |
| c6 | U(Q₉) — open question | 13 |

## Hand-in rules
- **C1–C4:** the values, and for each value an explicit labelling attaining it, given as the list of the 2^d vertices in increasing label order, written as 0/1 strings. Marked correct on values alone, but a value with no labelling behind it will not survive later cells, which build on the construction.
- **C5:** either a labelling of Q₉ in the same format (its uphill paths are counted mechanically), or a proof of the lower bound.
- **C6:** all three of (1) the value; (2) an explicit labelling attaining it; (3) a proof that no labelling gives fewer uphill paths.
- A lower-bound proof may be computer-assisted: include the code, it must run in under 10 minutes on a laptop, and explain why the computation proves the bound.
- Say clearly which cells are solved and which are partial.

## Library
`lib/uphill.py`: `count_uphill(order,d)` (exact DP), `valleys`, `read_labelling`/`write_labelling` (submission format), `brute_force_U(d)` for d ≤ 3, `local_search(d)` (annealing, upper bounds only), `layer_order(d)`.
