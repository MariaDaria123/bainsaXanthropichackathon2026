# Swarm log: p4
_generated 2026-09-26T15:34 by tools/swarm_report.py; see SWARM_CONTEXT.md for how to read it_

## Summary
- **Tasks:** 3 done, 4 running, 14 open (9 spawned by agents)
- **Findings (excluding proposed tasks):** 18: conjectured 15, observed 3
- **Passed the 2-critic gate** (kept a strong label): 0
- **Downgraded by the gate** (claimed strong, not accepted twice): 15
- **Workers:** IusesMacBo-a1, IusesMacBo-a2, cloud-1, cloud-2

## Accepted results (two blind ACCEPTs)
- none yet

## Near-proofs (claimed strong, downgraded by the gate)
- claimed **[PROVED]**, now [CONJECTURED]: Minimal counterexample (least k, then least sum m_i) satisfies: 1<gcd<k; m_i | N=lcm pairwise gcds | lcm(1..k-1); every prime power dividing some m_i divides two m's; no m_i is a prime power; no prime divides all m_i; >=3 m's divisible by k-1 (if exactly 3, two more divisible by k-2); density sum 1/gcd(h_i,M)<=1 on every subfamily; for 7<=k<=30 each prime p>=k/2 divides 0 or exactly 2 m's. Also k>=7 (k<=6 excluded by O'Bryant sec 4.1, audited line by line; O'Bryant's unargued 'k>=5' remark closed via items 4',5,6). These are all constraints in O'Bryant Lemma 6; his Grow search (k<=19) uses only C1,C2,C4 and the density test with M=lcm of gcds.  
  _IusesMacBo-a1 · task `p4-literature-ce0fb3` · downgraded: MINOR/MINOR (round 2)_
- claimed **[PROVED]**, now [CONJECTURED]: O'Bryant Lemma 6 item 8, case k=30, l=3: the claim 'two of 17,19,23,29 lie in separate P_i' is unjustified; repaired: some large prime q!=p lies in some P_s, divides >=10 moduli, contradicting item 8's argument applied to q (needs >=10 disjoint nonempty subsets of 9 primes).  
  _IusesMacBo-a1 · task `p4-literature-ce0fb3` · downgraded: MINOR/MINOR (round 2)_
- claimed **[PROVED]**, now [CONJECTURED]: For k in {8,12,14,18,20,24,30}: if DCCC holds for all sizes <k then it holds for k. For 24 and 30 this is conditional on sizes 21,22,23 (not proved in fetched literature).  
  _IusesMacBo-a1 · task `p4-literature-ce0fb3` · downgraded: MINOR/MINOR (round 2)_
- claimed **[PROVED]**, now [CONJECTURED]: O'Bryant Lemma 6 ends item 6 with 'this proves k>=5' without argument; closed: for k=4, item 5 gives >=3 multiples of 3; all 4 contradicts no-prime-divides-all (C4'), exactly 3 needs two more multiples of 2 among 1 remaining modulus.  
  _IusesMacBo-a1 · task `p4-literature-ce0fb3` · downgraded: MINOR/MINOR (round 2)_
- claimed **[PROVED]**, now [CONJECTURED]: For k=25, if a prime power p^e satisfies p^e >= 25, then in any pairwise-disjoint counterexample family of size 25 (all pairwise gcds <= 24), at most one modulus m_i has v_p(m_i) >= e (else gcd(m_i,m_j) >= p^e >= 25, contradiction).  
  _cloud-1 · task `p4-proof-9c5676` · downgraded: MINOR/MINOR (round 2)_
- claimed **[PROVED]**, now [CONJECTURED]: If index i's p-adic valuation dominates every other modulus's p-adic valuation down to some level c, lowering v_p(m_i) to exactly c changes no pairwise gcd of the family and preserves pairwise disjointness (Lemma 2).  
  _cloud-1 · task `p4-proof-9c5676` · downgraded: MINOR/MINOR (round 2)_
- claimed **[PROVED]**, now [CONJECTURED]: Main reduction theorem: any size-25 counterexample to the disjoint-congruence-classes claim can be transformed (same a_i, same pairwise gcds) into a size-25 counterexample where every modulus divides L = lcm(1,...,24) = 5354228880 = 2^4*3^2*5*7*11*13*17*19*23 (1920 divisors), so a search for a size-25 counterexample may assume WLOG all moduli divide L.  
  _cloud-1 · task `p4-proof-9c5676` · downgraded: MINOR/MINOR (round 2)_
- claimed **[PROVED]**, now [CONJECTURED]: For p in {13,17,19,23} (exactly the primes with k/2 < p < k for k=25) and any size-25 counterexample reduced to divide L, if p divides two distinct moduli m_i,m_j then gcd(m_i,m_j)=p exactly, so the map i -> (a_i mod p) is injective on the index set divisible by p, giving |{i : p | m_i}| <= p, i.e. sum_{i: p|m_i} 1/gcd(m_i,p) <= 1.  
  _cloud-1 · task `p4-proof-9c5676` · downgraded: MINOR/MINOR (round 2)_
- claimed **[COMPUTED]**, now [CONJECTURED]: L=lcm(1,...,24)=5354228880=2^4*3^2*5*7*11*13*17*19*23; E_p (max e with p^e<=24) is 4,2,1,1,1,1,1,1,1 for p=2,3,5,7,11,13,17,19,23 respectively; every p^(E_p+1) is >=25; d(L)=1920.  
  _cloud-1 · task `p4-proof-9c5676` · downgraded: MINOR/MINOR (round 2)_
- claimed **[PROVED]**, now [CONJECTURED]: For subgroups G_1..G_k of finite index in any group G, letting N be the intersection of the cores of the G_i, G/N is finite and a family of cosets x_1G_1,...,x_kG_k is pairwise disjoint in G iff the corresponding cosets are pairwise disjoint in G/N, with the same indices n_i; hence WLOG G is finite.  
  _cloud-2 · task `p4-proof-f59824` · downgraded: MINOR/MINOR (round 2)_
- claimed **[PROVED]**, now [CONJECTURED]: If [G:G_i] and [G:G_j] are coprime finite indices then xG_i and yG_j intersect for every x,y in G; hence in a pairwise disjoint family gcd(n_i,n_j) >= 2 for every i<j.  
  _cloud-2 · task `p4-proof-f59824` · downgraded: MINOR/MINOR (round 2)_
- claimed **[PROVED]**, now [CONJECTURED]: For a pairwise disjoint family of finite-index cosets x_1G_1,...,x_kG_k, sum_i 1/n_i <= 1.  
  _cloud-2 · task `p4-proof-f59824` · downgraded: MINOR/MINOR (round 2)_
- claimed **[PROVED]**, now [CONJECTURED]: If gcd(n_i,n_j) in {2,3,4,5} for all pairs among n_1..n_6 (necessary for a k=6 counterexample by Lemma 2 plus the counterexample condition gcd<=5), then writing D_i = {p in {2,3,5}: p|n_i}, every D_i is nonempty and |D_i cap D_j| = 1 for all i != j.  
  _cloud-2 · task `p4-proof-f59824` · downgraded: MINOR/MINOR (round 2)_
- claimed **[COMPUTED]**, now [CONJECTURED]: Exhaustive search over all 7^6=117649 assignments D:{1..6}->{nonempty subsets of {2,3,5}} finds exactly 147 valid tuples (|D_i cap D_j|=1 for all pairs), collapsing to exactly 4 patterns up to the S_6 x S_3 symmetry (relabel indices, relabel primes).  
  _cloud-2 · task `p4-proof-f59824` · downgraded: MINOR/MINOR (round 2)_
- claimed **[COMPUTED]**, now [CONJECTURED]: Each of the 4 shared-prime patterns for a k=6 candidate can be realized by explicit integers n_1..n_6 with every pairwise gcd in {2,3,4,5} and sum 1/n_i <= 1 (using distinct large prime cofactors coprime to 2,3,5), so the density bound (iii) never by itself excludes any of the 4 patterns.  
  _cloud-2 · task `p4-proof-f59824` · downgraded: MINOR/MINOR (round 2)_

## Dead ends and obstructions
- [CONJECTURED] O'Bryant Lemma 6 item 8, case k=30, l=3: the claim 'two of 17,19,23,29 lie in separate P_i' is unjustified; repaired: some large prime q!=p lies in some P_s, divides >=10 moduli, contradicting item 8's argument applied to q (needs >=10 disjoint nonempty subsets of 9 primes).  _(IusesMacBo-a1 · `p4-literature-ce0fb3`)_
- [CONJECTURED] O'Bryant Lemma 6 ends item 6 with 'this proves k>=5' without argument; closed: for k=4, item 5 gives >=3 multiples of 3; all 4 contradicts no-prime-divides-all (C4'), exactly 3 needs two more multiples of 2 among 1 remaining modulus.  _(IusesMacBo-a1 · `p4-literature-ce0fb3`)_
- [OBSERVED] Lemmas 1-3 and the 4-pattern classification give only necessary numeric conditions on the indices n_1..n_6 of a hypothetical k=6 group-form counterexample; they do not construct or rule out an actual group G with subgroups of these indices and pairwise disjoint cosets, so k=6 for the group form remains open after this task.  _(cloud-2 · `p4-proof-f59824`)_

## Task timeline (done tasks)
| Finished | Task | Worker | Minutes | Critics | Parent | Result |
|---|---|---|---|---|---|---|
| 15:23 | (a) Pin down the current certified boundary (our cell c5 + O'Bryant 20 | IusesMacBo-a1 | 12 | MINOR/MINOR (round 2) | human | `swarm/results/p4-literature-ce0fb3/result.md` (7bb9ad3 15:23) |
| 15:24 | (a) For k=25 prove the strongest finite reduction: restrict moduli to  | cloud-1 | 20 | MINOR/MINOR (round 2) | human | `swarm/results/p4-proof-9c5676/result.md` (c93ff65 15:24) |
| 15:24 | (c) Prove the basic reductions for the coset form: (i) WLOG G finite ( | cloud-2 | 20 | MINOR/MINOR (round 2) | human | `swarm/results/p4-proof-f59824/result.md` (38a82b0 15:24) |

## Task tree (who spawned what)
- `p4-proof-f69ad5` [open] (b) Prove gcd(m_i,m_j) >= c*k with an explicit absolute c for a natural special class: all moduli sq
- `p4-literature-f8d1f7` [open] (c) Find the source of the coset version (Z.-W. Sun's group conjecture; relation to Herzog-Schonheim
- `p4-proof-805c62` [open] (c) Settle k=6 for a natural class of groups: abelian (reduce to integer congruences), nilpotent (pr
- `p4-construction-2758d8` [open] (a) Hunt for counterexamples at k=25..30 (pairwise disjoint, all pairwise gcd <= k-1) by heuristic, 
- `p4-certificate-acdc9a` [open] (c) Exclude k=6 counterexamples in all finite groups of order <= N, N as large as feasible (sympy.co
- `p4-obstruction-324244` [open] (b) Locate exactly where the sieve / Rankin-trick step loses the exp factor. Either improve the cons
- `p4-proof-e26a5c` [open] (b) Write a COMPLETE proof of gcd(m_i,m_j) >= k*exp(-(2+o(1))*sqrt(log k/log log k)) (adapting Forna
- `p4-literature-0afc53` [open] (b) Read Fornal-Sun, arXiv 2607.24655 (July 2026) in full. Extract every lemma with exact hypotheses
- `p4-certificate-68026c` [claimed] (a) Certified exhaustive search deciding k=25 with tools/cert.py over the reduced domain from the bo
- `p4-literature-ce0fb3` [done] (a) Pin down the current certified boundary (our cell c5 + O'Bryant 2006, arXiv math/0604347: k<=20,
  - `p4-literature-86341a` [open] (a) Locate and check a proof of the group form for k=5 (cell claims known) and test whether O'Bryant
  - `p4-certificate-3ea465` [claimed] (a) Write a certified (tools/cert.py, <10 min) search for k=21,22,23 using constraints C1-C7 (moduli
  - `p4-proof-9f5f3f` [claimed] (a) Extend O'Bryant Lemma 6 item 8 beyond k=30: for 31<=k<=210 the omega-collision gives gcd>=210 wh
- `p4-proof-9c5676` [done] (a) For k=25 prove the strongest finite reduction: restrict moduli to divisors of L=lcm(1..24), use 
  - `p4-proof-d8a34e` [open] (a) Check whether the same valuation-lowering technique (Lemma 2) plus Lemma 1's one-exceeder argume
  - `p4-certificate-6d543a` [open] (a) Using the Main Reduction Theorem's finite domain (moduli restricted to the 1920 divisors of L=lc
  - `p4-proof-2d83fd` [claimed] (a) Extend Lemma 3's density/injectivity argument to primes p in (k/3,k/2], e.g. p in {9,11} for k=2
- `p4-proof-f59824` [done] (c) Prove the basic reductions for the coset form: (i) WLOG G finite (pass to G/N, N = intersection 
  - `p4-construction-15017f` [open] (c) For each of the 4 numeric patterns (I-IV in result.md), attempt to construct an actual finite gr
  - `p4-verify-84a21e` [open] (c) Check whether the numeric (abelian, G=Z, G_i=m_iZ) disjoint-congruence-class form of k=6 is alre
  - `p4-pattern-20e03c` [open] (c) Refine the 4-pattern classification by also tracking the exponent of the shared prime 2 (v_2=1 g
