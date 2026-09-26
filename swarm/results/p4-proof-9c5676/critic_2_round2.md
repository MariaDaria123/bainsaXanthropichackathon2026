# Critic #2 report — p4-proof-9c5676 (blind, fresh context)

Scope actually reviewed: `swarm/results/p4-proof-9c5676/result.md`, `problems/p4/cells/c6/cell.md`,
`problems/p4/problem.md` (for definitions and criterion (*) that result.md relies on), and the
one cited script `swarm/results/p4-proof-9c5676/scripts/check_L.py` (executed). `notes.md`,
`swarm/board/`, other results, and any log were not opened.

## 1. Statement check

Status is declared `PARTIAL` and the write-up is explicit, in its own words, that it proves only
"a reduction lemma" and does **not** decide k = 25. The task goal it was given ("prove the
strongest finite reduction … Full proof of the reduction lemma, written so that a search over the
reduced set is a valid certificate") is exactly what is delivered — no silent weakening, no silent
strengthening, no special case dressed up as the general statement. The Main Reduction Theorem's
statement is a clean, correctly quantified implication ("if a counterexample F of size k=25
exists, then a counterexample F* exists with the same pairwise gcds … and every m_i* | L") plus
its correct contrapositive. Lemma 3 is explicitly scoped to hold only *inside* an already-reduced
family (all m_i* | L) — it is not misapplied to a general F. This passes checklist item 1.

## 2. Step-by-step check

I reconstructed and independently re-derived every proof step (not just read them):

- **Lemma 1** (at most one index can have v_p(m_i) ≥ e when p^e ≥ 25): this is exactly
  "d | a, d | b ⇒ d | gcd(a,b)" applied with d = p^e; if two indices qualified, their gcd would
  be ≥ p^e ≥ 25 > 24, contradicting the counterexample hypothesis. Correct, and essentially
  forced — I could not find a way for it to fail.
- **Corollary 1a/1b**: correct instantiations of Lemma 1 at e = E_p+1 (p ≤ 23) and e = 1 (p ≥ 25).
  I reran `check_L.py` and confirmed p^(E_p+1) ≥ 25 for every p ≤ 23, including the *tight* case
  p = 5 (5² = 25 exactly — the proof would break at p = 5 if k were 26, and the write-up
  correctly flags this as "checked exactly" rather than asserting slack).
- **Lemma 2** (lowering one index's p-exponent down to the max of the rest preserves every gcd
  involving that index, hence disjointness and the gcd multiset): I stress-tested this
  computationally — 119,516 random trials (`p ∈ {2,3,5,7,11,13}`, random m_i, random co-primes,
  c set to the true max of the others' v_p) — zero counterexamples to gcd(m_i,mj) = gcd(m_i',m_j).
  The hand proof (case q ≠ p unaffected; case q = p, min(c, v_p(m_j)) = v_p(m_j) both before and
  after since v_p(m_i) ≥ c ≥ v_p(m_j)) is complete and matches.
- **Composability / induction over primes**: the potentially fragile step. I checked specifically
  whether an index that is the "exceeder" for two different primes p, q can be handled safely by
  two sequential Lemma-2 applications. It can: Lemma 2(i)'s proof establishes v_q(m_i') = v_q(m_i)
  for every q ≠ p "by construction," so a later step at a different prime never disturbs a bound
  already installed, and re-invoking Corollary 1a/1b on the *current* intermediate family F_{t-1}
  (rather than stale information from F_0) is explicitly and correctly justified ("the corollaries
  hold for any such family, not only for F itself" — true, since F_{t-1} is proved to remain a
  counterexample at each step). I did not find a gap here.
- **Main Reduction Theorem**: correctly assembles the above; m_i* | L follows because v_p(m_i*) is
  bounded by E_p for every p ≤ 23 and is 0 for every p ≥ 25, i.e. m_i* | Π p^{E_p} = L. Verified
  the arithmetic (L = 2⁴·3²·5·7·11·13·17·19·23 = 5,354,228,880, d(L)=1920) independently by
  rerunning the script.
- **Lemma 3** (the four half-range primes / density form): I built an actual disjoint family with
  `problems/p4/lib/congruence.py` — 13 classes r (mod 13), r = 0..12 — confirmed pairwise disjoint
  with all pairwise gcd = 13, then confirmed by direct search that **no** 14th class with modulus
  divisible by 13 can be appended while remaining disjoint from all 13 (every residue mod 13 is
  already taken), which is exactly Lemma 3(b)+(c)'s claim (|I_13| ≤ 13) realized at the boundary.
  Part (a)'s "t = 1 forced" step (gcd/p < 2 since gcd ≤ 24, p ≥ 13) is arithmetically exact and
  correctly uses the counterexample hypothesis (gcd ≤ 24), not an unstated assumption. The
  write-up is also honest that this argument does *not* extend to p ≤ 11 (2p ≤ 24 there, so t = 2
  is possible) and does not claim it does.

No instance of "clearly / obviously / routine / similarly / WLOG" without argument. "Trivially"
appears 3 times, each attached to a literal identity (F_0 = F by definition; unchanged pairs of
indices not involving the modified one) rather than a skipped inferential step — acceptable.

## 3. Testable-lemma checks (code run)

- `check_L.py` rerun: output matches the document verbatim (`L = 5354228880`, the 9-prime
  factorisation, all `p^(E_p+1) ≥ 25`, `{13,17,19,23}` as exactly the primes with 2p > 24,
  `d(L) = 1920`), runtime 0.014 s. Exact integer arithmetic (`math.lcm`, `math.gcd`, trial
  division) as claimed, no exact-arithmetic violation in the load-bearing computations.
- My own scripts (not cited by the author, used only to referee): Lemma 1 pigeonhole verified as
  logically forced; Lemma 2 verified over ~1.2×10⁵ random cases; Lemma 3's |I_p| ≤ p bound
  verified concretely against the library's own `disjoint` function at p = 13.

## 4. Cited-code compliance

`check_L.py` is not run through `tools/cert.py`/`tools/rerun.py`. The write-up gives a specific,
correct reason: it computes four fixed numeric quantities by direct exact arithmetic, not an
exhaustive search over a combinatorial domain with pruning rules and survivors — the
`Certificate`/`rerun.py` machinery has no object to attach to here, and forcing it in would not
add any exactness or reproducibility that isn't already present. This is honest rather than a
loophole: the write-up never claims a computational cell is settled, and explicitly names the
future `certify`-track task as the place where the real 5-part certificate belongs. I agree with
this reasoning.

One nitpick, not a correctness issue: `check_L.py`'s `is_prime` helper uses a float
`int(n ** 0.5) + 1` loop bound. For n ≤ 23 this cannot mis-round (floats represent these integers
exactly), and I confirmed the actual output is correct, but CLAUDE.md's rule 4 says computation
must use exact (int/Fraction) or interval arithmetic, and strictly this line is a float operation.
Trivial fix: `math.isqrt(n) + 1`. This does not change any stated result.

## 5. Labels

Every [PROVED] label carries a complete, checkable proof (verified above); no [COMPUTED] or
[CONJECTURED] label is misused; the top-level Status line correctly reads PARTIAL and is not
oversold anywhere in the body (the "What remains open" section is unusually candid about scope:
no search was run, Lemma 3 doesn't cover p ≤ 11, and the 1920²⁵-scale raw product is explicitly
called out as not a real search-cost estimate).

## 6. Literature

"Cited vs ours" section correctly states nothing outside `problem.md`'s own definitions/criterion
is used, names the one preprint found and correctly declines to use it as a black box or cite an
argument from it it could not verify (full text unreachable). No citing-as-proving violation.

## Overall

I could not find a mathematical gap, an overclaim, a mislabeled claim, or a failing computation.
The one issue I found (float sqrt in a helper never used for a load-bearing exact value beyond
n ≤ 23) is cosmetic and does not affect any stated result — I list it as a fix worth making for
strict rule-4 hygiene, not because it currently produces a wrong number.

VERDICT: MINOR — fix: replace `int(n ** 0.5) + 1` with `math.isqrt(n) + 1` in `check_L.py`'s
`is_prime` to keep the script float-free per CLAUDE.md rule 4 (does not change any reported
result; everything else checked out under independent re-derivation and re-execution).
