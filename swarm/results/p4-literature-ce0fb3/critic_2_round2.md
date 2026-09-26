# Critic #2 (blind) — p4-literature-ce0fb3

Material judged: `result.md`, `problems/p4/cells/c6/cell.md`, the task goal, cited code `verify.py`, and the cited source `obryant.tex`, which I compared line by line with the audit. I did not read notes.md, the board, other critics, or logs.

## 1. Statement check
- The write-up states plainly that it is a literature audit, that its status is OPEN/partial, and that it decides no new k. It does not claim any c6 direction (a)/(b)/(c). Nothing in it silently weakens the cell.
- Task goal (a): "certified boundary". Claim 1.1 says c5 has nothing on disk. I checked: `problems/p4/cells/c5/cell.md` is a placeholder, and `cert/`, `data/`, `work/` are empty. Claim 1.2 says the §4.4 Mathematica search is not a certificate under repo rules. The source confirms "slightly less than a week" and gives no node counts. Claim 1.3 says {24,30} are only conditional on sizes < k. That is correct: [OB]'s Theorem says "a counterexample with minimal k does not have k ∈ {24,30}", which is exactly the conditional form. The labelling is honest.
- Claim 1.3 is labelled [PROVED] and correctly quantified: "if DCCC holds for all sizes < k then for k", for k−1 prime and 7 ≤ k ≤ 30. The proof uses item 5 (≥ 3 multiples of p = k−1) and item 8 (with p = k−1 ≥ k/2, so exactly 2). These contradict each other. The proof is correct, and I checked that the list of k is right.
- Claims 1.1 and 1.4 are [OBSERVED] and presented as such. The cell's "k ≤ 5" wording is quoted correctly from cell.md.

## 2. Step-by-step audit (my checks of each item)
- **Lemma 5.** The coset reduction m_iℤ+Mℤ = g_iℤ is right. So is the pigeonhole step, including the added point that the two residues come from distinct indices. Bézout gives M ∈ m_iℤ+m_jℤ, then (∗) applies. Correct. The source typo "1≤i≤k" really is in obryant.tex.
- **Item 1.** The valuation argument is correct. The side check m_i/p ≠ 1 is correct and avoids circularity, because item 2 does not use item 1. N | L_k and N = lcm(m_i) are correct.
- **Items 2, 3.** Correct. Item 3 correctly uses the fact that a prime power dividing an lcm divides one of the terms.
- **Items 4 and 4′.** Correct. The bounds t = ⌈k/p⌉ ∈ [2, k−1] are justified, the scaled family is disjoint, and minimality gives gcd ≥ pt ≥ k. The 4′ generalisation is valid, because the argument only uses "p divides every m_j". The prime-power case reduces to 4′ via item 2.
- **Item 5.** Correct, and it covers the 0, 1 and 2 multiple cases uniformly: delete one multiple, and no remaining pair has gcd k−1.
- **Item 6.** Correct. The two deletions each give ≥ 2 multiples of k−2. If m_4..m_k held at most one of them, both m_2 and m_3 would be multiples of k−2, and (k−1)(k−2) ≥ k for k ≥ 4. This is cleaner than [OB]'s "renumber" sentence.
- **k ≥ 5.** Correct: it uses 4′ for the case of four multiples of 3, and item 6 for the case of three.
- **Item 8, steps (i)–(v).** Correct. (ii) uses 2p ≥ k. (iv) uses ∏ of ≥ 3 distinct primes ≥ 30 ≥ k, which is where k ≤ 30 comes in. (v) is Σ|P_s| ≤ π(k−1)−1.
- **Item 8, exceptional case (30, 3).** I confirm that [OB]'s sentence "two of the four primes 17,19,23,29 are in separate P_i's" does not follow. With p = 17, P_1 = {19,23,29} is compatible with everything derived up to that point. The repair is valid:
  - The 9 tuples with first coordinate q are hit by 9 distinct i > 3, because ω is a bijection, and each such m_i is divisible by q. Together with m_1, that gives ≥ 10 multiples of q.
  - q ≥ 17 ≥ 15, so (i)+(ii) apply to q (2q ≥ 34 ≥ 30). But 10 pairwise disjoint nonempty subsets of the 9 primes < 30 other than q cannot exist.
  - The repair is sound.
- **§3a (k = 3..6).** Correct. The distinctness argument (m_i = m_j forces gcd = m_i ≥ 6) and the multiples-of-10 count (≥ 3 of the six distinct values) both check out.

## 3. Tests run
- `python3 verify.py`: 3.85 s wall. Exact ints and Fractions via sympy/fractions, deterministic.
  - Item-8 table: the only failure is (30, 10, 3, 27). The rows r = 4..10 match the [OB] table entry for entry.
  - k−1 prime list: [8,12,14,18,20,24,30].
  - k = 7 example: behaves as stated.
  - Sun's 10,15,36,42,66: exhaustive over a_1 = 0 and full residue ranges finds no disjoint system.
  - Admissible moduli for k ≤ 6: as stated.
- My own random tests (`/tmp/c2test.py`, exact):
  - Lemma 5 with random M a multiple of the lcm: 15465 triggering cases, 0 disjoint systems.
  - Item-1 reduction gcd(m_i/p, m_j) = gcd(m_i, m_j) when v_p(m_i) > v_p(N): 102615 cases, 0 violations.
  - Monotonicity of the density sum in M: 0 violations. This matters for point M1 below.

## 4. Local fixes needed (MINOR)
- **M1. §2 sanity check and C6.** The claims "Sun's moduli pass the test on every subfamily" and "Grow uses … the single choice M = lcm (a special case of C6)" are only checked with M = lcm of the pairwise gcds. That is enough for the "not sufficient" conclusion, but the write-up does not say why.
  - Needed: one line. If M | M′, then gcd(h, M) | gcd(h, M′), so Σ1/gcd(h_i, M′) ≤ Σ1/gcd(h_i, M). Hence M = lcm is the strongest instance.
  - It follows that Grow's test is **equivalent** to C6, not weaker. The sentence "uses **fewer** [constraints]" should drop C6 from the comparison. It stays true for C3, C4′, C5 and C7.
- **M2. §4 Completeness.** "No other structural constraint appears in [OB]" is fair for Lemma 6. [OB] Lemma 6's own header also asserts "k ≥ 4". Worth noting that C8 subsumes it, so the list is visibly complete.
- **M3. Claim 1.2.** "6 ≤ k ≤ 10 … not audited here" is honest. But C8's "k ≥ 7" and all of Claim 1.3 for k ≥ 8 then rest on unaudited or uncertified steps. For k = 8 in particular, Claim 1.3 needs the DCCC for size 7, which is only in §4.2. The "What remains open" section should say explicitly that, under repo rules, the certified unconditional boundary is k ≤ 6.

No claim is mislabelled. No [PROVED] step fails. No counterexample was found.

VERDICT: MINOR
