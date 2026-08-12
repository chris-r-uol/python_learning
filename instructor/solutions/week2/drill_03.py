"""
Drill 3 - count_above

SOLUTION. Instructor copy. Verify with:

    python check.py

"""


def count_above(counts, threshold):
    """Return how many values in `counts` are strictly greater than `threshold`.

    count_above([10, 20, 30], 15) -> 2
    count_above([10, 20, 30], 20) -> 1     <- 20 is NOT greater than 20

    "Strictly greater" is the whole of the second example: a value sitting
    exactly on the threshold does not count. `>` and `>=` differ only there,
    and only there is it tested.

    Idea: a loop with an `if` inside it, and boundaries as a decision you
    make rather than one you fall into (Part 1, sections 2 and 3).
    """
    found = 0
    for value in counts:
        if value > threshold:
            found = found + 1
    return found
