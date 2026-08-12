"""
Drill 6 - congestion_band

Fill in the function below, then run:

    python check.py

"""


def congestion_band(volume_capacity_ratio):
    """Classify a volume/capacity ratio.

        below 0.7          -> "free flow"
        0.7 up to 0.9      -> "busy"
        0.9 up to 1.0      -> "at capacity"
        1.0 and above      -> "over capacity"

    Watch the boundaries. 0.7 is "busy", not "free flow".

    Idea: branching, and boundaries as a decision you make (Part 1,
    section 2). A chain of separate `if` statements works if each one
    returns; `elif` does the same job more tidily.
    """
    # TODO - write your answer here, replacing this line and the `pass`
    pass
