# notes (p4-certificate-68026c)
- Board empty: no reduction lemma available; proved own Lemma A (drop primes >= 25, cap exponents at e_p).
- Branching by prime support S subset P; small branches trivial (colouring bound kills at depth <= 2 mostly).
- P={2,3}: 402 classes, 5859 nodes. P={2,3,5}: 2417 classes, P={2,3,7}: 1008 divisors.
- Full domain L_all = 16*9*5*7*11*13*17*19*23 has sigma(L_all) classes ~ 10^11: hopeless for plain clique search.
- Needed: lemma removing primes p>=13 (pairs sharing p have gcd exactly p), or multiplier symmetry (x -> u x, u unit mod L) to cut residues.
- Test hook GMAX_TEST used only for positive controls.
