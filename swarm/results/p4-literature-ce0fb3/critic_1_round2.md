# Critic #1: p4-literature-ce0fb3 (blind)

Judged: `result.md`, `problems/p4/cells/c6/cell.md`, the task goal, the cited `verify.py`, and the cited primary source `obryant.tex` (used to check the audit against the original text). I did not read notes.md, the board or the logs.

## 1. Statement check
- The write-up states that it decides no new size k and gives status OPEN/partial. It makes no claim to settle any c6 direction. Nothing is silently weakened.
- Claim 1.3 is correctly limited to "if DCCC holds for all sizes < k, then it holds for k", for k ∈ {8,12,14,18,20,24,30}. It says explicitly that 24 and 30 are conditional on 21–23 (and 21–29), which [OB] does not settle. I checked this against the source: [OB] §4.3 gives only the item-5 versus item-8 clash, so this reading is correct.
- Claim 1.1 says `problems/p4/cells/c5/` is empty. Verified: it holds only `cell.md` and `.gitkeep` files.
- Claims 1.2 and 1.4 are labelled [GAP] and [OBSERVED]. Neither is presented as proved.

## 2. Step-by-step check

**Lemma 5.** Correct. The added point that the two colliding cosets must have different indices is valid, because each coset lists distinct residues mod M. The Bézout step is also valid: gcd(m_i, m_j) | M, so M ∈ m_iℤ + m_jℤ. The typo in the source ("1≤i≤k" in the statement) is confirmed in `obryant.tex` line 174.

**Item 1.** Correct. For j ≠ i we have v_p(m_j) ≤ r−1, so v_p(gcd(m_i/p, m_j)) = v_p(gcd(m_i, m_j)). The new family is disjoint by (∗), keeps the same gcds and has a smaller Σm. I checked the gcd identity exhaustively for m_i, m_j < 200 and p ≤ 7.

**Item 3.** Correct. v_p(N) is the maximum of v_p over the pairwise gcds.

**Items 4 and 4′.** Correct.
- The pigeonhole step gives t = ⌈k/p⌉ residues that are congruent mod p.
- The rescaled classes are disjoint: gcd/p divides (a_j − a_i)/p if and only if gcd divides a_j − a_i.
- The case analysis gives 2 ≤ t < k.
- The conclusion gcd ≥ pt ≥ k follows.
- 4′ really is stronger than item 4. It uses only "p divides every m_j".

**Item 5.** Correct. It covers the cases of zero, one and two multiples of k−1. The source writes out only "exactly two".

**Item 6.** Correct. Bullet 3 argues well: at most one of m_4..m_k is a multiple of k−2, so both m_2 and m_3 must be. Then (k−1)(k−2) divides gcd(m_2, m_3), and (k−1)(k−2) ≥ k for k ≥ 4. This is cleaner than the source's "renumber" remark.

**k ≥ 5.** Correct. For k = 4: if all four m's are multiples of 3, this contradicts 4′. If exactly three are, item 6 needs two more multiples of 2 among the one remaining modulus, which is impossible.

**Item 8.**
- Steps (i)–(v) are correct. I checked each against the source text.
- The table is reproduced by `verify.py` and matches the [OB] table entry for entry, for r = 4..10.
- The r = 3 row (k = 7) is correctly shown to be infeasible.
- The exceptional case (30, 3) is handled as follows. Equality forces |P_s| = 3 and forces ω to be a bijection onto P_1×P_2×P_3. So the nine P-primes are all the primes < 30 except p.
- **The reported [OB] gap is real.** The three large primes in {17,19,23,29}\{p} can all lie in a single P_s (for example P_1 = {17,19,23}, with P_2 and P_3 split from {2,3,5,7,11,13}). So the source's "two of them are in separate P_i's" is unjustified.
- **The repair is valid.**
  - The 9 tuples with first coordinate q are all hit by ω.
  - q = min(P_1 ∩ P_i) implies q | m_i.
  - So q divides at least 10 moduli.
  - Rerunning (i)–(ii) with q (q ≥ 17 ≥ 15) needs 10 pairwise disjoint nonempty subsets of the 9 primes other than q. That is impossible.

**§3a (k = 3..6).** Correct.
- Equal moduli force m < k.
- The lists of admissible moduli are reproduced by `verify.py`.
- For k = 6: at most 3 of the 7 admissible moduli (6, 12, 15) are not multiples of 10, so at least 3 of the six distinct moduli are multiples of 10.

**Completeness claim.** I compared it with `obryant.tex`, lines 214–337 and 427–479.
- Lemma 6 has exactly items 1–8, plus the stated "k ≥ 4".
- The `Grow` search uses these constraints: candidates are divisors of L_k with more than one distinct prime factor; every subset satisfies 1 < gcd < k; and every subset passes Lemma 5 with the single choice M = lcm of its gcds. Moduli are enumerated in nondecreasing order.
- The write-up's description is accurate.

## 3. Tests run
- `verify.py` finished in 4.8 s wall clock. It is exact (int, Fraction, sympy integers) and deterministic.
  - Its output matches every claim in the write-up.
  - The Sun search is exhaustive over a_1 = 0 and every a_2..a_5 in its full residue range, and it finds no disjoint system.
- Lemma 5, random test: 2134 random families (ℓ ≤ 4, m ≤ 24, M a multiple of the lcm of the gcds) that fail the density test. An exhaustive residue search found a disjoint system in none of them. 0 counterexamples.
- (∗): checked exhaustively for all m_1, m_2 ≤ 12 and all residues. It holds.

## 4. Local fixes needed (MINOR)
1. **(∗) is used as a black box.** Every item leans on it, and it is [OB] Proposition 2 (Fraenkel). The hand-in rules say to cite *and check*. Add its short proof:
   - If x ≡ a_i (mod m_i) and x ≡ a_j (mod m_j), then gcd | a_i − a_j.
   - Conversely, if gcd | a_i − a_j, write a_i − a_j = u·m_i + v·m_j by Bézout. Then x = a_i − u·m_i lies in both classes.
2. **The certified boundary is not stated in one sentence.** The goal asks to "pin down the current certified boundary". The facts are all there (Claims 1.1–1.3) but are never combined. Add an explicit statement along these lines:
   - Written proofs audited here: sizes 3 ≤ k ≤ 6.
   - Written but not audited: 7 ≤ k ≤ 10.
   - Resting only on the uncertified `Grow` search: 11, 13, 15, 16, 17, 19.
   - Reduction steps that are each valid given all smaller sizes: 12, 14, 18, 20, 24, 30.
   - So the range fully proved in writing under our rules is k ≤ 6 (k ≤ 10 once §4.2 is audited), and 12 and upward inherit the dependence on the search.
3. (Cosmetic.) Item 8(i): "(Only P_i ≠ ∅ is used.)" is accurate. It would read better with a note that |P_i| ≥ 2 for i > ℓ is not needed anywhere.

None of these affects the correctness of a labelled claim. Every [PROVED] item is complete and checked, the one [COMPUTED] table is exact and exhaustive, and the [OB] gap and its repair are correct.

VERDICT: MINOR
