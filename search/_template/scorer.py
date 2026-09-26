"""Exact scorer for this cell. Written by the agent per cell, never evolved.

Rules: exact arithmetic only (ints, fractions); higher score = better,
so to minimise a count return its negative (e.g. score = -number_of_paths).
Invalid candidates get -1e18 automatically, so they never win.
"""

PARAMS = {"n": 8}  # passed to construct() and to the functions below


def validate(obj, params):
    """Return (True, None) if obj is a legal construction, else (False, reason)."""
    n = params["n"]
    if sorted(obj) != list(range(n)):
        return False, "not a permutation of 0..n-1"
    return True, None


def score(obj, params):
    """Exact objective. Example only: reward long ascending runs."""
    return sum(1 for a, b in zip(obj, obj[1:]) if b > a)
