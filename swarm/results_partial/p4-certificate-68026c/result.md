**Status:** OPEN (partial progress). k = 25 is NOT decided. Only the branches listed as certified below are claimed.

**Target (cell p4 c6(a)).** Decide k = 25: must every family of 25 pairwise disjoint classes a_i (mod m_i) have a pair with gcd(m_i, m_j) ≥ 25? A *counterexample* is 25 pairwise disjoint classes with every pairwise gcd ≤ 24.

Notation. For a prime p < 25 let e_p be the largest e with p^e ≤ 24: e_2 = 4, e_3 = 2, e_p = 1 for p ∈ {5,7,11,13,17,19,23}. For a set P of primes < 25 put L_P = ∏_{p∈P} p^{e_p}; L_all = 16·9·5·7·11·13·17·19·23.

---

## Claim 1 [PROVED] (Lemma A, reduction)
If a counterexample of size 25 exists, then a counterexample of size 25 exists in which every modulus divides L_all, and whose moduli are, prime by prime, obtained from the original ones by lowering exponents (so the set of primes used can only shrink).

**Proof.** Let (a_i, m_i), i = 1..25, be a counterexample. Two facts are used throughout:
(F1) by (∗), disjointness of classes i, j depends only on g_ij = gcd(m_i, m_j) and on a_i − a_j mod g_ij;
(F2) a disjoint pair has g_ij ≥ 2, since 1 divides every a_i − a_j.

Step 1 (primes p ≥ 25). Suppose p ≥ 25 is prime and p | m_i. If also p | m_j for some j ≠ i, then p | g_ij, so g_ij ≥ 25, contradicting g_ij ≤ 24. So p divides m_i and no other modulus. Replace m_i by m_i' = m_i / p^{v_p(m_i)} and a_i by a_i mod m_i'. For every j ≠ i, p ∤ m_j, so gcd(m_i', m_j) = gcd(m_i, m_j) = g_ij. Since g_ij | m_i' and a_i' ≡ a_i (mod m_i'), we get a_i' − a_j ≡ a_i − a_j (mod g_ij). By (F1) every pair keeps its disjointness status and every gcd is unchanged. By (F2) m_i' ≥ g_ij ≥ 2. Repeat for each prime ≥ 25 dividing some modulus (finitely many).

Step 2 (primes p < 25). Fix a prime p < 25 and write v_i = v_p(m_i). For i ≠ j, p^{min(v_i, v_j)} divides g_ij ≤ 24, hence min(v_i, v_j) ≤ e_p. So at most one index i has v_i > e_p (two such indices would give a pair with min > e_p). If such i exists, replace m_i by m_i' = m_i / p^{v_i − e_p} and a_i by a_i mod m_i'. For j ≠ i we have v_j ≤ e_p, so min(v_p(m_i'), v_j) = min(e_p, v_j) = v_j = min(v_i, v_j), and the exponents of all other primes are untouched; therefore gcd(m_i', m_j) = g_ij. As in Step 1, g_ij | m_i' gives a_i' ≡ a_i (mod g_ij), and by (F1) disjointness is preserved; all gcds are unchanged. Do this for each of the 9 primes below 25; a step for prime p does not change any other prime's exponents, so after all steps v_p(m_i) ≤ e_p for all p and i.

The result is 25 pairwise disjoint classes (pairwise disjoint classes are distinct) with the same pairwise gcds, all ≤ 24, and every modulus divides L_all. Primes were only removed, never added. ∎

**Branching.** Every reduced counterexample has a prime support S = {p : p | m_i for some i} ⊆ {2,3,5,7,11,13,17,19,23}. Branch P covers every reduced counterexample with S ⊆ P, i.e. every modulus divides L_P. Deciding k = 25 means certifying branch P = all nine primes.

## Claim 2 [COMPUTED] (certified branches)
There is no family of 25 pairwise disjoint classes with every modulus dividing L_P and every pairwise gcd ≤ 24, for P = {2,3,5} (L = 720) and P = {2,3,7} (L = 1008). These contain the branches {2}, {3}, {2,3}, {2,5}, which were also run separately. Wall clocks on an Apple laptop, single core: 390 s and 375 s, under the 10-minute limit but not by a wide margin.

Combined with Lemma A: **no counterexample of size 25 has all its prime factors < 25 inside {2,3,5}, or all inside {2,3,7}** (after reduction: a counterexample whose moduli use only primes in P ∪ {primes ≥ 25} reduces to one in branch P, since Step 1 removes primes ≥ 25 and Step 2 keeps the support inside P).

| branch P | L_P | classes | nodes | wall | status |
|---|---|---|---|---|---|
| {2} | 16 | 30 | 24 | <0.01 s | certified, 0 survivors |
| {3} | 9 | 12 | 6 | <0.01 s | certified, 0 survivors |
| {2,5} | 80 | 185 | 139 | 0.01 s | certified, 0 survivors |
| {2,3} | 144 | 402 | 2133 | 0.1 s | certified, 0 survivors |
| {2,3,5} | 720 | 2417 | 3 987 911 | 390 s | certified, 0 survivors |
| {2,3,7} | 1008 | 3223 | 3 502 201 | 375 s | certified, 0 survivors |

Prune counts (certificate_<P>.json): {2,3,5}: R2 2388, R4 3 984 124, R5 28 554; {2,3,7}: R2 3194, R4 3 499 537, R5 36 368; {2,3}: R2 388, R4 2113, R5 2627; {2,5}: R2 176, R4 130, R5 777; {2}: R2 26, R4 20, R5 52; {3}: R2 10, R4 4, R5 12. (R1 and R3 are built into the enumeration and count 0.)
Earlier run without R5 (240 s cap, not claimed): {2,3,5} reached 980 000 nodes and {2,3,7} 860 000 nodes, both unfinished.

**Enumeration (search.py).** Vertices: all classes (m, a) with m | L_P, m ≥ 2, 0 ≤ a < m, sorted by (m, a). Edge between two classes iff they are disjoint by (∗) and their gcd ≤ 24. A counterexample in the branch is exactly a 25-clique. Depth-first clique search on bitsets with these rules (each also registered with its proof in the certificate):
- R1 canonical order: a family is enumerated only as its increasing index sequence. Proof: both conditions are symmetric; pairwise disjoint classes are distinct, so each family has exactly one increasing listing.
- R2 translation: the first (smallest) class has a = 0. Proof: shifting every residue by −a_1 preserves all differences, hence all disjointness relations and gcds; the smallest class (m_1, a_1) becomes (m_1, 0), which is still smallest (residue 0 is the least residue of modulus m_1; classes of larger modulus stay larger). So every family has a translate whose first class has residue 0.
- R3 compatibility: only classes adjacent to all chosen classes are candidates. Proof: every pair in a counterexample must be disjoint with gcd ≤ 24.
- R4 colouring bound: greedy proper colouring of the candidate set; if (chosen) + (colours) < 25, prune. Proof: colour classes are independent sets; a clique among candidates uses at most one vertex per colour class.
- R5 multiplier: the second class (m_2, a_2) has a_2 = 0 or a_2 | m_2. Proof: the maps x ↦ ux + t (u a unit mod L_P, t any integer) send a class (m, a) to (m, (ua + t) mod m); they keep every modulus, every gcd, and every disjointness relation, because g | a_i − a_j iff g | u(a_i − a_j) when gcd(u, g) = 1. So the image of a counterexample is a counterexample. Pick the image whose sorted list is lexicographically least. Its first class has residue 0: otherwise translating by −a_1 fixes all moduli and turns the first class into (m_1, 0), giving a smaller list (this is R2). Let (m_2, a_2) be its second class and d = gcd(a_2, m_2) (d = m_2 if a_2 = 0). Every unit mod m_2 lifts to a unit mod L_P (m_2 | L_P), so there is a unit u with u·a_2 ≡ d (mod m_2). The map x ↦ ux fixes (m_1, 0), which stays first (moduli do not change and 0 is the least residue), and sends (m_2, a_2) to (m_2, d mod m_2). All other classes have modulus ≥ m_2, so the second class of the image is ≤ (m_2, d mod m_2). If d mod m_2 < a_2 the image is smaller, a contradiction. So a_2 = d mod m_2, i.e. a_2 = 0 or a_2 | m_2. R1, R2 and R5 all describe this one lexicographically least representative, so they apply together.
A branch reports "certified" only if the search finishes; if a 25-clique were found, the script raises an error printing it (none was). Survivors: 0 in every certified branch, so rule 5 of the certificate is vacuous.

**Positive control.** With the test hook GMAX_TEST=k (allowing gcd ≤ k instead of ≤ k−1), the engine finds the family 0,…,k−1 (mod k) for k = 6 and k = 12 in branch {2,3}; (both with R5 in place). Without the hook, an earlier version without R5 also returned no clique for k = 6, 8, 9 in branch {2,3}, consistent with the problem being believed true (not claimed here). This checks the search is not vacuous.

## What remains open
- Every branch not contained in {2,3,5} or {2,3,7}, e.g. {2,3,5,7}, {2,3,11}, {2,3,13}, {2,5,7}, and ultimately P = all nine primes (L_all = 16·9·5·7·11·13·17·19·23 = 5 354 228 880, giving σ(L_all) − 1 = 17 557 585 919 classes, far too many for plain clique search). A proof of k = 25 needs a further reduction lemma, e.g. one removing the primes p ≥ 13 (for these, any two moduli divisible by p have gcd exactly p since 2p > 24).
- Nothing here bears on (b) or (c).

## Cited vs ours
Everything above is ours: Lemma A is elementary and proved in full above; the search and certificates are ours. (∗) is the CRT criterion stated in problem.md.

**Verification:**
`python swarm/results/p4-certificate-68026c/search.py P23 600` (and P2, P3, P25, P235, P237): writes certificate_<P>.json via tools/cert.py, exact integer arithmetic, < 1 s for the small branches, 390 s ({2,3,5}) and 375 s ({2,3,7}).
`python swarm/results/p4-certificate-68026c/rerun.py P2 P3 P25 P23 P235 P237`: re-executes and compares nodes, pruned, n_survivors, n_undecided, finished, certified with the stored certificates: ALL OK for P2 P3 P25 P23 (see rerun_*.json); P235 and P237 reruns: OK, identical counts (reruns ran concurrently, wall 555 s and 526 s; under 600 s but close to the limit, so run them one at a time).
