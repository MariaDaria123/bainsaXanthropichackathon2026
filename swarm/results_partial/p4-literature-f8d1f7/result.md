**Status:** OPEN (partial progress) — literature track only, per task p4-literature-f8d1f7.

**Task target restated.** Part (c) of p4 c6: for a group G, finite-index subgroups G_1,...,G_k
and pairwise disjoint cosets x_1G_1,...,x_kG_k, is there i<j with gcd(n_i,n_j) ≥ k where
n_i=[G:G_i]? Find the source (Sun's group conjecture; relation to Herzog-Schönheim) and the
proof for k≤5.

**Method note (environment constraint).** In this session `WebFetch` was refused by the
egress proxy for every domain tested (arxiv.org, nju.edu.cn, wikipedia.org, r.jina.ai,
even example.com), so no PDF/HTML could be opened directly. All citations below come from
`WebSearch` result snippets (which quote/paraphrase the source pages and give their URLs).
This is weaker than reading the primary source myself: I did **not** verify Zhu's or Sun's
arguments line by line, so nothing here is claimed as independently [PROVED] by this track —
claims are tagged by what the literature asserts, per the task's own tag set.

---

## 1. Source of the conjecture

**[PROVED]** (existence/attribution, i.e. this is a documented fact about the literature, not
a math claim) Zhi-Wei Sun posed in 2004:

> Conjecture 1.2 (Sun). Let a_1G_1,...,a_kG_k (k>1) be finitely many pairwise disjoint left
> cosets in a group G with [G:G_i] < ∞ for all i=1,...,k. Then gcd([G:G_i],[G:G_j]) ≥ k for
> some 1 ≤ i < j ≤ k.

Primary source: Z.-W. Sun, *Groups and Combinatorial Number Theory* —
https://arxiv.org/pdf/math/0411289 (2004 preprint/talk; Conjecture 1.2 is cited under this
number by the 2008 confirmation paper below). Also restated in Sun's own conjecture list:
*Notes on Conjectures of Zhi-Wei Sun* — http://maths.nju.edu.cn/~zwsun/conj.pdf, and in a
talk *A talk given at Université de Saint-Étienne (France) on Feb. 1, 2005* —
http://maths.nju.edu.cn/~zwsun/Cover.pdf. (These last two nju.edu.cn URLs could not be
opened in this session — WebFetch was blocked — so they are reported as *found* by search,
not as *read*; treat them as secondary confirmation, not as independently checked.)

This is the exact statement quoted in the swarm's own cell text (part (c)), matching what
WebSearch surfaces for arXiv:0807.2207's abstract/introduction.

## 2. Relation to the Herzog–Schönheim conjecture

**[GAP]** (conceptual — this is a "how do the two conjectures relate" question, not a proved
theorem, so it gets no proved/computed label)

The Herzog–Schönheim conjecture (1974) is about a **coset partition**: G_1α_1,...,G_sα_s
cover *all* of G and are pairwise disjoint (an exact partition of the whole group), and it
concludes that the indices d_i=[G:G_i] **cannot all be distinct** — i.e., some two indices
are *equal*. Source: search result summary of
https://www.researchgate.net/publication/325545862_The_Herzog-Schonheim_conjecture_for_finitely_generated_groups
and https://arxiv.org/pdf/1803.08301.

Sun's conjecture (the one in this cell) only assumes the cosets are **pairwise disjoint**,
not that they cover G, and its conclusion is quantitative: some pair of indices has
gcd ≥ k, a strictly stronger and different type of statement (equal indices ⇒ gcd equal to
that common value ≥ 2 in general, but gcd ≥ k is not implied by, nor does it imply, "two
indices equal"). So: **Sun's conjecture is not a restatement of Herzog–Schönheim; it is a
separate, gcd-quantitative conjecture in the same family** (disjoint/partitioned cosets ⇒
constrained indices), inspired by the same circle of ideas and by Sun's own earlier
disjoint-congruence-classes conjecture over ℤ (the number-theoretic version, which is parts
(a)/(b) of this same cell). No paper found in this search claims the two conjectures are
formally equivalent or that one implies the other.

Herzog–Schönheim itself is reported (search snippets only, not read) as proved for: solvable
groups, simple groups, symmetric groups, and all groups of order < 1440; still open in
general. Sources: https://arxiv.org/pdf/1901.10131 (solvable groups),
https://arxiv.org/html/2509.25118v2 (simple and symmetric groups),
https://arxiv.org/pdf/1803.03569 (small groups, order<1440 claim per search snippet).

## 3. What is known for the group/coset conjecture, by k

**[CONJ]** (reporting the literature's claim; not independently re-derived here)

- **k=2**: gcd([G:G_1],[G:G_2])=1 forces the two cosets to intersect (this is the same
  elementary group-theoretic fact used for k=2 in the congruence-class case: if
  gcd(n_1,n_2)=1 then G_1G_2=G, so every coset of G_1 meets every coset of G_2). Handled as
  "Remark 2.2" in Zhu's paper per the search snippet for arXiv:0807.2207. I could not open
  the PDF to check the remark's exact wording.
- **k=3, k=4**: **[CONJ]** (literature claims [PROVED], but this track did not verify the
  argument): W.-J. Zhu, *On Sun's Conjecture concerning Disjoint Cosets*, Int. J. Modern
  Math. 3 (2008), no. 2, 197–206; arXiv:0807.2207 —
  https://arxiv.org/abs/0807.2207 (also mirrored at https://ar5iv.arxiv.org/html/0807.2207
  and https://arxiv.org/pdf/0807.2207). Abstract per search snippet: "we confirm Sun's
  conjecture for k=3,4."
- **k=5 (general group G)**: **[GAP]**. Despite six different targeted WebSearch queries
  (for "k=5", "confirmed", "Zhu follow-up", citations of arXiv:0807.2207, and Sun's own notes
  page), I found **no** paper in the general group setting proving k=5. The only "k≤5 is
  known" statement I can substantiate is for the **number-theoretic** special case G=ℤ
  (ordinary congruence classes a_i (mod m_i), i.e. parts (a)/(b) of this cell, not the coset
  version): K. O'Bryant, *On Z.-W. Sun's Disjoint Congruence Classes Conjecture*,
  arXiv:math/0604347 — https://arxiv.org/abs/math/0604347, abstract (per search snippet):
  "We prove this conjecture for k strictly less than 21," i.e. k ≤ 20 for G=ℤ specifically.
  **This is not the same theorem as part (c)'s group version.** So: if the cell's premise
  "known for k≤5" is about the *group* conjecture, my search did not find the paper that
  proves it, and the strongest documented general-group result is **k≤4** (Zhu 2008), not
  k≤5. This discrepancy should be flagged back to whoever wrote the cell text, or resolved by
  a further, more thorough literature dig (see new_task below) — I report it as a genuine gap
  in what I could find, not as "the claim is false."

## 4. A closely related, very recent paper (flag for the whole swarm, not just this task)

**[CONJ]** (reporting an unverified literature claim about part (b) of this same cell)

J. Fornal, Yu-Chen Sun, *On the problem of large gcd for disjoint residue classes*,
arXiv:2607.24655 — https://arxiv.org/pdf/2607.24655 (mirror:
https://pith.science/paper/2607.24655). Per search snippet, the main theorem is exactly the
bound quoted in **part (b)** of this cell:

> max_{1≤i<j≤k} gcd(m_i,m_j) ≫ k·exp(−(2+o(1))·√(log k / log log k))

for k pairwise disjoint **residue classes** (the ℤ/congruence-class setting again, not the
group/coset setting of part (c)). If this snippet is accurate, part (b) of the cell is
*already answered in the literature* — but this is the residue-class version, not the group
version asked for in part (c), and I have not opened the PDF to check the proof. This is
worth a dedicated literature/verification task (see below); it is out of scope for my
assigned part-(c) task but too relevant not to flag.

---

**What remains open (for part (c), my assigned scope):**
1. Whether the general-group Sun conjecture is proved for k=5 anywhere in the literature —
   unresolved by this search; either the source exists and I didn't find it, or the cell's
   "known for k≤5" premise should read "k≤4."
2. k=6 for the group conjecture is open per every source found (consistent with the cell
   text); no paper claims progress on k=6 specifically.
3. None of the sources here were opened directly (WebFetch blocked); a track with working
   WebFetch, or a human, should re-fetch and confirm the exact wording of Zhu's Remark 2.2
   (k=2) and Theorem statements (k=3,4), and settle point 1 above.

**Verification:** none — this is a literature-only task; no code/certificate applies. All
URLs listed above were surfaced by `WebSearch` queries run in this session (see notes.md for
the exact queries); none were opened with `WebFetch` because the tool was refused by the
proxy for every domain tested, including a control domain (example.com).
