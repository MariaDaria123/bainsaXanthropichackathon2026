# notes (not seen by critics)

- First idea tried: replace m_i by gcd(m_i, L) directly. WRONG — gcd(m_i,L) | m_i means the
  new modulus is *smaller*, so the new class a_i (mod gcd(m_i,L)) is a *superset* of the old
  class a_i (mod m_i). Shrinking the modulus this way can create new intersections with other
  classes; disjointness is not obviously preserved. Dropped this in favor of the valuation-
  lowering argument (Lemma 2), which only lowers a prime's exponent down to the level that is
  already "invisible" to every other gcd in the family — that's what makes it provably safe.

- Checked whether Lemma 3's injectivity argument extends to small primes p <= 11: fails,
  because 2p <= 24 is possible for p <= 12, so gcd(m_i,m_j) divisible by p need not force
  gcd = p exactly (could be 2p, 3p, etc., still <= 24). So t=1 is not forced and two moduli
  divisible by p could still collide at a *different* shared residue after accounting for the
  extra factor. Did not pursue further given the time box; flagged as open in result.md.

- Tried to fetch arxiv 2607.24655 ("On the problem of large gcd for disjoint residue
  classes") for the previously-certified k range and to see if their reduction matches mine;
  WebFetch was blocked by the environment's proxy for arxiv.org and pith.science. Proceeded
  with an independently derived proof instead (this is allowed/required by the "citing !=
  proving" rule anyway).

- Did not attempt to actually run a search over divisors of L (1920 per slot) — out of scope
  for a 25-minute proof-track task whose deliverable is explicitly "the reduction lemma",
  not the search itself.
