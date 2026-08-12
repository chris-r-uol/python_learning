"""
Drill 3 - count_above

SOLUTION. Instructor copy. Verify with:

    python check.py

"""


def count_above(counts, threshold):
    """Return how many values in `counts` are strictly greater than `threshold`.

    count_above([10, 20, 30], 15) -> 2

    Idea: a loop with an `if` inside it (Part 1, sections 2 and 3).
    """
    found = 0
    for value in counts:
        if value > threshold:
            found = found + 1
    return found
