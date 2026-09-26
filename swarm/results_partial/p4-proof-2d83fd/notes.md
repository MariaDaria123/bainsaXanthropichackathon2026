# notes (not seen by critics)

- Task says "primes p in (k/3,k/2], e.g. p in {9,11}". 9 is not prime; read it as
  "prime-power thresholds p^E_p" (the same objects Lemma 1/Corollary 1a of p4-proof-9c5676
  bound), since that's the only reading consistent with the example given. Verified with
  check_range.py that {9,11} are exactly the p^E_p values in (25/3,25/2].

- First attempt: tried to directly reuse p4-proof-9c5676's "Main Reduction Theorem" (assume
  all m_i | L) to simplify the argument. Realized the shared board currently lists that
  theorem as [CONJECTURED] (critics downgraded it, round 2), not [PROVED]/FACT, so leaning on
  it would make my own result only as strong as an unverified dependency. Reworked the proof
  to NOT need "all m_i | L" at all — only needs the 3-line Sub-lemma A (which I reprove
  myself) applied directly to the original family F. This makes the result fully
  self-contained. Cleaner anyway.

- Key realization: unlike Lemma 3's range (q > k/2, forcing gcd = q exactly, single case),
  here gcd ∈ {q, 2q} is possible, and MOREOVER whether a given pair falls into "q" or "2q"
  is not globally consistent for a fixed index — it depends on both indices' v_2. Had to
  split I_q into I_q^0 (odd) and J_q (has a factor of 2), and show each piece separately is
  homogeneous (all-q or all-2q), which is what actually licenses injectivity within each
  piece. Originally tried to claim injectivity mod q on ALL of I_q directly — wrong, since
  two indices in J_q could satisfy a_i ≡ a_j (mod 9) while still being disjoint via the extra
  factor of 2 (gcd=18, need a_i not≡a_j mod 18, which is weaker than mod 9). Caught this
  before writing it into result.md.

- Checked: |I_q| <= 3q is NOT better than the trivial 25 for q=9 (27) or q=11 (33). Decided
  to report this honestly rather than oversell it — the real content is the case-split
  structure / cheaper pairwise check, not a smaller headcount. This matches the "Partial
  credit is real" / "reporting failure beats bluffing" rules.

- Noticed in passing: prior task's Lemma 3 range {13,17,19,23} missed q=16=2^4 (also > k/2).
  Not in my assigned scope (task explicitly says (k/3,k/2]); logged as an observation /
  new_task rather than fixed here, to stay in time budget.

- Did not attempt q=7 (<=k/3, needs 3-way split) — explicitly out of range per task wording.
