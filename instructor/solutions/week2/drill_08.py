"""
Drill 8 - every_nth

SOLUTION. Instructor copy. Verify with:

    python check.py

"""


def every_nth(values, n):
    """Return a new list containing every nth value, starting with the first.

    every_nth([0,1,2,3,4,5,6], 3) -> [0, 3, 6]

    Idea: building a new list, and `range` with a step (Part 1, section 3).
    """
    return values[::n]
