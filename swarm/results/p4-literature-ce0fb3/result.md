# p4 c6 — literature track p4-literature-ce0fb3: certified boundary and the structure of a minimal counterexample

**Status:** OPEN (partial progress). This is a literature audit. It decides no new size k.

## 0. Sources (all fetched in this session)
- [OB] K. O'Bryant, *On Z.-W. Sun's disjoint congruence classes conjecture*, arXiv math/0604347. The TeX source was fetched from https://arxiv.org/e-print/math/0604347 and is saved as `obryant.tex` in this directory. Abstract page: https://arxiv.org/abs/math/0604347 . Numbering in the source (all environments share one counter): Conjecture 1 (DCCC), Proposition 2 (criterion (∗)), Theorem 3, Conjecture 4 (group form), **Lemma 5** (density test), **Lemma 6** (structure of a minimal counterexample, items 1–8).
- [FS] J. Fornal, Y.-C. Sun, *On the problem of large gcd for disjoint residue classes*, arXiv 2607.24655 (27 July 2026). Pages fetched: https://arxiv.org/abs/2607.24655 and the TeX source https://arxiv.org/e-print/2607.24655 . It proves max gcd ≫ k·exp(−(2+o(1))√(log k / log log k)). Its introduction says: "O'Bryant proved the integer conjecture for k≤20. Zhu proved the group-theoretic conjecture for k=3,4. Sun proved the cases k=2 and the case in which G is a finite p-group."
- [Zhu] W.-J. Zhu, *On Sun's conjecture concerning disjoint cosets*, arXiv 0807.2207, https://arxiv.org/abs/0807.2207 . Abstract: proves the group form for k = 3, 4.

## 1. Current boundary

**Claim 1.1** [OBSERVED]: In the sources fetched, the largest published range for the integer statement is still O'Bryant's k ≤ 20. [FS] (July 2026) cites nothing beyond it. Our cell c5 has no result on disk yet: `problems/p4/cells/c5/` holds only a placeholder. So the boundary this repo has certified cannot be read off.

**Claim 1.2** [GAP / literature-computation, not a certificate]: O'Bryant's proof for k ≤ 19 (Section 4.4) is a Mathematica search, `Grow`. The source says it "required slightly less than a week", and it reports no node counts. Under our hand-in rules it is **not** a certificate: it runs longer than 10 minutes, lacks parts 3–5 of the certificate, and we have not rerun it. Only these parts of O'Bryant's k ≤ 20 are fully written proofs: 3 ≤ k ≤ 6 (Section 4.1, audited in §3a below), 6 ≤ k ≤ 10 (Section 4.2, whose heading is "6 ≤ k ≤ 10"; hand casework, not audited here) and k ∈ {8,12,14,18,20} (Section 4.3, audited below).

**Claim 1.3** [PROVED, given Lemma 6 as repaired below]: Let k ∈ {8,12,14,18,20,24,30}. If the DCCC holds for every size < k, then it holds for size k. For k = 24 and k = 30 this is **conditional**: it needs all sizes up to 23 (resp. 29) first, and 21, 22, 23 are not settled in [OB]. So O'Bryant does **not** decide 24 or 30 outright.
*Proof.* Let p = k−1. Then p ∈ {7,11,13,17,19,23,29}, which is prime (checked in `verify.py`). Also p ≥ k/2, and 7 ≤ k ≤ 30. Take a counterexample of minimal size k and, among those, one with minimal Σm_i. Item 5 says at least three m's are multiples of p. Item 8 says that a prime ≥ k/2 dividing some m divides exactly two m's. These contradict each other. ∎

**Claim 1.4** [OBSERVED]: The cell statement says the group form is "known for k ≤ 5". The fetched sources only support k ≤ 4 ([Zhu]; [FS] repeats "k=3,4"). We found no fetched source for k = 5.

## 2. Line-by-line audit of Lemma 5 (density test)

**Lemma 5** [PROVED]. Let a_1 (mod m_1), …, a_ℓ (mod m_ℓ) be integer classes. Let M be any common multiple of all gcd(m_i, m_j), i<j. If Σ_{i≤ℓ} 1/gcd(m_i, M) > 1, then two of the classes meet.
*Proof (written out; the source's statement has a typo, "1≤i≤k" should read "1≤i≤ℓ").* Write g_i = gcd(m_i, M). Modulo M, the set a_i + m_iℤ reduces to the coset a_i + g_iℤ/Mℤ, because m_iℤ + Mℤ = g_iℤ. That coset contains exactly M/g_i residues mod M, and they are distinct. The hypothesis says Σ M/g_i > M. By pigeonhole, some residue r mod M lies in two of these cosets. Those two cosets must belong to **different** indices i ≠ j, because each single coset lists distinct residues. The source leaves this point implicit. So a_i + αm_i = a_j + βm_j + γM for some integers α, β, γ. Since gcd(m_i, m_j) divides M, Bézout gives integers δ, ε with M = δm_i + εm_j. Substituting, a_i − a_j ∈ m_iℤ + m_jℤ = gcd(m_i, m_j)ℤ. By (∗) the two classes meet. ∎
Sanity checks [COMPUTED, `verify.py`]:
- The moduli 20,15,12,6,6,6,6 have all pairwise gcds in (1,7) and pass the test with M = lcm of the gcds. The subfamily 15,12,6,6,6,6 fails it. This matches the example in [OB].
- Sun's moduli 10,15,36,42,66 pass the test on every subfamily. Yet no disjoint residues exist: an exhaustive search over a_1 = 0 (translation invariance) and all a_2..a_5 (15·36·42·66 tuples) finds none. So Lemma 5 on all subfamilies is necessary but **not sufficient**, as [OB] states.

## 3. Line-by-line audit of Lemma 6

Setting: k ≥ 2 is the least size that has a counterexample, meaning k pairwise disjoint classes with all gcd(m_i, m_j) < k. Among the counterexamples of size k, take one with minimal Σm_i. Such a family exists because the sums are positive integers. Write N = lcm{gcd(m_i, m_j) : i<j} and L_k = lcm(1, …, k−1). "Minimality of k" means: for every t with 2 ≤ t < k, every disjoint family of t classes has a pair with gcd ≥ t.

| item | statement | uses | verdict |
|---|---|---|---|
| 1 | m_i ∣ N, N ∣ L_k, N = lcm(m_1..m_k) | minimal Σm | [PROVED] |
| 2 | 1 < gcd(m_i,m_j) < k | (∗) | [PROVED] |
| 3 | q prime power, q ∣ m_i ⇒ q ∣ m_j for some j ≠ i | item 1 | [PROVED] |
| 4 | no m_i is a prime power (nor 1) | minimal k (+ item 3, which is avoidable) | [PROVED] |
| 4′ | (strengthening) no prime divides every m_i | minimal k only | [PROVED] |
| 5 | at least three m's are multiples of k−1 | minimal k | [PROVED]; the source only writes out the case "exactly two" |
| 6 | if exactly three m's are multiples of k−1, two further m's are multiples of k−2 | minimal k | [PROVED] |
| — | "this proves … that k ≥ 5" (end of item 6 proof) | items 4′,5,6 | [GAP] in [OB] (no argument given); closed below [PROVED] |
| 7 | Lemma 5 inequality for every subfamily and every admissible M | Lemma 5 | [PROVED] |
| 8 | 7 ≤ k ≤ 30, p ≥ k/2 prime, p ∣ some m ⇒ p divides exactly two m's | items 2,3,4 | [PROVED] after repair; the source's final case (k=30, ℓ=3) has a [GAP], fixed below |

Proofs, written out in full:

**Item 1.** Suppose m_i ∤ N. Then some prime p has r := v_p(m_i) > v_p(N) (r ≥ 1). Take j ≠ i. If p^r ∣ m_j, then p^r ∣ gcd(m_i, m_j) ∣ N, a contradiction. So v_p(m_j) ≤ r−1. Hence v_p(gcd(m_i/p, m_j)) = min(r−1, v_p(m_j)) = v_p(m_j) = min(r, v_p(m_j)). Every other prime has the same valuation in m_i/p as in m_i. So gcd(m_i/p, m_j) = gcd(m_i, m_j) for every j ≠ i. By (∗), whether two classes are disjoint depends only on the gcd of their moduli and the difference of their residues. So replacing m_i by m_i/p leaves a disjoint family of size k with the same gcds, all < k, and a smaller Σm. This contradicts the minimal choice. Also m_i/p ≠ 1: otherwise gcd(m_i/p, m_j) = 1 for j ≠ i, but this gcd equals gcd(m_i, m_j) > 1 by item 2 (whose proof does not use item 1). Hence m_i ∣ N.
Next, each gcd(m_i, m_j) lies in {1, …, k−1}, so it divides L_k, and therefore N ∣ L_k.
Finally, gcd(m_i, m_j) ∣ m_i gives N ∣ lcm(m_i), and m_i ∣ N gives lcm(m_i) ∣ N. ∎

**Item 2.** gcd < k is the hypothesis. If gcd(m_i, m_j) = 1, then 1 divides a_i − a_j, and by (∗) the classes meet. ∎

**Item 3.** Let q = p^r ∣ m_i. By item 1, q ∣ N. Since q is a prime power and N is the lcm of the gcds, q divides one of them, say gcd(m_a, m_b) with a ≠ b. One of a, b differs from i, and q divides that modulus. ∎

**Item 4 and 4′.** Suppose a prime p divides every m_j. (For item 4: if m_1 = p^r, then r ≥ 1, because m_1 = 1 would give gcd 1. Item 2 then gives p ∣ m_j for all j.)
- If p ≥ k, any pair has gcd ≥ p ≥ k, a contradiction.
- So p < k. Put t = ⌈k/p⌉. Then 2 ≤ t ≤ ⌈k/2⌉ < k, which holds for k ≥ 3; k ≥ 3 holds because k = 2 has no counterexample, by item 2.
- The k residues a_j fall into p classes mod p, so some t of them are congruent mod p; renumber them 1..t. The renumbering is harmless: only "p divides every m_j" is used from here on.
- For i<j≤t, gcd(m_i/p, m_j/p) = gcd(m_i, m_j)/p, and (a_j − a_i)/p is an integer. If gcd/p divided (a_j − a_i)/p, then gcd would divide a_j − a_i, which is false by (∗). So the t classes (a_j − a_1)/p (mod m_j/p), j ≤ t, are pairwise disjoint.
- By minimality of k, some pair among them has gcd(m_i/p, m_j/p) ≥ t. Then gcd(m_i, m_j) ≥ pt ≥ k, a contradiction. ∎
Item 4′ is stronger than [OB]'s item 4 and uses the same argument.

**Item 5.** Suppose at most two m's are multiples of k−1. Delete one class, choosing one of those multiples if there are any. The remaining k−1 classes are disjoint, and no two of them are both multiples of k−1. So no remaining gcd equals k−1. Every gcd is < k, so every remaining gcd is ≤ k−2 < k−1. That is a counterexample of size k−1 ≥ 2, contradicting minimality of k. ∎

**Item 6.** Suppose exactly m_1, m_2, m_3 are the multiples of k−1 (k ≥ 4).
- Delete classes 1 and 2. In the remaining k−2 classes only m_3 is a multiple of k−1, so every gcd is < k−1. By minimality (k−2 ≥ 2), some remaining pair has gcd ≥ k−2, hence gcd = k−2. So at least two of m_3, …, m_k are multiples of k−2.
- In the same way, deleting classes 1 and 3 shows that at least two of m_2, m_4, …, m_k are multiples of k−2.
- Suppose at most one of m_4, …, m_k were a multiple of k−2. The two bullets then force (k−2) ∣ m_3 and (k−2) ∣ m_2. Since k−1 and k−2 are coprime, (k−1)(k−2) ∣ gcd(m_2, m_3). But (k−1)(k−2) ≥ k for k ≥ 4, a contradiction.
- So at least two of m_4, …, m_k are multiples of k−2. ∎

**k ≥ 5 (closing [OB]'s unargued remark)** [PROVED]. k = 2 is impossible by item 2 and k = 3 by §3a. Suppose k = 4. By item 5, at least three of m_1..m_4 are multiples of k−1 = 3. If all four are, the prime 3 divides every m_i, contradicting item 4′. If exactly three are, item 6 says at least two of the remaining 4 − 3 = 1 moduli are multiples of 2, which is impossible. Hence k ≥ 5. ∎

**Item 7.** A subfamily of a disjoint family is disjoint. Apply Lemma 5 to it. ∎

**Item 8.** Let 7 ≤ k ≤ 30, let p ≥ k/2 be a prime dividing some m, and suppose m_1..m_ℓ are exactly the multiples of p.
- By item 3, ℓ ≥ 2. Also p ∣ gcd of two m's, so p < k by item 2.
- Assume ℓ ≥ 3. Put P_i = {primes q ∣ m_i} \ {p}. All these primes are < k, because m_i ∣ L_k.
- (i) For i ≤ ℓ, P_i ≠ ∅ by item 4. For i > ℓ, |P_i| ≥ 2 by item 4, since p ∤ m_i. (Only P_i ≠ ∅ is used.)
- (ii) For s ≠ t ≤ ℓ, P_s ∩ P_t = ∅. A common q would give pq ∣ gcd(m_s, m_t) with pq ≥ 2p ≥ k.
- (iii) For i > ℓ and s ≤ ℓ, P_s ∩ P_i ≠ ∅: gcd(m_s, m_i) > 1 and p ∤ m_i. So ω_i := (min(P_1∩P_i), …, min(P_ℓ∩P_i)) ∈ P_1×…×P_ℓ is defined. Its ℓ coordinates are distinct primes by (ii).
- (iv) If ω_i = ω_j for i ≠ j > ℓ, then the product of ℓ ≥ 3 distinct primes divides gcd(m_i, m_j). That product is ≥ 2·3·5 = 30 ≥ k, a contradiction. So ω is injective on the k−ℓ indices i > ℓ, and k − ℓ ≤ ∏|P_s|.
- (v) By (ii), Σ|P_s| ≤ r − 1, where r = π(k−1). So ∏|P_s| ≤ maxprod(r−1, ℓ), the largest product of ℓ positive integers with sum ≤ r−1. If ℓ > r−1, no such family of P_s exists at all.
- [COMPUTED, `verify.py`, exhaustive over all partitions] For every 7 ≤ k ≤ 30 and every 3 ≤ ℓ ≤ k, k − ℓ > maxprod(π(k−1)−1, ℓ), with the single exception (k, ℓ) = (30, 3), where maxprod(9, 3) = 27 = k − ℓ. The computed table agrees with [OB]'s table entry for entry (rows r = 4..10). [OB]'s table starts at r = 4, while k = 7 has r = 3. That case is covered: r − 1 = 2 < 3 ≤ ℓ, so it is infeasible.
- Exceptional case k = 30, ℓ = 3. Equality forces |P_1| = |P_2| = |P_3| = 3, and ω is a bijection onto P_1×P_2×P_3. The nine primes in P_1 ∪ P_2 ∪ P_3 are all the primes < 30 except p. Since p ≥ 15, p ∈ {17,19,23,29}, so some q ∈ {17,19,23,29} \ {p} lies in some P_s, say P_1.
  - **[GAP in OB]**: [OB] asserts that "two of the four primes 17,19,23,29 are in separate P_i's". That need not hold: the three large primes other than p could all lie in one P_s.
  - **Repair [PROVED].** Exactly 9 tuples in P_1×P_2×P_3 have first coordinate q, and each is some ω_i. For each such i, q = min(P_1∩P_i), so q ∣ m_i. Together with m_1, q divides at least 10 moduli.
  - Now q ≥ 17 ≥ k/2, so run the argument above with q in place of p. With ℓ_q ≥ 10, (v) needs ℓ_q ≤ r−1 = 9 pairwise disjoint nonempty sets, which is impossible. Contradiction.
  - (When two large primes do lie in different P_s, [OB]'s own argument also works: 3 of the m_i are then divisible by their product, which is ≥ 17·19 > 30.)
- Hence ℓ = 2. ∎

## 3a. Audit of [OB] Section 4.1 (3 ≤ k ≤ 6) [PROVED]
[OB] uses only m_i ∣ L_k (item 1), 1 < gcd < k (item 2) and "m_i is not 1 or a prime power" (item 4). Since gcd(m_i, m_i) = m_i, two equal moduli m_i = m_j force m_i < k.
- k = 3: divisors of L_3 = 2 are 1, 2; both are 1 or a prime power. No admissible modulus.
- k = 4: divisors of L_4 = 6 that are not 1 or prime powers: only 6. Then all m_i = 6 and gcd = 6 ≥ 4. Contradiction.
- k = 5: L_5 = 12; admissible: 6, 12. Any two admissible moduli have gcd ∈ {6, 12} ≥ 5. Contradiction.
- k = 6: L_6 = 60; admissible: 6, 10, 12, 15, 20, 30, 60 (checked in `verify.py`). Each is ≥ 6, so the six moduli are distinct. Only 6, 12, 15 are not multiples of 10, so at least 3 of the six are multiples of 10, and two of them have gcd ≥ 10 ≥ 6. Contradiction.
Every step checked; no gap. (For k = 5 [OB] writes "gcd < k < 6", meaning gcd < 5 < 6 ≤ every admissible gcd.)

## 4. Complete list of constraints on a minimal counterexample (size k, minimal k, then minimal Σm)
All [PROVED] above, except where marked.
- C1. 1 < gcd(m_i, m_j) < k for all i ≠ j.
- C2. m_i ∣ N = lcm of pairwise gcds, N ∣ L_k = lcm(1..k−1), and N = lcm(m_i). So every prime factor of every m_i is < k (it divides a gcd < k).
- C3. Every prime power dividing some m_i divides at least two m's.
- C4. No m_i is 1 or a prime power. More strongly (C4′), no prime divides all m_i.
- C5. At least three m's are divisible by k−1. If exactly three are, at least two others are divisible by k−2.
- C6. Density: for every subfamily h_1..h_ℓ and every common multiple M of its pairwise gcds, Σ 1/gcd(h_i, M) ≤ 1. This is necessary but not sufficient (Sun's 10,15,36,42,66).
- C7. For 7 ≤ k ≤ 30: every prime p ≥ k/2 divides either 0 or exactly 2 of the m's.
- C8. k ≥ 5 (closed above); in fact k ≥ 7 by §3a and the unaudited §4.2 gives more.
- Consequence of C5 + C7: for 7 ≤ k ≤ 30, k−1 is not prime, i.e. k ∉ {8,12,14,18,20,24,30}. (k ≤ 6 is excluded by §3a, not by C5 and C7.)

**Completeness.** C1–C7 are all the constraints stated in [OB] Lemma 6 (items 1–8, with items 1–3 folded into C1–C3 and item 7 = C6); C4′ and C8 are our additions. No other structural constraint appears in [OB]. The `Grow` search of [OB] §4.4 uses **fewer**, not more: candidates are divisors of L_k with ≥ 2 distinct prime factors (C2 + C4), each pair has 1 < gcd < k (C1), and each subfamily passes Lemma 5 with the single choice M = lcm of its pairwise gcds (a special case of C6). Moduli are enumerated in nondecreasing order (repeats allowed). It does not use C3, C4′, C5 or C7.

Not audited here [GAP for this report]: the 6 ≤ k ≤ 10 casework in Section 4.2 and the Mathematica search of Section 4.4 (k ≤ 19).

## Cited vs ours
- Cited: Lemma 5, items 1–8 and Section 4.3 are [OB]. The asymptotic bound is [FS]. The group form for k = 3, 4 is [Zhu].
- Ours:
  - We checked every step line by line and filled the implicit steps (distinct indices in Lemma 5; the cases of 0 or 1 multiples in item 5; the r = 3 row in item 8).
  - We close [OB]'s unargued "k ≥ 5" remark (items 4′, 5, 6) and audit §4.1 (3 ≤ k ≤ 6).
  - We give a correct argument for the k = 30, ℓ = 3 case of item 8, where [OB]'s argument has a gap.
  - We strengthen item 4 to C4′ (no prime divides all moduli).
  - We flag three discrepancies: 24 and 30 are only conditional; the k ≤ 19 search is not a certificate under our rules; the cell's "group form known for k ≤ 5" is not supported by the fetched sources.

**What remains open:**
- Sizes 21, 22, 23 are not proved anywhere we fetched, so 24 and 30 remain conditional.
- Item 8 for k > 30: step (iv) needs a product of ℓ distinct primes ≥ k. That holds for ℓ ≥ 4 when k ≤ 210, but ℓ = 3 needs a new argument.
- No size k ≥ 25 is decided.

**Verification:** `python3 swarm/results/p4-literature-ce0fb3/verify.py` runs exact integer and Fraction checks: the item-8 table, the list of k with k−1 prime, the Lemma 5 examples, the exhaustive Sun counterexample, and the k ≤ 6 moduli lists. It takes about 4 s wall clock (measured 3.5 s and 3.95 s by the critics).
