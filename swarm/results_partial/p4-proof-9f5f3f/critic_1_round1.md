# Critic #1 — p4-proof-9f5f3f (blind)

Judged: `result.md`, `problems/p4/cells/c6/cell.md`, `problems/p4/problem.md`, and the cited script `table.py`, which I ran. I did not read notes.md, the board, or any logs.

## 0. Statement check
- The write-up says plainly that its status is **OPEN/PARTIAL**: no size k is decided, and the task target (rule out k = 32, 38, 42, 44, 48) is **not** reached. It makes no overclaim against cell c6(a).
- Everything depends on F1–F4 (items 1–5 of O'Bryant's Lemma 6 as audited in p4-literature-ce0fb3) and on minimality of k. The header says this, and it also says that sizes < k are unsettled for k ≥ 21. So the conditional status is disclosed.
- The claims do not quietly weaken the cell. They are lemmas about a hypothetical minimal counterexample, and they are labelled that way.

## 1. Claim 1 [COMPUTED] — the counting test fails for ℓ = 3 and several ℓ ≥ 4
- **Reran `table.py`:** 0.74 s user / 4.1 s wall. The output matches the table in result.md row for row: k=32 → ℓ∈{3,4,5}; 38 → {3..6}; 42 → {3..6}; 44 → {3..7}; 48 → {3..8}, with the same maxprod and k−ℓ values.
- **Exactness:** the script uses integers only. `primepi`/`isprime` from sympy are exact. `maxprod` is exhaustive recursion over compositions whose sum is ≤ S. I spot-checked it by hand: S=10, ℓ=3 → 36 (from 3·3·4); S=10, ℓ=5 → 32 (from 2^5). Both are correct.
- The assertion that {32, 38, 42, 44, 48} are exactly the k in [31, 48] with k−1 prime passes.
- **Logic:** ω maps R (|R| = k−ℓ) into ∏P_s, so if ω is injective then k−ℓ ≤ ∏|P_s| ≤ maxprod(π(k−1)−1, ℓ). This is correct. The claim is honestly framed as "this argument fails", not as "configurations exist".
- **Injectivity for ℓ ≥ 4, k ≤ 210:** a collision would give a product of ℓ distinct primes dividing the gcd, and that product is ≥ 210 ≥ k, which contradicts F2. This is correct.
- **Minor (M1):** this injectivity sub-claim is tagged "[PROVED]" inline, but it uses F2: gcd(m_s, m_t) = p makes the P_s disjoint, gcd(m_s, m_i) > 1 makes ω defined, and gcd < k is needed. F2 is on the board only as [CONJECTURED]. The inline tag should say "conditional on F1–F3", as Claims 2 and 3 do.
- **Minor (M2):** "the task's premise … is false" is slightly overstated. The task's literal sentence says that an ω-collision gives gcd ≥ 210 when ℓ ≥ 4, and that is true. What fails is the pigeonhole that would force a collision. The wording should be changed to say that.
- **Minor (M3):** `table.py` is not wrapped through `tools/cert.py`/`tools/rerun.py` (repo rule 4). The script is not load-bearing for any positive proof step, since it only shows that an argument fails, so this is a hygiene issue and not a correctness issue.

## 2. Claim 2 [PROVED, cond. F1–F3] — structure of the multiples of p = k−1
- (a) L_k = lcm(1..p), so v_p(L_k) = 1, and F1 then gives v_p(m_s) = 1. ✓
- (b) gcd(m_s, m_t) is a multiple of p and < p+1, so it equals p. ✓
- (c) u_s = 1 would make m_s = p a prime power, which F3 excludes. The step p·gcd(u_s, u_t) = p is correct. ✓
- (d) This follows from (∗), since gcd = p ∤ a_s − a_t. ✓ (Here ℓ ≤ p is trivial anyway.)
No gaps.

## 3. Claim 3 [PROVED, cond. F1–F3] — fiber reduction
- The pullback under φ(t) = a_s + pt is valid: p is invertible mod m_i because p ∤ m_i and p is prime. The preimage of a_s (mod p·u_s) is 0 (mod u_s). Preimages of disjoint sets are disjoint. gcd(p·u_s, m_i) = gcd(u_s, m_i) holds by the argument given. ✓
- **Tested:** 43,119 random fibers of random pairwise-disjoint families with p ∈ {3, 5, 7, 11} and v_p(m_s) = 1. The new families were always pairwise disjoint and the gcds were always preserved. 0 failures.
- The density consequence is correct, and the write-up correctly notes that it finishes nothing.

## 4. Claim 4 [PROVED, minimality + F2] — G_t is a linear union of cliques for t > (k−1)/2
- (a) Any t indices form a disjoint family of size t < k, so by minimality they span an edge of G_t. The complement of a vertex cover is independent, so it has ≤ t−1 vertices. ✓
- (b) The edge-set identity is correct, with F2 giving the upper bound g ≤ k−1. The two cases are both handled with explicit arguments:
  - If g | h, then h ≥ 2g ≥ 2t > k−1.
  - If g ∤ h, then lcm(g, h) ≥ 2h > k−1.
  ✓
- **Tested:** 555,111 (g, h) checks on random moduli sets with all pairwise gcds < k, k ∈ [5, 30], t = ⌊(k−1)/2⌋+1. There was never a pair of moduli in D_g ∩ D_h. 0 failures.
- **Special cases:**
  - t = k−1: τ(K_n) = n−1 ≥ 2, so |D_{k−1}| ≥ 3. ✓
  - t = k−2 with |D_{k−1}| = 3: if |D_{k−2}| ≤ 1, then G_{k−2} is a triangle with τ = 2 < 3, so |D_{k−2}| ≥ 2. By (b) at most one of these lies in D_{k−1}, so at least one lies outside it. ✓
  - The stronger "two" of item 6 is deferred explicitly to the other file and is not claimed here. That is acceptable.
- **Scope note:** the special case covers only |D_{k−1}| = 3, and it says so.

## 5. Banned phrases / labels / literature
- None of the banned phrases appear without an argument.
- No [CONJECTURED] item is presented as proved.
- The "Cited vs ours" section is present. The ω-map is correctly credited to O'Bryant, and nothing published is used as a black box for the cell statement itself.

## 6. Overall
Every labelled claim is correct as written and survived both the rerun and the random tests. The result does not decide any k and does not reach the task goal. The write-up says so honestly, so as a contribution it is a partial result (a no-go observation plus structural lemmas).

Local fixes needed:
- **M1:** add "conditional on F1–F3" to the inline [PROVED] tag in Claim 1.
- **M2:** reword "premise is false" to "the pigeonhole step fails".
- **M3:** optionally route `table.py` through tools/cert.py.

VERDICT: MINOR
