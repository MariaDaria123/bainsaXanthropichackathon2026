# notes (not seen by critics)

Time-boxed to 25 min. Plan:
1. Generalise the k=25 Main Reduction Theorem (swarm/results/p4-proof-9c5676) to any k:
   moduli of a size-k counterexample can be replaced (same pairwise gcds) by moduli dividing
   L_k = lcm(1,...,k-1). Fast, mechanical, PROVED.
2. Computed L_k, factorisation, divisor counts for k=21,22,23: all equal L_20=232792560
   (since 21=3*7, 22=2*11 add no new prime power), d(L_k)=960, C1-filtered (>=2 prime
   factors) = 947.
3. Tried to build a real cert.py exhaustive search over modulus MULTISETS (not yet full
   residue assignment) using pruning rules C1 (domain filter), C3 (>=3 multiples of k-1,
   monotone feasibility prune), C4 (primes >= ceil(k/2): count must end 0 or 2, prune at
   count=3). Measured raw node rate: ~300k nodes/s in plain Python DFS over 947 candidates,
   nondecreasing sequences, depth k=21-23.
4. Reality check: even with C1/C3/C4 pruning, branching factor is far too large (947 choices
   per slot, only lightly cut by C4 since big primes are a small fraction of candidates) to
   reach depth 21-23 in the 10-minute-per-script / 25-minute-total budget. This matches the
   board's own observation that O'Bryant's *published* search (with C1,C2,C4,density only,
   no C3/C5/C6/C7) took a WEEK of Mathematica for k<=19. A from-scratch pure-Python DFS in a
   few minutes cannot realistically re-derive or extend that.
5. Decision: run the search with a strict per-k wall-clock budget (25s), record the actual
   node counts reached (honest, not a claim of completion), and mark k=21,22,23 UNFINISHED
   via cert.py's own finished=False/certified=False path (raising TimeoutError inside the
   `with C.size(k)` block so the partial record is still written).
6. Did NOT implement C2 (no prime divides all k moduli) or C5 (subfamily density beyond the
   big-prime case, which folds into C4) as forward prunes -- only as leaf checks -- because
   they are family-completion properties, not needed for an honest "unfinished, N nodes
   reached" report, and adding them as forward prunes would not change the fundamental
   branching-factor problem in the available time.
7. C4's "exactly 0 or 2" and C3's ">=3 multiples of k-1" are CITED from the shared board,
   which itself has them as CONJECTURED (from O'Bryant Lemma 6, with two audited repaired
   gaps). This search's pruning is therefore only as sound as those cited lemmas -- flagged
   explicitly in result.md, not silently upgraded.

Dead end avoided: did not attempt to build the full O'Bryant "Grow" residue-CRT search (a
much bigger undertaking, explicitly out of scope for one 25-minute slot); logged as new_task.
