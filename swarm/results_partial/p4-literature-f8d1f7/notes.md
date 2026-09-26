# Notes (not seen by critics)

## Environment issue
WebFetch was refused by the egress proxy for every URL tried, including arxiv.org (abs and
pdf), ar5iv, nju.edu.cn, en.wikipedia.org, r.jina.ai reader, and even https://example.com as
a control. `curl` through the same proxy also got CONNECT 403 for arxiv.org. So this whole
task ran on WebSearch snippets only, never on a directly-read page. Flagged this prominently
in result.md so critics don't assume PDFs were actually opened.

## Search queries run (WebSearch), in order
1. Herzog-Schonheim conjecture disjoint cosets gcd index
2. Zhi-Wei Sun group conjecture cosets pairwise disjoint gcd k
3. "On Sun's conjecture concerning disjoint cosets" abstract arxiv 0807.2207
4. Sun conjecture disjoint cosets gcd indices k=5 proved
5. Sun conjecture cosets k=5 gcd Wan-Jie Zhu OR Yonutiu OR proof five
6. "disjoint cosets" conjecture "k=5" gcd indices proof group theory
7. zwsun conj.pdf "disjoint cosets" k=5 conjecture Sun 2004
8. "Sun's conjecture" cosets "for k" "5" proved 2010..2021 group index gcd (multi-pass)
9. O'Bryant "disjoint congruence classes" conjecture k proved cosets abstract
10. Sun conjecture "pairwise disjoint" cosets "k \le 5" OR "k<=5" OR "for k=5"
11. "International Journal of Modern Mathematics" Zhu 2008 Sun conjecture cosets citations extended k=5
12. Wan-Jie Zhu Sun conjecture disjoint cosets k=5 follow-up paper
13. Zhi-Wei Sun 2004 conjecture disjoint cosets original source paper
14. "Sun" conjecture cosets k=2 trivial gcd proof "index" group
15. arxiv 0807.2207 abstract "we confirm" k=3,4,5 OR "3,4,5" Sun conjecture
16. O'Bryant "Disjoint Congruence Classes" math/0604347 abstract congruence classes k<21
17. "Sun's conjecture" cosets group "k=5" 2013..2021 proved confirmed
18. "On the problem of large gcd for disjoint residue classes" Fornal Sun abstract main theorem

## Key finding / possible discrepancy
Every search converges on: k=2 trivial, k=3,4 by Zhu (arXiv:0807.2207, 2008) for the GENERAL
GROUP conjecture. The "k<=20" result (O'Bryant, math/0604347) is for G=Z (congruence
classes), a DIFFERENT, weaker-hypothesis special case (parts a/b of the cell, not part c).
No search surfaced a general-group k=5 paper. Two hypotheses:
(A) the cell text's "known for k<=5" conflates the two settings (ℤ vs general G), or
(B) there is a k=5 group paper that WebSearch's snippets just never surfaced despite 18
    distinct queries.
Did not have time in the 25-min box to try author-name-based searches (e.g. searching for
"Zhu" co-authors, or Chinese-language sources, or Sun's problem list's own citation trail
past 2009) which might resolve this. Proposed as new_task.

## Interesting side find
arXiv:2607.24655 (Fornal & Yu-Chen Sun) apparently proves *exactly* the bound quoted in cell
part (b), for the residue-class (not coset) setting. If confirmed by opening the actual PDF,
this could let another track close part (b) outright by writing out the argument. Flagged as
new_task, not claimed as done since I never read the PDF.

## What I did NOT do (be honest)
- Did not open a single PDF/HTML page directly (proxy blocked WebFetch entirely).
- Did not verify Zhu's or O'Bryant's or Fornal-Sun's proofs line by line — this is explicitly
  a literature-attribution task, so result.md tags everything as [CONJ]/[GAP] rather than
  [PROVED], per the honesty rule.
