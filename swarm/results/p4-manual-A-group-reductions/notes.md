# notes (manual-claude, item A)
- Base: swarm/results/p4-proof-f59824 (MINOR/MINOR round 2).
- Fixes: (1) "lossless"/"controls" wording -> necessary-only, with the 16/32 example; (2) added exponent layer Sub-lemma (c) + pairwise falsification script; (3) cert domain_proof string corrected; (4) cert-protocol gap reframed as bookkeeping (problems/ read-only for us).
- Idea not pursued (time): for gcd d pair, [G:G_i∩G_j] = lcm*s, s in 1..d; disjoint needs s<d. Might give a group-level constraint for pattern I (d=2 forces [G:G_i∩G_j] = lcm exactly, |G_iG_j| = |G|/2).
- Subagent authors for B/C failed (API usage limit); doing B/C inline.
- Round 3: MINOR/ACCEPT. Only objection: Lemma 2 Step 2 parametrisation typo (a'=ac^{-1},b'=cb -> a'=ac,b'=c^{-1}b). Fixed after round 3; 3-round cap reached, so NOT re-refereed; gate not passed.
