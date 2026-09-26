"""p4 c6(a), k = 25: certified exhaustive search, one certificate per branch.

Branch P (a set of primes < 25): all moduli divide L_P = prod_{p in P} p^{e_p}, e_p = floor(log_p 24).
Claim per branch: no 25 pairwise disjoint classes with moduli m | L_P, m >= 2, all pairwise gcd <= 24.
usage: python search.py BRANCH_NAME [time_limit_s]      (branches listed in BRANCHES)
Writes certificate_<BRANCH>.json (or $CERT_OUT).
"""
import os, sys, time
from math import gcd
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = next(p for p in [HERE, *[os.path.join(HERE, *[".."] * i) for i in range(1, 7)]]
            if os.path.exists(os.path.join(p, "tools", "cert.py")))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from cert import Certificate

K = int(os.environ.get("K_TARGET", 25))
GMAX = int(os.environ.get("GMAX_TEST", K - 1))   # test hook only; certificates use GMAX = K-1
BRANCHES = {"P23": (2, 3), "P235": (2, 3, 5), "P237": (2, 3, 7), "P2": (2,), "P3": (3,), "P25": (2, 5)}


def e(p):
    t = 0
    while p ** (t + 1) <= K - 1:
        t += 1
    return t


def divisors_of(P):
    ds = [1]
    for p in P:
        ds = [d * p ** i for d in ds for i in range(e(p) + 1)]
    return sorted(d for d in ds if d >= 2)


def main():
    name = sys.argv[1]
    limit = float(sys.argv[2]) if len(sys.argv) > 2 else 300.0
    P = BRANCHES[name]
    L = 1
    for p in P:
        L *= p ** e(p)
    out = os.environ.get("CERT_OUT") or os.path.join(HERE, f"certificate_{name}.json")
    C = Certificate(problem="p4", cell="c6a-k25-" + name,
                    domain=f"sets of {K} distinct classes (a mod m), m | L={L}, m >= 2, 0 <= a < m, "
                           f"pairwise disjoint with pairwise gcd <= {K-1}; primes P={P}",
                    domain_proof="Lemma A (result.md): any counterexample of size 25 reduces to one with every "
                                 "modulus dividing L_all = 16*9*5*7*11*13*17*19*23 with the same pairwise gcds; "
                                 "this branch covers exactly those reduced counterexamples whose moduli use only primes in P.",
                    out=out)
    C.rule("R1", "Canonical order: classes sorted by (m, a); only increasing index sequences enumerated.",
           "Disjointness and the gcd condition are symmetric; equal classes are never disjoint (gcd(m,m)=m | 0), "
           "so each family is a set and has exactly one increasing listing.")
    C.rule("R2", "Translation: the first (smallest in (m,a) order) class has a = 0.",
           "Shifting all residues by -a_1 preserves every difference a_i - a_j, so disjointness and gcds are kept; "
           "the smallest class (m1,a1) becomes (m1,0), still smallest among classes of modulus m1 since 0 is the least "
           "residue, and classes of larger modulus stay larger. So every family has a translate with a_1 = 0.")
    C.rule("R3", "Compatibility: a class is added only if it is disjoint from, and has gcd <= 24 with, every chosen class.",
           "Both conditions are pairwise and required of every pair in a counterexample.")
    C.rule("R4", "Colouring bound: if |chosen| + (number of colours in a greedy proper colouring of the candidate "
                 "compatibility graph) < 25, prune.",
           "Candidates are the classes compatible with all chosen ones and later in order. Any extension adds a clique "
           "of the compatibility graph on candidates; a clique meets each colour class (an independent set) at most once.")
    C.rule("R5", "Multiplier: the second class (m2, a2) of the family (second in (m, a) order) has a2 = 0 or a2 | m2.",
           "The affine maps x -> u x + t (u a unit mod L_P) send classes (m, a) to (m, (u a + t) mod m), keep every modulus, "
           "and keep disjointness and gcds, because g | (a_i - a_j) iff g | u (a_i - a_j) for gcd(u, g) = 1. Take the image "
           "of a family whose sorted list is lexicographically least. Its first class has a1 = 0 (else translate by -a1: "
           "moduli are fixed, so the first class becomes (m1, 0), smaller). Let (m2, a2) be its second class and d = gcd(a2, m2). "
           "Units mod L_P surject onto units mod m2, so some unit u has u a2 = d mod m2; x -> u x fixes (m1, 0), which stays first "
           "(moduli fixed, 0 least residue), and sends (m2, a2) to (m2, d). Every other class has modulus >= m2, so the new second "
           "class is <= (m2, d). If d < a2 this image is smaller, contradiction; hence a2 = d, i.e. a2 | m2 (a2 = 0 is allowed). "
           "R2 is the first half of this argument.")
    classes = [(m, a) for m in divisors_of(P) for a in range(m)]
    n = len(classes)
    nbr = [0] * n
    for i in range(n):
        mi, ai = classes[i]
        for j in range(i + 1, n):
            mj, aj = classes[j]
            g = gcd(mi, mj)
            if g <= GMAX and (ai - aj) % g != 0:
                nbr[i] |= 1 << j
                nbr[j] |= 1 << i
    t0 = time.perf_counter()

    class Timeout(Exception):
        pass

    def colour_bound(cand):
        cols = 0
        c = cand
        while c:
            cols += 1
            q = c
            while q:
                low = q & -q
                v = low.bit_length() - 1
                q &= ~nbr[v] & ~low
                c &= ~low
        return cols

    def dfs(chosen, cand):
        C.node()
        if C._cur["nodes"] % 20000 == 0 and time.perf_counter() - t0 > limit:
            raise Timeout
        if chosen == K:
            return True
        if chosen + colour_bound(cand) < K:
            C.prune("R4")
            return False
        c = cand
        while c:
            low = c & -c
            v = low.bit_length() - 1
            c ^= low
            if dfs(chosen + 1, c & nbr[v]):
                raise RuntimeError(f"found clique through {classes[v]}")
        return False

    try:
        with C.size(K) as rec:
            rec["branch"] = name
            rec["n_classes"] = n
            for i, (m, a) in enumerate(classes):
                if a != 0:
                    C.prune("R2")
                    continue
                later = ((1 << n) - 1) ^ ((1 << (i + 1)) - 1)
                cand = later & nbr[i]
                C.node()
                c = cand
                while c:
                    low = c & -c
                    j = low.bit_length() - 1
                    c ^= low
                    m2, a2 = classes[j]
                    if a2 != 0 and m2 % a2 != 0:
                        C.prune("R5")
                        continue
                    if dfs(2, c & nbr[j]):
                        raise RuntimeError("found")
    except Timeout:
        nodes = C.sizes[-1]["nodes"]
        C.sizes.pop()
        C.unfinished(K, nodes)
        C.sizes[-1]["branch"] = name
    C.finish()


if __name__ == "__main__":
    main()
