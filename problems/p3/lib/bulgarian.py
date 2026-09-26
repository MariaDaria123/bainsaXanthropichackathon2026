"""p3 — Bulgarian solitaire. Exact shift, depths, cycles and D_B(n).

Partitions are weakly decreasing tuples. B removes one card from every pile and
adds one pile of size s = number of piles.
d_B(lam) = min i >= 0 with B^i(lam) cyclic;  D_B(n) = max over partitions of n.

Algorithm for all partitions of n at once: B is a function on a finite set,
so its functional graph splits into cycles plus trees hanging off them. A node
is cyclic iff it lies on a cycle; we find every cycle by walking from each
unvisited node until a node repeats, then d_B(x) = 1 + d_B(B(x)) off the cycles.
"""
import sys


def B(lam):
    return tuple(sorted([x - 1 for x in lam if x > 1] + [len(lam)], reverse=True))


def partitions(n, maxpart=None):
    """All partitions of n as weakly decreasing tuples."""
    if maxpart is None:
        maxpart = n
    if n == 0:
        yield ()
        return
    for first in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - first, first):
            yield (first,) + rest


def rank(n):
    """The k with T_{k-1} < n <= T_k."""
    k = 0
    while k * (k + 1) // 2 < n:
        k += 1
    return k


def T(k):
    return k * (k + 1) // 2


def staircase(k):
    return tuple(range(k, 0, -1))


def analyse(n):
    """Return (depth dict, set of cyclic partitions, list of cycles)."""
    parts = list(partitions(n))
    state = {}                      # 0 unvisited, 1 on stack, 2 done
    cyclic, cycles = set(), []
    for start in parts:
        if state.get(start):
            continue
        path, x = [], start
        while not state.get(x):
            state[x] = 1
            path.append(x)
            x = B(x)
        if state[x] == 1:           # found a new cycle
            i = path.index(x)
            cyc = path[i:]
            cycles.append(cyc)
            cyclic.update(cyc)
        for y in path:
            state[y] = 2
    depth = {c: 0 for c in cyclic}
    for start in parts:
        path, x = [], start
        while x not in depth:
            path.append(x)
            x = B(x)
        dd = depth[x]
        for y in reversed(path):
            dd += 1
            depth[y] = dd
    return depth, cyclic, cycles


def dB(lam):
    seen, x, i = {}, tuple(lam), 0
    orbit = []
    while x not in seen:
        seen[x] = i
        orbit.append(x)
        x = B(x)
        i += 1
    return seen[x]                  # first index that is on the cycle


def DB(n):
    """Return (D_B(n), list of partitions attaining it)."""
    depth, _, _ = analyse(n)
    m = max(depth.values())
    return m, [p for p, v in depth.items() if v == m]


def table(nmax):
    rows = []
    for n in range(1, nmax + 1):
        m, arg = DB(n)
        k = rank(n)
        rows.append({"n": n, "rank_k": k, "offset_from_T(k-1)": n - T(k - 1), "DB": m,
                     "n_maximisers": len(arg), "example_maximiser": list(arg[0])})
    return rows


def _selftest():
    assert B((2, 1, 1, 1, 1)) == (5, 1) and B((5, 1)) == (4, 2) and B((4, 2)) == (3, 2, 1)
    assert B((3, 2, 1)) == (3, 2, 1)
    assert dB((2, 1, 1, 1, 1)) == 3
    depth, cyc, _ = analyse(6)
    assert depth[(2, 1, 1, 1, 1)] == 3 and (3, 2, 1) in cyc
    assert sum(1 for _ in partitions(10)) == 42
    assert rank(6) == 3 and rank(7) == 4 and rank(1) == 1
    return "p3 bulgarian OK"


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for r in table(int(sys.argv[1])):
            print(r)
    else:
        print(_selftest())
