# p4 c6 (a) — proof track p4-proof-9f5f3f: item 8 of O'Bryant's Lemma 6 beyond k = 30, case k−1 prime

**Status:** OPEN (partial progress). No size k is decided. The target (rule out k = 32, 38, 42, 44, 48 given all smaller sizes) is **not** reached.

Setting throughout (same as swarm/results/p4-literature-ce0fb3/result.md §3): k ≥ 5 is the least size with a counterexample, i.e. classes a_1 (mod m_1), …, a_k (mod m_k), pairwise disjoint, with every gcd(m_i, m_j) < k; among those of size k we take one with minimal Σ m_i. L_k = lcm(1, …, k−1). "Minimality of k" means: every pairwise disjoint family of t classes, 2 ≤ t < k, has a pair with gcd ≥ t. We use only these facts, each proved in full in p4-literature-ce0fb3 §3 (items 1–4), and re-derive what else we need:
- (F1) m_i ∣ L_k (item 1). (F2) 1 < gcd(m_i, m_j) < k for i ≠ j (item 2). (F3) no m_i is 1 or a prime power (item 4). (F4) at least three m's are multiples of k−1 (item 5).
These items are on the board as [CONJECTURED] (downgraded MINOR/MINOR), not as FACTS. Every claim below that uses them is therefore conditional on them; we flag this, and the proofs of F1–F4 are short enough to be re-checked from that file.

## Claim 1 [COMPUTED, conditional on F1–F3] — ω is injective for ℓ ≥ 4, but the pigeonhole step of item 8 fails

Recall item 8's argument for a prime p ≥ k/2 dividing exactly the moduli m_1..m_ℓ, ℓ ≥ 3: P_s = (primes of m_s) \ {p} are pairwise disjoint nonempty sets of primes < k, not containing p; for i > ℓ, ω_i = (min(P_1∩P_i), …, min(P_ℓ∩P_i)) is defined; ω_i = ω_j (i ≠ j) forces the product of ℓ distinct primes to divide gcd(m_i, m_j).

For ℓ ≥ 4 and k ≤ 210 that product is ≥ 2·3·5·7 = 210 ≥ k, so ω is **injective** [PROVED, conditional on F1–F3: F1 puts every prime of every m below k, so |⋃P_s| ≤ π(k−1) − 1; F2 gives gcd(m_s, m_t) = p (so the P_s are disjoint), makes ω_i defined (gcd(m_s, m_i) > 1 and p ∤ m_i), and supplies the bound gcd < k that the collision contradicts; F3 gives P_s ≠ ∅. This is step (iv) of item 8 with 210 in place of 30]. So the task's sentence "an ω-collision gives gcd ≥ 210 when ℓ ≥ 4" is true. What fails is its implied conclusion: injectivity does not by itself exclude ℓ ≥ 4. But injectivity only gives k − ℓ ≤ ∏|P_s| ≤ maxprod(π(k−1)−1, ℓ). The script `table.py` (exact integers, exhaustive over partitions, ~1 s) shows this inequality **does not** give a contradiction for the following (k, ℓ):

| k | π(k−1) | ℓ not excluded by counting (ℓ: maxprod vs k−ℓ) |
|---|---|---|
| 32 | 11 | 3: 36≥29; 4: 36≥28; 5: 32≥27 |
| 38 | 12 | 3: 48≥35; 4: 54≥34; 5: 48≥33; 6: 32≥32 |
| 42 | 13 | 3: 64≥39; 4: 81≥38; 5: 72≥37; 6: 64≥36 |
| 44 | 14 | 3: 80≥41; 4: 108≥40; 5: 108≥39; 6: 96≥38; 7: 64≥37 |
| 48 | 15 | 3: 100≥45; 4: 144≥44; 5: 162≥43; 6: 144≥42; 7: 128≥41; 8: 64≥40 |

For ℓ = 3 the counting test **does not apply at all**: injectivity is not proved there (2·3·5 = 30 < k), so collisions are allowed. The ℓ = 3 entries are listed only to show that the test fails for ℓ = 3 even if injectivity were assumed. For ℓ ≥ 4, every ℓ not listed is excluded by the counting test (either k − ℓ > maxprod, or ℓ > π(k−1) − 1 so that ℓ disjoint nonempty P_s cannot exist). So a proof for k − 1 prime, 31 < k ≤ 48, must handle ℓ = 3 **and** the listed ℓ ≥ 4. Injectivity of ω plus counting handles none of them. (The counting only uses Σ|P_s| ≤ π(k−1) − 1; a surviving row is not a configuration, only a failure of this argument.)

## Claim 2 [PROVED, conditional on F1–F3] — structure of the multiples of p = k−1

Let k ≥ 5 with p = k−1 prime, and let m_1, …, m_ℓ be exactly the moduli divisible by p. Then:
(a) v_p(m_s) = 1 for s ≤ ℓ; (b) gcd(m_s, m_t) = p for s ≠ t ≤ ℓ; (c) m_s = p·u_s with u_s ≥ 2, p ∤ u_s, and gcd(u_s, u_t) = 1 for s ≠ t; (d) the residues a_1, …, a_ℓ are pairwise distinct mod p, hence ℓ ≤ p.

*Proof.* (a) Every integer in {1, …, k−1} = {1, …, p} has p-adic valuation ≤ 1, because p² > p. So v_p(L_k) = 1, and by F1 v_p(m_s) ≤ 1; since p ∣ m_s, v_p(m_s) = 1.
(b) p divides gcd(m_s, m_t), and by F2 gcd(m_s, m_t) < k = p + 1. The only multiple of p in [p, p] is p. So gcd = p.
(c) Put u_s = m_s / p, an integer. By (a), p ∤ u_s. If u_s = 1 then m_s = p is a prime power, contradicting F3; so u_s ≥ 2. For s ≠ t, gcd(m_s, m_t) = gcd(p u_s, p u_t) = p·gcd(u_s, u_t), which is p by (b); so gcd(u_s, u_t) = 1.
(d) The classes s, t are disjoint, so by (∗) gcd(m_s, m_t) = p does not divide a_s − a_t. So a_s ≢ a_t (mod p). There are only p residues mod p, so ℓ ≤ p. ∎

## Claim 3 [PROVED, conditional on F1–F3] — fiber reduction

Same setting as Claim 2; R = {i : i > ℓ} (moduli not divisible by p). Fix s ≤ ℓ. For each i ∈ R choose b_i with p·b_i ≡ a_i − a_s (mod m_i) (possible since p ∤ m_i and p is prime, so gcd(p, m_i) = 1). Then the k − ℓ + 1 classes
  0 (mod u_s),   b_i (mod m_i) for i ∈ R
are pairwise disjoint, and gcd(u_s, m_i) = gcd(m_s, m_i) for i ∈ R (all other gcds are unchanged).

*Proof.* Let φ(t) = a_s + p t. For i ∈ R: φ(t) ≡ a_i (mod m_i) ⟺ p t ≡ a_i − a_s (mod m_i) ⟺ t ≡ b_i (mod m_i), multiplying by the inverse of p mod m_i. So φ^{-1}(a_i mod m_i) = b_i mod m_i. Next, φ(t) ≡ a_s (mod p u_s) ⟺ p t ≡ 0 (mod p u_s) ⟺ u_s ∣ t. So φ^{-1}(a_s mod m_s) = 0 mod u_s. Preimages of pairwise disjoint sets under a map are pairwise disjoint. Finally gcd(p u_s, m_i) = gcd(u_s, m_i) because p ∤ m_i (a common divisor d of p u_s and m_i is coprime to p, since p ∤ m_i and p is prime, so d ∣ u_s). ∎
Consequence [PROVED, conditional on F1–F3]: Σ_{i∈R} 1/m_i + 1/u_s ≤ 1 for every s ≤ ℓ (trivial density bound 2 of problem.md applied to this disjoint family). This is recorded as a tool; it does not by itself finish anything.
Remark [PROVED, conditional on F1–F3 and minimality of k] (suggested by a critic). The reduced family has size k − ℓ + 1, and k − ℓ + 1 < k because ℓ ≥ 2. If k − ℓ + 1 ≥ 2, minimality of k gives a pair in it with gcd ≥ k − ℓ + 1. Its gcds equal those among {m_s} ∪ {m_i : i ∈ R}. So some pair in {s} ∪ R has gcd(m, m') ≥ k − ℓ + 1. This is the same statement as Claim 4(a) with t = k − ℓ + 1 applied to the index set {s} ∪ R, so the fiber gives nothing new here. It would give something new only if the fiber were iterated or combined with the u_s-structure.

## Claim 4 [PROVED, uses only minimality of k and F2] — high gcd graphs are linear unions of cliques

For 2 ≤ t ≤ k−1 let G_t be the graph on {1..k} with an edge ij iff gcd(m_i, m_j) ≥ t.
(a) (deletion lemma, generalising items 5 and 6) Every set of t indices spans an edge of G_t; equivalently the vertex cover number τ(G_t) ≥ k − t + 1.
(b) If t > (k−1)/2, then G_t is the union of the cliques on D_g = {i : g ∣ m_i}, g = t, …, k−1, and |D_g ∩ D_h| ≤ 1 for g ≠ h in [t, k−1].

*Proof.* (a) Any t of the classes form a pairwise disjoint family of size t with 2 ≤ t < k; by minimality of k it has a pair with gcd ≥ t, i.e. an edge of G_t. For the equivalent form: let C be a vertex cover (every edge has an endpoint in C). The complement of C spans no edge, so by the first sentence it has at most t − 1 vertices; hence |C| ≥ k − (t − 1) = k − t + 1.
(b) If ij is an edge, g := gcd(m_i, m_j) satisfies t ≤ g ≤ k−1 (upper bound by F2), and g ∣ m_i, g ∣ m_j, so i, j ∈ D_g. Conversely i ≠ j both in D_g gives g ∣ gcd(m_i, m_j), so gcd ≥ g ≥ t. So the edge set of G_t is exactly the union of the edge sets of the cliques on the D_g, t ≤ g ≤ k−1. Now let t ≤ g < h ≤ k−1 and suppose i ≠ j both lie in D_g ∩ D_h. Then g and h both divide gcd(m_i, m_j), so lcm(g, h) ∣ gcd(m_i, m_j), and gcd(m_i, m_j) ≤ k−1 by F2. Two cases. If g ∣ h, then h is a multiple of g other than g, so h ≥ 2g ≥ 2t > k−1, contradicting h ≤ k−1. If g ∤ h, then lcm(g, h) is a multiple of h different from h, so lcm(g, h) ≥ 2h > 2t > k−1, contradicting lcm(g, h) ≤ gcd(m_i, m_j) ≤ k−1. So |D_g ∩ D_h| ≤ 1. ∎
Special cases recovered: t = k−1: G_{k−1} is the clique on D_{k−1}, whose vertex cover number is |D_{k−1}| − 1 (or 0 if |D_{k−1}| ≤ 1); (a) requires ≥ 2, so |D_{k−1}| ≥ 3 (item 5). t = k−2 with |D_{k−1}| = 3: if |D_{k−2}| ≤ 1 then G_{k−2} is just the triangle on D_{k−1} (a one-element D_{k−2} gives no edge), whose vertex cover number is 2 < 3 = k − (k−2) + 1, contradicting (a). So |D_{k−2}| ≥ 2. By (b) at most one element of D_{k−2} lies in D_{k−1}, so at least one further modulus outside D_{k−1} is a multiple of k−2. (Item 6 claims two; the extra step is the one in p4-literature-ce0fb3 item 6, using that deleting two of the three multiples of k−1 in two different ways must each leave a pair with gcd k−2.) Claim 4(b) needs k − 2 > (k−1)/2, i.e. k ≥ 4.

## What remains open
- The target: for k ∈ {32, 38, 42, 44, 48}, rule out ℓ = 3 and the ℓ ≥ 4 values listed in Claim 1. Neither the ω-count nor Claims 2–4 finish it. A natural next lemma: combine Claim 4(b) for t ≈ k/2 (the D_g, g ∈ [t, k−1], form a linear hypergraph whose union must have vertex cover ≥ k − t + 1) with Claim 2(c) (u_s pairwise coprime) and the rule "a large prime q ≥ k/2 dividing ≥ 3 moduli carries its own P-structure", as in the k = 30 repair.
- Everything is conditional on sizes < k, which for k ≥ 21 are themselves not settled.

## Cited vs ours
- Cited: items 1–5 of O'Bryant's Lemma 6 (arXiv math/0604347) as audited in swarm/results/p4-literature-ce0fb3/result.md; the ω-map of item 8 is O'Bryant's.
- Ours: Claim 1 (the counting table for k − 1 prime, 31 < k ≤ 48, showing that the pigeonhole of item 8 fails for several ℓ ≥ 4 even though ω is injective there, and that for ℓ = 3 the test does not apply); Claims 2, 3 (structure and fiber reduction for p = k − 1); Claim 4 (deletion lemma in vertex-cover form and the linear-clique structure of G_t for t > (k−1)/2, which contains items 5, 6 as special cases).

**Verification:** `python3 swarm/results/p4-proof-9f5f3f/table.py` — exact integer arithmetic, exhaustive recursion over all partitions for maxprod; about 1 s wall clock (measured 1.3 s). It also asserts that {32, 38, 42, 44, 48} are exactly the k in [31, 48] with k − 1 prime. The script is not wrapped in tools/cert.py / tools/rerun.py (repo rule 4). It supports no positive proof step: it only shows that an argument fails, and Claim 1 is labelled [COMPUTED] for that reason. Wrapping it is left to the certificate track.
