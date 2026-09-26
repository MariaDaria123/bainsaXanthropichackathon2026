"""ShinkaEvolve evaluator. Generic: all problem logic lives in scorer.py next to this file."""
import argparse
import os
import sys

from shinka.core import run_shinka_eval

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scorer  # noqa: E402


def get_kwargs(run_idx):
    return dict(scorer.PARAMS)


def validate_fn(obj):
    try:
        return scorer.validate(obj, scorer.PARAMS)
    except Exception as exc:  # a crashing candidate is simply invalid
        return False, f"validate raised {exc!r}"


def aggregate_fn(results):
    # Shinka only ever selects programs marked correct; this is a second safety net.
    if not results or not validate_fn(results[0])[0]:
        return {"combined_score": -1e18, "public": {}, "private": {}}
    obj = results[0]
    value = scorer.score(obj, scorer.PARAMS)
    return {
        "combined_score": float(value),
        "public": {"score": value},
        "private": {"object": repr(obj)[:20000]},
    }


def main(program_path, results_dir):
    os.makedirs(results_dir, exist_ok=True)
    metrics, correct, err = run_shinka_eval(
        program_path=program_path,
        results_dir=results_dir,
        experiment_fn_name="run_experiment",
        num_runs=1,
        get_experiment_kwargs=get_kwargs,
        validate_fn=validate_fn,
        aggregate_metrics_fn=aggregate_fn,
    )
    print("correct:", correct, "| error:", err)
    print("combined_score:", metrics.get("combined_score"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--program_path", default="initial.py")
    parser.add_argument("--results_dir", default="results")
    args = parser.parse_args()
    main(args.program_path, args.results_dir)
