# p4 c6 — Beyond the boundary (13 pts, judged, open question)

Three directions beyond the certified range; any one of them counts. Any of the following.

(a) Decide a size k ≥ 25.

(b) The asymptotic form. It is known that a pairwise disjoint family of size k always has a pair with

    gcd(m_i, m_j) ≥ k · exp( −(2 + o(1)) · sqrt( log k / log log k ) ),

which is k^{1−o(1)} but not linear in k. Prove the statement in full, or prove the weaker bound gcd(m_i, m_j) ≥ c·k for some absolute constant c > 0, or improve the exponential factor above.

(c) The group form. Let G be a group, let G_1, …, G_k be subgroups of finite index n_i = [G : G_i], and let x_1 G_1, …, x_k G_k be pairwise disjoint cosets. Is there a pair i < j with gcd(n_i, n_j) ≥ k? This is known for k ≤ 5 and open for every k ≥ 6; settling k = 6 counts as progress.

Hand-in rules: as in problems/p4/problem.md (written proof; computation only with the full 5-part exhaustiveness certificate; unfinished sizes reported as unfinished; cite and check any published argument used).
