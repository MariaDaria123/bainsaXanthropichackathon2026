**Status:** PARTIAL (basic reductions proved, k=6 numeric candidates classified, group-theoretic realizability left open)

# Target (restated exactly)

Group form (p4 c6, part (c)). Let G be a group, let G_1,…,G_k ≤ G be subgroups of finite
index n_i = [G:G_i], and let x_1G_1,…,x_kG_k be pairwise disjoint cosets. Question: is
there a pair i<j with gcd(n_i,n_j) ≥ k? Known for k ≤ 5, open for every k ≥ 6.

**This task's goal** (not the full question): prove the three basic reductions

  (i)   WLOG G is finite (pass to G/N, N = intersection of the cores of the G_i),
  (ii)  coprime indices force the cosets to meet, so every pairwise gcd is ≥ 2,
  (iii) Σ 1/n_i ≤ 1,

and then enumerate all index 6-tuples (n_1,…,n_6) with pairwise gcd in [2,5] and
Σ1/n_i ≤ 1 that a k=6 counterexample could have. (A counterexample to "gcd ≥ 6" must
have *every* pairwise gcd ≤ 5; combined with (ii) this means every pairwise gcd lies in
{2,3,4,5}.)

---

# Lemma 1 (reduction to a finite group) [PROVED]

**Statement.** Let G, G_1,…,G_k, x_1,…,x_k be as above, n_i=[G:G_i]<∞. Let
Core_i = core_G(G_i) = ∩_{g∈G} gG_ig^{-1} and N = ∩_{i=1}^k Core_i. Then:
(a) N is a normal subgroup of G of finite index;
(b) Ḡ := G/N is a finite group, each Ḡ_i := G_i/N is a subgroup of Ḡ with
    [Ḡ:Ḡ_i] = n_i;
(c) for every i,j and every x,y ∈ G: xG_i ∩ yG_j ≠ ∅ in G ⟺ x̄Ḡ_i ∩ ȳḠ_j ≠ ∅ in Ḡ
    (bar = image in Ḡ).
Hence x_1G_1,…,x_kG_k is pairwise disjoint in G iff x̄_1Ḡ_1,…,x̄_kḠ_k is pairwise
disjoint in the *finite* group Ḡ, with the same index data n_1,…,n_k. So any
counterexample can be assumed to live in a finite group.

**Proof.**

*(a) N normal of finite index.* Fix i. G acts on the set X_i = G/G_i of left cosets
(|X_i| = n_i) by left multiplication: g·(xG_i) = (gx)G_i. This defines a homomorphism
φ_i : G → Sym(X_i), and Sym(X_i) ≅ S_{n_i} after numbering X_i. Compute the kernel:
g ∈ ker φ_i ⟺ gxG_i = xG_i for all x ∈ G ⟺ x^{-1}gx ∈ G_i for all x ⟺ g ∈ xG_ix^{-1}
for all x ⟺ g ∈ ∩_{x∈G} xG_ix^{-1} = Core_i. So Core_i = ker φ_i, in particular Core_i
is normal in G (kernel of a homomorphism), and G/Core_i ≅ im(φ_i) ≤ S_{n_i}, so
[G:Core_i] = |G/Core_i| divides n_i! and in particular is finite.

N = ∩_i Core_i is an intersection of normal subgroups, hence normal. The map
ρ: G → ∏_{i=1}^k G/Core_i, g ↦ (gCore_1,…,gCore_k) is a homomorphism with kernel
∩_i Core_i = N, so G/N embeds into ∏_i G/Core_i, giving
[G:N] = |G/N| ≤ ∏_{i=1}^k |G/Core_i| = ∏_{i=1}^k [G:Core_i] ≤ ∏_{i=1}^k n_i! < ∞.
So N has finite index. Also N ⊆ Core_i ⊆ G_i for every i (Core_i ⊆ G_i because the
identity coset G_i is fixed by every element of Core_i = ker φ_i, i.e. gG_i = G_i for
g ∈ Core_i, i.e. g ∈ G_i).

*(b) Ḡ finite, indices preserved.* Ḡ = G/N is a group of order [G:N] < ∞, i.e. finite.
Since N ⊆ G_i and N ⊴ G, the image Ḡ_i := G_i/N = {gN : g ∈ G_i} is a subgroup of Ḡ.
Define ψ: G/G_i → Ḡ/Ḡ_i by ψ(gG_i) = (gN)Ḡ_i. This is well defined and a bijection:
- Well defined: if gG_i = g'G_i then g^{-1}g' ∈ G_i, so (g^{-1}g')N ∈ Ḡ_i (as N ⊆ G_i,
  the quotient map restricted to G_i surjects onto Ḡ_i), i.e. (gN)^{-1}(g'N) ∈ Ḡ_i, i.e.
  (gN)Ḡ_i = (g'N)Ḡ_i.
- Injective: if (gN)Ḡ_i = (g'N)Ḡ_i then (g^{-1}g')N ∈ Ḡ_i, i.e. g^{-1}g' ∈ G_iN = G_i
  (using N ⊆ G_i, so G_iN = G_i), i.e. gG_i = g'G_i.
- Surjective: every element of Ḡ/Ḡ_i is (gN)Ḡ_i for some g ∈ G because the quotient
  map G → Ḡ is surjective.
So ψ is a bijection and [Ḡ:Ḡ_i] = [G:G_i] = n_i.

*(c) Disjointness transfers.*
(⇒) If z ∈ xG_i ∩ yG_j, write z = xg_i = yg_j with g_i ∈ G_i, g_j ∈ G_j. Then
z̄ = x̄ ḡ_i with ḡ_i ∈ Ḡ_i, so z̄ ∈ x̄Ḡ_i; likewise z̄ ∈ ȳḠ_j. So x̄Ḡ_i ∩ ȳḠ_j ≠ ∅.
(⇐) If w ∈ x̄Ḡ_i ∩ ȳḠ_j, pick any preimage z ∈ G of w under G → Ḡ (surjective). Since
w = x̄ ḡ_i for some ḡ_i ∈ Ḡ_i = G_i/N, we have zN = xg_iN for some g_i ∈ G_i, so
z ∈ xg_iN ⊆ xG_i (using N ⊆ G_i, g_iN ⊆ G_i). Likewise z ∈ yG_j. So xG_i ∩ yG_j ≠ ∅.

This proves (c), and (a)+(b)+(c) together give Lemma 1. ∎

---

# Lemma 2 (coprime indices ⟹ cosets meet ⟹ pairwise gcd ≥ 2) [PROVED]

**Statement.** If [G:G_i]=n_i, [G:G_j]=n_j and gcd(n_i,n_j)=1, then for **every** choice
of x,y ∈ G the cosets xG_i, yG_j intersect. Consequently, in any pairwise disjoint
family x_1G_1,…,x_kG_k of finite-index cosets, gcd(n_i,n_j) ≥ 2 for every i<j.

**Proof.** By Lemma 1 applied to the two-element family {G_i,G_j} (using
N' = Core_i ∩ Core_j) we may assume G =: H is finite, with A := G_i, B := G_j,
[H:A]=n_i, [H:B]=n_j, gcd(n_i,n_j)=1 — cosets meet in the original group iff they meet
in H, so it suffices to treat this finite case.

*Step 1: [H:A∩B] = n_i n_j exactly.* Let C = A∩B. By the tower law,
[H:C] = [H:A]·[A:C] = n_i·[A:C], and also [H:C] = [H:B]·[B:C] = n_j·[B:C]. In
particular n_i | [H:C] and n_j | [H:C]; since gcd(n_i,n_j)=1, n_i n_j | [H:C].

For the reverse inequality, the map A/C → H/B, aC ↦ aB is well defined (aC=a'C ⟹
a^{-1}a' ∈ C ⊆ B ⟹ aB=a'B) and injective (aB=a'B, a,a'∈A ⟹ a^{-1}a' ∈ B ∩ A = C ⟹
aC=a'C). So [A:C] ≤ [H:B] = n_j, hence [H:C] = n_i[A:C] ≤ n_i n_j.
Combining, [H:C] = n_i n_j exactly, and then [A:C] = n_j exactly.

*Step 2: AB = H.* By Lagrange (H finite), |A| = |H|/n_i, |B| = |H|/n_j,
|C| = |A|/[A:C] = |H|/(n_i n_j). The map A×B → H, (a,b) ↦ ab, has image AB, and for
a fixed product ab, the pairs (a',b') ∈ A×B with a'b'=ab are exactly a'=ac^{-1}, b'=cb
for c ∈ C (check: a'b'=ab ⟺ a^{-1}a' = b(b')^{-1} =: c; the left side is in A, the
right side is in B, so c ∈ A∩B = C; conversely any c ∈ C gives a valid pair). So every
element of AB has exactly |C| preimages, giving |AB| = |A||B|/|C| =
(|H|/n_i)(|H|/n_j)/(|H|/(n_in_j)) = |H|. Since AB ⊆ H and |AB| = |H| < ∞, AB = H.

*Step 3: cosets meet.* For x,y ∈ H: xA ∩ yB ≠ ∅ ⟺ ∃ a∈A,b∈B with xa=yb ⟺
x^{-1}y = ab^{-1} ∈ AB (using that B is a subgroup, b^{-1} ranges over B as b does).
Since AB = H, x^{-1}y ∈ H always holds, so xA ∩ yB ≠ ∅ for every x,y ∈ H.

By the reduction (Lemma 1(c) for the pair), xG_i ∩ yG_j ≠ ∅ for every x,y in the
original G. In particular a pairwise disjoint family cannot have gcd(n_i,n_j)=1 for any
pair, so gcd(n_i,n_j) ≥ 2 for all i<j. ∎

---

# Lemma 3 (density bound) [PROVED]

**Statement.** For a pairwise disjoint family x_1G_1,…,x_kG_k of finite-index cosets,
Σ_{i=1}^k 1/n_i ≤ 1.

**Proof.** By Lemma 1, WLOG G is finite, say |G| = M < ∞. By Lagrange,
|G_i| = M/n_i, so |x_iG_i| = M/n_i for every i. The sets x_1G_1,…,x_kG_k are pairwise
disjoint subsets of the finite set G, so the sum of their sizes is at most |G|:
Σ_{i=1}^k M/n_i ≤ M. Dividing by M > 0 gives Σ_{i=1}^k 1/n_i ≤ 1. ∎

---

# Classification of the numeric candidates for k = 6

**Scope note, up front:** the literal set of integer 6-tuples (n_1,…,n_6) satisfying
gcd ∈ [2,5] pairwise and Σ1/n_i ≤ 1 is *infinite* — `scripts/check_scaling.py` itself
produces one such tuple per pattern and shows it can always be scaled up by fresh
coprime cofactors. So "enumerate all index 6-tuples" is answered here by classifying
the finite invariant that actually controls the pairwise-gcd constraints — the
shared-{2,3,5}-prime pattern D_i = {p∈{2,3,5}: p|n_i} — not by listing literal n_i
values. What follows proves this reduction is lossless for the gcd constraints
(Sub-lemma, [PROVED]), then enumerates the reduced object exhaustively
([COMPUTED]), then exhibits one concrete integer witness per pattern showing the
density bound never excludes it ([COMPUTED]).

A counterexample of size k=6 needs, for every i<j: gcd(n_i,n_j) ≤ 5 (else that pair
already witnesses the statement) **and** gcd(n_i,n_j) ≥ 2 (Lemma 2), so
gcd(n_i,n_j) ∈ {2,3,4,5} for all 15 pairs.

**Sub-lemma (shared-prime pattern) [PROVED].** For i ≠ j write
D_i = {p ∈ {2,3,5} : p | n_i}. If gcd(n_i,n_j) ∈ {2,3,4,5} for all i<j then:
(a) D_i ≠ ∅ for every i, and
(b) |D_i ∩ D_j| = 1 for every i ≠ j.

*Proof.* A gcd value in {2,3,4,5} is divisible by **at most one** prime ≤ 5, since
2·3=6, 2·5=10, 3·5=15 are all > 5 and would force gcd ≥ 6 if two different primes ≤5
both divided it. Also gcd(n_i,n_j) cannot be divisible by any prime q ≥ 7 (that would
force gcd(n_i,n_j) ≥ q ≥ 7 > 5). So the only primes that can divide gcd(n_i,n_j) are
elements of {2,3,5}, and at most one of them does.
- If D_i ∩ D_j = ∅ for some i≠j, then no prime ≤5 divides both n_i,n_j, and (by the
  previous paragraph) no prime ≥7 can divide gcd(n_i,n_j) either, so gcd(n_i,n_j)=1,
  contradicting gcd(n_i,n_j) ≥ 2. So |D_i ∩ D_j| ≥ 1, and D_i∩D_j can contain at most
  one prime (else gcd would be a multiple of two distinct primes ≤5, forcing gcd ≥ 6,
  excluded), so |D_i∩D_j| = 1.
- Taking j any other index and using |D_i∩D_j|=1 ≥ 1 shows D_i ≠ ∅. ∎

**Enumeration [COMPUTED].** `scripts/enumerate_patterns.py` brute-forces every function
D: {1,…,6} → {seven nonempty subsets of {2,3,5}} (7^6 = 117 649 tuples, exhaustive by
construction — every D_i is one of exactly the 7 nonempty subsets of the 3-element set
{2,3,5}, so this range is complete) and keeps exactly those with |D_i∩D_j|=1 for all
i<j (147 valid tuples), then quotients by the full symmetry group S_6 (permuting the 6
indices) × S_3 (permuting the primes 2,3,5). Runtime: 0.08 s (rerun with
`python3 scripts/enumerate_patterns.py`).

Result: **exactly 4 patterns** up to this symmetry:

| Pattern | D-multiset (canonical) | Description |
|---|---|---|
| I   | {2},{2},{2},{2},{2},{2} | all six share only prime 2 |
| II  | {2},{2},{2},{2},{2},{2,3} | five share only 2, one shares 2 and 3 |
| III | {2},{2},{2},{2},{2,3},{2,5} | four share only 2, two share 2 with a second prime each (3 and 5) |
| IV  | {2},{2},{2},{2},{2},{2,3,5} | five share only 2, one divisible by all of 2,3,5 |

(The prime "2" here is a representative of the symmetry class; relabelling 2↔3↔5 gives
the other 3+6+3+3−... — concretely 3 rotations of Pattern I/III/IV and 6 of Pattern II
under S_3, i.e. 15 labelled variants in total, all listed by the same script if the
S_3 quotient is skipped.)

A hand argument reaching the same 4 patterns (independent cross-check of the computer
search): a repeated 2-or-3-element subset among the D_i is impossible, since if D_i=D_j
with |D_i|≥2 then |D_i∩D_j|=|D_i|≥2, violating the sub-lemma; any two *distinct*
2-element subsets of a 3-set automatically meet in exactly 1 element, so several
distinct doubletons are mutually consistent, but a singleton {q} is only consistent
with a doubleton if q lies in it, and the full set {2,3,5} forces every other D_j to be
a common singleton (else two different singletons among the rest would meet in ∅).
Checking which combinations fill 6 slots gives exactly patterns I–IV (three distinct
doubletons only fill 3 slots and admit no valid fourth entry, so they cannot extend to
k=6) — matching the exhaustive search exactly.

**Realizability of the numeric constraints (density) [COMPUTED].** For each of the 4
patterns, `scripts/check_scaling.py` exhibits an explicit integer 6-tuple with every
pairwise gcd in {2,3,4,5} (in fact all equal to 2 in these examples) and
Σ 1/n_i ≤ 1, using distinct "private" prime cofactors (11,13,17,19,23,29,31) that are
coprime to 2,3,5 and to each other, computed with exact `Fraction` arithmetic. Runtime:
< 0.1 s. Sample output:
```
Pattern I  : n = [22, 26, 34, 38, 46, 58],   gcds all = 2, sum 1/n_i = 5503064/30808063
Pattern II : n = [66, 26, 34, 38, 46, 58],   gcds all = 2, sum 1/n_i = 13708459/92424189
Pattern III: n = [66, 130, 34, 38, 46, 58],  gcds all = 2, sum 1/n_i = 54323189/462120945
Pattern IV : n = [330, 26, 34, 38, 46, 58],  gcds all = 2, sum 1/n_i = 62940829/462120945
```
All four sums are (far) below 1, exactly, with exact integer gcds computed by
`math.gcd`. This shows that the density bound (iii) never rules out any of the 4
patterns: coprime "private" cofactors can always be inflated to push Σ1/n_i as low as
needed, without disturbing the pairwise gcds.

---

# What remains open

Lemmas 1–3 and the classification are proved reductions to **necessary numeric
conditions** on the tuple (n_1,…,n_6). They show:
- gcd(n_i,n_j) ≥ 2 always (Lemma 2), and
- Σ1/n_i ≤ 1 always (Lemma 3), and
- if additionally every pairwise gcd is ≤ 5 (i.e. we are looking at a would-be
  counterexample to k=6), the shared-prime structure of the n_i must be one of exactly
  4 patterns (up to relabelling primes and reordering indices).

They do **not** show that any of these 4 numeric patterns can be realized by an actual
group G with subgroups G_1,…,G_6 of these indices and pairwise disjoint cosets
x_1G_1,…,x_6G_6 — nor do they rule this out. That realizability question (constructing
such a G, or proving none of the 4 patterns can occur as *actual* disjoint cosets) is
exactly the open content of k=6 for the group form, and is not resolved here. In
particular the numeric analogue (disjoint congruence classes, problems p4 c1–c5) is a
necessary special case of this question when G = ℤ and G_i = m_iℤ, but the group form
is more general (non-abelian G, non-normal G_i), so even a full resolution of the
numeric k=6 case would not by itself settle the group form.

# Cited vs ours

Lemma 1(a)'s fact "the kernel of the action on cosets is the core, index divides n!"
and the standard formula |AB| = |A||B|/|A∩B| (Step 2 of Lemma 2, used only for finite
H) are classical group-theory facts; we reprove both from scratch above rather than
citing them, since CLAUDE.md rule 2 requires citing ≠ proving. Everything else
(Lemma 1(b),(c), Lemma 2 Steps 1 and 3, Lemma 3, the shared-prime sub-lemma, the
4-pattern classification, the scaling construction) is original work for this task; we
are not aware of a published source for the group-form reductions or for the k=6
pattern classification specifically.

# Verification
- `python3 swarm/results/p4-proof-f59824/scripts/enumerate_patterns.py` — exhaustive
  over all 7^6 = 117 649 candidate D-assignments, 0.08 s, deterministic, exact
  (frozenset/int arithmetic only).
- `python3 swarm/results/p4-proof-f59824/scripts/check_scaling.py` — exact `Fraction`
  and `math.gcd` arithmetic, < 0.1 s, asserts pass for all 4 patterns.
- `python3 swarm/results/p4-proof-f59824/scripts/cert_search.py` — same enumeration,
  wrapped through `tools.cert.Certificate` per CLAUDE.md rule 4 (records domain,
  domain_proof, node count 117649, and all 4 surviving patterns as decided
  survivors with minimal_part/minimality_proof); writes
  `swarm/results/p4-proof-f59824/scripts/certificate.json`. 0.08 s, reran and
  re-asserts 147 valid / 4 patterns.

**Certificate-protocol gap (flagged by both critics, not yet closed):** this task is
authorized to write only inside `swarm/results/p4-proof-f59824/`, so `cert_search.py`
above writes its certificate there, not to `problems/p4/cells/c6/cert/search.py`
(currently just a `.gitkeep`). That means `python tools/rerun.py p4 c6` and
`python tools/gate.py p4 c6` cannot yet run against this work — promoting this
finding still requires copying `cert_search.py`'s logic verbatim into
`problems/p4/cells/c6/cert/search.py` and running `tools/rerun.py p4 c6` at
promotion time. This is an explicit outstanding step, not a silent gap.
