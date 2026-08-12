"""
Drill 7 - average

SOLUTION. Instructor copy. Verify with:

    python check.py

"""


def average(values):
    """Return the mean of `values`, or None if there are none.

    Most real bugs live in the empty case. Handle it deliberately.

    average([2, 4, 6]) -> 4.0
    average([]) -> None

    Idea: None, and deciding what happens when there is no answer
    (Part 1, section 4).
    """
    if len(values) == 0:
        return None
    return sum(values) / len(values)
