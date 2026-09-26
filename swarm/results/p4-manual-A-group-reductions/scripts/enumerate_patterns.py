"""
Exhaustive enumeration of the "shared-prime pattern" of a hypothetical size-6
counterexample to the group form of the disjoint-coset conjecture, under the
reductions proved in result.md:

  (ii)  gcd(n_i, n_j) >= 2 for every pair (coprime indices force the cosets to meet)
  upper bound needed for a *counterexample*: gcd(n_i, n_j) <= 5 for every pair
        (else the pair already witnesses gcd >= k = 6, so it is not a counterexample)

So every pairwise gcd lies in {2,3,4,5}. Such a gcd is divisible by at most one
prime <= 5 (since 2*3=6, 2*5=10, 3*5=15 are all > 5). Hence for i != j the two
numbers n_i, n_j cannot share two *different* primes from {2,3,5}, and they also
cannot share any prime >= 7 (that would already force gcd >= 7 > 5). So:

  D_i := { p in {2,3,5} : p | n_i }   is nonempty for every i (else gcd(n_i,n_j)
          could only come from a shared prime >= 7, forcing gcd >= 7, contradiction
          -- unless the pair is coprime, contradicting (ii)),
  and for every i != j:  |D_i cap D_j| = 1  exactly.

This script brute-forces all functions D: {1..6} -> {nonempty subsets of {2,3,5}}
(8-1=7 choices each, 7^6 = 117649 tuples, well under the 10-minute budget) and
keeps those with |D_i cap D_j| = 1 for all i<j. It reports the surviving patterns
up to the symmetry group S_6 x S_3 (permute the 6 indices; permute the 3 primes),
which is the exhaustiveness certificate for the classification in result.md.

Runtime: < 2 seconds.
"""
from itertools import combinations, product, permutations

PRIMES = (2, 3, 5)
SUBSETS = [frozenset(s) for r in range(1, 4) for s in combinations(PRIMES, r)]  # 7 nonempty subsets

def canonical(Dtuple):
    """Canonical form of a 6-tuple of subsets under S_6 (reorder) x S_3 (relabel primes)."""
    best = None
    for perm in permutations(PRIMES):
        remap = dict(zip(PRIMES, perm))
        relabeled = tuple(frozenset(remap[p] for p in D) for D in Dtuple)
        # sort the 6 entries (as sorted tuples of ints) to kill the S_6 symmetry
        key = tuple(sorted(tuple(sorted(D)) for D in relabeled))
        if best is None or key < best:
            best = key
    return best

def valid(Dtuple):
    for i, j in combinations(range(6), 2):
        if len(Dtuple[i] & Dtuple[j]) != 1:
            return False
    return True

def main():
    seen = {}
    count_checked = 0
    count_valid = 0
    for Dtuple in product(SUBSETS, repeat=6):
        count_checked += 1
        if valid(Dtuple):
            count_valid += 1
            key = canonical(Dtuple)
            if key not in seen:
                seen[key] = Dtuple
    print(f"tuples checked: {count_checked}")
    print(f"valid tuples:   {count_valid}")
    print(f"distinct patterns up to S_6 x S_3: {len(seen)}")
    print()
    for key in sorted(seen):
        # describe multiset of subset-sizes and multiplicities
        sizes = sorted(len(s) for s in key)
        print(key, " sizes:", sizes)

if __name__ == "__main__":
    main()
