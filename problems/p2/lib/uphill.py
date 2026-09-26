"""p2 — Uphill paths on the hypercube.

Vertices of Q_d are ints 0..2^d-1 (bit strings in submission format). A labelling
is given as `order`: the list of vertices in increasing label order.

Exact count (dynamic programming, Python ints, no overflow):
  paths(v) = 1                                   if v is a valley (no lower neighbour)
           = sum_{w ~ v, f(w) < f(v)} paths(w)    otherwise
  U(labelling) = sum_v paths(v)
Proof of the recursion: an uphill path ending at v is either (v) with v a valley,
or an uphill path ending at a lower neighbour w extended by v. A valley has no
lower neighbour, so the two cases are exclusive and exhaustive.
"""
from itertools import permutations
import random


def neighbours(v, d):
    return [v ^ (1 << i) for i in range(d)]


def to_str(v, d):
    return format(v, f"0{d}b")


def from_str(s):
    return int(s, 2)


def validate(order, d):
    n = 1 << d
    if len(order) != n or sorted(order) != list(range(n)):
        raise ValueError(f"not a bijection onto the {n} vertices of Q_{d}")


def count_uphill(order, d, adj=None):
    """Exact number of uphill paths of the labelling `order` on Q_d."""
    label = [0] * len(order)
    for i, v in enumerate(order):
        label[v] = i
    paths = [0] * len(order)
    total = 0
    for v in order:                                  # increasing label
        lower = [w for w in (adj[v] if adj else neighbours(v, d)) if label[w] < label[v]]
        paths[v] = 1 if not lower else sum(paths[w] for w in lower)
        total += paths[v]
    return total


def count_uphill_graph(order, adj):
    """Same count for an arbitrary graph given as adjacency lists."""
    label = {v: i for i, v in enumerate(order)}
    paths, total = {}, 0
    for v in order:
        lower = [w for w in adj[v] if label[w] < label[v]]
        paths[v] = 1 if not lower else sum(paths[w] for w in lower)
        total += paths[v]
    return total


def valleys(order, d):
    label = {v: i for i, v in enumerate(order)}
    return [v for v in order if all(label[w] > label[v] for w in neighbours(v, d))]


def read_labelling(path_or_lines):
    lines = open(path_or_lines).read().split() if isinstance(path_or_lines, str) else path_or_lines
    order = [from_str(s.strip()) for s in lines if s.strip()]
    d = len(lines[0].strip())
    validate(order, d)
    return order, d


def write_labelling(order, d, path=None):
    txt = "\n".join(to_str(v, d) for v in order)
    if path:
        open(path, "w").write(txt + "\n")
    return txt


def brute_force_U(d):
    """Exhaustive minimum over all labellings, d <= 3 (8! = 40320). Returns (U, one optimal order)."""
    n = 1 << d
    adj = [neighbours(v, d) for v in range(n)]
    best, arg = None, None
    for perm in permutations(range(n)):
        u = count_uphill(perm, d, adj)
        if best is None or u < best:
            best, arg = u, list(perm)
    return best, arg


def layer_order(d):
    """Baseline: order by Hamming weight, then lexicographically."""
    return sorted(range(1 << d), key=lambda v: (bin(v).count("1"), v))


def local_search(d, iters=20000, seed=0, start=None, temp0=2.0):
    """Simulated annealing over transpositions. Exploration / upper bounds only."""
    rng = random.Random(seed)
    n = 1 << d
    adj = [neighbours(v, d) for v in range(n)]
    order = list(start) if start else layer_order(d)
    cur = count_uphill(order, d, adj)
    best, best_order = cur, order[:]
    for it in range(iters):
        t = temp0 * (1 - it / iters) + 1e-9
        i, j = rng.randrange(n), rng.randrange(n)
        order[i], order[j] = order[j], order[i]
        new = count_uphill(order, d, adj)
        if new <= cur or rng.random() < pow(2.718281828, (cur - new) / t):
            cur = new
            if cur < best:
                best, best_order = cur, order[:]
        else:
            order[i], order[j] = order[j], order[i]
    return best, best_order


def _selftest():
    # Q1: labels 1,2 -> paths (v1), (v1,v2) = 2
    assert count_uphill([0, 1], 1) == 2
    # Q2 is the 2x2 grid; IMO 2022 P6 gives 2n^2 - 2n + 1 = 5 for n = 2
    assert brute_force_U(2)[0] == 5
    # general-graph counter agrees with the hypercube counter
    o = layer_order(3)
    assert count_uphill(o, 3) == count_uphill_graph(o, {v: neighbours(v, 3) for v in range(8)})
    # I/O round trip
    assert read_labelling(write_labelling(o, 3).split())[0] == o
    return "p2 uphill OK"


if __name__ == "__main__":
    print(_selftest())
