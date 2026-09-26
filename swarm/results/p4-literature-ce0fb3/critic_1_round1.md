# Critic #1 — p4-literature-ce0fb3 (blind)

Judged: `result.md`, `problems/p4/cells/c6/cell.md`, task goal (a), cited code `verify.py`, and the cited source `obryant.tex`, which I used only to check the audit's quotes against the original. I did not read notes.md, the board, or the logs.

## 1. Statement check
- Status is OPEN (partial). The write-up claims to decide no new size and does not claim c6 is solved. The task was a literature audit for goal (a), and the write-up delivers one. No silent weakening.
- Claim 1.3 [PROVED] has the right quantifiers. It says: for k in {8,12,14,18,20,24,30}, if DCCC holds for all sizes < k, then it holds for k. It states explicitly that 24 and 30 are only **conditional**, because 21–23 are open. This matches OB's Theorem 3 wording ("a counterexample with minimal k does not have k∈{24,30}"). Correct.
- Claim 1.1 [OBSERVED]: I checked that `problems/p4/cells/c5/` holds only `cell.md` and `.gitkeep` files. True.
- Claim 1.4 [OBSERVED]: the cell does say "known for k ≤ 5". The write-up flags this as unsupported and does not assert it false. Labelled correctly.
- Every [OBSERVED] or [GAP] item is kept apart from the proved material. Nothing unproved is presented as proved.

## 2. Step-by-step audit
I compared each item against `obryant.tex` lines 200–336.
- **Lemma 5.** Correct. The reduction m_iℤ+Mℤ = g_iℤ is right. The pigeonhole step correctly forces two distinct indices, and the write-up spells out that point, which OB leaves implicit. Bézout then gives a_i−a_j ∈ gcd(m_i,m_j)ℤ. The typo note (1≤i≤k should be 1≤i≤ℓ) is accurate: the source has "with 1≤i≤k".
- **Item 1.** The valuation computation is right. v_p(m_j) ≤ r−1 for every j≠i gives min(r−1,v_p(m_j)) = min(r,v_p(m_j)), so all gcds are preserved and Σm drops. I tested this: 20k random families, 0 violations.
- **Items 2, 3.** Correct.
- **Items 4 / 4′.** Correct. The argument uses only "p divides every m_j". p ≥ k is ruled out directly. For p < k, t = ⌈k/p⌉ satisfies 2 ≤ t < k. The residues a_i ≡ a_j (mod p) make the quotient classes integral and disjoint, and the gcds scale by p. Minimality at size t then gives gcd ≥ pt ≥ k. Item 4′ is a genuine, correct strengthening of OB's item 4.
- **Item 5.** Correct, and the write-up covers the 0- and 1-multiple cases that OB omits. After the deletion, no remaining pair has gcd k−1, so every remaining gcd is ≤ k−2.
- **Item 6.** Correct. The "at most one of m_4..m_k" case forces (k−1)(k−2) | gcd(m_2,m_3), and (k−1)(k−2) ≥ k for k ≥ 4. This is cleaner than OB's "renumber m_2 and m_3".
- **Item 8.** Steps (i)–(v) are correct. The (k,ℓ) table is confirmed by rerun; the only failure is (30,3). Equality Σ|P_s| ≤ 9 with ∏|P_s| ≥ 27 forces (3,3,3); I checked this exhaustively. ω is then a bijection.
  - **OB gap confirmed.** OB's "two of the four primes 17,19,23,29 are in separate P_i's" (tex line 333) does not follow. With p = 29, the primes 17, 19 and 23 could all lie in P_1.
  - **Repair checked.** The 9 tuples with first coordinate q give q | m_i for 9 indices i > 3. Adding m_1 gives ℓ_q ≥ 10. Rerunning (ii)/(v) for the prime q ≥ 17 ≥ k/2 needs 10 pairwise disjoint nonempty subsets of a 9-element set, which is impossible. The repair only uses (i), (ii) and (v), so it is not circular. Valid.
- **Claim 1.3 proof.** Item 5 gives ≥ 3 multiples of p = k−1. Item 8 then says exactly 2. p ≥ k/2 and 7 ≤ k ≤ 30 hold for the listed k; I verified that k−1 is prime for exactly these seven k in [7,30]. Correct.

## 3. Tests run
- (∗) brute-force check for all m1, m2 ≤ 24 and all residues: agrees with `congruence.meet`.
- Lemma 5, randomised: 2116 families satisfying the hypothesis with M a multiple of the lcm of the gcds, 50 residue draws each. 0 disjoint families found.
- Item-1 reduction preserves gcds: 0 violations.
- maxprod equality case for (30,3): only (3,3,3).

## 4. Cited code
Ran `python3 swarm/results/p4-literature-ce0fb3/verify.py`. It is exact (int/Fraction), deterministic, and took 3.95 s wall clock. The output matches every figure quoted:
- the only table failure is (30,10,3,27);
- the table rows match OB;
- the k-list is [8,12,14,18,20,24,30];
- the 7-moduli example gives True/True/False;
- the Sun 10,15,36,42,66 search passes on every subset and finds no disjoint residues. It is exhaustive over a_1 = 0 × Z_15 × Z_36 × Z_42 × Z_66, and translation invariance is valid.

This is not a proof-step certificate. The only proof step that relies on code is the item-8 table, a finite exhaustive integer-partition computation of about 200 (k,ℓ) cases. It is fully reproducible, and the write-up does not claim a tools/cert.py certificate for it. Given its size this is acceptable.

## 5. Local nits (non-blocking)
1. Runtime: the write-up says "about 30 s wall clock"; I measured 3.95 s. Only the wording is off.
2. OB's §4.2 heading is "6 ≤ k ≤ 10", and the write-up says "k = 7, 8, 9, 10". Harmless, because §4.1 covers k = 6.
3. The "k ≥ 5" [GAP] is labelled honestly, and it is easy to fill. For k = 4, item 5 gives ≥ 3 multiples of 3. If exactly 3, item 6 needs two further moduli but only one remains. If all 4 are multiples of 3, this contradicts C4′. The write-up could state this in one line.
4. C2 wording: "every prime factor of every m_i is < k" follows from m_i | N | L_k. Fine as written.

## 6. Labels and literature
The labels match the content. OB's arguments are rewritten in full and checked, not cited as black boxes. The "Cited vs ours" section is present and accurate. The contributions it claims are real: the item-8 repair, C4′, and the filled implicit steps.

Every strong claim is correct and complete as written. The nits above are cosmetic.

VERDICT: ACCEPT
