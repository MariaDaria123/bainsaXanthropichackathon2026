"""Exhaustiveness-certificate library.

Every computational proof step goes through this. It records, per size:
  - nodes visited (C.node())
  - prunes per registered rule (C.prune("R1"))
  - survivors, each with a decision, the minimal part forcing it and a minimality proof
  - wall clock
and writes cert/certificate.json (or $CERT_OUT). tools/rerun.py re-executes the
script and compares the counts.

A size counts as certified only if it finished and every survivor is decided.
"""
import hashlib, json, os, sys, time, platform
from contextlib import contextmanager


class CertificateError(Exception):
    pass


class Certificate:
    def __init__(self, problem, cell, domain, domain_proof, out=None):
        self.problem, self.cell = problem, cell
        self.domain, self.domain_proof = domain, domain_proof
        script = os.path.abspath(sys.argv[0])
        self.script = script
        self.out = out or os.environ.get("CERT_OUT") or os.path.join(os.path.dirname(script), "certificate.json")
        self.rules = {}
        self.sizes = []
        self._cur = None
        self._t0 = time.perf_counter()

    # ---- rules -------------------------------------------------------
    def rule(self, rid, statement, proof):
        if not statement or not proof:
            raise CertificateError(f"rule {rid}: statement and proof are both required")
        self.rules[rid] = {"id": rid, "statement": statement, "proof": proof}

    # ---- per-size recording -------------------------------------------
    @contextmanager
    def size(self, n):
        rec = {"size": n, "nodes": 0, "pruned": {r: 0 for r in self.rules},
               "survivors": [], "finished": False, "wall_s": None}
        self._cur = rec
        t = time.perf_counter()
        try:
            yield rec
            rec["finished"] = True
        finally:
            rec["wall_s"] = round(time.perf_counter() - t, 3)
            undecided = [s for s in rec["survivors"] if not s["decision"] or s["decision"] == "undecided"]
            rec["n_survivors"] = len(rec["survivors"])
            rec["n_undecided"] = len(undecided)
            rec["certified"] = rec["finished"] and not undecided
            self.sizes.append(rec)
            self._cur = None

    def node(self, k=1):
        self._cur["nodes"] += k

    def prune(self, rid, k=1):
        if rid not in self.rules:
            raise CertificateError(f"prune with unregistered rule {rid}: every rule needs a statement and proof")
        self._cur["pruned"][rid] += k

    def survivor(self, obj, decision, minimal_part=None, minimality_proof=None):
        """Record an object that survived pruning.

        decision: e.g. "counterexample", "excluded: <reason>", or "undecided".
        minimal_part: the smallest sub-object that already forces the decision.
        minimality_proof: why no smaller part forces it.
        """
        if decision and decision != "undecided" and (minimal_part is None or not minimality_proof):
            raise CertificateError("a decided survivor needs minimal_part and minimality_proof")
        self._cur["survivors"].append({"object": repr(obj), "decision": decision or "undecided",
                                       "minimal_part": repr(minimal_part) if minimal_part is not None else None,
                                       "minimality_proof": minimality_proof})

    def unfinished(self, n, reached):
        """Record a size that was started but not completed (e.g. time limit)."""
        self.sizes.append({"size": n, "nodes": reached, "pruned": {}, "survivors": [], "finished": False,
                           "certified": False, "n_survivors": 0, "n_undecided": 0, "wall_s": None,
                           "note": "UNFINISHED - not claimed"})

    # ---- output ---------------------------------------------------------
    def finish(self):
        with open(self.script, "rb") as f:
            sha = hashlib.sha256(f.read()).hexdigest()
        data = {
            "problem": self.problem, "cell": self.cell,
            "domain": self.domain, "domain_proof": self.domain_proof,
            "rules": list(self.rules.values()),
            "sizes": self.sizes,
            "certified_sizes": [s["size"] for s in self.sizes if s["certified"]],
            "total_wall_s": round(time.perf_counter() - self._t0, 3),
            "script_sha256": sha,
            "python": sys.version.split()[0], "platform": platform.platform(),
        }
        os.makedirs(os.path.dirname(os.path.abspath(self.out)), exist_ok=True)
        with open(self.out, "w") as f:
            json.dump(data, f, indent=1)
        print(json.dumps({"certified_sizes": data["certified_sizes"],
                          "nodes": {str(s["size"]): s["nodes"] for s in self.sizes},
                          "total_wall_s": data["total_wall_s"]}))
        return data
