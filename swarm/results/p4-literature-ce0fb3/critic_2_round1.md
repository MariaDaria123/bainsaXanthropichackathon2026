# Critic #2 — p4-literature-ce0fb3

Scope: `result.md` against `problems/p4/cells/c6/cell.md` and task goal (a). I checked it against `obryant.tex` (lines 150–430) and ran `verify.py`. I did not read notes.md, the board, or logs.

## 1. Statement check
- Status is OPEN/partial. The write-up says plainly that no size k ≥ 25 is decided, so it does not claim c6(a). That is honest. Nothing is presented as a solution of the cell.
- Claim 1.3 [PROVED] is stated with the right quantifiers: "DCCC for all sizes < k implies DCCC for size k, for k ∈ {8,12,14,18,20,24,30}". This is exactly O'Bryant's "a minimal counterexample does not have k ∈ {24,30}". The write-up correctly says this is conditional for 24 and 30, because sizes 21–23 are open. It does not weaken the cell and adds no hidden assumption.
- Claims 1.1 and 1.4 are labelled [OBSERVED], and they are observations. I checked 1.1: `problems/p4/cells/c5/` holds only cell.md and .gitkeep files. The quotes from the source match: "slightly less than a week" is at line 477, and the item-8 exceptional case is at lines 331–335.

## 2. Step-by-step audit (each compared with the source)
- **Lemma 5.** The proof is correct. It makes explicit a step the source leaves implicit: the pigeonhole collision must come from two different indices. The typo i≤k → i≤ℓ is correctly noted.
- **Item 1.** Correct. The valuation argument v_p(m_j) ≤ r−1 makes gcd(m_i/p, m_j) = gcd(m_i, m_j), and the replacement lowers Σm. A replaced modulus m_i/p = 1 is impossible because the gcds do not change and are > 1. The write-up does not say this, but it follows from what is written.
- **Items 2 and 3.** Correct.
- **Items 4 and 4′.** Correct. The bounds 2 ≤ t = ⌈k/p⌉ < k, the reduction to t classes, and the step gcd ≥ pt ≥ k are all checked. Only "p divides every m" is used, so the strengthening 4′ is valid.
- **Item 5.** Correct. It covers the cases of 0, 1 or 2 multiples; the source writes out only "exactly two".
- **Item 6.** Correct. The deletions of {1,2} and {1,3} and the coprimality of k−1 and k−2 are checked. For k = 4 the conclusion is vacuous-contradictory, which is logically fine.
- **"k ≥ 5" [GAP].** Flagged honestly. Local fix, optional: for k = 4, item 5 gives at least three multiples of 3. If exactly three, item 6 needs two more multiples of 2 among the single remaining index, which is impossible. If all four are multiples of 3, this contradicts 4′. So the gap closes in two lines with the write-up's own tools.
- **Item 8.** Steps (i)–(v) are correct:
  - (ii) uses pq ≥ 2p ≥ k.
  - (iii) uses p ∤ m_i for i > ℓ.
  - (iv) uses a product of ≥ 3 distinct primes, which is ≥ 30 ≥ k.
  - (v) uses disjoint subsets of the r−1 primes < k other than p.
  - The ℓ = k edge case (k−ℓ = 0) is harmless because maxprod = 0 whenever ℓ > r−1 ≤ 9.
- **Gap in [OB] at k = 30, ℓ = 3: confirmed real.** [OB] says "two of 17,19,23,29 are in separate P_i's". This does not follow: for example p = 17 with P_1 = {19,23,29} and P_2 ∪ P_3 = {2,3,5,7,11,13}. **The repair is correct.** The 9 tuples with first coordinate q are 9 distinct ω_i, because ω is a bijection. So q divides m_1 and 9 further moduli, which gives ℓ_q ≥ 10. The P-sets for q would then be 10 pairwise disjoint nonempty subsets of 9 primes, which is impossible. Disjointness holds because qq′ ≥ 34 > 30.

## 3. Tests
- `verify.py` runs in 3.5 s wall clock. It is exact and deterministic. Its results:
  - The item-8 table has its only failure at (30, 3, 27), and it matches [OB]'s table row for row (r = 4..10).
  - The list of k with k−1 prime is {8,12,14,18,20,24,30}.
  - The Lemma 5 examples (20,15,12,6⁴ passes; the subset fails) are reproduced.
  - Sun's family 10,15,36,42,66 is exhaustively confirmed non-disjoint over a_1 = 0 and the full product of the other residues, with translation invariance justified.
- My own test: a random test of Lemma 5 found 0 violations in 148,289 triggered cases (ℓ ≤ 5, moduli ≤ 40, M a random multiple of the lcm of the gcds).
- No certificate is claimed, so the 5-part certificate does not apply.

## 4. Local fixes (MINOR)
1. §4, the "Consequence" line: "k−1 is not prime (for k ≤ 30)" is too broad. Item 8 needs 7 ≤ k. Write "for 7 ≤ k ≤ 30". (k ≤ 6 is excluded by §4.1, not by C5 and C7.)
2. Claim 1.2 calls §4.2 "k = 7,8,9,10". The source's title is 6 ≤ k ≤ 10. Also, §4.1 (k ≤ 6) is described as a "fully written proof", but the report never says whether it was audited. `verify.py` only lists admissible moduli. Either audit §4.1 or add it to the "Not audited" list.
3. Optionally close the "k ≥ 5" gap with the two-line argument in §2 above.
4. Task (a) asks for "EVERY structural constraint". The list C1–C7 covers everything in Lemma 6 plus C4′. It would help to say so explicitly ("these are all constraints stated in [OB] Lemma 6"), and to mention that the Grow search of §4.4 uses no further constraints beyond those in Lemma 6. If it does use more, list them.

The labels are otherwise accurate. Nothing [OBSERVED] or [GAP] is passed off as proved, and "Cited vs ours" is present and correct.

VERDICT: MINOR
