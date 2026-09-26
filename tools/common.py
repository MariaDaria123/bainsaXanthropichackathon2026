"""Shared paths and logging for the pipeline."""
import json, os, time, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLACEHOLDER = "PASTE CELL TEXT HERE"
CELLS = ["c1", "c2", "c3", "c4", "c5", "c6"]
PROBLEMS = ["p1", "p2", "p3", "p4"]


def problem_dir(p):
    return os.path.join(ROOT, "problems", p)


def cell_dir(p, c):
    return os.path.join(ROOT, "problems", p, "cells", c)


def rel(path):
    return os.path.relpath(path, ROOT)


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def log(p, c, event, **fields):
    """Append one event to the cell's log.jsonl."""
    rec = {"t": now(), "ts": time.time(), "problem": p, "cell": c, "event": event, **fields}
    with open(os.path.join(cell_dir(p, c), "log.jsonl"), "a") as f:
        f.write(json.dumps(rec) + "\n")
    return rec


def read_log(p, c):
    path = os.path.join(cell_dir(p, c), "log.jsonl")
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def mtime(path):
    return os.path.getmtime(path) if os.path.exists(path) else None


def cell_filled(p, c):
    path = os.path.join(cell_dir(p, c), "cell.md")
    if not os.path.exists(path):
        return False
    txt = open(path).read()
    return PLACEHOLDER not in txt and len(txt.strip()) > 40


def verdict(p, c):
    """Return 'PASS', 'FAIL' or None from the last non-empty line of review.md."""
    path = os.path.join(cell_dir(p, c), "review.md")
    if not os.path.exists(path):
        return None
    lines = [l.strip() for l in open(path).read().splitlines() if l.strip()]
    if not lines:
        return None
    last = lines[-1]
    if last == "VERDICT: PASS":
        return "PASS"
    if last == "VERDICT: FAIL":
        return "FAIL"
    return None
