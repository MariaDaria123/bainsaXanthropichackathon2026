# notes (manual-claude, item B)
- Base: swarm/results/p4-proof-9c5676 (MINOR/MINOR round 2; critic 1: rule-4 cert.py wrapping; critic 2: float sqrt).
- Fixes: isqrt; float K/2<p -> integer 2p>K; check_L wrapped in tools/cert.py with a non-numeric size label so it cannot be misread as "k=25 certified"; hand proof of L facts so no proof step depends on code; composability wording; removed unverified preprint mention (citation gate); added test_lemma2.py falsification.
- Not attempted: p=11 analogue (gcd can be 11 or 22, injectivity fails); the actual search.
