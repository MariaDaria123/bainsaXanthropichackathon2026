"""Starting program for ShinkaEvolve. Only the EVOLVE block is changed by the LLM."""

# EVOLVE-BLOCK-START
def construct(params):
    """Return one candidate object for this cell (for example a labelling as a list).

    Replace this baseline with the best simple construction you know.
    """
    n = params.get("n", 8)
    return list(range(n))
# EVOLVE-BLOCK-END


def run_experiment(**params):
    """Called by evaluate.py. Do not rename."""
    return construct(params)
