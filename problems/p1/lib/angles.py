"""p1 — Angles between lines. Evaluation, rigorous enclosure, and a numeric maximiser.

theta(l, l') = arccos |<x,x'>| / (|x||x'|)   in [0, pi/2]
S(l_1..l_N) = sum_{i<j} theta(l_i, l_j)
Fejes Toth configuration: d orthogonal axes, each used floor/ceil(N/d) times.

Rigour: `S_enclosure` takes rational vectors (int or Fraction). cos^2 of every
angle is then an exact rational; we take sqrt and arccos in mpmath at DPS digits
and widen every endpoint by 10^-(DPS-10), which dominates mpmath's rounding
error (mpmath evaluates elementary functions to within a few ulps of working
precision). arccos is decreasing, so [acos(c_hi), acos(c_lo)] encloses theta.
"""
from fractions import Fraction
from itertools import combinations
import math, random
import mpmath as mp

DPS = 60


def fejes_toth_value(N, d):
    """S of the conjectured optimum, as a multiple of pi/2 (exact integer)."""
    q, r = divmod(N, d)
    coincident = r * math.comb(q + 1, 2) + (d - r) * math.comb(q, 2)
    return math.comb(N, 2) - coincident          # S = value * pi/2


def fejes_toth_S(N, d):
    return fejes_toth_value(N, d) * mp.pi / 2


def cos2(x, y):
    """Exact cos^2 of the angle between lines spanned by x, y (rational input)."""
    dot = sum(Fraction(a) * Fraction(b) for a, b in zip(x, y))
    nx = sum(Fraction(a) ** 2 for a in x)
    ny = sum(Fraction(b) ** 2 for b in y)
    return dot * dot / (nx * ny)


def theta(x, y):
    """High-precision (not rigorous) angle."""
    with mp.workdps(DPS):
        if all(isinstance(t, (int, Fraction)) for t in list(x) + list(y)):
            c2 = cos2(x, y)
            c = mp.sqrt(mp.mpf(c2.numerator) / c2.denominator)
        else:
            xs, ys = [mp.mpf(t) for t in x], [mp.mpf(t) for t in y]
            c = abs(mp.fdot(xs, ys)) / mp.sqrt(mp.fdot(xs, xs) * mp.fdot(ys, ys))
        return mp.acos(min(c, mp.mpf(1)))


def S(vectors):
    with mp.workdps(DPS):
        return mp.fsum(theta(x, y) for x, y in combinations(vectors, 2))


def angle_enclosure(x, y):
    """Rigorous [lo, hi] for theta, rational input only."""
    c2 = cos2(x, y)
    with mp.workdps(DPS):
        eps = mp.mpf(10) ** (-(DPS - 10))
        c = mp.sqrt(mp.mpf(c2.numerator) / c2.denominator)
        c_lo, c_hi = max(mp.mpf(0), c - eps), min(mp.mpf(1), c + eps)
        lo, hi = mp.acos(c_hi) - eps, mp.acos(c_lo) + eps
        return max(lo, mp.mpf(0)), min(hi, mp.pi / 2 + eps)


def S_enclosure(vectors):
    """Rigorous [lo, hi] enclosing S for rational vectors."""
    lo = hi = mp.mpf(0)
    with mp.workdps(DPS):
        for x, y in combinations(vectors, 2):
            a, b = angle_enclosure(x, y)
            lo, hi = lo + a, hi + b
    return lo, hi


def maximize(N, d, restarts=30, iters=4000, seed=0):
    """Numeric hill climbing on (S^{d-1})^N. Exploration only - never a proof.
    Returns (best_S_float, vectors, fejes_toth_S_float)."""
    rng = random.Random(seed)

    def ang(u, v):
        c = abs(sum(a * b for a, b in zip(u, v)))
        return math.acos(min(1.0, c))

    def norm(v):
        n = math.sqrt(sum(t * t for t in v)) or 1.0
        return [t / n for t in v]

    best, best_vs = -1.0, None
    for _ in range(restarts):
        vs = [norm([rng.gauss(0, 1) for _ in range(d)]) for _ in range(N)]
        step = 0.5
        cur = sum(ang(vs[i], vs[j]) for i, j in combinations(range(N), 2))
        for it in range(iters):
            i = rng.randrange(N)
            cand = norm([t + step * rng.gauss(0, 1) for t in vs[i]])
            delta = sum(ang(cand, vs[j]) - ang(vs[i], vs[j]) for j in range(N) if j != i)
            if delta > 0:
                vs[i], cur = cand, cur + delta
            if it % 500 == 499:
                step *= 0.6
        if cur > best:
            best, best_vs = cur, [v[:] for v in vs]
    return best, best_vs, float(fejes_toth_S(N, d))


def _selftest():
    # N=3, d=2: three lines at 60 degrees give pi, equal to the FT value (3 choose 2 - 1) * pi/2 = pi
    assert fejes_toth_value(3, 2) == 2
    v60 = [(1, 0), (1, 1.7320508075688772), (-1, 1.7320508075688772)]
    assert abs(float(S(v60)) - math.pi) < 1e-9
    # axes in R^3: S = 3 pi/2, rigorous enclosure contains it
    lo, hi = S_enclosure([(1, 0, 0), (0, 1, 0), (0, 0, 1)])
    with mp.workdps(DPS):                            # compare at full precision, not mpmath's default 15 digits
        assert lo <= 3 * mp.pi / 2 <= hi and hi - lo < mp.mpf(10) ** -40
        lo2, hi2 = S_enclosure([(1, 0), (1, 1)])       # 45 degrees
        assert lo2 <= mp.pi / 4 <= hi2
    # d+k lines, k coincident pairs: value C(N,2) - k
    assert fejes_toth_value(5, 3) == 10 - 2 and fejes_toth_value(6, 4) == 15 - 2
    best, _, ft = maximize(4, 3, restarts=5, iters=1500)
    assert best <= ft + 1e-6, (best, ft)
    return "p1 angles OK"


if __name__ == "__main__":
    print(_selftest())
