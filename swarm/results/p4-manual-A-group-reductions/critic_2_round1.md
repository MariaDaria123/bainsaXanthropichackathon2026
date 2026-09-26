# Critic 2, round 1 — p4-manual-A-group-reductions (blind; transcribed from the critic subagent's hand-back)
Judged result.md, cell.md, cited scripts only.
1. Statement check: k=6 explicitly open; Lemmas 1-3 exact with quantifiers; Sub-lemma hypothesis exactly what a k=6 counterexample needs; reframing honest, necessary-only with 16/32 example.
2. Step check: Lemma 1 (a)(b)(c), Lemma 2 steps 1-3 and finite reduction, Lemma 3, Sub-lemma (a)-(c): correct. 4-pattern classification re-derived by hand; labelled counts 147 match. Witnesses 66,130,330 checked.
3. Tests: all subgroups of S4 (30), A4 (10), A5 (59): coprime pairs (56,13,118) satisfy [H:A∩B]=n_i n_j, AB=H, all coset pairs meet; 2000 random greedy disjoint families per group: sum<=1, gcd>=2. No failures.
4. Code: all four scripts run, exact, deterministic, fast; certificate reproducible (differs only in wall clock); not wired into rerun.py/gate.py (disclosed, bookkeeping).
5. Labels OK. 6. Literature: classical facts reproved, no black box.
Local fixes: (1) Status must read PARTIAL (repo allows SOLVED/PARTIAL only); (2) garbled "3+6+3+3-..." sentence -> 15 labelled variants; (3) hand cross-check: add that the full set meets any doubleton in 2 elements, so doubletons are excluded before the singleton argument; (4) optional: say the pairwise condition is the full pairwise constraint and the "at most one index" statements are consequences.
VERDICT: MINOR
